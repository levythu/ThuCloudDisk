from swiftclient import client
from ThuCloudDisk.settings import *
import os
import requests
import magic
import json

SH2_API_ADDR=u"59.66.137.32:9144"
class Swift:
    def __init__(self):
        self.host = SWIFT_HOST
        self.user_name = SWIFT_USER
        self.user_pass = SWIFT_SECRET
        self.authurl ='http://'+ self.host +'/v2.0'
        self.tenant = SWIFT_TENANT

    def connect(self):
        auth = client.get_auth(self.authurl,self.user_name,self.user_pass,tenant_name=self.tenant,auth_version='2')
        self.storage_url = auth[0]
        self.http_conn = client.http_connection(self.storage_url)
        self.token = auth[1]

    # If the container does not exist, return None: however, the function will almost never returns None [l TODO]
    # otherwise, return Tuple: (httpHeader, [object List]); and the header is currently nothing
        # the returned obj list will have the folder itself in it.
        # all the file names are their full path
    # if the path (not the container) does not exist, returns an empty list

    def list_container(self,container_name,prefix=None,delimiter=None):
        PREFIX=u"fmap-file-"
        try:
            if (prefix==None):
                prefix=u""
            r=requests.get(u"http://"+SH2_API_ADDR+u"/fs/"+container_name+u"/"+prefix)
            forRet=[]
            if (r.status_code!=200):
                return (r.headers, forRet)
            result=r.json()
            try:
                for obj in result:
                    objVal=json.loads(obj["Val"])
                    if (objVal["type"]=="dir"):
                        forRet.append({"subdir": prefix+obj["Key"]+u"/"})
                    else:
                        i4Maniputate={}
                        for k in objVal:
                            if (k.startswith(PREFIX)):
                                i4Maniputate[k[len(PREFIX):]]=objVal[v]
                        i4Maniputate["bytes"]=int(i4Maniputate["content-length"])
                        i4Maniputate["name"]=prefix+obj["Key"]
                        forRet.append(i4Maniputate)
                forRet.append({"name":prefix, "bytes": 0})
                print forRet
                return (r.headers, forRet)
            except:
                print forRet
                return (r.headers, [])
        except:
            return None

    def put_container(self,container_name):
        if(self.list_container(container_name) == None):
            #headers={"X-Container-Meta-Access-Control-Allow-Origin":"http://thucloud.com",
                     #"Access-Control-Allow-Methods": "HEAD, GET, PUT, POST, COPY, OPTIONS, DELETE"}
            client.put_container(self.storage_url,self.token,container_name,http_conn=self.http_conn)
            return True
        return False

    def get_object(self,container,object):
        try:
            return client.get_object(self.storage_url,self.token,container,object,http_conn = self.http_conn)
        except:
            return None
    def delete_folder(self,container,prefix):
        print 'prefix',prefix
        all_related_objects = client.get_container(self.storage_url,self.token,container,prefix=prefix,http_conn=self.http_conn)
        for o in all_related_objects[1]:
            self.delete_object(container,prefix='',name=o['name'])
        return False
    def get_object_to_file(self,container,userpath,filename):
        filepath = os.path.join(LOCAL_BUFFER_PATH,userpath)
        filepath = filepath + filename
        GetBufferSize = 1024*1024*10
        prefix = userpath.replace('./','')
        objectName = prefix + filename
        try:
            res = client.get_object(self.storage_url,self.token,container,objectName)
            fileSize = res[0]['content-length']
            fileDate = res[0]['last-modified']
            filename = filename
            data = res[1]
            f = file(filepath, 'wb')
            f.write(data)
            f.close()
            return fileSize, fileDate, filepath, filename
        except:
            return False

    def put_object_of_foler(self,container,prefix,folder):
        folder = prefix + folder
        client.put_object(self.storage_url,self.token,container,folder+'/')
        return True
    def put_object_from_file(self,container,prefix,filepath):
        if True:
            content_length = os.path.getsize(filepath);

            content_type = magic.from_file(filepath,mime=True);
            strlist = filepath.split('/')
            for value in strlist:
                object = value
            object = prefix+object
            fp = open(filepath,'rb')
            client.put_object(self.storage_url,self.token,container,object,fp,content_length=content_length,content_type=content_type)
            return True
        #except:
        #    return False

    def delete_object(self, container, prefix, name):
        try:
            object_name = prefix + name
    	    client.delete_object(self.storage_url, self.token, container, object_name)
	    return True
        except:
            return False

if __name__ == '__main__':
    #def get_new_file_path(container,object):
    swift = Swift();
    swift.connect();
    print swift.list_container('test@thucloud.com');
    #swift.put_container('demo-container1');
    # print swift.list_container('xiaoh16@gmail.com');
    #print swift.put_container('ThuCloudDisk-container');
    #swift.put_object_from_file('ThuCloudDisk-container',prefix='',filepath='/home/chengls10/Desktop/2')
    #print swift.get_object_to_file('ThuCloudDisk-container','1.py')
    #print swift.delete_object('ThuCloudDisk-container','1.py')
