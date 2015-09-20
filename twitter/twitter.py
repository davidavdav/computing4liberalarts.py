#!/usr/bin/env python

import urllib
import base64
import httplib
import os, sys
import json

from . import secret

def get_bearer():
    ck_encoded = urllib.quote(secret.consumer_key)
    cs_encoded = urllib.quote(secret.consumer_secret)

    auth_encoded = urllib.base64.b64encode(ck_encoded + ":" + cs_encoded)

    host = "api.twitter.com"
    url = "/oauth2/token"
    params = urllib.urlencode({"grant_type" : "client_credentials"})

    req = httplib.HTTPSConnection(host)
    req.putrequest("POST", url)
    req.putheader("Host", host)
    req.putheader("Authorization", "Basic %s" % auth_encoded)
    req.putheader("Content-Type" ,"application/x-www-form-urlencoded;charset=UTF-8")
    req.putheader("Content-Length", str(len(params)))
    req.putheader("Accept-Encoding", "utf-8")
    req.endheaders()

    req.send(params)
    resp = req.getresponse()

    if resp.status != 200:
        raise Exception("Not OK, ", resp.reason)
    return resp.read()

def get_access_token():
    bearer_file = "bearer.json"
    access_token = ""
    if not os.path.exists(bearer_file):
        bearer_json = get_bearer()
        with open(bearer_file, "w") as fd:
            print >>fd, bearer_json
        access_token = json.loads(bearer_json)["access_token"]
    else:
        access_token = json.load(open(bearer_file))["access_token"]
    return access_token

access_token = get_access_token()

def search(query):
    host = "api.twitter.com"
    url = "/1.1/search/tweets.json"

    urlquery = url + "?" + urllib.urlencode({"q": query})

    req = httplib.HTTPSConnection(host)
    req.putrequest("GET", urlquery)
    req.putheader("Host", host)
    req.putheader("Authorization", "Bearer %s" % access_token)
    req.putheader("Accept-Encoding", "utf-8")
    req.endheaders()

    resp = req.getresponse()
    if resp.status != 200:
        raise Exception("Not OK, ", resp.reason)
    return json.loads(resp.read())

if __name__ == "__main__":
    print json.dumps(search("syria"), indent=4)

