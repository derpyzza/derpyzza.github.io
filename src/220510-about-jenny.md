@post_title Writing Jenny
@post_subtitle My tiny static site generator
@post_date 2022.05.10
---

<div class="infobox note">
  <h3>Notice</h3>
  This post is pretty old.
  It was written for an older version of this site, which
  had a radically different design to what it is now, which leads to it having weird
  quirks that you won't notice in any other post on this site.
  I originally got rid of this post when i got rid of the old site,
  as i wanted to start afresh, but i've brought it back as i wanted to preserve a record
  of my writing. As such, this post doesn't fit in very well with the rest of my site, and sticks out a bit.
  I've cleaned it up just enough to make it work on this new site, but that still leaves
  it with sections that don't make sense in the current layout.
  But that's alright.
</div>

# Jenny
i've been wanting to start a small blog to kinda document my projects and stuff for a while now, and a couple days ago i decided to just sit down and finally make one. going into it however, i had some requirements i needed to satisfy:

- the site needed to be lightweight. like *really* lightweight. like fits-in-under-512-kb-so-i-can-join-the-[512kb-club][1] lightweight.
- quick and easy to use / deploy. i didn't want to learn a super cool fancy website builder tool that reads your mind and spits out your dream site.
- no javascript, atleast to start out with.
- no fancy databases. each post would just be a separate html file.
- free and open source.

essentially, i wanted a very minimal setup. i write a post, post appears on my website. simple. before writing jenny i tried out [jekyll][2], and while jekyll sort of ticked off all my requirements,
i still didn't like it too much. the main reason was because i didn't really understand how it worked too well, and i really did not want to sit down and read the documentation for it ( im lazy ).
so as a fix for my problems, i just wrote jenny :D [jenny is derived from the word 'generator'. as in, 'jenny-rator'. i uwu-fied it kinda ig](_)

# What
is jenny? jenny, is a small, super opinionated [opinionated as in i was too lazy to add any sort of user friendly features for anyone that isn't me](_) static site generator.
it reads in every <mark>.md</mark> file from a <mark>src/</mark> directory, translates them to a <mark>.html</mark> with the help of a template <mark>.html</mark> file which tells the script how to generate the output files, and places them into a <mark>public/</mark> directory. this way, i can just write all my posts in markdown (which is essentially just plain text with extra features), and have the script turn my posts to a web friendly format for
others like you to see!

# Why
would you write your own static site generator? why not use a different one like hugo or something if you didn't like jekyll? why not just simply write your posts in html? well, those are all
perfectly valid questions. the real reason i wrote my own static site generator instead of just searching for a better one to use ( there's like [billions][3] of them ) is primarily because it sounded
like an interesting project. it's functionally very simple, you can extend it as much as you want, and it's quite a useful tool, so writing my own was loads more fun and educational than using someone 
else's project. if however, you do not care about all that stuff and just want a simple way to write your posts, i would just recommend using a static site generator written by someone else. and as 
for writing my posts in html, while it's a perfectly acceptable way to write a blog, it's frankly quite a chore. so writing my own generator sounded a seemed to be the best way to get exactly 
what i wanted :)

# How
does it really work? ( as of the time of writing ) jenny is essentially just a small python script that expects three things: a <mark>src/</mark> directory that contains <mark>.md</mark> files, an 
<mark>assets/</mark> directory that contains a stylesheet and two template <mark>.html</mark> files ( one for the main page, and one for the actual posts themselves ) and a <mark>public</mark> directory. the script reads through every <mark>.md</mark> file in the <mark>src/</mark> directory, and first off preprocesses the file for some metadata. metadata for jenny follows the following syntax:
```
  $command args...
```
metadata must always begin with a dollar symbol, immediately followed by a command or keyword that tells the program what kind of data it is, followed by a space delimited string of arguements to the
command. currently, jenny only supports three commands: title, subtitle, and data. all three of these are used in displaying the title of the post on the post page, as well as displaying the title on
the main page. after the preprocessing stage, jenny converts the raw markdown posts to a <mark>.html</mark> page using the aforementioned template files, and stores the post to a list of posts along with their titles, subtitles, and dates. jenny then just takes all that data, and feeds it through another template to produce an index file as the landing page of the blog. and... that's it! jenny is in itself a super basic script. it only does what it needs to, and nothing else. it ends up being slightly not user friendly as a direct cause of that simplicity sometimes, but that's my fault for just rushing the implementation a bit hehe.

# Final notes
so, that's jenny! jenny was quite fun to work on, and most importantly, jenny is a very useful tool for me personally, which really makes all the html and css i had to write worth it in the end.
as of writing this, jenny is still missing a couple features that i would like to add, namely some nice configuration features to make setting up a blog easier, as well as a checker thing that only updates the files that have been recently edited. i plan to write a blog post a week and my blog folder will really start filling up quickly, and i dont want to sit there waiting for python to try and format all the scripts.
i'd like to quickly thank [bob nystrom][4], and [kenton hamaluik][5] for their lovely static site generators, which i used as reference. go check them out, they were really helpful!
this is my first ever blog post, so sorry for the monotonous tone. it'll definitely get better soon lol.

[1]:https://512kb.club
[2]:https://jekyllrb.com/
[3]:https://jamstack.org/generators/
[4]:https://github.com/munificent/game-programming-patterns
[5]:https://github.com/hamaluik/blog.hamaluik.ca
