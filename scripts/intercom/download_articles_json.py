import requests
import json
import os

url = "https://api.intercom.io/articles"
headers = {
    'Intercom-Version': '2.9',
    'accept': 'application/json',
    'authorization': 'Bearer ' + os.environ.get('INTERCOM_API_KEY')
}

def get_data(url, headers):
    response = requests.get(url, headers=headers)
    return response.json()

def get_all_pages(url, headers):
    data_list = []
    while url:
        response = get_data(url, headers)
        data_list.extend(response['data'])
        url = response['pages'].get('next', None)
    return data_list

data = get_all_pages(url, headers)

with open('./docs/docs/intercom/articles.json', 'w') as f:
    json.dump(data, f, indent=4)
