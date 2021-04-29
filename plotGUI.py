# https://stackoverflow.com/questions/30048457/wxpython-refresh-a-plot-with-another-graph-by-a-button-event
# https://stackoverflow.com/questions/7647760/how-i-can-set-gap-in-vertical-boxsizer
# pythonw ~/Desktop/wxp/plotGUI.py

# Have TODO
# Simulated Response
# create simple wxDialog for LRA Model plot

# Nice TODO
# sinc function segment necessary?
# smoothing function between segments
# save/load wavebuilder segment arrays in custom file format (xml, json)?
# highlight current segment on plot
# additional parameters? alter sine shape, etc
# read LRA models parameters from files in a folder
# show LRA model resonant frequency on plot? or in parameters?

# BUG 
# Waveform segment times shift around when amplitude is changed
# Deleting waveform segments causes weird behavior

import numpy as np
import matplotlib
import wx
from scipy.io.wavfile import write as wavWrite
from pubsub import pub

#local imports
import lra_panel 
import waveform_panel 

# all these matplotlib backend stuff ....
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure

class myApp(wx.Frame):
    def __init__(self, title = "Haptic Waveform Designer  v1.3"):
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
        self.waves = []

    def theUI(self):
        # define main panel 
        mainPanel = wx.Panel(self)
        mainPanel.SetBackgroundColour("#ffffff")

        # All the statics
        font = wx.Font(36, family = wx.FONTFAMILY_SWISS, style = 0, weight = 90, 
                            underline = False, faceName ="", encoding = wx.FONTENCODING_DEFAULT)

        # textLeftTop = wx.StaticText(mainPanel, label = "Haptic Waveform Designer")
        # textLeftTop.SetFont(font)

        # png = wx.StaticBitmap(mainPanel, -1, wx.Bitmap("squid.png", wx.BITMAP_TYPE_ANY))

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

        # Plot 
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.axes.set_ylabel("Voltage")
        self.axes.set_xlabel("Time (ms)")
        self.axes.set_title("Waveform")
        self.canvas = FigureCanvas(mainPanel, -1, self.figure)
        self.axes.grid(alpha = 0.5)
        self.whichPlot = "builder"

        #register for waveform plot updates
        pub.subscribe(self.update_plot, 'update_waveform_data')

        wvfm_panel = waveform_panel.waveform_builder(mainPanel)
        lra_pnl = lra_panel.lra_panel(mainPanel)



        # declare sizers
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        top_sizer = wx.BoxSizer(wx.HORIZONTAL)
        top_sizer.Add(self.canvas, 1, wx.EXPAND)
        top_sizer.Add(lra_pnl, 0, wx.TOP | wx.RIGHT, 60)
        mainSizer.Add(top_sizer, 1, wx.EXPAND)
        mainSizer.Add(wvfm_panel, 0, wx.ALL|wx.EXPAND, 10)

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

    def update_plot(self, data):
        [time, values] = data
        self.figure.set_canvas(self.canvas)
        self.axes.clear()
        self.axes.set_ylabel("Voltage")
        self.axes.set_xlabel("Time (ms)")
        self.axes.set_title("Waveform")
        self.axes.grid(alpha = 0.5)
        self.axes.plot(time, values)
        self.canvas.draw()

    # TODO 
    def highlight_plot(self, data):
        [min, max] = data
        self.axes.axvspan(min, max, color='red', alpha=0.5)


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
        with wx.FileDialog(self, "Save .wav file", wildcard="WAV files (*.wav)|*.wav",
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
