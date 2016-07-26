import json, requests
import hashlib
import ConfigParser
import codecs

config = ConfigParser.ConfigParser()
config.readfp(open('updater.settings'))
repoName = config.get("Section1", "repo")
whitelist = config.getboolean("Section1", "whitelist")
BoWList = config.get("Section1", "list").split("\n")


def goThroughFiles(data):
    for content in data:
        print content["name"]
        if (content["name"] in BoWList)!=whitelist:
            continue

        if(content["type"]=="dir"):
            resp = requests.get(url="https://api.github.com/repos/"+ repoName +"/contents/"+content["name"])
            goThroughFiles(json.loads(resp.text))
        try:
            f=codecs.open(content["name"], "rb+", "utf-8")
            sha1 = hashlib.sha1()
            sha1.update(f.read().encode('utf-8'))
            hashoff=format(sha1.hexdigest())
        except IOError:
            f=codecs.open(content["name"], "w", "utf-8")
            hashoff="null"


        resp=requests.get(url=content["download_url"])
        sha1 = hashlib.sha1()
        sha1.update(resp.text.encode('utf-8'))
        hashon=format(sha1.hexdigest())
        print("SHA1: "+hashon)
        print("SHA1: "+hashoff)

        if hashon!=hashoff:
            f.write(resp.text.encode('utf-8'))
            print("writing")


resp = requests.get(url="https://api.github.com/repos/"+ repoName +"/contents")
data = json.loads(resp.text)

goThroughFiles(data)
