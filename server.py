import firebase_admin
from firebase_admin import credentials, storage,db
import numpy as np

import cv2
from ultralytics import YOLO

import sys
import os

from PyQt5.QtWidgets import *
from PyQt5 import  uic
from PyQt5.QtCore import *
from multiprocessing import Process, Queue
import multiprocessing as mp
import datetime
import time

path = os.path.dirname(os.path.realpath(__file__))
form_class = uic.loadUiType(path+"/mydesign.ui")[0]

def producer(q):
    
    proc=mp.current_process()
    
    while True:
        now=datetime.datetime.now()
        data=str(now)
        q.put(data)
        time.sleep(1)
        
class Consumer(QThread):
    poped = pyqtSignal(str)
    def __init__(self,q):
        super().__init__()
        self.q=q
        
    def run(self):
        if not self.q.empty():
            data=q.get()
            self.poped.emit(data)         
                        
class MyApp(QMainWindow,form_class):
    def __init__(self,q):
        super().__init__()
        self.setupUi(self)
        
        self.PROJECT_ID = "test-5bee0"#자신의 project id
        self.cred = credentials.Certificate(path+"/testapp.json")
        self.app = firebase_admin.initialize_app(self.cred, {
            'storageBucket': f"{self.PROJECT_ID}.appspot.com",    
            'databaseURL': "https://test-5bee0-default-rtdb.firebaseio.com/"
        })
        
        self.bucket = storage.bucket()
        self.dir = db.reference().child('user')
        self.blobs=self.bucket.list_blobs(prefix='use/') 
        self.model=YOLO(path+'/best (2).pt')
        self.start_bt.clicked.connect(self.btn1func)
        self.end_bt.clicked.connect(QCoreApplication.instance().quit)
        self.flag=True
        self.consumer=Consumer(q)
        self.consumer.poped.connect(self.print_data)
        self.consumer.start()
        
    def btn1func(self):
        pass
        
    def check_return(self,img):
        result1=self.model(img)
        clist=result1[0].boxes.cls
        cls=set()
        for cno in clist:
            cls.add(self.model.names[int(cno)])
        if ('kick' not in cls) or (('kick' in cls) and ('block' in cls)) or (('kick' in cls) and ('busstop' in cls)):
            result = False
            self.textBrowser.append('반납불가')
        elif len(cls)==1 and 'kick' in cls:
            result = True
            self.textBrowser.append('반납가능')
        return result

    def change_stop(self,target,result):
        if (result==True):
            target.set(True)
            self.textBrowser.append('반납완료')
         
    def run(self):
        file_name=[]
        uid=self.dir.get()
        k_uid=list(uid.keys())#유저이름 전부 가져오기
        self.textBrowser.setPlainText(f'{k_uid}')
        blobs=self.bucket.list_blobs(prefix='use/',delimiter='')
        for blob in blobs:
            file_name.append(blob.name[4:])
        file_name.remove('')
        if(len(file_name))!=0:
            self.textBrowser.append(f'find image')
            file=file_name[0]
            id=file.split('.')[0]
            if id in k_uid:
                target_db=self.dir.child(str(id)).child('stop')
                target = self.bucket.get_blob('use/'+str(id)+'.jpg')
                arr = np.frombuffer(target.download_as_string(),np.uint8)
                img = cv2.imdecode(arr,cv2.COLOR_BGR2BGR555)
                t=time.time()
                result=self.check_return(img)
                self.textBrowser.append(f'calctime={time.time()-t}')   
                self.textBrowser.append(result)
                self.change_stop(target_db,result)
                self.bucket.blob('use/'+str(id)+'.jpg').delete()
            else:
                self.textBrowser.append('not in user')
                self.bucket.blob('use/'+str(id)+'.jpg').delete()
        else:
            self.textBrowser.setPlainText('no image')     
            pass
                            
        time.sleep(1) 
        
    @pyqtSlot(str)
    def print_data(self,data):
        print(data)
        self.textBrowser.append(data)                  
if __name__=='__main__':
    q=Queue()
    p=Process(name="producer",target=producer,args=(q,),daemon=True)
    p.start()
    
    app=QApplication(sys.argv)
    my=MyApp(q)
    my.show()
    app.exec_()