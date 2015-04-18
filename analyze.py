#! /usr/bin/python

import sys
import os
import json

DATA_DIR = 'data'

def load_user_data(user_id):
  fp = os.path.join(DATA_DIR, user_id + '_profile')
  with open(fp, 'r') as f:
    u = json.loads(f.read())
    print json.dumps(u, indent=2)

  with open(fp.replace('_profile', '_followers'), 'r') as f:
    followers = json.loads(f.read())
    print json.dumps(followers, indent=2)

  with open(fp.replace('_profile', '_following'), 'r') as f:
    following = json.loads(f.read())
    print json.dumps(following, indent=2)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print 'Pass in a user id to start analyzing'
        exit()

    user_id = sys.argv[1]

    print 'Starting with', user_id

    load_user_data(user_id)