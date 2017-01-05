from pymongo import MongoClient
from xpinyin import Pinyin
from mu_sanic import config
import urllib.request
import  datetime
client = MongoClient(config.mongohost)
db = client['Hakurei-Site']
pin = Pinyin()
class BlogInfo:
    def __init__(self):
        self.blog = db['BlogInfo']

    def init(self,title,markdown):
        self.blog.create_index("url", unique=True)
        url = pin.get_pinyin(str(title).replace('-','').replace(' ',''))
        raw = {
                "url":url,
                "title":title,
                "markdown":markdown
                }
        self.blog.update_one({"url":url},{"$set":raw},upsert=True)
        return True

    def new8th(self):
        return self.blog.find().sort('$natural',-1).limit(7)
    
    def all(self):
        return self.blog.find()
    
    def find(self,url):
        return self.blog.find_one({'url':urllib.request.unquote(url)})


class AuthInfo:
    def __init__(self):
        self.authi = db['authInfo']
        
    def init(self,user,github):
        raw = {
                "user":user,
                "github":github,
                "user_auth":'True'
                }
        self.authi.insert_one(raw)
        return True
    
    def find_user(self,user):
        return self.authi.find_one({'github':user})


class ActiInfo:
    def __init__(self):
        self.acti = db['ActiInfo']
    
    def init(self,name,time,place):
        time = datetime.datetime.strptime(time,"%Y.%m.%d")
        expiretime = time + datetime.timedelta(days=1)
        self.acti.create_index('expiretime',expireAfterSeconds=0)
        raw = {
                "expiretime":expiretime,
                "name":name,
                "time":time,
                "place":place
                }
        self.acti.insert_one(raw)
        return True

    def remove(self,name):
        self.acti.remove({'name':urllib.request.unquote(name)})
        return True
    
    def all(self):
        return self.acti.find()

    def newest(self):
        return self.acti.find().sort('time',1).limit(1)
