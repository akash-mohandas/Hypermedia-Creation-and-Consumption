import tkinter
import cv2
import PIL.Image, PIL.ImageTk

##global height,width,canvas,my_rect
class Object_Track:
    
    
    def __init__(self):
        self.window=tkinter.Tk()
        self.window.title = "Select Frame"
        self.my_rect = None
        self.vid = cv2.VideoCapture(r"C:\Users\aakas\Downloads\videoplayback.mp4")
        self.width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH) 
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.canvas=tkinter.Canvas(self.window,width=self.width,height=self.height)

        if self.vid.isOpened():
            ret,self.frame = self.vid.read()
            self.frame = cv2.cvtColor(self.frame,cv2.COLOR_BGR2RGB)
            photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.frame))
            self.canvas.create_image(0,0,image=photo,anchor=tkinter.NW)

        self.canvas.bind("<Button-1>",self.mouse_click)
        self.b1 = tkinter.Button(self.window,text="FINISH",command=self.obj_track)
        self.b1.pack(side=tkinter.BOTTOM)
        self.canvas.pack()
        self.window.mainloop()
    def mouse_click(self,event):
        if self.my_rect:
            self.canvas.delete(self.my_rect)
        self.x1 = max(0,event.x-25)
        self.y1 = max(0,event.y-25)
        self.x2 = min(self.width,event.x+25)
        self.y2 = min(self.height,event.y+25)
        self.my_rect = self.canvas.create_rectangle((self.x1,self.y1),(self.x2,self.y2),outline='blue')

    def obj_track(self):
        self.tracker = cv2.TrackerBoosting_create()
        bbox = (self.x1,self.y1,self.x2,self.y2)
        ok = self.tracker.init(self.frame,bbox)
        while True:
            ok, self.frame = self.vid.read()
            
            if not ok:
                break
            self.timer = cv2.getTickCount()
            ok, bbox = self.tracker.update(self.frame)
            self.fps = cv2.getTickFrequency()/(cv2.getTickCount()-self.timer)
            if ok:
                p1 = (int(bbox[0]),int(bbox[1]))
                p2 = (int(bbox[2]),int(bbox[3]))
                cv2.rectangle(self.frame,p1,p2,(255,0,0),2,1)
            cv2.imshow("Tracking",self.frame)
            k=cv2.waitKey(1) &0xff
            if k==27:
                break
                
Object_Track()
