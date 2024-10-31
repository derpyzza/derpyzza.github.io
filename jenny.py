#!/usr/bin/python3

import os
import re
import sys
import glob
import markdown
import datetime
from bs4 import BeautifulSoup as Soup

src_dir = "src"
out_dir = "public"
res_dir = "assets"
list_template = "index_template.html"
post_template = "template.html"
list_files = ['archive']

if not list_template.endswith(".html"):
    list_template = list_template + ".html"
if not post_template.endswith(".html"):
    post_template = post_template + ".html"

if not os.path.exists(src_dir):
    print(f"creating input dir {src_dir}/...")
    os.mkdir( src_dir )
if not os.path.exists( out_dir ):
    print(f"creating output dir {out_dir}/...")
    os.mkdir( out_dir )


# taken from https://leancrew.com/all-this/2020/06/ordinals-in-python/
def ordinal(n):
  s = ('th', 'st', 'nd', 'rd') + ('th',)*10
  v = n%100
  if v > 13:
    return f'{n}{s[v%10]}'
  else:
    return f'{n}{s[v]}'

def pretty_date( date ):
    bits = date.split(".")
    new = datetime.datetime(int(bits[0]), int(bits[1]), int(bits[2]))
    day = new.strftime("%d")
    day = ordinal(int(day))
    full = new.strftime("%b, %Y")
    day += " "
    day += full
    return day


# extract any variables in a file.
def preprocess_file(file):
    vars = {
        'post_content': "",
        'generate_toc': True,
        'post_languages': ['en'],
        'file_name': file.name,
    }
    keep_scanning = True
    for line in file:
        stripped = line.lstrip()
 
        if stripped.startswith('@') and keep_scanning:
            command,_,args = stripped.rstrip('\n').lstrip('@').partition(' ')
            args = args.strip().split('+')

            # If only one item in list just convert it into a string
            if len(args) == 1:
                args = "".join(args)

            if command == 'generate_toc':
                if args[0].strip().lower() == 'false':
                    vars['generate_toc'] = False;
                # default case
                else:
                    vars['generate_toc'] = True
            else:
                vars[command] = args
        elif stripped.startswith("---"):
            keep_scanning = False
            continue
        else: 
            vars['post_content'] += line;
    return vars

posts = []

def process_notes(post):
    soup = Soup(post, 'html.parser')
    # Link subscript counter
    note_count = 1
    link_count = 1
    links = []
    notes = []
    has_links = False
    has_notes = False
    for a in soup.find_all('a'):
        href = a['href']
        if href.startswith("#"):
            continue
        link_text = a.string
        if href == "_":
            has_notes = True
            aside = soup.new_tag('aside')

            aside_num = soup.new_tag('b')
            aside_num.string = f"{note_count}."

            aside.append(aside_num)
            aside.append(" ")
            aside.append(link_text)

            sup = soup.new_tag('small')
            sup['id'] = f"note-{note_count}-src"
            _a = soup.new_tag('a', href=f"#note-{note_count}-dest")
            _a.string = f"[{note_count}]"
            sup.append(_a)

            a.replace_with(sup)
            sup.parent.insert_after(aside)
            notes.append({'body': link_text})            
            note_count += 1
        else:
            has_links = True
            # Is a proper link
            link = soup.new_tag('a')
            link["id"] = f"link-{link_count}"
            link["href"] = href
            link.string = link_text

            a.replace_with(link)
            links.append({'body': href, 'title': link_text})
            link_count += 1
    return (has_links, has_notes, { 'links': links, 'notes': notes }, str(soup))

def build_footnotes(post, links, has_links, has_notes):

    if not has_links and not has_notes:
        return post

    notes = links['notes']
    links = links['links']
    
    soup = Soup(post, 'html.parser')
    sec = soup.new_tag('section')
    sec['id'] = "backmatter"

    if has_notes:
        # === Notes handling ===
        title = soup.new_tag('h2')
        title.string = "Footnotes"
        sec.append(title)
        ls = soup.new_tag('ol')
        i = 1

        for note in notes:
            li = soup.new_tag('li')
            li['id'] = f"note-{i}-dest" 

            li.append(note['body'])

            backlink = soup.new_tag('a', href=f"#note{i}-src")
            backlink.append('↩')

            li.append(" ")
            li.append(backlink)
            ls.append(li)
            i += 1
        sec.append(ls)
    # === Notes handling ===

    if has_links:
        # === Links handling ===
        title = soup.new_tag('h2')
        title.string = "Links"
        sec.append(title)
        ls = soup.new_tag('ul')
        i = 1
        for link in links:
            li = soup.new_tag('li')
            link_name = soup.new_tag('b')
            link_name.append(f"{link['title']}:")

            li.append(link_name)
            li.append(" ")
            li.append(link['body'])

            a = soup.new_tag('a', href=f"#link-{i}")
            a.string = "↩"

            li.append(a)
            ls.append(li)
            i += 1
        sec.append(ls)
        # === Links handling ===
    soup.append(sec)
    return str(soup)

"""
    Turns all headings into links to the header, plus generates a table of content for the page
"""
def process_headings( post, generate_toc = True ):
    soup = Soup(post, 'html.parser')

    count = 0
    headings = soup.find_all(re.compile(r"^h[1-3]$"))
    if not headings:
        return str(soup)

    table_soup = Soup("", "html.parser")
    # table['id'] = "toc"

    table_root = soup.new_tag('ul')
    table_root['class'] = "toc"

    title = soup.new_tag('a', href=" ")
    title.append("Table of contents")    

    table_root.append(title)
    table_soup.append(table_root)

    current_ul = table_root
    ul_stack = [table_root]
    prev_level = 1

    first = None

    for h in headings:
        if h.text == 'Archive' or h.text == "Notice" or h.text == "Note" or h.text == 'Hint':
            continue

        level = int(h.name[1])
        h_text = h.text
        head = soup.new_tag(f"h{level + 1}")

        head['id'] = f"{h_text.replace(' ', '-').lower()}"
        href = f"#{h_text.replace(' ', '-').lower()}"
        a = soup.new_tag('a', href=href)
        a.append("#")

        a_tag = table_soup.new_tag("a", href=href)
        li_tag = table_soup.new_tag("li")
        li_tag.append(h_text)
        a_tag.append(li_tag)

        head.append(a)
        head.append(" ")
        head.append(h_text)

        h.replace_with(head)
        if first == None:
            first = head
        if level > prev_level:

            new_ul = table_soup.new_tag("ul")
            ul_stack[-1].append(new_ul)
            ul_stack.append(new_ul)
            current_ul = new_ul
        elif level < prev_level:
            for _ in range(prev_level - level):
                ul_stack.pop()
            current_ul = ul_stack[-1]
        count += 1

        current_ul.append(a_tag)
        prev_level = level

    # skip toc generation
    if not generate_toc:
        return str(soup)
        

    table = soup.new_tag('div')
    table['id'] = "toc"

    table.append(table_soup)

    first.insert_before(table)

    return str(soup)
    pass

def process_code_blocks(post):
    soup = Soup(post, 'html.parser')

    for c in soup.find_all('code'):
        wrapper = soup.new_tag('div')
        wrapper['class'] = 'code-highlight'
        code = soup.new_tag('code')
        code.string = c.string
        wrapper.append(code)
        
        c.replace_with(wrapper)
        wrapper.insert_before(soup.new_tag('br'))
        wrapper.insert_after(soup.new_tag('br'))
    return str(soup)


def format_file(post, template):

    # Necessary for every post
    # TODO error handling.
    try:
        template = template.replace("{{title}}", post['post_title'])
        template = template.replace("{{content}}", post['post_content'])
        template = template.replace("{{date}}", pretty_date(post['post_date']))
    except Exception as err:
        print(f"Error: could not process file {post["file_name"]}, err: {err}")
        exit()

    if "post_subtitle" in post:
        template = template.replace("{{subtitle}}", f"<h4>{post['post_subtitle']}</h4>")
    else:
        template = template.replace("{{subtitle}}", "")
    return template
    
def process_posts():
    # Globbed files are unsorted >:[
    post_list = sorted(glob.glob(f"{src_dir}/**/*.md", recursive=True))
    for f in post_list:
        post = {}

        # Read and preprocess the source file.
        print(f"generating {f}...")
        template = open(f"{res_dir}/{post_template}", 'r').read()
        with open( f, 'r' ) as file:

            post = preprocess_file(file)

            post['post_content'] = markdown.markdown( post["post_content"] )

            if not (file.name == "src/archive.md"):
                (has_links, has_notes, links, post['post_content']) = process_notes(post['post_content'])
                post['post_content'] = process_headings(post['post_content'], post['generate_toc'])
                post['post_content'] = build_footnotes(post['post_content'], links, has_links, has_notes)                
            post['post_content'] = process_code_blocks(post['post_content'])

        file_name = os.path.basename( f )
        destination = os.path.join( out_dir , os.path.splitext( file_name )[ 0 ][7:] + ".html" )
        post["dest"] = destination
        destination.rstrip(".md")

        # skip file if the current file is a list file rather than a post file.
        if f.lstrip(src_dir+"/").rstrip(".md") in list_files:
            continue

        print(f"creating file {destination}...")
        with open( destination, 'w', encoding="utf-8" ) as file:
            template = format_file(post, template)
            file.write(template)
        posts.append(post)


def process_index(file: str):
    # list index template file.
    index = open(f'{res_dir}/{list_template}', 'r').read()
    content = open(f'{src_dir}/{file}.md', 'r').read()
    content = markdown.markdown(content)
    list = ''
    last_year = "0"
    file_name = f"{out_dir}/{file}.html"

    for post in reversed(posts):
        year = "".join(post['post_date']).split('.')[0]
        if not (year == last_year):
            # Nasty little hack, but i have a slight headache and i'm losing 
            # my will to keep working on this script anymore today.
            # ( he says as if he wouldn't put in nasty little hacks in his code otherwise )
            last_year = year
            list += f"<h3>{last_year}</h3>"
        list += "<li>"
        list += "<a href=\"/" + post['dest'] + "\">"
        list += "".join(post['post_title'])
        list += "</a></li>"

    print(f"creating file {file}...")
    with open (file_name, 'w') as f:
        index = index.replace("{{content}}", content)
        index = index.replace("{{title}}", file.capitalize())
        index = index.replace("{{posts}}", process_headings(list, False))
        f.write(index)

def create_new_post(name: str):
    today = date.today().strftime("%Y.%m.%d")
    
    if name:
        post = today.replace(".", "").removeprefix("20") + "-" + name + ".md"
    else:
        name = "[title]"
        post = today + ".md"
    file = f"{src_dir}/{post}"
    with open (file, 'w') as f:
        f.write(f"""@post_title {name}
@post_date {today}
@post_subtitle [post_subtitle]
@post_tags tag1 + tag2
---

# {name.capitalize()}

Hello this is a new post wooooo
""")
        f.close()
        pass


# TODO implement match case cmdline arg handling...

if len(sys.argv) < 2:
    print("welcome to jenny!")
    exit()
else:
    match sys.argv[1]:
        case "build":
            process_posts()
            for f in list_files:
                print(f"processing {f}...")
                process_index(f)
        case "new-post":
            print("Input a name for your post:")
            name = input()
            create_new_post(name)
            pass
