from swiftclient import client
from ThuCloudDisk.settings import *
import os
import magic
class Swift:
    def __init__(self):
        self.host = SWIFT_HOST
        self.user_name = SWIFT_USER
        self.user_pass = SWIFT_SECRET
        self.authurl ='http://'+ self.host +'/v2.0'
        self.tenant = SWIFT_TENANT
    def connect(self):
        auth = client.get_auth(self.authurl,self.user_name,self.user_pass,tenant_name=self.tenant,auth_version='2',os_options=self.os_options)
        self.storage_url = auth[0]
        self.http_conn = client.http_connection(self.storage_url)
        self.token = auth[1]


    def list_container(self,container_name,prefix=None,delimiter=None):
        try:
            return client.get_container(self.storage_url,self.token,container_name,prefix=prefix,delimiter=delimiter,http_conn=self.http_conn)
        except:
            return None

    def put_container(self,container_name):
        if(self.list_container(container_name) == None):
            headers={"X-Container-Meta-Access-Control-Allow-Origin":"http://thucloud.com",
                     "Access-Control-Allow-Methods": "HEAD, GET, PUT, POST, COPY, OPTIONS, DELETE"}
            client.put_container(self.storage_url,self.token,container_name,http_conn=self.http_conn)
            return True
        return False

    def get_object(self,container,object):
        try:
            return client.get_object(self.storage_url,self.token,container,object,http_conn = self.http_conn)
        except:
            return None

    def get_object_to_file(self,container,userpath,filename):
        filepath = os.path.join(LOCAL_BUFFER_PATH,userpath)
        filepath = filepath + filename
        GetBufferSize = 1024*1024*10
        try:
            res = client.get_object(self.storage_url,self.token,container,filename)
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
 	
    def put_object_from_file(self,container,prefix,filepath):
        try:
            content_length = os.path.getsize(filepath);
            content_type = magic.from_file(filepath,mime=True);
            strlist = filepath.split('/')
            for value in strlist:
                object = value

            fp = open(filepath,'rb')
            client.put_object(self.storage_url,self.token,container,object,fp,content_length=content_length,content_type=content_type)
            return True
        except:
            return False
    
    def delete_object(self, container, name):
        try:
    	    print client.delete_object(self.storage_url, self.token, container, name)
	    return True
        except:
            return False 
if __name__ == '__main__':
    #def get_new_file_path(container,object):
    swift = Swift('10.0.0.120','demo','admin','secrete','5000',os_options={'endpoint_type':'internalURL'})
    swift.connect();
    #print swift.list_container('xiaohe-container');
    #print swift.put_container('ThuCloudDisk-container');
    #swift.put_object_from_file('ThuCloudDisk-container',prefix='',filepath='/home/chengls10/Desktop/2')
    #print swift.get_object_to_file('ThuCloudDisk-container','1.py')
    #print swift.delete_object('ThuCloudDisk-container','1.py')
