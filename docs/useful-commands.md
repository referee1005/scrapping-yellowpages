To create a project, run:

```bash
scrapy startproject [project_name] [directory_name]
```

[directory_name] can be omitted, if ommitted, it will be same as project name

After the project is created, run the following command to create a templated spider:

```bash
cd [project_root_directory]
scrapy genspider example example.com
```

This will generate a example.py spider in the [directory_name]/spiders folder and use example.com as the startup_url

To crawl using [quotes_spider.py](tutorial/spiders/quotes_spider.py), run from root directory of "tutorial" project:

```bash
scrapy crawl quotes
```

The best way to learn how to extract data with Scrapy is trying selectors using the shell Scrapy shell. Run:

```bash
scrapy shell "http://quotes.toscrape.com/page/1/"
```

The simplest way to store the scraped data is by using Feed exports, with the following command:

```bash
scrapy crawl quotes -o quotes.json
```

Or JL for JSON Lines (good for streaming / appending)

```bash
scrapy crawl quotes -o quotes.jl
```

