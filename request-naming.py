import json
import requests

config_file = open('config.json', 'r')
config = json.load(config_file)

src_url = config['src_url']
dest_url = config['dest_url']

src_token = config['src_token']
dest_token = config['dest_token']

src_header = get_header(src_token)
dest_header = get_header(dest_token)

endpoint = '/api/config/v1/service/requestNaming'

def get_header(token):
    data = {
    "Authorization": "Api-token " + token,
    "Content-Type": "application/json"
    }
    return data

def get_req_list():
    url = src_url + endpoint
    res = requests.get(url, headers=src_header)
    if res.status_code != 200:
        print('could not fetch request names')
        print(res.text)
        exit()
    return json.loads(res.text)

def get_specific_req(id):
        url = src_url + endpoint + '/' + id
        res = requests.get(url, headers=src_header)
        if res.status_code != 200:
            print('could not fetch request name')
            print(res.text)
            exit()
        new_req = json.loads(res.text)
        # delete unwanted entries
        new_req.pop('metadata', None)
        new_req.pop('id', None)
        # to test on local env
        #new_req['name'] = new_req['name'] + '-new'
        #new_req['namingPattern'] = new_req['namingPattern'] + '-new'
        return json.dumps(new_req)

def post_req(req_list):
    url = dest_url + endpoint
    for v in req_list['values']:
        print(v)
        new_req = get_specific_req(v['id'])
        res = requests.post(url, data=new_req, headers=dest_header)
        if res.status_code != 201:
            print('could not create request name')
            print(res.text)
            print(new_req)
            exit()
        print('creating new request naming')

def main():
    req_list = get_req_list()
    print(req_list)
    post_req(req_list)
    print('Done')

if __name__ == "__main__":
    # execute only if run as a script
    main()