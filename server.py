import firebase_admin
from firebase_admin import credentials, storage,db
import numpy as np
import time
import cv2
from ultralytics import YOLO
import os

path = os.path.dirname(os.path.realpath(__file__))

PROJECT_ID = "kickboard-user"#자신의 project id
cred = credentials.Certificate(path+"/siung-key.json")
app = firebase_admin.initialize_app(cred, {
    'storageBucket': f"{PROJECT_ID}.appspot.com",    
    'databaseURL': "https://kickboard-user-default-rtdb.firebaseio.com/"
})

bucket = storage.bucket()
dir = db.reference().child('user')
blobs=bucket.list_blobs(prefix='use/',delimiter='')
model=YOLO(path+'/best (2).pt')
file_name=[] 

def check_return(img):
    dKick=[]
    dBlock=[]
    dBus=[]
    result=model.predict(img)
    IsReturn = True
    for r in result:
        boxes=r.boxes
        for box in boxes:
            b=np.array(box.xyxy[0])
            c=box.cls
            name=model.names[int(c)]
            if(name=='kick'):
                dKick.append(b)
            elif(name=='block'):
                dBlock.append(b)
            elif(name=='bus'):
                dBus.append(b)
                
    for b in dBlock:
        x=b[0]    
        y=b[1]
        xs=dKick[0][0];xe=dKick[0][2]
        ys=dKick[0][1];ye=dKick[0][3]
        if((x>=xs and x<=xe) and ((x>=ys and y<=ye))):
            IsReturn=False
            break
        
    return IsReturn

def change_stop(target,result):
    if (result==True):
        target.set(True)
        
if __name__=='__main__':  
    dir = db.reference().child('user')
    while 1:
        uid=dir.get()
        file_name=[]
        k_uid=list(uid.keys())#유저이름 전부 가져오기
        blobs=bucket.list_blobs(prefix='use/',delimiter='')
        for blob in blobs:
            file_name.append(blob.name[4:])
        file_name.remove('')
        print(file_name)
        if(len(file_name))!=0:
            print('find image')
            file=file_name[0]
            id=file.split('.')[0]
            if id in k_uid:
                target_db=dir.child(str(id)).child('stop')
                target = bucket.get_blob('use/'+str(id)+'.png')
                arr = np.frombuffer(target.download_as_string(),np.uint8)
                img = cv2.imdecode(arr,cv2.COLOR_BGR2BGR555)
                #t=time.time()
                result=check_return(img)
                #print(f'calctime={time.time()-t}')   
                print(result)
                change_stop(target_db,result)
                #bucket.blob('use/'+str(id)+'.png').delete()
            else:
                print('not in user')
                #bucket.blob('use/'+str(id)+'.png').delete()
        else:
            print('no image')     
            pass
                      
        time.sleep(1)
    