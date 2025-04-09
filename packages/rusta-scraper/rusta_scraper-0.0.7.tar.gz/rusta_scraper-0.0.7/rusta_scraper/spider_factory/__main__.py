import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from spider_factory import SpiderClient
from spider_factory import list_of_strings
spider_client = SpiderClient()
import argparse
parser = argparse.ArgumentParser(description='Run Scrapy spiders with common input.')
parser.add_argument('--scrape', type=str, help='week rolling active', required=True)
parser.add_argument('--ctr', type=list_of_strings, help='Countries. SE NO DE FI. For multiple countries seperate with "," ', required=False)
parser.add_argument('--debug', type=str, required=False)
spider_client.run_spider(parser)