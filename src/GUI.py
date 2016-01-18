import Tkinter as tk
import tkFileDialog
import Tkconstants
from matplotlib import pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import gc
import plotGBTMap as gPlot
import sys
import matplotlib.animation as manimation
def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    return array[idx]

class GUI:
   def __init__(self, master):
      self.master=master
      self.frame = tk.Frame(self.master)
      self.data=np.array([])
      self.Num=0
      self.Num_Freq=0
      self.fig=plt.figure(figsize=(7,6))
      self.fig_Freq=plt.figure(figsize=(9, 5))
      self.inFileTxt=None
      self.freq_Txt=None
      self.vMin_Txt=None
      self.vMax_Txt=None
      self.ax_Main=None
      self.mark=None
      self.metaDic={}
      self.setUp()
      #self.inFileTxt=None
#      self.frame.pack()
   def setUp(self):
      self.master.protocol('WM_DELETE_WINDOW', self.close)
      self.master.wm_title("GBT Map Plot Machine")
      ##Define the control pannel##
      stepOne = tk.LabelFrame(self.master, text=" Control: ")
      stepOne.grid(row=0, column=0, columnspan=95, sticky='WN', \
                   padx=5, pady=5, ipadx=5, ipady=5)
      ##OpenFile
      inFileLbl = tk.Label(stepOne, text="Select the File:")
      inFileLbl.grid(row=0, column=0, sticky='W', padx=5, pady=2)
      self.inFileTxt = tk.Entry(stepOne)
      self.inFileTxt.grid(row=0, column=1, columnspan=7, sticky="WE", pady=3)
      self.inFileTxt.insert(0,"/home/chto/Desktop/NewProject3/VictorNewMap/fir_1hr_80-68_newpol_clean_map_I_800.npy")
      inFileBtn = tk.Button(stepOne, text="Browse ...",command=self.askopenfile)
      inFileBtn.grid(row=0, column=8, sticky='W', padx=5, pady=2)
      self.inFileTxt.bind("<Return>", self.EnterFileEvent)
      ###PlotButton
      plotBtn = tk.Button(stepOne, text="Plot",command=self.plotButton)
      plotBtn.grid(row=3, column=0, sticky='W', padx=5, pady=2)
      ###Save Button##
      self.outMovieTxt = tk.Entry(stepOne)
      self.outMovieTxt.grid(row=3, column=1, columnspan=7, sticky="WE", pady=3)
      self.outMovieTxt.insert(0,"./GBTPlotTool/Movie_Test/test.mp4")
      saveMovieBtn = tk.Button(stepOne, text="saveMov",command=self.plotSaveMov)
      saveMovieBtn.grid(row=3, column=8, sticky='W', padx=5, pady=2)

      self.outFreqTxt = tk.Entry(stepOne)
      self.outFreqTxt.grid(row=3, column=9, columnspan=7, sticky="WE", pady=3)
      self.outFreqTxt.insert(0,"./GBTPlotTool/Movie_Test/test.png")
      saveFreqBtn = tk.Button(stepOne, text="saveFreq",command=self.plotSaveFig)
      saveFreqBtn.grid(row=3, column=16, sticky='W', padx=5, pady=2)


      ###Freq
      freq_TxtLabel=tk.Label(stepOne, text="Freq:")
      freq_TxtLabel.grid(row=4, column=0, sticky='W', padx=5, pady=2)
      self.freq_Txt = tk.Entry(stepOne,width=5)
      self.freq_Txt.grid(row=4, column=0, columnspan=5, sticky="W", pady=3,padx=50)
      self.freq_Txt.insert(0,"0")
      ###Freq Button###
      IncrFreqBtn = tk.Button(stepOne, text=">>",command=self.IncFreq)
      IncrFreqBtn.grid(row=4, column=1, sticky='W', padx=50, pady=2)
      DecFreqBtn = tk.Button(stepOne, text="<<",command=self.DecFreq)
      DecFreqBtn.grid(row=4, column=1, sticky='W', padx=0, pady=2)
      ###Plot Pannel###
      stepTwo = tk.LabelFrame(self.master, text=" Plot: ", width=600, height=500)
      stepTwo.grid(row=0, column=95,columnspan=70,rowspan=10 ,sticky='NW', \
                   padx=5, pady=10, ipadx=5, ipady=5)
      ##Freq Plot Pannel###
      stepThree = tk.LabelFrame(self.master, text=" Freq Plot: ", width=700, height=450)
      stepThree.grid(row=0, column=0,columnspan=60,rowspan=20 ,sticky='WN', \
                   padx=5, pady=180, ipadx=5, ipady=0)
      
      self.freq_Txt.bind("<Return>", self.EnterEvent)
      ####PLot Range##########
      vMax_TxtLabel=tk.Label(stepOne, text="Vmax:")
      vMax_TxtLabel.grid(row=5, column=0, sticky='W', padx=5, pady=2)
      self.vMax_Txt = tk.Entry(stepOne,width=5)
      self.vMax_Txt.grid(row=5, column=0, columnspan=1, sticky="W", pady=3, padx=60)
      self.vMax_Txt.insert(0,"5")
      vMin_TxtLabel=tk.Label(stepOne, text="Vmin:")
      vMin_TxtLabel.grid(row=5, column=1, sticky='W', padx=0, pady=2)
      self.vMin_Txt = tk.Entry(stepOne,width=5)
      self.vMin_Txt.grid(row=5, column=1, columnspan=1, sticky="W", pady=3, padx=60)
      self.vMin_Txt.insert(0,"-2")
      self.vMin_Txt.bind("<Return>", self.EnterEvent)
      self.vMax_Txt.bind("<Return>", self.EnterEvent)

   def close(self):
      self.master.destroy()
   def DecFreq(self):
      freq=self.freq_Txt.get()
      self.freq_Txt.delete(0,"end")
      self.freq_Txt.insert(0,repr(eval(freq)-1))
      self.plotFigure()
   def IncFreq(self):
      freq=self.freq_Txt.get()
      self.freq_Txt.delete(0,"end")
      self.freq_Txt.insert(0,repr(eval(freq)+1))
      self.plotFigure()
   def EnterFileEvent(self,event):
      self.data=np.array([])
      self.plotFigure() 
   def EnterEvent(self,event):
      self.plotFigure() 
   def plotButton(self):
       print "open_File"
       self.openFile()
       self.plotFigure()
   def plotFigure(self):
      try:
         self.figAgg_Main.get_tk_widget().delete(self.figAgg_Main._tkphoto)
         self.fig.clf()
         plt.close(self.fig)
      except:
         None
      try:
         freq=eval(self.freq_Txt.get())
      except:
         print "Don't be stupid"
      if freq>=0 and freq<=256:
         self.ax_Main=gPlot.plotKiyoMap(self.data,self.metaDic,self.fig,round(freq),eval(self.vMax_Txt.get()),eval(self.vMin_Txt.get()))
      else:
         print "Wong Freq"
      if self.Num==0:
         self.addFigure(self.fig)
         self.Num=1
      else:
         self.figAgg_Main.draw()

   def plotFreqFigure(self,xx=0,yy=0):
      try:
         self.figAgg_Freq.get_tk_widget().delete(self.figAgg_Main._tkphoto)
         self.fig_Freq.clf()
         plt.close(self.fig_Freq)
      except:
         None
      ax=self.fig_Freq.add_subplot(1,1,1)
      self.line,=ax.plot(self.data[:,yy,xx])
      ax.set_title("RA=%s,Dec=%s"%(repr(yy),repr(xx)))

      if self.Num_Freq==0:
         self.addFigure(self.fig_Freq,2)
         self.Num_Freq=1
      else:
         self.figAgg_Freq.draw()
   def onclick(self,event2):
       try:
         ix, iy = gPlot.findCoordinate(event2.xdata,event2.ydata,\
                                       self.metaDic,self.data.shape)
         print ix,iy 
         self.plotFreqFigure(ix,iy)
         if self.mark:
            try:
             self.mark.remove()
            except:
               pass
         self.mark=self.ax_Main.scatter(event2.xdata,event2.ydata,marker='x',color='black',s=60)
         self.figAgg_Main.draw()
       except:
         print "Unexpected error:", sys.exc_info()[0]
#         None
#       self.line.set_ylim([np.min(self.data[:,iy,ix]),np.max(self.data[:,iy,ix])])
#       self.line.set_ydata(self.data[:,iy,ix])
#       self.figAgg_Freq.draw()
       return

        
   def addFigure(self,figure,param=0):

       # set up a canvas with scrollbars
       if param==0:
         canvas = tk.Canvas(self.master,width=565, height=485)
         canvas.grid(row=0, column=100, pady=25,padx=10,sticky='NW')
       else:
         canvas = tk.Canvas(self.master,width=700, height=400)
         canvas.grid(row=0, column=0, columnspan=70, pady=200, padx =5, sticky='SW')
       # plug in the figure
       figAgg = FigureCanvasTkAgg(figure, canvas)
       if param==0:
         self.figAgg_Main=figAgg
         mplCanvas = self.figAgg_Main.get_tk_widget()
         mplCanvas.grid(sticky=Tkconstants.NSEW)
       else: 
         self.figAgg_Freq=figAgg
         mplCanvas = self.figAgg_Freq.get_tk_widget()
         mplCanvas.grid(sticky=Tkconstants.NSEW)
       canvas.create_window(0,0, window=mplCanvas,tags="Test")
       canvas.config(scrollregion=canvas.bbox(Tkconstants.ALL))
       if param==0:
          cid = figure.canvas.mpl_connect('button_press_event', self.onclick)

       #canvas.delete("all")
       

   def openFile(self):
      try:
         name=self.inFileTxt.get()
         self.data=np.load(name,'r')
         f = open(name+".meta",'r')
         meTa=f.readlines()
         self.metaDic=eval(meTa[0])
         f.close()
#         self.Num=0
      except:
         print "File Not Exist \n"
         print name
         self.inFileTxt.delete(0,'end')
      return
   def askopenfile(self):
        AskReturn=tkFileDialog.askopenfile()
        if AskReturn!=None:
            self.inFileTxt.delete(0,'end')
            self.inFileTxt.insert(0,AskReturn.name)
        return AskReturn
   def plotSaveMov(self):
      AskReturn=tkFileDialog.asksaveasfile()
      if AskReturn!=None:
         self.outMovieTxt.delete(0,'end')
         self.outMovieTxt.insert(0,AskReturn.name)
         try:
            self.plotMovie(self.outMovieTxt.get())
         except:
            None
      return AskReturn
   def plotSaveFig(self):
      AskReturn=tkFileDialog.asksaveasfile()
      if AskReturn!=None:
         self.outFreqTxt.delete(0,'end')
         self.outFreqTxt.insert(0,AskReturn.name)
         try:
            self.fig_Freq.savefig(self.outFreqTxt.get())
         except:
            None
      return AskReturn

   def plotMovie(self,name):
      window = tk.Toplevel(self.master)
      FFMpegWriter = manimation.writers['ffmpeg']
      fig = plt.figure()
      writer = FFMpegWriter(fps=3)
      with writer.saving(fig, name, 100):
         for i in xrange(self.data.shape[0]):
            print i
            ax=gPlot.plotKiyoMap(self.data,self.metaDic,fig,i,eval(self.vMax_Txt.get()),eval(self.vMin_Txt.get()))
            writer.grab_frame()
            plt.clf()
      plt.close(fig)
      fig.clf()

                


          
