# https://stackoverflow.com/questions/30048457/wxpython-refresh-a-plot-with-another-graph-by-a-button-event
# https://stackoverflow.com/questions/7647760/how-i-can-set-gap-in-vertical-boxsizer
# pythonw ~/Desktop/wxp/plotGUI.py

import numpy as np
import matplotlib
import wx

# all these matplotlib backend stuff ....
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure

#import lra model
import model

class myApp(wx.Frame):
    def __init__(self, title = "draft 1.0"):
        wx.Frame.__init__(self, None, title=title, size=(1000,750))
        self.freq = 1
        self.manualFreq = 1
        self.manualAmp = 1
        self.sliderFreq = 1
        self.sliderAmp = 1
        self.theUI()

    def theUI(self):
        # define main panel 
        mainPanel = wx.Panel(self)
        mainPanel.SetBackgroundColour("#ffffff")

        # All the statics
        font = wx.Font(20, family = wx.FONTFAMILY_SWISS, style = 0, weight = 90, 
                            underline = False, faceName ="", encoding = wx.FONTENCODING_DEFAULT)

        textLeftBottom = wx.StaticText(mainPanel, label = "it is wednesday my dudeeee")
        textLeftTop = wx.StaticText(mainPanel, label = "Yeeyee gui title")
        textManualAmp = wx.StaticText(mainPanel, label = "Amplitude")
        textManualFreq = wx.StaticText(mainPanel, label = "Frequency")
        textSliderAmp = wx.StaticText(mainPanel, label = "Amplitude")
        textSliderFreq = wx.StaticText(mainPanel, label = "Frequency")
        textLeftTop.SetFont(font)

        png = wx.StaticBitmap(mainPanel, -1, wx.Bitmap("squid.png", wx.BITMAP_TYPE_ANY))

        # create number input
        freqInput = wx.TextCtrl(mainPanel, -1)
        ampInput = wx.TextCtrl(mainPanel, -1)
        self.Bind(wx.EVT_TEXT, self.manualGetFreq, freqInput)
        self.Bind(wx.EVT_TEXT, self.manualGetAmp, ampInput)

        # create button to plot
        button0 = wx.Button(mainPanel, -1, label = "plot!")
        self.Bind(wx.EVT_BUTTON, self.plotStuff, button0)

        #msd plot button
        plot_msd_button = wx.Button(mainPanel, -1, label = "plot msd")
        self.Bind(wx.EVT_BUTTON, self.plotMSD, plot_msd_button)

        # create slider
        sliderAmp = wx.Slider(mainPanel, -1, minValue = -100, maxValue = 100, style = wx.SL_HORIZONTAL|wx.SL_LABELS, name = "amp")
        sliderFreq = wx.Slider(mainPanel, -1, minValue = 1, maxValue = 100, style = wx.SL_HORIZONTAL|wx.SL_LABELS, name = "freq")
        self.Bind(wx.EVT_SLIDER, self.changeFreqSlider, sliderFreq)
        self.Bind(wx.EVT_SLIDER, self.changeAmpSlider, sliderAmp)

        # Plot are
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.axes.set_ylabel("some magnitude")
        self.axes.set_xlabel("some x value")
        self.axes.set_title("Fantastic title")
        self.canvas = FigureCanvas(mainPanel, -1, self.figure)

        # declare sizers
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        rightSizer = wx.BoxSizer(wx.VERTICAL)
        leftSizer = wx.BoxSizer(wx.VERTICAL)
        manualSizer = wx.BoxSizer(wx.VERTICAL)
        sliderSizer = wx.BoxSizer(wx.VERTICAL)

        # put things in sizers
        manualSizer.AddStretchSpacer()
        manualSizer.Add(textManualAmp, 1, wx.EXPAND)
        manualSizer.Add(ampInput, 1, wx.EXPAND)
        manualSizer.Add(textManualFreq, 1, wx.EXPAND)
        manualSizer.Add(freqInput, 1, wx.EXPAND)
        manualSizer.Add(button0, 1, wx.EXPAND)
        manualSizer.AddStretchSpacer()

        sliderSizer.AddStretchSpacer()
        sliderSizer.Add(textSliderAmp, 1, wx.EXPAND)
        sliderSizer.Add(sliderAmp, 1, wx.EXPAND)
        sliderSizer.Add(textSliderFreq, 1, wx.EXPAND)
        sliderSizer.Add(sliderFreq, 1, wx.EXPAND)
        sliderSizer.AddStretchSpacer()

        leftSizer.AddStretchSpacer()
        leftSizer.Add(textLeftTop, 1, wx.CENTER)
        leftSizer.AddStretchSpacer()
        leftSizer.Add(self.canvas, 1, wx.EXPAND)
        leftSizer.AddStretchSpacer()
        leftSizer.AddStretchSpacer()
        leftSizer.Add(textLeftBottom, 1, wx.CENTER)
        leftSizer.AddStretchSpacer()

        rightSizer.Add(manualSizer, 1, wx.CENTER)
        rightSizer.Add(sliderSizer, 1, wx.CENTER)
        rightSizer.Add(png, 1, wx.EXPAND)
        mainSizer.AddSpacer(25)
        mainSizer.Add(leftSizer, 1, wx.EXPAND) 
        mainSizer.AddSpacer(25)
        mainSizer.Add(rightSizer, 1, wx.EXPAND)
        mainSizer.AddSpacer(25)
    
        # Put sizer to the main panel
        mainPanel.SetSizer(mainSizer)     

    def manualGetFreq(self, evt):
        if len(evt.GetString()) == 0:
            self.manualFreq = 1
        else:
            self.manualFreq = float(evt.GetString())

    def manualGetAmp(self, evt):
        if len(evt.GetString()) == 0:
            self.manualAmp = 1
        else:
            self.manualAmp = float(evt.GetString())
    
    def changeFreqSlider(self,evt):
        self.figure.set_canvas(self.canvas)
        self.axes.clear()
        self.axes.set_ylabel("some magnitude")
        self.axes.set_xlabel("some x value")
        self.axes.set_title("yeeyee plot title")
        obj = evt.GetEventObject() 
        self.sliderFreq = obj.GetValue() 
        t = np.linspace(-2*np.pi, 2*np.pi, 2000)
        x = self.sliderAmp*np.sin(self.sliderFreq*t)/t
        self.axes.plot(t, x)
        self.canvas.draw()

    def changeAmpSlider(self, evt):
        self.figure.set_canvas(self.canvas)
        self.axes.clear()
        self.axes.set_ylabel("some magnitude")
        self.axes.set_xlabel("some x value")
        self.axes.set_title("yeeyee plot title")
        obj = evt.GetEventObject() 
        self.sliderAmp = obj.GetValue() 
        t = np.linspace(-2*np.pi, 2*np.pi, 2000)
        x = self.sliderAmp*np.sin(self.sliderFreq*t)/t
        self.axes.plot(t, x)
        self.canvas.draw()

    def plotStuff(self, evt):
        self.figure.set_canvas(self.canvas)
        self.axes.clear()
        self.axes.set_ylabel("some magnitude")
        self.axes.set_xlabel("some x value")
        self.axes.set_title("yeeyee plot title")
        f = self.manualFreq
        a = self.manualAmp
        t = np.linspace(-2*np.pi, 2*np.pi, 2000)
        x = a*np.sin(f*t)/t
        self.axes.plot(t, x)
        self.canvas.draw()

    #test method for displaying lra response spectrum

    def plotMSD(self, evt):
        self.figure.set_canvas(self.canvas)
        self.axes.clear()
        self.axes.set_ylabel("Z (ohms)")
        self.axes.set_xlabel("Frequency (Hz)")
        self.axes.set_title("LRA Response")
        
        lra = model.test_lra()
        [freq,Z] = lra.get_impedance_spectrum()
        self.axes.loglog(freq, abs(Z))
        self.canvas.draw()


# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    frame = myApp()
    frame.Show()
    app.MainLoop()