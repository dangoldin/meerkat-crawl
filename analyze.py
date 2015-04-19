#! /usr/bin/python

import sys
import os
import json
from collections import deque

DATA_DIR = '/Users/danielgoldin/data/meerkat'

OUT_DIR = '/Users/danielgoldin/data/meerkat-out'

profiles_to_analyze = deque()
profiles_done = set()

DEBUG = False

def read_and_parse(fp):
    try:
        with open(fp, 'r') as f:
            return json.loads(f.read())
    except Exception as e:
        print 'Failed to read', fp, e
        return {}

def analyze_user(user_id):
    if user_id not in profiles_done:
        fp = os.path.join(DATA_DIR, user_id + '_profile')
        u = read_and_parse(fp)
        if DEBUG:
            print json.dumps(u, indent=2)

        # Can skip the followers for now and just iterate through the followers
        following = read_and_parse(fp.replace('_profile', '_following'))
        if DEBUG:
            print json.dumps(following, indent=2)

        profiles_done.add(user_id)

        following = [f['id'] for f in following['result'] if f['id'] not in profiles_done]
        return following
    return []

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print 'Pass in a user id to start analyzing'
        exit()

    user_id = sys.argv[1]

    print 'Starting with', user_id

    profiles_to_analyze.append(user_id)

    with open(os.path.join(OUT_DIR, 'network'), 'w') as f:
        while len(profiles_to_analyze):
            user_id = profiles_to_analyze.popleft()
            try:
                following = analyze_user(user_id)
                profiles_to_analyze.extend(following)

                for fr in following:
                    f.write("{0},{1}\n".format(user_id, fr))

                print 'Finished for user id', user_id
            except Exception as e:
                print 'Failed to analyze',user_id,e
