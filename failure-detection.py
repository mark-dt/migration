import json
import requests


config_file = open('config.json', 'r')
config = json.load(config_file)
src_url = config['src_url']
#endpoint = config['tag_endpoint']
src_token = config['src_token']

endpoint = '/service/failureDetection/parameterSelection/parameterSets'
endpoint = '/service/failureDetection/parameterSelection/rules'

src_header = {
    "Authorization": "Api-token " + src_token,
    "Content-Type": "application/json"
}

def get_tag_list():
    url = src_url + endpoint
    res = requests.get(url, headers=src_header)
    if res.status_code != 200:
        print('could not tagging rules')
        print(res.text)
        exit()
    print(res.status_code)
    #print(res.text)
    return res.text
    #return json.loads(res.text)

def get_specific_tag(id):
        url = src_url + endpoint + '/' + id
        res = requests.get(url, headers=src_header)
        if res.status_code != 200:
            print('could not tag details')
            print(res.text)
            exit()
        tag = json.loads(res.text)
        return tag

def update_tag(tag):
    url = dest_url + endpoint + '/' + tag['id']
    payload = json.dumps(tag)
    res = requests.put(url, data=payload, headers=dest_header)
    if res.status_code >= 400:
        print('could not update tagging rule')
        print(res.text)
        print(payload)
        exit()
    print(res.text)
    print('Succesfully updated Tag')

def main():
    tag_list = get_tag_list()
    print('Done')

if __name__ == "__main__":
    main()