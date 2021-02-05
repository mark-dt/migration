import json

def get_config_template():
    temp = {
    'src_url' : '',
    'dest_url' : '',
    'src_token' : '',
    'dest_token' : ''
    }
    return temp

def create_config_json():
    src_url = input("Please enter a the source URL of your tenant:\n")
    dest_url = input("Please enter a the destination URL of your tenant:\n")
    src_token = input("Please enter a the source token of your tenant:\n")
    dest_token = input("Please enter a the destination token of your tenant:\n")
    template = get_config_template()
    template['src_url'] = src_url
    template['dest_url'] = dest_url 
    template['src_token'] = src_token
    template['dest_token'] = dest_token
    with open('config.json', 'w') as config_file:
        json.dump(template, config_file)

def main():
    create_config_json()
    print('Done, please open config.json and verify the content.')

if __name__ == "__main__":
    main()