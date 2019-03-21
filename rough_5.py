import cv2
import tkinter
import tkinter.filedialog
import PIL.Image
import PIL.ImageTk
import numpy as np
import pyaudio
import wave
import time


class Begin:
    def __init__(self):
        self.win = tkinter.Tk()
        self.create_link_press = False
        self.save_file_press= False
        self.panelA,self.panelB = None, None
        self.slider1, self.slider2, self.my_rect = None, None, [None,None,None]
        self.frames1,self.frames2 = [], []
        self.pos1, self.pos2 = 0,0
        self.audio1, self.audio2 = None, None
        self.b1=tkinter.Button(self.win,text="Import Primary Video",command=self.import_primary)
        #b1.pack(side='top')
        self.b2=tkinter.Button(self.win,text="Import Secondary Video",command=self.import_secondary)
        #b2.pack(side='top')
        self.b3=tkinter.Button(self.win,text="Create Hyperlink",command=self.button_press_one)
        self.b4=tkinter.Button(self.win,text="Import Primary Audio",command=self.audio_one)
        self.b7=tkinter.Button(self.win,text="Import Secondary Audio",command=self.audio_two)
        self.b5=tkinter.Button(self.win,text="Connect Video")
        self.b6=tkinter.Button(self.win,text="Save File",command=self.button_press_two)
        self.b1.grid(row=0,column=1)
        self.b2.grid(row=1,column=1)
        self.b3.grid(row=2,column=1)
        self.b4.grid(row=0,column=2)
        self.b7.grid(row=1,column=2)
        self.b5.grid(row=0,column=4)
        self.b6.grid(row=0,column=5)
        self.l1 = tkinter.Label(self.win,text='Actions')
        self.l1.grid(row=0,column=0)
        image = np.zeros((240,320,3),np.uint8)
        image = PIL.Image.fromarray(image)
        image = PIL.ImageTk.PhotoImage(image)
##        self.panelA = tkinter.Label(image=image)
##        self.panelA.image = image
##        self.panelA.grid(row=3)
        self.canvas = tkinter.Canvas(self.win,width=320,height=240)
        self.win.image = image
        self.canvas.create_image(0,0,image=image,anchor=tkinter.NW)
        self.canvas.grid(row=3)
        self.panelB = tkinter.Label(image=image)
        self.panelB.image = image
        self.panelB.grid(row=3,column=1,columnspan=4)
##        self.panelA.bind("<Button-1>",self.mouse_click)
##        self.lb1 = tkinter.Listbox()
##        if text:
##            self.lb1.insert(1,text)
##            self.lb1.grid(row=0,column=3)
        self.bboxes=[]
        self.colors=['blue','green','red']
        self.bbox = tuple()
        self.position_1, self.position_2, self.secondary_videos = [], [],[]
        self.win.mainloop()

    def mouse_click(self,event):
        print(event.x,event.y)
        length = len(self.bboxes)
        if length<=2:
            if self.my_rect[length]:
                self.canvas.delete(self.my_rect[length])
            self.x1= max(0,event.x - 25)
            self.x2 = min(self.width1,event.x + 25)
            self.y1 = max(0,event.y - 25)
            self.y2 = min(self.height1, event.y + 25)
            self.my_rect[length] = self.canvas.create_rectangle((self.x1,self.y1,),(self.x2,self.y2),outline=self.colors[length])
            #self.create_link_press = False
            self.bbox=(self.x1,self.y1,self.x2-self.x1,self.y2-self.y1)
            
    def audio_one(self):
        self.audio1 = tkinter.filedialog.askopenfilename()

    def audio_two(self):
        self.audio2 = tkinter.filedialog.askopenfilename()

    def button_press_one(self):
        if self.bbox and len(self.bboxes)<=2 :
            self.create_link_press = True
            self.bboxes.append(self.bbox)
            self.position_1.append(self.pos1)
            self.position_2.append(self.pos2)
            self.secondary_videos.append(self.path2)
        self.create_link_press = True
##        text = tkinter.StringVar()
##        e=tkinter.Entry(self.win)
##        e.grid(row=1,column=6)
##        text = e.get()
##        self.lb1.insert(1,text)
##        self.lb1.grid(row=0,column=3)

    def button_press_two(self):
        self.save_file_press = True
        self.win.destroy()
        
    def import_primary(self):
        
        self.path1 = tkinter.filedialog.askopenfilename()
        vid = cv2.VideoCapture(self.path1)
        self.width1 = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height1 = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        
        if vid.isOpened():
            while True:
                ret,image = vid.read()
                if not ret:
                    break
                self.frames1.append(image)
        self.canvas = tkinter.Canvas(self.win,width=self.width1,height=self.height1)    
        image =cv2.cvtColor(self.frames1[0],cv2.COLOR_BGR2RGB)
        image = PIL.Image.fromarray(image)
        image = PIL.ImageTk.PhotoImage(image)
##            self.panelA = tkinter.Label(image=image)
##            self.panelA.image = image
##            self.panelA.grid(row=3)
##            self.panelA.bind("<Button-1>",self.mouse_click)
        self.win.image = image
        self.canvas.create_image(0,0,image=image,anchor=tkinter.NW)
        self.canvas.grid(row=3)
        self.canvas.bind("<Button-1>",self.mouse_click)
            
        self.slider1 = tkinter.Scale(self.win,from_=1, to = len(self.frames1),orient = tkinter.HORIZONTAL,command=self.display_frame1)
        self.slider1.grid(row=4)

    def display_frame1(self,pos):
        self.pos1=int(pos)-1
        print(self.pos1)
        image =cv2.cvtColor(self.frames1[self.pos1],cv2.COLOR_BGR2RGB)
        image = PIL.Image.fromarray(image)
        image = PIL.ImageTk.PhotoImage(image)
##        self.panelA = tkinter.Label(image=image)
##        self.panelA.image = image
##        self.panelA.grid(row=3)
##        self.panelA.bind("<Button-1>",self.mouse_click)
        self.win.image = image
        self.canvas.create_image(0,0,image=image,anchor=tkinter.NW)
        self.canvas.bind("<Button-1>",self.mouse_click)

    def display_frame2(self,pos):
        self.pos2=int(pos)-1
        print(self.pos2)
        image =cv2.cvtColor(self.frames2[self.pos2],cv2.COLOR_BGR2RGB)
        image = PIL.Image.fromarray(image)
        image = PIL.ImageTk.PhotoImage(image)
        self.panelB = tkinter.Label(image=image)
        self.panelB.image = image
        self.panelB.grid(row=3,column=1,columnspan=4)
        #self.panelB.bind("<Button-1>",self.mouse_click)
        
    def import_secondary(self):
        
        self.path2 = tkinter.filedialog.askopenfilename()
        vid = cv2.VideoCapture(self.path2)
        
        if vid.isOpened():
            while True:
                ret,image = vid.read()
                if not ret:
                    break
                self.frames2.append(image)
            image =cv2.cvtColor(self.frames2[0],cv2.COLOR_BGR2RGB)
            image = PIL.Image.fromarray(image)
            image = PIL.ImageTk.PhotoImage(image)
            self.panelB = tkinter.Label(image=image)
            self.panelB.image = image
            self.panelB.grid(row=3,column=1,columnspan=4)
            #self.panelB.bind("<Button-1>",self.mouse_click)
            self.slider2 = tkinter.Scale(self.win,from_=1, to = len(self.frames2),orient = tkinter.HORIZONTAL,command=self.display_frame2)
            self.slider2.grid(row=4,column=1)

class Display_Video:
    def __init__(self,window,window_title,aud1,aud2,bboxes=[],pos1=[],pos2=[],video_source1=0,video_source2=[]):
        self.window = window
        self.window.title(window_title)
        self.play_press = False
        self.pause_press = False
        self.stop_press = False
        self.play=tkinter.Button(self.window,text="Play",command=self.play_button_press)
        self.pause=tkinter.Button(self.window,text="Pause",command=self.pause_button_press)
        self.stop=tkinter.Button(self.window,text="Stop",command=self.stop_button_press)
        self.video_source1 = video_source1
        #self.x1,self.x2,self.y1,self.y2 = x1,x2,y1,y2
        self.vid = MyVideoCapture(self.video_source1)
        self.pos1 = pos1
        self.pos11 = pos1.copy()
        self.pos2= pos2
        self.track=[250,250,250]
        self.linked = True
        self.video_source2 = video_source2
        self.aud1 = aud1
        self.aud2 = aud2
        self.bboxes = bboxes.copy()
        self.bboxes1 = bboxes.copy()
        self.colors = [(0,0,255),(0,255,0),(255,0,0)]
        self.trackers=[]
        self.indexes=[]
        self.canvas = tkinter.Canvas(window,width=self.vid.width,height=self.vid.height)
        self.canvas.bind("<Button-1>",self.mouse_click)
        self.canvas.grid(row=0,column=0,columnspan=5)
        self.play.grid(row=1,column=0)
        self.pause.grid(row=1,column=2)
        self.stop.grid(row=1,column=4)
        

        #self.tracker = cv2.TrackerBoosting_create()
        for i in self.bboxes:
            self.trackers.append(cv2.TrackerBoosting_create())
        #self.bbox = (self.x1,self.y1,self.x2-self.x1,self.y2-self.y1)
        #self.multiTracker = cv2.MultiTracker_create()
        
        self.delay = 14
        self.stream= None
        self.update()

        self.window.mainloop()

    def update(self):
        if self.play_press:
            ret,frame = self.vid.get_frame()
            #print(frame.shape[:2])
            for i in range(len(self.pos1)):
                self.pos1[i]-=1
            if -1 in self.pos1 :
                count = self.pos1.count(-1)
                index = self.pos1.index(-1)
                self.indexes.append(index)
                while True:
                    ok = self.trackers[index].init(frame,self.bboxes[index])
                    count-=1
                    if count==0:
                        break
                    else:
                        index= index + 1 + self.pos1[index+1:].index(-1)
                        self.indexes.append(index)
            elif any([i<-1 for i in self.pos1]) and self.linked:
                self.delay = 10
                for i in self.indexes:
                    if(self.track[i]>=0):
                        ok,self.bboxes[i] = self.trackers[i].update(frame)
                        self.track[i]-=1
                    else:
                        self.bboxes[i]=(0,0,0,0)
                        self.delay = 24
                    self.p1=(int(self.bboxes[i][0]),int(self.bboxes[i][1]))
                    self.p2=(int(self.bboxes[i][0]+self.bboxes[i][2]),int(self.bboxes[i][1]+self.bboxes[i][3]))
                    cv2.rectangle(frame,self.p1,self.p2,self.colors[i],2,1)
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0,0,image=self.photo,anchor=tkinter.NW)
            #time.sleep(0.3)

        self.window.after(self.delay,self.update)

    def callback(self,in_data, frame_count, time_info, status):
   
        self.data = self.wf.readframes(frame_count)
        return (self.data, pyaudio.paContinue)

    
    def play_button_press(self):
        self.play_press = True
        if not self.stream :
            self.wf = wave.open(self.aud1,'rb')
            self.p = pyaudio.PyAudio()
            self.stream = self.p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),channels=self.wf.getnchannels(),rate=self.wf.getframerate(),output=True,stream_callback=self.callback)

    def pause_button_press(self):
        self.play_press = False
        #self.pause_press = True

    def stop_button_press(self):
        if self.stream:
            self.stream.close()
        self.stream = None
        self.stop_press = True
        self.play_press = False
        self.vid = MyVideoCapture(self.video_source1)
        self.pos1 = self.pos11.copy()
        self.track=[250,250,250]
        self.bboxes = self.bboxes1.copy()
        ret,frame = self.vid.get_frame()
        self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
        self.canvas.create_image(0,0,image=self.photo,anchor=tkinter.NW)        
        
    def mouse_click(self,event):
        for i in self.indexes:
            if((event.x >= int(self.bboxes[i][0]) and event.x<=int(self.bboxes[i][0]+self.bboxes[i][2])) and (event.y>=int(self.bboxes[i][1]) and event.y<=int(self.bboxes[i][1]+self.bboxes[i][3]))):
                self.vid=MyVideoCapture(self.video_source2[i])
                self.vid.skip_frames(self.pos2[i])
                self.linked = False
                self.delay = 24
                self.stream.close()
                self.wf.close()
                self.wf = wave.open(self.aud2,'rb')
                skip = int(self.pos2[i]/350 * 500)
                while True:
                    if not skip:
                        break
                    self.data= self.wf.readframes(1024)
                    skip-=1
                self.stream = self.p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),channels=self.wf.getnchannels(),rate=self.wf.getframerate(),output=True,stream_callback=self.callback)

                #self.bbox= (0,0,0,0)
                #self.canvas = tkinter.Canvas(self.window,width=self.vid.width,height=self.vid.height)

class MyVideoCapture:

    def __init__(self,video_source=0):
        self.vid=cv2.VideoCapture(video_source)

        if not self.vid.isOpened():
            raise ValueError("Unable to open video source",video_source)

        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret,frame = self.vid.read()
            if ret:
                return (ret,cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
            else:
                return (ret,None)
        else:
            return (False,None)
        
    def skip_frames(self,frames):
        if self.vid.isOpened():
            while(frames):
                ret,frame = self.vid.read()
                frames-=1
        
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()


a = Begin()
print(a.bboxes)
if a.create_link_press :
    b= Display_Video(tkinter.Tk(),"Hypermedia",a.audio1,a.audio2,a.bboxes,a.position_1,a.position_2,a.path1,a.secondary_videos)
    
