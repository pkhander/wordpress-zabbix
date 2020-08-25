"""This modules helps with Wordpress API connection and adding the content to a page"""

import requests
from helper import load_config, config

load_config()
USERNAME = config['wordpress_api']['USERNAME']
PASSWORD = config['wordpress_api']['PASSWORD']
URL = config['wordpress_api']['URL']


def create_post(content):
    """ Adds body to our page"""

    post_data = {
        'title': 'API Post(TEST)',
        'content': content,
        'status': 'publish',
    }
    return post_data


def get_token():
    """ Gets jwt(oken) using wordpress credentials"""

    auth_data = {"username": USERNAME,
                 "password": PASSWORD}
    response = requests.post(URL + '/jwt-auth/v1/token',  data=auth_data)
    if response.status_code == 200 and 'token' in response.json():
        token = response.json()["token"]
        return token
    else:
        print("Invalid response")
        return None


def post_to_website(token, post_data):
    """ Posts the data on website using the content"""

    header = {'Authorization': 'Bearer ' + token}
    resp = requests.post(URL + '/wp/v2/pages/4103',
                         headers=header, data=post_data)
    if resp.status_code == 201:
        return True
    else:
        # print(resp)
        return False


def notify(content):
    """ Takes content and a new post is created on the website"""

    token = get_token()
    if token is not None:
        post_data = create_post(content)
        return post_to_website(token, post_data)
    else:
        print("Invalid token!! Post will not happen")
        return False


def main():
    """Main Function"""
    print("I do nothing")


if __name__ == "__main__":
    main()
