#! /usr/bin/python

import os
import sys
import requests
import json
from collections import deque

DATA_DIR = 'data'

profiles_to_parse = deque()
profiles_done = set()

def put(url, data):
    r = requests.put(url, data=json.dumps(data), headers={'Content-Type': 'application/json'}, verify=False)
    if r.status_code == 200:
        return json.loads(r.content)
    else:
        return {}

def get(url):
    r = requests.get(url, verify=False)
    if r.status_code == 200:
        return json.loads(r.content)
    else:
        return {}

def get_profile(user_id):
    return get('https://resources.meerkatapp.co/users/{0}/profile?v=2'.format(user_id))

def get_complete_info(user_id):
    print 'Getting data for', user_id
    profile_path = os.path.join(DATA_DIR, user_id + '_profile')

    if not os.path.exists(profile_path):
        p = get_profile(user_id)
        with open(profile_path, 'w') as f:
            f.write(json.dumps(p, indent=2))
    else:
        with open(profile_path, 'r') as f:
            p = json.loads(f.read())

    if not os.path.exists(profile_path.replace('_profile', '_followers')):
        followers = get(p['followupActions']['followers'])
        with open(profile_path.replace('_profile', '_followers'), 'w') as f:
            f.write(json.dumps(followers, indent=2))
    else:
        with open(profile_path.replace('_profile', '_followers'), 'r') as f:
            followers = json.loads(f.read())

    if not os.path.exists(profile_path.replace('_profile', '_following')):
        following = get(p['followupActions']['following'])
        with open(profile_path.replace('_profile', '_following'), 'w') as f:
            f.write(json.dumps(following, indent=2))
    else:
        with open(profile_path.replace('_profile', '_following'), 'r') as f:
            following = json.loads(f.read())

    profiles_done.add(user_id)

    new_users = []
    for f in followers['result']:
        if f['id'] not in profiles_done:
            new_users.append(f['id'])
    for f in following['result']:
        if f['id'] not in profiles_done:
            new_users.append(f['id'])
    return new_users

def search(username):
    return put('https://social.meerkatapp.co/users/search?v=2', {'username' : username})

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print 'Pass in a username to start crawling'
        exit()

    username = sys.argv[1]

    print 'Searching for', username
    u = search(username)
    if u:
        user_id = u['result'][0] # Just pick the first one
        print 'Found user_id', user_id
    else:
        print 'Could not find user_id', r.content
        exit()

    profiles_to_parse.append(user_id)

    while len(profiles_to_parse):
        user_id = profiles_to_parse.popleft()
        try:
            new_user_ids = get_complete_info(user_id)
            print 'Found {0} new user ids'.format(len(new_user_ids))
            profiles_to_parse.extend(new_user_ids)
        except Exception as e:
            print 'Failed to get data for user_id {0}: {1}'.format(user_id, e)

