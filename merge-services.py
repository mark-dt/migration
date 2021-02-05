import requests
import json

config_file = open('config.json', 'r')
config = json.load(config_file)

src_url = config['src_url']

src_token = config['src_token']

endpoint = '/api/config/v1/service/detectionRules/FULL_WEB_REQUEST'

header = {
    "Authorization": "Api-token " + src_token,
    "Content-Type": "application/json"
}


def merge_services():
    url = src_url + endpoint 
    data = {
	    "type": "FULL_WEB_REQUEST",
	    "name": "<service-name-to-merge>",
	    "description": "Merging services",
	    "enabled": True,
	    "detectAsWebRequestService": False,
	    "conditions": [
	        {
	            "attributeType": "SERVER_NAME",
	            "compareOperations": [
	                {
	                    "type": "STARTS_WITH",
	                    "invert": "false",
	                    "ignoreCase": "true",
	                    "values": [
                            "abc",
	                    ]
	                }
	            ]
	        }
	    ]
	}
    payload = json.dumps(data)

    res = requests.post(url, data=payload, headers=header)
    print(res.request.body)
    print(res.request.headers)
    print(res.text)

def get_all_detection_rules():
    url = src_url + endpoint 
    r = requests.get(url, headers=header)
    print(r.text)


def delete_rule(id):
    url = src_url + endpoint + '/' + id
    res = requests.delete(url, headers=header)
    if res.status_code != 204:
        print('could not delete rule')
        print(res.text)
        exit()
    print('rule')

import time
def main():
    merge_services()
    time.sleep(2)
    get_all_detection_rules()
    print('Done')

if __name__ == "__main__":
    main()