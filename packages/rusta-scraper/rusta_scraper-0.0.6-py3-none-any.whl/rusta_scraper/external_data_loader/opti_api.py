import requests
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import snow_flake.snowflake_connection as snowflake_connection
import external_data_loader.constants as const
import snowflake.connector.errors as snowflake_errors
import logging as logger

from pathlib import Path

home = Path.home()


sys.path.append(home)
log_dir = os.path.join(home, "rusta_logs")
try:
        os.makedirs(log_dir, exist_ok=True)
except Exception as e:
    print(f"Error creating log directory: {e}")
    SystemExit(1)

try:
    log = logger.getLogger(__name__)
    fh = logger.FileHandler(os.path.join(log_dir, "opti_loader.log"))
    formatter = logger.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    fh.setFormatter(formatter)
    fh.setLevel(logger.INFO)
    log.addHandler(fh)

    

except Exception as e:
    log.error(f"Error in creating logger: {e}")
    sys.exit(1)


def get_company_id(market_id):
    if market_id == "SWE":
        return "10"
    elif market_id == "FIN":
        return "23"
    elif market_id == "NOR":
        return "20"
    elif market_id == "DEU":
        return "22"
    else:
        return None
    

def get_missing_prices():
    #prep
    # url = f"https://prep.rusta.com/api/MissingPrices"
    url = f"https://prod.rusta.com/api/MissingPrices"
    headers = {
        "accept": "text/json",
        # prep
        # "Authorization": "AE184CFC3DC14025A6E4C13AECC96E24"
        "Authorization": "84722A714CBA49E9969EDEECBD6B3A45"
    }
    
    response = requests.request("GET", url, headers=headers)
    print(response.text)
    if response.status_code == 200 and response.content != b'[]':
        result = response.json()
        if len(result) > 0:
            return result
        else:
            return None
    else:
        log.error(f"Error in getting missing prices: {response.text}")
        return None

def get_prices(articles):
    url = f"https://prod.rusta.com/api/GetPrices"
    headers = {
        "accept": "text/json",
        # prep
        # "Authorization": "AE184CFC3DC14025A6E4C13AECC96E24"
        "Authorization": "84722A714CBA49E9969EDEECBD6B3A45"
    }
    body = articles
    
    response = requests.request("POST", url, headers=headers, json=body)
    print(response.text)
    if response.status_code == 200 and response.content != b'[]':
        result = response.json()
        if len(result) > 0:
            return result
        else:
            return None
    else:
        log.error(f"Error in getting missing prices: {response.text}")
        return None

def load_opti_missing_prices():
    import time
    snowflake = snowflake_connection.Snowflake()
    prices = []
    price_data = get_missing_prices()
    if price_data:
        for price in price_data:
            company = get_company_id(price.get("marketId", ""))
            
            if str(price.get("priceTypeId", "")) == "None":
                price["priceTypeId"] = "False"
            prices.append({
                const.ARTICLE_ID: price.get("catalogEntryCode", ""),
                const.ARTICLE_NAME: price.get("name", ""),
                const.COMPANY: company,
                const.PRICE_TYPE_ID: price.get("priceTypeId", ""),
                const.INSERT_DATE: time.strftime("%Y-%m-%d", time.localtime())
            })
        try:
            
            
            snowflake.execute_query("""DELETE FROM RUSTA_CRAWLER.RUSTA_WEB_CRAWLER.MISSING_PRICES""", "RUSTA_CRAWLER_DWH")
            snowflake.save_data_to_db(prices, "MISSING_PRICES")
        
        except snowflake_errors.DatabaseError as e:
            log.error(f"Error in saving price data to Snowflake: {e}")
            sys.exit(1)
    else:
        log.warning("No missing prices found")
        return

def load_prices():
    import time
    snowflake = snowflake_connection.Snowflake()
    missing_articles = snowflake.execute_query("""SELECT "ARTICLE ID" FROM ACTIVE_ARTICLE_STATUS_NOT_FOUND WHERE "SCRAPE DATE" = CURRENT_DATE""", "RUSTA_CRAWLER_DWH")
    articles = []
    if missing_articles:
        for article in missing_articles:
            articles.append(article[0])
    price_data = get_prices(articles)
    prices = []
    if price_data:
        for price in price_data:
            company = get_company_id(price.get("marketId", ""))
            prices.append({
                const.ARTICLE_ID: price.get("code", ""),
                const.COMPANY: company,
                "price_code" : price.get("priceCode", ''),
                "price_type_id": price.get("priceTypeId", ''),
                "unit_price": price.get("unitPrice", ''),
                "valid_from": price.get("validFrom", ''),
                "valid_until": price.get("validUntil", ''),
                const.INSERT_DATE: time.strftime("%Y-%m-%d", time.localtime())
            })
        try:
            
            
            snowflake.execute_query("""DELETE FROM RUSTA_CRAWLER.RUSTA_WEB_CRAWLER.PRICES""", "RUSTA_CRAWLER_DWH")
            snowflake.save_data_to_db(prices, "PRICES")
        
        except snowflake_errors.DatabaseError as e:
            log.error(f"Error in saving price data to Snowflake: {e}")
            sys.exit(1)
    else:
        log.warning("No missing prices found")
        return




if __name__ == "__main__":
    load_opti_missing_prices()
    result = load_prices()

    