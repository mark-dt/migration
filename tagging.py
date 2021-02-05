import json
import requests

config_file = open('config.json', 'r')
config = json.load(config_file)
src_url = config['src_url']
endpoint = config['tag_endpoint']
src_token = config['src_token']

src_header = {
    "Authorization": "Api-token " + src_token,
    "Content-Type": "application/json"
}

app_list_file_name = 'app-list-short.json'

def get_rule_template():
    data = {
            'type': 'SERVICE',
            'enabled': True,
            #'valueFormat': '<placeholder>',
            'propagationTypes': [],
            'conditions': [
                {
                    'key': {
                        'attribute': 'SERVICE_NAME'
                    },
                    'comparisonInfo': {
                        'type': 'STRING',
                        'operator': 'CONTAINS',
                        'value': '<placeholder>',
                        'negate': False,
                        'caseSensitive': True
                    }
                }
            ]
        }
    return data

def get_tag_template(app_name):
    data = {
    'name': app_name,
    'rules': [
        {
        'type': 'SERVICE',
        'enabled': True,
        'valueFormat': '{Service:DetectedName}',
        'propagationTypes': [],
        'conditions': [
            {
            'key': {
                'attribute': 'SERVICE_TYPE'
            },
            'comparisonInfo': {
                'type': 'SERVICE_TYPE',
                'operator': 'EQUALS',
                'value': 'CUSTOM_SERVICE',
                'negate': False
            }
            },
            {
            'key': {
                'attribute': 'SERVICE_DETECTED_NAME'
            },
            'comparisonInfo': {
                'type': 'STRING',
                'operator': 'BEGINS_WITH',
                'value': app_name,
                'negate': False,
                'caseSensitive': True
            }
            }
        ]
        }
    ]
    }
    return data

def get_tag_list():
    # get a list of all the tags in an environmet
    url = src_url + endpoint
    res = requests.get(url, headers=src_header)
    if res.status_code != 200:
        print('could not tagging rules')
        print(res.text)
        exit()
    return json.loads(res.text)

def get_specific_tag(id):
    # based on the id tries to return the tag details
    url = src_url + endpoint + '/' + id
    res = requests.get(url, headers=src_header)
    if res.status_code != 200:
        print('could not tag details')
        print(res.text)
        exit()
    tag = json.loads(res.text)
    return tag

def update_tag(tag):
    # pushes an update to a specified tag
    url = src_url + endpoint + '/' + tag['id']
    payload = json.dumps(tag)
    res = requests.put(url, data=payload, headers=src_header)
    if res.status_code >= 400:
        print('could not update tagging rule')
        print(res.text)
        print(payload)
        exit()
    print(res.text)
    print('Succesfully updated Tag: ' + tag['id'])


def push_new_tag(tag):
    # generates new tagging rule
    url = src_url + endpoint 
    payload = json.dumps(tag)
    res = requests.post(url, data=payload, headers=src_header)
    if res.status_code >= 400:
        print('could not create tagging rule')
        print(res.text)
        print(payload)
        exit()
    print(res.text)
    print('Succesfully pushed new Tag')

'''
def insert_new_rule(tag, app_name, condition_value):
    # given a tag 
    for r in tag['rules']:
        if r['valueFormat'] == app_name:
            for c in r['conditions']:
                if c['comparisonInfo']['value'] == condition_value:
                    # if app_name and same condition are already present in the rule just return tag
                    return tag

    # otherwise update rules with new data
    template = get_rule_template()
    template['valueFormat'] = app_name
    template['conditions'][0]['comparisonInfo']['value'] = condition_value
    tag['rules'].append(template)
    return tag
'''

def get_update_template(app_name):
    data = {
        'type': 'SERVICE',
        'enabled': True,
        'valueFormat': '{Service:DetectedName}',
        'propagationTypes': [],
        'conditions': [
            {
            'key': {
                'attribute': 'SERVICE_TYPE'
            },
            'comparisonInfo': {
                'type': 'SERVICE_TYPE',
                'operator': 'EQUALS',
                'value': 'CUSTOM_SERVICE',
                'negate': False
            }
            },
            {
            'key': {
                'attribute': 'SERVICE_DETECTED_NAME'
            },
            'comparisonInfo': {
                'type': 'STRING',
                'operator': 'BEGINS_WITH',
                'value': app_name,
                'negate': False,
                'caseSensitive': True
            }
            }
        ]
        }

    return data

def refactor_tags():
    app_list = open(app_list_file_name, 'r')
    app_list = json.load(app_list)
    tags_to_update = []
    for t in tag_list['values']:
        if t['name'] in app_list:
            tags_to_update.append(t['id'])
    
    for tag_id in tags_to_update:
        tag = get_specific_tag(tag_id)
        template = get_update_template(tag['name'])
        skip = False
        for r in tag['rules']:
            for c in r['conditions']:
                if c['comparisonInfo']['value'] == tag['name']:
                    # skip if custom service rule already present
                    skip = True
        #template['valueFormat'] = app_name
        #template['conditions'][0]['comparisonInfo']['value'] = condition_value
        if not skip:
            tag['rules'].append(template)
            update_tag(tag)



def insert_new_rule(tag, condition_value):
    # given a tag and the condition, create a new rule and add that to the other tag rules
    for r in tag['rules']:
        for c in r['conditions']:
            if c['comparisonInfo']['value'] == condition_value:
                # if app_name and same condition are already present in the rule just return tag
                return tag

    # otherwise update rules with new data
    template = get_rule_template()
    #template['valueFormat'] = app_name
    template['conditions'][0]['comparisonInfo']['value'] = condition_value
    tag['rules'].append(template)
    return tag

def app_exists(app_name):
    # helper function checks if an automatic tag with the given app_name already exists
    # if so returns the id of the autmatic tag rule
    for t in tag_list['values']:
        if t['name'] == app_name:
            return True, t['id']
    return False, -1

def delete_tags():
    print('EXECUTION IS DANGEROUS')
    # do not execute this accidentally
    #exit()

    # will delete all apps defined in the list
    app_list = open(app_list_file_name, 'r')
    app_list = json.load(app_list)
    tags_to_delete = []
    for t in tag_list['values']:
        if t['name'] in app_list:
            tags_to_delete.append(t['id'])

    for tag_id in tags_to_delete:
        url = src_url + endpoint + '/' + tag_id
        res = requests.delete(url, headers=src_header)
        if res.status_code >= 400:
            print('could not delet tagging rule')
            print(res.text)
            print(payload)
            exit()
        print(res.text)
        print('Succesfully deleted Tag: ' + t['id'])


def create_tags():
    # based on the app_list it will get the actual tagging rules in the environment and try either
    # to create new rules or update if already present
    app_list = open(app_list_file_name, 'r')
    app_list = json.load(app_list)
    for k in app_list.keys():
        ret, tag_id = app_exists(k)
        # if app exists, we need to update rules
        if ret:
            tag = get_specific_tag(tag_id)
            for r in app_list[k]:
                tag = insert_new_rule(tag, r)
            update_tag(tag)
        else:
            tag = get_tag_template(k)
            for r in app_list[k]:
                tag = insert_new_rule(tag, r)
            push_new_tag(tag)


tag_list = get_tag_list()

def main():
    '''
    for t in tag_list['values']:
        if t['name'] == 'Anwendung':
            tag = get_specific_tag(t['id'])
            # hier kann man ein for-loop anlegen der durch die liste mit den neuen Anwendungen durchgeht
            # und an die funktioin insert_new_rule weitergibt
            tag = insert_new_rule(tag, 'test2', 'test2')
            tag = insert_new_rule(tag, 'test', 'test2')
            tag = insert_new_rule(tag, 'test3', 'test3')
            tag = insert_new_rule(tag, 'test', 'test3')
            tag = insert_new_rule(tag, 'test3', 'test')
            tag = insert_new_rule(tag, 'test3', 'test3')
            update_tag(tag)
    '''
    #create_tags()
    delete_tags()
    #refactor_tags()
    print('Done')



if __name__ == "__main__":
    # execute only if run as a script
    main()