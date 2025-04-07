import json
import os
import requests
from requests.structures import CaseInsensitiveDict
from osrs_net.item import Item
from osrs_net.util.file_io import read, get_base_dir


class GrandExchange:
    base_url = "https://prices.runescape.wiki/api/v1/osrs/latest"
    base_dir = get_base_dir()
    item_file_path = os.path.join(base_dir, 'resources', 'items.json')
    headers = {
        'User-Agent': 'osrs-net API Wrapper'
    }

    @classmethod
    def latest_price_by_id(cls, item_id):
        url = f"{cls.base_url}?id={item_id}"
        data = requests.get(url, headers=cls.headers).json()
        try:
            return data['data'][str(item_id)]
        except KeyError:
            return None
    
    @classmethod
    def latest_price_by_name(cls, item_name):
        item_id = cls.item_id_from_name(item_name)
        return cls.latest_price_by_id(item_id)
    
    @classmethod
    def item_name_from_id(cls, item_id):
        item_ids = json.loads(read(cls.item_file_path))
        try:
            return list(item_ids.keys())[list(item_ids.values()).index(item_id)]
        except NameError:
            return None

    @classmethod
    def item_id_from_name(cls, item_name):
        item_ids = CaseInsensitiveDict(json.loads(read(cls.item_file_path)))
        try:
            return item_ids[item_name]
        except KeyError:
            return None
