#! /usr/bin/python

import requests
import json

def get_url(url):
    r = requests.get(url)
    if r.status_code == 200:
        return json.loads(r.content)
    else:
        return {}

def get_profile(user_id):
    return get_url('https://resources.meerkatapp.co/users/{0}/profile?v=2'.format(user_id))

if __name__ == '__main__':
    p = get_profile('550099452400006f00a5277f')
    print json.dumps(p, indent=2)

    followers = get_url(p['followupActions']['followers'])
    following = get_url(p['followupActions']['following'])

    print json.dumps(followers, indent=2)
    print json.dumps(following, indent=2)


