from swiftclient import client
from ThuCloudDisk.settings import *
import os
import requests
import magic
import json

SH2_API_ADDR=u"controller:9144"
def read_in_chunks(file_object, chunk_size=1024):
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k."""
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data
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
                    # Ignore files that starts with a dot
                    tp=obj["Key"]
                    if (tp.startswith(".") and tp!="." and tp!=".."):
                        continue
                    if (objVal["type"]=="dir"):
                        forRet.append({"subdir": prefix+obj["Key"]+u"/"})
                    else:
                        i4Maniputate={}
                        for k in objVal:
                            if (k.startswith(PREFIX)):
                                i4Maniputate[(k[len(PREFIX):]).replace(u"-", u"_")]=objVal[k]
                        i4Maniputate["bytes"]=int(i4Maniputate["content_length"])
                        i4Maniputate["name"]=prefix+obj["Key"]
                        forRet.append(i4Maniputate)
                forRet.append({"name":prefix, "bytes": 0})
                return (r.headers, forRet)
            except Exception as e:
                print forRet, e
                return (r.headers, [])
        except:
            return None

    def put_container(self,container_name):
        r=requests.post(u"http://"+SH2_API_ADDR+u"/cn/"+container_name)
        if (r.status_code==201):
            return True
        return False

    # [l TODO] Implement it.
    def get_object(self,container,object):
        raise Exception("NOT IMPLEMENTED")

    def delete_folder(self,container,prefix):
        print "a trial to delete folder"
        r=requests.delete(u"http://"+SH2_API_ADDR+u"/fs/"+container+u"/"+prefix)
        return False

    def get_object_to_file(self,container,userpath,filename):
        filepath = os.path.join(LOCAL_BUFFER_PATH,userpath)
        filepath = os.path.join(filepath, container)
        filepath = os.path.join(filepath, filename)
        prefix = userpath
        objectName = prefix + filename
        try:
            r=requests.get(u"http://"+SH2_API_ADDR+u"/io/"+container+u"/"+objectName, stream=True)
            if (r.status_code!=200):
                return False
            header=r.headers
            fileSize = header['ori-content-length']
            fileDate = header['ori-last-modified']
            chunk_size=1*1024*1024  # 1MB
            with open(filepath, 'wb') as fd:
                for chunk in r.iter_content(chunk_size):
                    fd.write(chunk)
                fd.close()

            return fileSize, fileDate, filepath, filename
        except:
            return False

    def put_object_of_foler(self,container,prefix,folder):
        r=requests.post(u"http://"+SH2_API_ADDR+u"/fs/"+container+u"/"+prefix+folder)
        if (r.status_code==201 or r.status_code==202):
            return True
        return False

    def put_object_from_file(self,container,prefix,filepath):
        try:
            content_type = magic.from_file(filepath,mime=True);
            fp = open(filepath,'rb')
            filename=prefix+(filepath.split("/"))[-1]
            r=requests.put(u"http://"+SH2_API_ADDR+u"/io/"+container+u"/"+filename, data=read_in_chunks(fp), headers={"content-type": content_type})
            return True
            fp.close()
        except Exception as e:
            print "Exception @ put_object_from_file:", e
            return False

    def delete_object(self, container, prefix, name):
        print "a trial to delete object"
        try:
            r=requests.delete(u"http://"+SH2_API_ADDR+u"/fs/"+container_name+u"/"+prefix+name)
            return True
        except:
            return False

if __name__ == '__main__':
    pass
