
Ransomware.live is a ransomware groups observatory based on [ransomwatch](https://github.com/joshhighet/ransomwatch) and inspired by [ransomlook](https://github.com/RansomLook/RansomLook). 

Ransomware.live is a ransomware leak site monitoring tool. It will scrape all of the entries on various ransomware leak sites and published them [here](recentposts.md).

## 📜 License

ransomwatch is [licensed](https://github.com/jmousqueton/ransomwatch/blob/main/LICENSE) under [unlicense.org](https://unlicense.org/)

## ⚠️ Disclamer

Contents within ransomware.live, posts.json, groups.json and the docs/ & source/ directories are dynamically generated based on hosting choices of real-world threat actors in near-real-time.
whilst sanitisation efforts have been taken, by viewing or accessing ransomwatch you acknowledge you are doing so at your own risk.

## 🤖  How it works

`ransomware.live` is orginally based on [ransomwatch](https://github.com/joshhighet/ransomwatch) developped by [Joshhighet](https://github.com/joshhighet). It has been modified by [me](about.md?id=%f0%9f%91%a8%f0%9f%8f%bc%f0%9f%92%bc-about-me) : 
* new parsers fully in `python` to include **victims description**, **website** and **published date** when available, that's include a new scheme for posts : 
  ```json
      {
        "post_title": "",
        "group_name": "",
        "discovered": "",
        "description": "",
        "website": "",
        "published": ""
      },
  ```  
* Rewrite parsers using [beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) 
* Take a screenshot of ransomware gang websites when a new leak entry is detected 
* Add night/day theme ☀️/🌙
* Add ransom notes when available for each ransomware gang in the [profiles](profiles.md) page
* Add description of ransomware gang in the [profiles](profiles.md) page
* Add a [full list](allposts.md) of ransomware gang entries 
* Add a [Change Log](CHANGELOG.md)
* Add Pushover notification 
* Add a [RSS Feed](https://www.ransomware.live/rss.xml)
* Add a field `delay` in seconds for every Group locations before scraping (not mandatory)
* Add crypto wallet from [ransomwhe.re](https://ransomwhe.re/)
* And much more minor modifications


`ransomware.live` uses github actions to do everything ... yes it's server less 😄

`ransomware.live` is mainly developped in Python. It computes the following actions : 

* Scrape ransomware gang websites `python3 ransomwatch.py scrape`
* Parse the scraped websites `python3 ransomwatch.py parse`
  during this stage `ransomware.live`takes a screenshot of ransomware gang websites which has a new entry and also generate **.json** and **.cvs** files with all the ransomware gangs leaks
* Generate the website pages in markdown `python3 ransomwatch.py markdown` 
* Publish the website with [docsify](https://docsify.js.org/) on Github Pages 

Check [here](howitworks.md) for more details. 

## 🤖 Fonctionnement (French only 🇫🇷)

Retrouver les explications quant au fonctionnement de `ransomware.live` sur mon blog : [julien.io](https://julien.io/ransomware-live/). 

## 🛠️ ToDo 


| type | group |  task | progress | 
|--|--|--|--| 
| ~~Parser~~ | ~~Daixin~~ | ~~parse website~~ | ~~100%~~ | 
| Parser | all | Add published date when available in all parsers | 6% | 
| Markdown | Victims | Show published date instead of parsing date | 0 % | 

## 👨🏼‍💼 About me 

I'm **Julien Mousqueton**

- I'm **CTO** in Cyber Security 🛡 @ [Computacenter](https://www.computacenter.com) 🇫🇷
- I'm a **lecturer** 🎓 in Cyber Security @ [Ecole 2600](https://www.ecole2600.com) 🏴‍☠️
- I'm a **blogger** ✍🏻 at [julien.io](https://julien.io) in french 🇫🇷 

You can find more in [my resume](https://cv.julien.io) in English (also available in [French](https://cv.julien.io/fr) / aussi disponible en [français](https://cv.julien.io/fr))

## 🔭 Sources 

You can find all ransomware leaks in **json** format [here](https://raw.githubusercontent.com/JMousqueton/ransomwatch/main/posts.json) or in **CSV** format [here](https://www.ransomware.live/posts.csv).

## ♻️ Changelog 

You can find the changelog [here](CHANGELOG.md).

## ⚙️ Contribution

Ransomwatch.live is also reliant on third-party contributions. Please open a pull request or issue on the [Github repository](https://github.com/jmousqueton/ransomwatch/issues).

## 🤩 Credits

- [Josh Highet](https://github.com/joshhighet) for the original [ransomwatch](https://github.com/joshhighet/ransomwatch) project. 
- [Ransomlook](https://github.com/RansomLook/Ransomlook) for ideas of new features included in [Ransomware.live](https://www.ransomware.live).
- [ransomwhe.re](https://ransomwhe.re/) for the crypto wallet information 
- [Zscaler ThreatLabz](https://github.com/threatlabz/ransomware_notes) for the ransomware notes 
- [Valéry Rieß-Marchive](https://twitter.com/ValeryMarchive) for the idea💡 to included published date when available 

