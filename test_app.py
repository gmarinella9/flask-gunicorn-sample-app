from flask import Flask

from scrapyscript import Job, Processor
from scrapy.settings import Settings
from scrapy.spiders import Spider
from scrapy import Request
import json

def spider_results():

    # Define a Scrapy Spider, which can accept *args or **kwargs
    # https://doc.scrapy.org/en/latest/topics/spiders.html#spider-arguments
    class PythonSpider(Spider):
        name = 'myspider'

        def start_requests(self):
            yield Request(self.url)

        def parse(self, response):
            #title = response.xpath('//title/text()').extract()
            precio_meta = response.xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[1]/div/div[3]/div/div[1]/div/span/span[2]/text()').extract()
            return {'url': response.request.url, 'precio': precio_meta}

    # Create jobs for each instance. *args and **kwargs supplied here will
    # be passed to the spider constructor at runtime
    githubJob = Job(PythonSpider, url='https://articulo.mercadolibre.com.ar/MLA-850664638-cuadernos-anotador-2020-modelos-de-diseno-_JM#position=1&type=item&tracking_id=cb49fd5e-5e5d-4e33-903b-66f14e0f3ac5')
    # pythonJob = Job(PythonSpider, url='http://www.python.org')

    # Create a Processor, optionally passing in a Scrapy Settings object.
    cust_settings = Settings()
    cust_settings['USER_AGENT'] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36"
    processor = Processor(settings=cust_settings)

    # Start the reactor, and block until all spiders complete.
    data = processor.run([githubJob])

    # Print the consolidated results
    # print(json.dumps(data, indent=4))
    return json.dumps(data, indent=4)


app = Flask(__name__)

@app.route('/')
def home():
	print('\033[1;34m' + 'I can talk!' + '\033[0m')
	data = spider_results()
	return data

	
