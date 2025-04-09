import requests
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)


import snow_flake.snowflake_connection as snowflake_connection
import constants as const
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
    fh = logger.FileHandler(os.path.join(log_dir, "pim_loader.log"))
    formatter = logger.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    fh.setFormatter(formatter)
    fh.setLevel(logger.INFO)
    log.addHandler(fh)

    

except Exception as e:
    log.error(f"Error in creating logger: {e}")
    sys.exit(1)




def get_channels(ent_id):
    log.info(f"Fetching channels for entity id: {ent_id}")  # Added logging
    url = f"https://apieuw.productmarketingcloud.com/api/v1.0.0/channels?forEntityId={ent_id}&includeChannels=true&includePublications=false"
    headers = {
        "accept": "text/json",
        "X-inRiver-APIKey": "82833a25339d857579b60a848c09caf0"
    }

    channel = ""
    response = requests.request("GET", url, headers=headers)
    if response.status_code == 200 and response.content != b'[]':
        result = response.json()
        if len(result) > 0:
            for field in result:
                if field["displayName"] == "RustaEcom":
                    channel = field["displayName"]
                    break
        # if not channel:
                # log_warning(f"RustaEcom channel not found for entity id: {ent_id}")
    elif response.status_code == 200 and response.content == b'[]':
        log.warning(f"Channels for entity id: {ent_id} wasn't found")
    else:
        log.error(f"Error in getting channels for entity id: {ent_id}")
    log.info(f"Channel found: {channel}")  # Added logging
    return channel
#=====================================================
def get_missing_articels_values(ent_ids):
    log.info(f"Fetching missing article values for entity ids: {ent_ids}")  # Added logging
    url = f"https://apieuw.productmarketingcloud.com/api/v1.0.1/entities:fetchdata"
    
    headers = {
        "accept": "text/json",
        "X-inRiver-APIKey": "82833a25339d857579b60a848c09caf0"
    }


    payload = {
        "entityIds": ent_ids,
        "objects": "FieldValues",
        "fieldTypeIds": "ProductEnrichment,ItemPublicationCode,ItemEcomStatusSE,ItemEnableEcomSE,ItemEcomStatusNO,ItemEnableEcomNO,ItemEcomStatusDE,ItemEnableEcomDE,ItemEcomStatusFI,ItemEnableEcomFI,ItemActiveWebSE,ItemActiveWebNO,ItemActiveWebDE,ItemActiveWebFI,ItemLongCopy,ResourceFilename,ResourceType,OptionLongCopy,ProductType,ProductCategory",        "outbound": {
                    "linkTypeIds": "ItemImage,",
                    "objects": "FieldValues",
                    }, 
        "inbound": {
                    "linkTypeIds": "ProductOption",
                    "objects": "FieldValues",
                    }
    }


    response = requests.request("POST", url, json=payload, headers=headers)
    if response.status_code == 200:
        if response.content != b'[]':
            result = response.json()
            if len(result) > 0:
                log.info(f"Fetched data: {result}")  # Added logging
                return result
        else:
            log.warning(f"Empty response for entity ids in API fetch data: {ent_ids}")
            return {}
    

def get_linked_entity_id(ent_id, link_typeId):
    entity_id = None

    log.info(f"Fetching linked entity id for entity id: {ent_id} with link type: {link_typeId}")  # Added logging
    url = f"https://apieuw.productmarketingcloud.com/api/v1.0.0/entities/{ent_id}/links?linkTypeId={link_typeId}"


    headers = {
        "accept": "text/json",
        "X-inRiver-APIKey": "82833a25339d857579b60a848c09caf0"
    }

    response = requests.request("GET", url, headers=headers)

    if response.status_code == 200:
        if response.content != b'[]':
            result = response.json()
            if len(result) > 0 and link_typeId in ("OptionItem", "ProductOption"):
                entity_id = result[0]["sourceEntityId"]
        else:
            log.warning(f"Empty response for entity id linked entity: {ent_id}")
    else:
        log.warning(f"Error in getting linked entity id for entity id: {ent_id}")
    return entity_id

def get_entity_id(ent_id, type, type_value, field_type_id):
    url = f"https://apieuw.productmarketingcloud.com/api/v1.0.0/query"

    # log_info(f"Getting entity id for item number: {ent_id}")

    headers = {
        "accept": "text/json",
        "X-inRiver-APIKey": "82833a25339d857579b60a848c09caf0"
    }


 


    payload =  {

        "systemCriteria": [
            {
                "type": type,
                "value": type_value,
                "operator": "Equal"
            }
        ],
        "dataCriteria": [
            {
                "fieldTypeId": field_type_id,
                "value": ent_id,
                "operator": "Equal"
            }
        ]
     
}
     

                

    response = requests.request("POST", url, json=payload, headers=headers)
    entity_id = None
    if response.status_code == 200:
        if response.content != b'[]':
            result = response.json()
            if result["count"] == 1:
                # print("Entity found")
                # print(result["entityIds"][0])
                entity_id = result["entityIds"][0]
            else:
                log.warning(f"Multiple entities found for item number: {ent_id}")
        else:
            log.warning(f"Empty response for entity id in API query for item number: {ent_id}")
    else:
        log.error(f"Error in getting entity id in API query for item number: {ent_id}")

    return entity_id



def get_pim_data(item):
    option_entity_id = ""
    item_entity_id = get_entity_id(item, "EntityTypeId", "Item", "ItemNumber")
    if item_entity_id:
        option_entity_id = get_linked_entity_id(item_entity_id, "OptionItem")
        article_data = get_missing_articels_values([item_entity_id, option_entity_id])  
        return parser(article_data, item_entity_id, option_entity_id)
    else:
        return None

def parser(data, item_entity_id, option_entity_id):

    item_long_copy = {}
    item_ecom_status = {}
    item_enable_ecom = {}
    item_active_web = {}
    item_images = []
    option_long_copy = {}
    product_details = {}
    item_publish_code = ""
    item_image_resc_type = False  # Initialize item_image_resc_type
    item_image_file_name = ""  # Initialize item_image_file_name
    product_entity_id = ""
    product_enrichment = ""
    # Extract values
    for entry in data:
        if 'fieldValues' in entry:
            for field in entry['fieldValues']:
                if field['fieldTypeId'] == 'ItemLongCopy':
                    item_long_copy = field['value']
                elif field['fieldTypeId'] == 'ItemPublicationCode':
                    item_publish_code = field['value']
                elif field['fieldTypeId'].startswith('ItemEcomStatus'):
                    country_code = field['fieldTypeId'][-2:]
                    item_ecom_status[country_code] = field['value']
                elif field['fieldTypeId'].startswith('ItemActiveWeb'):
                    country_code = field['fieldTypeId'][-2:]
                    item_active_web[country_code] = field['value']
                elif field['fieldTypeId'].startswith('ItemEnableEcom'):
                    country_code = field['fieldTypeId'][-2:]
                    item_enable_ecom[country_code] = field['value']
                elif field['fieldTypeId'] == 'OptionLongCopy':
                    option_long_copy = field['value']
                
        if 'inbound' in entry:
            for inbound in entry['inbound']:
                if inbound.get('linkTypeId') == 'ProductOption':
                    product_entity_id = inbound['entityId']
                    for field in inbound['fieldValues']:
                        if field['fieldTypeId'] == 'ProductType':
                            product_details['ProductType'] = field['value']
                        if field['fieldTypeId'] == 'ProductEnrichment':
                            product_details['ProductEnrichment'] = field['value']
                        elif field['fieldTypeId'] == 'ProductCategory':
                            product_details['ProductCategory'] = field['value']
        if 'outbound' in entry:
            for outbound in entry['outbound']:
                if outbound.get('linkTypeId') == 'ItemImage':
                    resource_filename = None
                    resource_type = None
                    for field in outbound['fieldValues']:
                        if field['fieldTypeId'] == 'ResourceFilename':
                            resource_filename = field['value']
                        elif field['fieldTypeId'] == 'ResourceType' and field['value'] == 'F':
                            resource_type = field['value']
                            item_image_resc_type = True  # Set item_image_resc_type to True
                            item_image_file_name = resource_filename  # Set item_image_file_name
                            break  # Skip the list of images
                    if resource_filename and resource_type:
                        item_images.append({
                            'ResourceFilename': resource_filename,
                            'ResourceType': resource_type
                        })

    item_channel = ""
    option_channel = ""
    product_channel = ""
    if item_entity_id:
        item_channel = get_channels(item_entity_id)
    if option_entity_id:
        option_channel = get_channels(option_entity_id)
    if product_entity_id:
        product_channel = get_channels(product_entity_id)
    channels = {const.PRODUCT_CHANNEL: product_channel, 
                const.ITEM_CHANNEL: item_channel, 
                const.OPTION_CHANNEL: option_channel}
    entity_ids = {"item_entity_id": item_entity_id, "option_entity_id":option_entity_id, "product_entity_id":product_entity_id}
    

    return product_enrichment, item_publish_code, entity_ids, item_active_web,channels, item_long_copy, item_ecom_status, item_enable_ecom, option_long_copy, product_details, item_image_resc_type, item_image_file_name

def load_pim_data():
    snowflake = snowflake_connection.Snowflake()
    articles = None
    try:
        articles = snowflake.get_data_from_db("""SELECT distinct ARTICLE_ID from RUSTA_CRAWLER.RUSTA_WEB_CRAWLER.ACTIVE_SCRAPE_RESULT
                                           where ARTICLE_FOUND = False and SCRAPE_DATE  =
     (SELECT MAX(SCRAPE_DATE) FROM RUSTA_CRAWLER.RUSTA_WEB_CRAWLER.ACTIVE_SCRAPE_RESULT)""", "RUSTA_CRAWLER_DWH")
    
    except snowflake_errors.DatabaseError as e:
        log.error(f"Error in getting articles from Snowflake: {e}")
        sys.exit(1)
    import time
    start = time.time()
    ready_pim = []
    total_articles = len(articles)
    log.info(f"Total articles to process: {total_articles}")
    for article in articles:
        data = get_pim_data(article)
        if data:
            
            product_enriched, item_publish_code, entity_ids, item_active_web, channels, item_long_copy, item_ecom_status, item_enable_ecom, option_long_copy, product_details, item_image_resc_type, item_image_file_name = data
            
            ready_pim.append({ 
                const.ARTICLE_ID: article,
                const.PUBLICATION_CODE: item_publish_code,
                const.ITEM_ENTITY_ID: entity_ids.get("item_entity_id", ""),
                const.OPTION_ENTITY_ID: entity_ids.get("option_entity_id", ""),
                const.PRODUCT_ENTITY_ID: entity_ids.get("product_entity_id", ""),
                const.ITEM_LONG_COPY_SE: item_long_copy.get("sv-SE", ""),
                const.ITEM_ACTIVE_WEB_SE: item_active_web.get("SE", ""),
                const.ITEM_ECOM_STATUS_SE: item_ecom_status.get("SE", ""),
                const.ITEM_ENABLE_ECOM_SE: item_enable_ecom.get("SE", ""),
                const.OPTION_LONG_COPY_SE: option_long_copy.get("sv-SE", ""),

                const.ITEM_LONG_COPY_NO: item_long_copy.get("nb-NO", ""),
                const.ITEM_ACTIVE_WEB_NO: item_active_web.get("NO", ""),
                const.ITEM_ECOM_STATUS_NO: item_ecom_status.get("NO", ""),
                const.ITEM_ENABLE_ECOM_NO: item_enable_ecom.get("NO", ""),
                const.OPTION_LONG_COPY_NO: option_long_copy.get("nb-NO", ""),

                const.ITEM_LONG_COPY_DE: item_long_copy.get("de-DE", ""),
                const.ITEM_ACTIVE_WEB_DE: item_active_web.get("DE", ""),
                const.ITEM_ECOM_STATUS_DE: item_ecom_status.get("DE", ""),
                const.ITEM_ENABLE_ECOM_DE: item_enable_ecom.get("DE", ""),
                const.OPTION_LONG_COPY_DE: option_long_copy.get("de-DE", ""),
                
                const.ITEM_LONG_COPY_FI: item_long_copy.get("fi-FI", ""),
                const.ITEM_ACTIVE_WEB_FI: item_active_web.get("FI", ""),
                const.ITEM_ECOM_STATUS_FI: item_ecom_status.get("FI", ""),
                const.ITEM_ENABLE_ECOM_FI: item_enable_ecom.get("FI", ""),
                const.OPTION_LONG_COPY_FI: option_long_copy.get("fi-FI", ""),

                const.ITEM_IMAGE_RESC_TYPE: item_image_resc_type,
                const.ITEM_IMAGE_FILE_NAME: item_image_file_name,
                const.PRODUCT_ENRICHMENT: product_details.get("ProductEnrichment", ""),
                const.PRODUCT_TYPE: product_details.get("ProductType", ""),
                const.PRODUCT_CATEGORY: product_details.get("ProductCategory", ""),
                
                const.ITEM_CHANNEL: channels.get(const.ITEM_CHANNEL, ""),
                const.OPTION_CHANNEL: channels.get(const.OPTION_CHANNEL, ""),
                const.PRODUCT_CHANNEL: channels.get(const.PRODUCT_CHANNEL, ""),
                const.INSERT_DATE: time.strftime("%Y-%m-%d", time.localtime())

            } ) # Add item_image_file_name to the result
        else:
            log.warning(f"Data not found for article: {article}")
            
    try:
        snowflake.execute_query("DELETE FROM RUSTA_CRAWLER.RUSTA_WEB_CRAWLER.PIM_DATA", "RUSTA_CRAWLER_DWH")
        snowflake.save_data_to_db(ready_pim, "PIM_DATA")
    except snowflake_errors.DatabaseError as e:
        log.error(f"Error in saving data to Snowflake: {e}")

    endtime = time.time() - start
    print(f"Time taken: {endtime:.2f} seconds")

if __name__ == "__main__":
    load_pim_data()