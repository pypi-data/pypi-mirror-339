from abc import ABC, abstractmethod
import os
import sys
import logging
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from  spider.spiders import rusta_spider
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import Spider
import argparse
import datetime



# Step 1: Define the Spider interface
class Spider(ABC):
    @abstractmethod
    def create(self):
        pass

# Step 2: Create concrete classes
class NewSiteSpider(Spider):
    def create(self, *args, **kwargs) -> rusta_spider.NewEcomSpider:
        return rusta_spider.NewEcomSpider
    
# Step 3: Define the SpiderFactory class
class SpiderFactory(ABC):
    @abstractmethod
    def create_spider(self,  *args, **kwargs) -> Spider:
        pass

# Step 4: Implement concrete factories
class NewEcomSpiderFactory(SpiderFactory):

    def create_spider(self, *args, **kwargs) -> Spider:
        return NewSiteSpider()


# Client code
class SpiderClient():

    def __init__(self):
        home = os.path.expanduser("~")

        log_dir = os.path.join(home, "rusta_logs")

        try:
            os.makedirs(log_dir, exist_ok=True)
        except Exception as e:
            print(f"Error creating log directory: {e}")
            SystemExit(1)

        log_file = os.path.join(log_dir, f"spider factory {datetime.date.today().strftime('%Y-%m-%d')}.log")

        try:
            self.log = logging.getLogger(__name__)
            fh = logging.FileHandler(log_file)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
            fh.setFormatter(formatter)
            fh.setLevel(logging.INFO)
            self.log.addHandler(fh) 

        except Exception as e:
            print(f"Error setting up logging: {e}")

        self.log.info("SPIDER FACTORY - Initialized SpiderClient")
        
    def create_spider(self, factory: SpiderFactory, *args, **kwargs) -> None:
        spider_factory = factory.create_spider(*args, **kwargs)
        if kwargs.get('ctr'):
            ctr = kwargs.get('ctr')
            for c in ctr:
                sp = spider_factory.create()
                process = CrawlerProcess()
                kwargs['ctr'] = c
                process.crawl(sp, **kwargs)
        else:
            sp = spider_factory.create()
            process = CrawlerProcess()
            process.crawl(sp, **kwargs)
        process.start()

    def run_new_ecom_site_spider(self, scrape_type, ctr=None, debug=None):
        
        if ctr:
            ctr = [c.upper() for c in ctr]
        kwargs = { "ctr": ctr, "scrape": scrape_type, "debug": debug}
        new_site_factory = NewEcomSpiderFactory()  
        self.create_spider(new_site_factory, **kwargs)

    def list_of_strings(arg):
        return arg.split(',')

    def run_spider(self, parser):
        args = parser.parse_args()
        if args.scrape in ['week', 'rolling']:
            self.log.info("SPIDER FACTORY - Creating spider")
            self.run_new_ecom_site_spider(scrape_type=args.scrape)
        elif args.scrape == 'active' and args.ctr:
            for ctr in args.ctr:
                if ctr.upper() not in ['SE', 'NO', 'FI', 'DE']:
                    parser.error(f"Invalid country code: {ctr}")
            self.log.info(f"SPIDER FACTORY - Running spider for {ctr}")
            self.run_new_ecom_site_spider(ctr=args.ctr, scrape_type=args.scrape, debug=args.debug)
        else:
            parser.error("Please provide required arguments")
    

def list_of_strings(arg):
    return arg.split(',')

if __name__ == "__main__":
    spider_client = SpiderClient()
    parser = argparse.ArgumentParser(description='Run Scrapy spiders with common input.')
    parser.add_argument('--scrape', type=str, help='week rolling active', required=True)
    parser.add_argument('--ctr', type=list_of_strings, help='Countries. SE NO DE FI. For multiple countries seperate with "," ', required=False)
    parser.add_argument('--debug', type=str, required=False)
    spider_client.run_spider(parser)



    