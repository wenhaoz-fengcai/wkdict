<div align="center">

# wkdict (v0.1.0)

A dictionary app sits in your CLI environment.

[![PyPI version](https://badge.fury.io/py/wkdict.svg)](https://badge.fury.io/py/wkdict)
[![Build Status](https://travis-ci.org/jiaowoshabi/wkdict.svg?branch=master)](https://travis-ci.org/jiaowoshabi/wkdict)
[![GitHub issues](https://img.shields.io/github/issues/jiaowoshabi/wkdict.svg)](https://github.com/jiaowoshabi/wkdict/issues)
[![GitHub license](https://img.shields.io/github/license/jiaowoshabi/wkdict.svg)](https://github.com/jiaowoshabi/wkdict/blob/master/LICENSE)


![](https://s3-us-west-1.amazonaws.com/blogassetswenhao/wkdict/Screen+Shot+2019-05-22+at+10.20.04+PM.png)

</div>

## Install on Mac/Linux

Make sure you have the python3 installed on your machine, and use the following command to install `wkdict`

```
pip3 install wkdict
```

## Usage

In terminal, run the application using 

```
wkdict "word-you-wanna-lookup"
```

For example, `wkdict love` will give you the following result:

```
1) love	(UK, US) IPA: /lʌv/
   🏷  noun

	📗 Definitions
	☞ love (countable and uncountable, plural loves)
	☞ (uncountable) Strong affection.
	☞ (countable) A person who is the object of romantic feelings; a
	  darling, a sweetheart, a beloved.

	📘 Examples
	➡ A mother’s love is not easily shaken.
	➡ My husband’s love is the most important thing in my
	  life.
	➡ He on his side / Leaning half-raised, with looks of
	  cordial love / Hung over her enamoured.
...
``` 

## Command options

```
Usage: wkdict [OPTIONS] WORD

Options:
  --limit INTEGER  Maximum number of entries/examples shown.  [default: 3]
  --version        Show the version and exit.
  --help           Show this message and exit.
```

## Changelog

Curren app version(master branch) is `0.1.0`.

Changes in current version:

* Better formatting of dictionary entries
* Add unicode support
* Add test cases
* Add Command-Line Options




<div align="center">

This application is powered by [Wiktionary's](https://www.wiktionary.org/) Dictionary API

</div>