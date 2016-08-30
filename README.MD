# About

A simple script to scrape urls from [dotup.org](http://www.dotup.org/) or [light.dotup.org](http://light.dotup.org/).
Deprecated by [dotup-scrapy](https://github.com/onnudilol/dotup-scrapy).

# Usage

<pre><code>python dotup.py</code></pre>

will output a list of URLs to the current working directory.

<pre><code>python dotup.py light</code></pre>

will do the same for light.dotup.org URLs.

# Settings

Specify the oldest file in the format of { Number ID }.{ extension }.  The scraper will continue to fetch URLs until
it reaches that file.