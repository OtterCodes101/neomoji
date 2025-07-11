

# neomojimixer

A simple way to mix up the neomojis.

## What is this?

The neomojimixer makes it a little bit easier for everyone to create new combinations on the well known Neomojis.  
It works with Javascript to provide a experience like the well known piccrew sites.

Try it out here: [neomojimixer](https://entenbru.st/neomojimixer/)

## Did the authors agree to this?

Yes! I asked every author of the neomojis that is linked on the main file.  
Because of this all of this project and the neomojis you are creating are licensed by CC-BY-NC-SA 4.0, so feel free to use them for whatever you want, but please credit the authors not the neomojimixer and ==please don't use any of this for anything commercial==!

## How does it even work?

Basically this is a simple Javascript (no framework used here). It loads all the available parts from the JSON `parts.json` where the source and the name of the part is saved.  
While loading the site the script loads the JSON file and processes all the entries. I have chosen a JSON simply because it is a well known file format and can be easily used in other programs. Feel free to use the parts folder and the `parts.json` for any other project (CC-BY-SA-NC 4.0)  
The rest is just a normal Javascript that responds to `onCLick()` events on the various buttons.

The colour of the arms is determined by the last of the three entries named `"color"` in the JSON of `"body"` and `"arms"`. So only arms will be displayed who match the colour of the base neomoji (e.g. orange for neofox, yellow for neocat, etc). The data is structured in a way that the same arms will have the same position in every Array, so besides a colour change there shouldn't be any visible changes. I try my best to have every arm part ready in everz colour.

The export works in a way that in the background all the parts are drawn onto a canvas and then exported into a PNG that is then displayed. Direct canvas download isn't supported on the most mobile browsers so I chosen to got that little bit longer route, to make it more easily to download any of the mixed neomojis.

## I downloaded it localy, but it doesn't work?!?

Welcome to the world of Javascript!
Due to security reasons javascript that is displayed in a Brwoser can't access files diretly, so to speak on the PC the JavaScript si executed one. The solutions is relativly simple: Run a small http server locally.
I used [lighttpd](https://www.lighttpd.net/) on an Linux laptop, that I started manually every time I worked on the project and had no issues.

## You need help!

YES! I actually do! creating the first 95 elements took me over six hours to make. Some parts where as easy as simply two clicks, others had to be manually extracted, so any help is welcome, especially when you ask yourself the following questions:

`partX` **looks wonky/ doesn't work with** `partY`: As stated it took me quite some work to edit all the parts. So if you are good in editing PNG graphics or have more patience with GIMP, feel free to improve the files!

**I am missing** `partZ` : I haven't and can't add all of the parts the neomojis are made of. For example the `flop` or `up` variants are a little bit tricky because I have to flip the other three layers of the image and adjust for their position to make it fit. Maybe I will work on a solution later, but at the moment its not my main goal.

**"That isn't Javascript, that is an illness!" or "That HTML is ugly as fuck!"** : I am not a professional programmer or webdev of any kind. So if you can improve any of my code, to make it faster or better to read, feel free to send me a pull request. Every help in this way is welcome.

**Why isn't** `$neomoji` **available?** : Probably I don't know about the existence of the neomoji, couldn't reach the original author or they just didn't allowed the usage of it for the neomojimixer.

## Thanks to the following people

[Volpeon](https://is-a.wyvern.rip/@volpeon)
- For creating the [neofox](https://volpeon.ink/emojis/neofox/) and [neocat](https://volpeon.ink/emojis/neocat/) emojis
- For letting me use them in this project

[Justje](https://onemuri.nl)
- For creating the neorat emojis
- For letting me use them in this project

[EeveeEuphoria](https://yiff.life/@EeveeEuphoria)
- For creating the [neopossum emojis](https://yiff.life/@EeveeEuphoria/112039918021786980)
- For letting me use them in this project!

[olivvybee](https://honeycomb.engineer/@olivvybee)
- For creating the [neobread emojis](https://github.com/olivvybee/emojis) and [blobbee emojis](https://github.com/olivvybee/emojis)
- For letting me use them in this project!

[vftdan](https://mastodon.ml/@vftdan)
- For completly rewriting the JavaScript
- Adding drowpdown menus for the part selection

[Johann150](https://genau.qwertqwefsday.eu/@Johann150)
- For the permalink functionality

[Freeplay](https://wetdry.world/@freeplay)
- For redoing the complete User interface

[Fruye](https://codeberg.org/fruye)
- For QoL improvments of the UI

You
- For any feedback, bug report or pull request to improve this project!
