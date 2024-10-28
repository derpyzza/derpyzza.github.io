@post_title Hacky script, Perfect script
@post_date 2023.05.12
@post_subtitle a tale of one of those rare moments where i broke through the endless cycle of procrastination.
---

Back in 2022 i decided to start a tiny little personal blog. i designed a lightweight website, and spun up a 
quick little python script that acted as a static site generator [I named it jenny!](_) where i wrote my blogposts in markdown in a source folder somewhere, and my script then translated them into html files with the help of predefined templates. that blog only lasted one blogpost before i abandoned it / forgot about it.

Fast forward to april 2023. i started cutting out social media from my devices, and consuming a lot more medium-to-long-form-content, like books and blogs, which made me want to re-start my blog. there was, however, a problem with my old setup: my beloved little python script ***sucked***. it was a tiny hacky terribly-slow little script designed solely to work on that specific website with that specific design, with no error handling, no configuration ability, no nothing!

That was, obviously, completely unacceptable. i decided to create the ultimate tiny static site generator, one that is both flexible and configurable *and* tiny. the one tiny ssg to rule them all!!!

## Narrator voice: He did not, in fact, make the ultimate tiny ssg

So, i failed. Yup. My plans were big and grandiose, but my skills and patience were painfully limited.
originally, the plan was to simply remove all of my original painpoints with jenny, and to just make it more user friendly. the plan was to rewrite jenny in Go, as it is, and just add some tiny little QOL features, such as

+ error handling
+ project generation
+ modular codebase

Sounds simple, right? 

Right??

Wrong.

You see while it worked (mostly. i did not finish the whole thing), it had a major, unforgivable flaw: it was **boring**. working on it was not exciting in the least, as i was essentially just copying the python script to Go, and sprinkling a couple QOL features here and there. Absolutely unacceptable; where's the pizzaz? the glamour? the uniqueness and the quirkyness?? where's the excitement of it all???

I abandoned the go generator (surprise surprise), and that is when i started my slow descent to madness. i spent about two weeks staring at other ssgs, reading blogposts about ssgs, comparing programming languages, furiously scribbling notes, daydreaming about working on my ssg, etc. etc. all the while starting random little implementations of my ideas before scrapping them and going back to the procrastination/research loop.

## The inevitability of jenny

After struggling with fennel one day [I wanted to write a custom markdown parser, along with a lisp-based templating language in fennel](_), i wandered over to my original python repo. i decided to either use jenny, or some popular static site generator [But but my customization!! my minimalism!! noooooooooooo](_) to atleast get a blog up and running while i messed around with my better-stronger-faster-one-ssg-to-rule-them-all-ssg. 

I went ahead and pulled down the original jenny repo, and quickly tweaked it so that it was a tiny hacky terribly-slow little script designed solely to work on this specific website with this specific design, with no error handling, no configuration ability, no nothing.

## This website runs on jenny

It worked pretty well. i was able to get my website up and running, the way i wanted it to be. i can now post my notes and thoughts on this site, and have them go online without any problems, which is precisely what jenny is meant to do.

So perhaps i did not in fact need a super high powered ultra mega minimal exciting perfect static site generator to rule them all that will be done soon™. perhaps all i needed was a hacky little python script i wrote one year ago that works perfectly fine, right now.

* * *
 
<span>*i still am going to make my ultra minimal mega static site generator sometime soon tho. err maybe.* </span>
