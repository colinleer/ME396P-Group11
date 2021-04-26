# https://stackoverflow.com/questions/30048457/wxpython-refresh-a-plot-with-another-graph-by-a-button-event
# https://stackoverflow.com/questions/7647760/how-i-can-set-gap-in-vertical-boxsizer
# pythonw ~/Desktop/wxp/plotGUI.py

import numpy as np
import matplotlib
import wx
from scipy.io.wavfile import write as wavWrite
import model # local

# all these matplotlib backend stuff ....
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure

class myApp(wx.Frame):
    def __init__(self, title = "waveform builder version = 1.2-rahx"):
        wx.Frame.__init__(self, None, title=title, size=(1000,750))
        self.freq = 1
        self.amp = 1
        self.statusBar = self.CreateStatusBar(style = wx.BORDER_NONE) 
        self.t = []
        self.x = []
        self.wavRate = 44100
        self.samWidth = 3
        self.whichPlot = "builder"
        self.theUI()
        self.statusBar.SetStatusText('current amplitude = {0} , current frequency = {1}, showing plot: {2}'.format(self.amp, self.freq, self.whichPlot))

    def theUI(self):
        # define main panel 
        mainPanel = wx.Panel(self)
        mainPanel.SetBackgroundColour("#ffffff")

        # All the statics
        font = wx.Font(20, family = wx.FONTFAMILY_SWISS, style = 0, weight = 90, 
                            underline = False, faceName ="", encoding = wx.FONTENCODING_DEFAULT)

        textLeftTop = wx.StaticText(mainPanel, label = "Waveform Builder")
        textManualSection = wx.StaticText(mainPanel, label = "Manual Inputs")
        textSlider = wx.StaticText(mainPanel, label = "Slider Adjustment")
        textManualAmp = wx.StaticText(mainPanel, label = "Amplitude")
        textManualFreq = wx.StaticText(mainPanel, label = "Frequency")
        textSliderAmp = wx.StaticText(mainPanel, label = "Amplitude")
        textSliderFreq = wx.StaticText(mainPanel, label = "Frequency")
        textCourse = wx.StaticText(mainPanel, label = "ME-396P")
        textNames = wx.StaticText(mainPanel, label = "Rahmat Ashari, Colin Campbell, Peter Wang")
        textLeftTop.SetFont(font)

        png = wx.StaticBitmap(mainPanel, -1, wx.Bitmap("/Users/rahmatashari/Desktop/wxp/squid.png", wx.BITMAP_TYPE_ANY))

        # menubar 
        menuBar = wx.MenuBar()
        fileMenu = wx.Menu()
        aboutMenu = wx.Menu()
        openFileMenu = fileMenu.Append(wx.ID_ANY, "&Open")
        saveFileMenu = fileMenu.Append(wx.ID_ANY, "&Save")
        aboutSubMenu = aboutMenu.Append(wx.ID_ANY, "&About")
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(aboutMenu, "&About")
        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.onSaveAs, saveFileMenu)
        self.Bind(wx.EVT_MENU, self.About, aboutSubMenu)

        # create number inputs
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
        self.sliderAmp = wx.Slider(mainPanel, -1, minValue = -100, maxValue = 100, style = wx.SL_HORIZONTAL|wx.SL_LABELS, name = "amp")
        self.sliderFreq = wx.Slider(mainPanel, -1, minValue = 1, maxValue = 100, style = wx.SL_HORIZONTAL|wx.SL_LABELS, name = "freq")
        self.Bind(wx.EVT_SLIDER, self.changeFreqSlider, self.sliderFreq)
        self.Bind(wx.EVT_SLIDER, self.changeAmpSlider, self.sliderAmp)

        # Plot 
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.axes.set_ylabel("some magnitude")
        self.axes.set_xlabel("some x value")
        self.axes.set_title("Fantastic title")
        self.canvas = FigureCanvas(mainPanel, -1, self.figure)
        self.axes.grid(alpha = 0.5)
        self.whichPlot = "builder"

        # declare sizers
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        rightSizer = wx.BoxSizer(wx.VERTICAL)
        leftSizer = wx.BoxSizer(wx.VERTICAL)
        manualGrid = wx.GridSizer(2,2,10,10)
        sliderGrid = wx.GridSizer(2,2,5,5)

        manualGrid.Add(textManualAmp, 1, wx.CENTER)
        manualGrid.Add(ampInput, 1, wx.CENTER | wx.EXPAND)
        manualGrid.Add(textManualFreq, 1, wx.CENTER)
        manualGrid.Add(freqInput, 1, wx.CENTER | wx.EXPAND)

        sliderGrid.Add(textSliderAmp, 1, wx.EXPAND)
        sliderGrid.Add(self.sliderAmp, 1, wx.EXPAND | wx.EXPAND)
        sliderGrid.Add(textSliderFreq, 1, wx.EXPAND)
        sliderGrid.Add(self.sliderFreq, 1, wx.EXPAND | wx.EXPAND)

        leftSizer.AddStretchSpacer()
        leftSizer.Add(textLeftTop, 1, wx.CENTER)
        leftSizer.AddStretchSpacer()
        leftSizer.Add(self.canvas, 1, wx.EXPAND)
        leftSizer.AddStretchSpacer()
        leftSizer.AddStretchSpacer()
        leftSizer.AddStretchSpacer()
        leftSizer.Add(textCourse, 1, wx.CENTER)
        leftSizer.Add(textNames, 1, wx.CENTER)
        #leftSizer.AddStretchSpacer()

        rightSizer.AddStretchSpacer()
        rightSizer.Add(textManualSection, 1, wx.CENTER)
        rightSizer.Add(manualGrid, 1, wx.CENTER | wx.EXPAND)
        rightSizer.Add(button0, 1, wx.EXPAND)
        rightSizer.AddStretchSpacer()
        rightSizer.Add(textSlider, 1, wx.CENTER)
        rightSizer.Add(sliderGrid, 1, wx.CENTER)
        rightSizer.AddStretchSpacer()
        rightSizer.Add(png, 1, wx.EXPAND)
        rightSizer.AddStretchSpacer()

        mainSizer.AddSpacer(25)
        mainSizer.Add(leftSizer, 1, wx.EXPAND) 
        mainSizer.AddSpacer(25)
        mainSizer.Add(rightSizer, 1, wx.EXPAND)
        mainSizer.AddSpacer(25)
    
        # Put sizer to the main panel
        mainPanel.SetSizer(mainSizer)

    # get frequency if nputted manually
    def manualGetFreq(self, evt):
        if len(evt.GetString()) == 0:
            self.freq = self.freq
        else:
            self.freq = float(evt.GetString())
            self.sliderFreq.SetMin(self.freq -  10)
            self.sliderFreq.SetMax(self.freq +  10)
        #self.updateStatus()
        self.sliderFreq.SetValue(self.freq)

    # get amplitude if imputed manually
    def manualGetAmp(self, evt):
        if len(evt.GetString()) == 0:
            self.amp = self.amp
        else:
            self.amp = float(evt.GetString())
            self.sliderAmp.SetMin(self.amp -  10)
            self.sliderAmp.SetMax(self.amp +  10)
        #self.updateStatus()
        self.sliderAmp.SetValue(self.amp)

    # plot once the manual inputs are provided
    def plotStuff(self, evt):
        self.whichPlot = "builder"
        self.figure.set_canvas(self.canvas)
        self.axes.clear()
        self.axes.set_ylabel("some magnitude")
        self.axes.set_xlabel("some self.x value")
        self.axes.set_title("yeeyee plot title")
        self.axes.grid(alpha = 0.5)
        f = self.freq
        a = self.amp
        self.t = np.linspace(-2*np.pi, 2*np.pi, (self.wavRate - 1) * self.samWidth, endpoint = False)
        self.x = a*np.sin(f*self.t)/self.t
        self.axes.plot(self.t, self.x)
        self.canvas.draw()
        self.updateStatus()
    
    # update plot depending on freq value on slider
    def changeFreqSlider(self,evt):
        self.whichPlot = "builder"
        self.figure.set_canvas(self.canvas)
        self.axes.clear()
        self.axes.set_ylabel("some magnitude")
        self.axes.set_xlabel("some self.x value")
        self.axes.set_title("yeeyee plot title")
        self.axes.grid(alpha = 0.5)
        obj = evt.GetEventObject() 
        self.freq = float(obj.GetValue())
        self.t = np.linspace(-2*np.pi, 2*np.pi, (self.wavRate - 1) * self.samWidth, endpoint = False)
        self.x = self.amp * np.sin(self.freq * self.t)/self.t
        self.axes.plot(self.t, self.x)
        self.canvas.draw()
        self.updateStatus()

    # update plot depending on amp value on slider
    def changeAmpSlider(self, evt):
        self.whichPlot = "builder"
        self.figure.set_canvas(self.canvas)
        self.axes.clear()
        self.axes.set_ylabel("some magnitude")
        self.axes.set_xlabel("some self.x value")
        self.axes.set_title("yeeyee plot title")
        self.axes.grid(alpha = 0.5)
        obj = evt.GetEventObject() 
        self.amp = float(obj.GetValue())
        self.t = np.linspace(-2*np.pi, 2*np.pi, (self.wavRate - 1) * self.samWidth, endpoint = False)
        self.x = self.amp * np.sin(self.freq * self.t)/self.t
        self.axes.plot(self.t, self.x)
        self.canvas.draw()
        self.updateStatus()

    def updateStatus(self):
        self.statusBar.SetStatusText('current amplitude = {0} , current frequency = {1}, showing plot: {2}'.format(self.amp, self.freq, self.whichPlot))

    # Displays About Dialog 
    def About(self, evt):
        text = """
        Waveform builder GUI, a project for ME-396 taught at the University of Texas at Austin. Built by Knights of Ni!: Rahmat Ashari, Colin Campell, and Peter Wang
        """
                
        dlg = wx.MessageDialog(self, text, "Hello", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    # test method for displaying lra response spectrum
    def plotMSD(self, evt):
        self.whichPlot = "LRA"
        self.figure.set_canvas(self.canvas)
        self.axes.clear()
        self.axes.set_ylabel("Z (ohms)")
        self.axes.set_xlabel("Frequency (Hz)")
        self.axes.set_title("LRA Response")
        
        lra = model.test_lra()
        [freq,Z] = lra.get_impedance_spectrum()
        self.axes.loglog(freq, abs(Z))
        self.canvas.draw()
        self.updateStatus()

    def onSaveAs(self, event):
        with wx.FileDialog(self, "Save wave file", wildcard="WAV files (*.wav)|*.wav",
                        style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

            # the user changed their mind
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     

            # save the current contents in the file
            pathname = fileDialog.GetPath()
            try:
                wavWrite(str(pathname), self.wavRate, self.x)
            except IOError:
                wx.LogError("Cannot save current data in file {}.".format(pathname))

# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    frame = myApp()
    frame.Show()
    app.MainLoop()
