#!/usr/bin/env python3
from tkinter import *
from PIL import ImageTk, Image
import os
from os import system
from platform import system as platform
import sys
from subprocess import call
import tempfile

filename=""
page_number="" 
img_file=""

class MainFrame (Frame):
  def __init__(self, master, *pargs):
    Frame.__init__(self, master, *pargs)
    self.pack(fill=BOTH, expand=YES)
    self.canv = Canvas(self, bg="blue",bd=1)
    #self.canv = Canvas(self, width=400, height=400,bg="blue",bd=1)
    self.canv.pack()
    #self.canv.pack(fill=BOTH, expand=YES)
    #self.canv.create_rectangle(50, 50, 250, 150, fill='red')
    self.o_img = Image.open(img_file)
    width,height = self.o_img.size
    self.o_height = height
    self.o_width  = width
    self.image_ratio = width/height
    self.photo_img = ImageTk.PhotoImage(self.o_img.copy())
    #self.photo_img = ImageTk.PhotoImage(self.o_img.resize((400,400)))
    self.ca_img = self.canv.create_image(0,0, image=self.photo_img, anchor = NW)
    #self.button1=Button(self,text="Hello",background="green")
    #self.button1.pack()
    self.item = None
    self.bind('<Configure>', self._resize_frame)
    self.canv.bind('<Motion>', self._guide_line, '+')
    self.canv.bind('<Leave>', self._leave_canvas, '+')

    self.canv.bind('<Button-1>', self._canvas_b1,'+')
    self.canv.bind("<B1-Motion>", self._canvas_b1_motion, '+')
    self.canv.bind("<ButtonRelease-1>", self._canvas_b1_release, '+')

  def _canvas_b1(self,event):
    self.start = [event.x, event.y]
  def _canvas_b1_motion( self, event ):
    if self.item is not None:
      self.canv.delete(self.item)
    self.item = self.canv.create_rectangle( self.start, (event.x,event.y) )
    self._guide_line(event)

  def _canvas_b1_release( self, event ):
    print([self.o_width,self.o_height])
    rx = 1/self.canv.winfo_width()*self.o_width/150*72
    ry = 1/self.canv.winfo_height()*self.o_height/150*72
    x = int(self.start[0]*rx)
    y = int(self.start[1]*ry)
    x1 = int( event.x*rx )
    y1 = int( event.y*ry )
    W = abs( x1 - x )
    H = abs( y1 - y )
    x = min( x,x1)
    y = min(y,y1)
    print( x,"\t",y,"\t",W,"\t",H )
    command = ['pdftocairo' ]
    command += ['-f', page_number, '-l', page_number]
    command += ['-x', str(x), '-y',str(y),'-W',str(W),'-H',str(H),'-paperh',str(H),'-paperw',str(W) ]
    command += ['-pdf',filename, 'out.pdf']
    print(' '.join(command))
    call(command)
    self.canv.delete(self.item)
    self.start= None;
    self.item = None;
    self._guide_line(event)




  def _resize_frame(self,event):
    new_width = event.width
    new_height = event.height
    if new_width >= new_height*self.image_ratio:
      new_width = int(new_height*self.image_ratio)
    else:
      new_height = int(new_width/self.image_ratio)
    self.photo_img = ImageTk.PhotoImage(self.o_img.resize((new_width, new_height)))
    self.canv.config(width=new_width,height=new_height)
    self.canv.itemconfig(self.ca_img,image=self.photo_img )

    #self.background_image = ImageTk.PhotoImage(self.image)
    #self.background.configure(image =  self.background_image)

  def _guide_line(self,event):
    self.canv.delete('no')
    dashes = [3, 2]
    self.x = self.canv.create_line(event.x, 0, event.x, 1000, dash=dashes, tags='no')
    self.y = self.canv.create_line(0, event.y, 1000, event.y, dash=dashes, tags='no')
  def _leave_canvas(self,event):
    self.canv.delete('no')




def main():
  if len(sys.argv) !=3 :
    print( "usage: ",sys.argv[0], "file_name.pdf page_number")
    exit(0)
  print ("good")
  global filename, page_number, img_file
  filename = sys.argv[1]
  page_number = sys.argv[2]
  tmp_dir = tempfile.mkdtemp()
  img_file = tmp_dir+'/out_test'
  command=['pdftocairo', '-f', page_number, '-l', page_number, '-singlefile','-png',filename, img_file]
  call(command)
  img_file += '.png'
  print(img_file)

  root = Tk()
  root.geometry("800x1024")
  main_frame = MainFrame(root)
  if platform() == 'Darwin':  # How Mac OS X is identified by Python
    system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
  root.after(1000, lambda: root.focus_force())

  root.mainloop()

if __name__ == '__main__':
#    try:
#        from tkinter import *
#    except ImportError:
#        from Tkinter import *
    main()



