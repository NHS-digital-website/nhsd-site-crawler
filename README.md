# NHSD Crawler

This project contains code for the NHSD sitemap generator and content compare tool.

The spiders use the scrapy framework, for which documentation can be found here,
https://docs.scrapy.org/

## Requirements and Installation

Scrapy requires Python 3.7+. You can check your python version with the command, `python --version`.

Before running the crawlers the scrapy package must first be installed. This can be done with pip:

`pip install Scrapy`

Once installed scrapy crawlers can be ran with the scrapy tool:

`scrapy crawl [spider-name]`

Further installation information can be found here,
https://docs.scrapy.org/en/latest/intro/install.html

## Sitemap Generator

The sitemap generator is a simple scrapy spider designed to crawl the NHSD site and output found URLs.

It will follow all links until there are no more unique pages to crawl.

Note: There is no depth limit so this scraper can get stuck in loops on pages where URLs can be generated to an infinite depth.


### Usage

`scrapy crawl nhsd-sitemap-generator`

## Content compare tool

The content comare tool will crawl a reference site for unique pages and resources.

Any found page content and resources are then matched to a test site to validate content.

Note: There is no depth limit so this scraper can get stuck in loops on pages where URLs can be generated to an infinite depth.


### Usage

`scrapy crawl nhsd-sitemap-generator`


## Code Overview

Inside the `nhsd` project directory you'll find code for the nhsd spiders.

`settings.py` defines the spider pipelines, middleware, and spider configuration.

`pipelines.py` contains code for exporting items yielded by the spider. These items are defined in `items.py`.

`middlewares.py` contains boilerplate middleware code created when the project was initalised.

The `spiders` directory contains code for the spiders themselves. This is where the spider logic can be modified as needed.
