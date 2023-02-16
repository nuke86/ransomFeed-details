<div align="center">
<h1>
  <a href="https://www.ransomware.live">
    ransomware.live 
  </a>
</h1>
</div>

<p align="center">
  <a href="https://github.com/jmousqueton/ransomwatch/actions/workflows/codeql-analysis.yml">
    <img src="https://github.com/jmousqueton/ransomwatch/actions/workflows/codeql-analysis.yml/badge.svg" alt="ransomwatch codeql-analysis analysis" />
  </a>
  <a href="https://github.com/jmousqueton/ransomwatch/actions/workflows/ransomwatch.yml">
    <img src="https://github.com/jmousqueton/ransomwatch/actions/workflows/ransomwatch.yml/badge.svg" alt="ransomwatch engine" />
  </a>
  <a href="https://github.com/jmousqueton/ransomwatch/actions/workflows/ransomwatch-build.yml">
    <img src="https://github.com/jmousqueton/ransomwatch/actions/workflows/ransomwatch-build.yml/badge.svg" alt="ransomwatch dockerimage builder" />
  </a>
  <a href="https://github.com/jmousqueton/ransomwatch/actions/workflows/codeql-analysis.yml">
    <img src="https://github.com/jmousqueton/ransomwatch/actions/workflows/codeql-analysis.yml/badge.svg" alt="ransomwatch codeql analysis" />
  </a>
</p>

[Ransomware.live](https://www.ransomware.live) is a website powered by a modified version of [ransomwatch](https://github.com/joshhighet/ransomwatch).

Ransomware.live is an Ransomware gang tracker, running within github actions, groups are visited & posts are indexed within this repository every hour

missing a group ? try the [_issue template_](https://github.com/jmousqueton/ransomware.live/issues/new?assignees=&labels=✨+enhancement&template=newgroup.yml&title=new+group%3A+)

```shell
curl -sL https://raw.githubusercontent.com/jmousqueton/ransomware.live/main/posts.json | jq
curl -sL https://raw.githubusercontent.com/jmousqueton/ransomware.live/main/groups.json | jq
```

---

<h4 align="center">⚠️</h4>

<h4 align="center">
  content within <code>ransomware.live</code>, <code>posts.json</code>, <code>groups.json</code> and the <code>docs/ & source/</code> directories is dynamically generated based on website of threat actors. <br><br> whilst sanitisation efforts have been taken, by viewing or accessing Ransomware.live generated material you acknowledge you are doing so at your own risk.
</h4>

---

## Technicals

The [torproxy](https://github.com/jmousqueton/ransomware.live/torproxy) from [**jmousqueton/ransomware.live/torproxy** registry](https://github.com/jmousqueton/jmousqueton/pkgs/container/ransomwatch%2Ftorproxy) is introduced into the github actions workflow as a [service container](https://docs.github.com/en/actions/guides/about-service-containers) to allow onion routing within [ransomwatch.yml](https://github.com/JMousqueton/ransomware.live/blob/main/.github/workflows/ransomwatch.yml)

The frontend is ultimatley markdown, generated with [markdown.py](https://github.com/jmousqueton/ransomware.live/blob/main/markdown.py) and served with [docsifyjs/docsify](https://github.com/docsifyjs/docsify) thanks to [pages.github.com](https://pages.github.com)

Any graphs or visualisations are generated with [plotting.py](https://github.com/jmousqueton/ransomware.live/blob/main/plotting.py) with the help of [matplotlib/matplotlib](https://github.com/matplotlib/matplotlib)

_Post indexing is done with a mix of [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) and command line with `grep`, `awk` and `sed` within [parsers.py](https://github.com/jmousqueton/ransomware.live/blob/main/parsers.py)._

[`groups.json`](https://github.com/jmousqueton/ransomware.live/blob/main/groups.json) contains hosts, nodes, relays and mirrors for a tracked group or actor

[`posts.json`](https://github.com/jmousqueton/ransomware.live/blob/main/posts.json) contains parsed posts, noted by their discovery time and accountable group

[Ransomware.live](https::/www.ransomware.live) uses Ransomware Note from [Zscaler ThreatLabz](https://github.com/threatlabz/ransomware_notes)

[Ransomware.live](https::/www.ransomware.live) uses Ransomware group description from [Malpedia](https://malpedia.caad.fkie.fraunhofer.de/)

## Analysis tools

All rendered source HTML is stored within [ransomwatch/tree/main/source](https://github.com/jmousqueton/ransomware.live/tree/main/source) - change tracking and revision history of these blogs is made possible with git

### [screenshotter.py](https://github.com/jmousqueton/ransomare.live/blob/main/screenshotter.py)

_A script to generate high-resolution screenshots of all online hosts within `groups.json`_

### [srcanalyser.py](https://github.com/jmousqueton/ransomware.live/blob/main/srcanalyser.py)

_A [beautifulsoup](https://code.launchpad.net/~leonardr/beautifulsoup/bs4) script to fetch emails, internal and external links from HTML within `source/`_

## Cli operations

_fetching sites requires a local tor circuit on tcp://9050 - establish one with;_

```shell
docker run -p9050:9050 ghcr.io/jmousqueton/ransomwatch/torproxy:latest
```

### Group management

_manage the groups within [groups.json](groups.json)_

#### Add new location (group or additional mirror)

```shell
python3 ransomwatch.py add --name acmecorp --location abcdefg.onion
```

## Scraping

```shell
python3 ransomwatch.py scrape 
```

or to force scraping host with `enabled: False`

```shell
python3 ransomwatch.py scrape --force 1
```


## Parsing

Iterate files within the `source/` directory and contribute findings to `posts.json`

> for a crude health-check across all parsers, use `assets/parsers.sh`

```shell
pyhton3 ransomwatch.py parse
```

## Get crypto wallets

Parse the [ransomwhe.re](https://ransomwhe.re) API to get crypto wallet for Ransomware gang

```shell
pyhton3 addcrypto.py 
```

## Generating page

```shell
python3 ransomwatch.py markdown 
```

## Generating RSS Feed based on posts.json

```shell
python3 generateRSS.py  
```

## Misc

### [source.zsh](https://github.com/jmousqueton/ransomare.live/blob/main/assets/sources.zsh)

_Scan well knowd sites for new Ransomware Gang site_ 

```shell
./asset/sources.zsh 
```
### [sitemap.sh](https://github.com/jmousqueton/ransomware.live/blob/main/assets/sitemap.sh)

_Generate sitemap.xlm_ 

```shell
./asset/sitemap.sh
```

### [OrderGroups.sh](https://github.com/jmousqueton/ransomware.live/blob/main/assets/orderGroups.sh)

_Re-order `groups.json` by group name_

```shell
./asset/orderGroups.sh
```

---

_ransomware.live is [licensed](https://github.com/jmousqueton/ransomware.live/blob/main/LICENSE) under [unlicense.org](https://unlicense.org)_
