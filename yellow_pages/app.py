from flask import Flask, request, jsonify
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor, defer
from threading import Thread
from flask_cors import CORS
import csv
import traceback

# Import your Scrapy spider
from yellow_pages.spiders.crawl import CrawlSpider

app = Flask(__name__)
CORS(app)

# Initialize Scrapy settings
settings = get_project_settings()
runner = CrawlerRunner(settings)

# Global variable to store spider output
spider_output = []


# Function to run Scrapy spider
@defer.inlineCallbacks
def run_spider(param1, param2, count):
    global spider_output
    try:
        # Run the spider and wait for it to complete
        d = runner.crawl(CrawlSpider,
                         param1=param1,
                         param2=param2,
                         count=count)
        d.addBoth(
            lambda _: reactor.stop())  # Stop reactor when spider completes
        reactor.run()
        # print(dir(runner))
        # print(d)
        # spider_output = getattr(runner, 'spider_output',
        #                         None)  # Access spider output here
    except Exception as e:
        print(f"Error while running spider: {e}")
        # traceback.print_exc()
    finally:
        if reactor.running:
            reactor.stop()  # Stop reactor from main thread


# Endpoint to trigger Scrapy spider
@app.route('/scrape', methods=['GET'])
def scrape():
    try:
        # data = request.json
        param1 = request.args.get('query1')
        param2 = request.args.get('query2')
        count = request.args.get('count')
        print('request---------------------------------->', request, param1,
              param2, count)
        # Reset spider output
        global spider_output
        spider_output = []

        # Run spider in a separate thread
        thread = Thread(target=run_spider, args=(param1, param2, count))
        thread.start()

        # Wait until spider completes
        thread.join()

        filename = f'{param1}_{param2}_results.csv'
        with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            spider_output = [dict(row) for row in reader]
        # Respond with spider output if available
        if spider_output:
            return jsonify(spider_output), 200
        else:
            return jsonify({"message": "No data returned from spider."}), 500

    except Exception as e:
        return jsonify({"message": f"Error starting scraping: {e}"}), 500


if __name__ == '__main__':
    # reactor.run()
    app.run('0.0.0.0', debug=True)
