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

endpoint = '/api/config/v1/conditionalNaming/service'

def get_header(token):
    data = {
    "Authorization": "Api-token " + token,
    "Content-Type": "application/json"
    }
    return data


def get_svcs_list():
    url = src_url + endpoint
    res = requests.get(url, headers=src_header)
    if res.status_code != 200:
        print('could not fetch services')
        print(res.text)
        exit()
    return json.loads(res.text)

def get_specific_svc(id):
        url = src_url + endpoint + '/' + id
        res = requests.get(url, headers=src_header)
        if res.status_code != 200:
            print('could not fetch specific service')
            print(res.text)
            exit()
        new_svcs = json.loads(res.text)
        print(new_svcs)
        exit()
        # delete unwanted entries
        new_svcs.pop('metadata', None)
        new_svcs.pop('id', None)
        for r in new_svcs['rules']:
            r.pop('id', None)
            for m in r['methodRules']:
                m.pop('id', None)
        # DELETE THIS
        new_svcs['name'] = new_svcs['name'] + '-new'
        return json.dumps(new_svcs)

def post_svcs(svcs_list):
    url = dest_url + endpoint
    for v in svcs_list['values']:
        new_svcs = get_specific_svc(v['id'])
        res = requests.post(url, data=new_svcs, headers=dest_header)
        if res.status_code != 201:
            print('could not create custom service')
            print(res.text)
            print(new_svcs)
            exit()
        print('creating custom service')

def main():
    svcs_list = get_svcs_list()
    print (svcs_list)
    post_svcs(svcs_list)
    print('Done')

if __name__ == "__main__":
    main()