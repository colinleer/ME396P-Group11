# https://stackoverflow.com/questions/30048457/wxpython-refresh-a-plot-with-another-graph-by-a-button-event
# https://stackoverflow.com/questions/7647760/how-i-can-set-gap-in-vertical-boxsizer
# pythonw ~/Desktop/testCode/WaveformBuilder.py

# Have TODO
# [DONE] Simulated Response


# Nice TODO
# [DONE] save/load wavebuilder segment arrays in custom file format (xml, json)?
# [DONE] highlight current segment on plot
# [DONE] read LRA models parameters from files in a folder
# show LRA model resonant frequency on plot? or in parameters?
# smoothing function between segments
# [WONT DO] additional parameters? alter sine shape, etc
# [WONT DO] sinc function segment necessary?


# BUG 
# [FIXED] Waveform segment times shift around when amplitude is changed 
# [FIXED] Deleting waveform segments causes weird behavior 

import numpy as np
import matplotlib
import wx
from scipy.io.wavfile import write as wavWrite
from pubsub import pub
import json

#local imports
import lra_panel 
import waveform_panel 

# matplotlib backend stuff ....
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
        #self.t = []
        #self.x = []
        #self.wavRate = 44100
        #self.samWidth = 3
        #self.whichPlot = "builder"
        self.theUI()
        self.currentFile = ""
        self.statusBar.SetStatusText("working on new file")
        self.waveSegment = []
        self.loadedInfo = 0
        
    #pub.sendMessage("test", data = 0)


    def theUI(self):
        # define main panel 
        mainPanel = wx.Panel(self)
        mainPanel.SetBackgroundColour("#ffffff")

        # All the statics
        font = wx.Font(36, family = wx.FONTFAMILY_SWISS, style = 0, weight = 90, 
                            underline = False, faceName ="", encoding = wx.FONTENCODING_DEFAULT)

        # menubar 
        menuBar = wx.MenuBar()
        fileMenu = wx.Menu()
        aboutMenu = wx.Menu()
        openFileMenu = fileMenu.Append(wx.ID_ANY, "&Load Waveform")
        saveFileMenu = fileMenu.Append(wx.ID_ANY, "&Save Waveform")
        exportFileMenu = fileMenu.Append(wx.ID_ANY, "&Export as .wav")
        aboutSubMenu = aboutMenu.Append(wx.ID_ANY, "&About")
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(aboutMenu, "&About")
        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.onOpen, openFileMenu)
        self.Bind(wx.EVT_MENU, self.onSaveAs, saveFileMenu)
        self.Bind(wx.EVT_MENU, self.onExportAs, exportFileMenu)
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
        pub.subscribe(self.getWaveSegment, "waveSegmentData")
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
        mainPanel.SetSizerAndFit(mainSizer)
        self.Center()

    def getWaveSegment(self, data):
        self.waveSegment = data

    def getLRACoeff(self, data):
        self.LRACoeff = data

    #update waveform plot with new data
    def update_plot(self, data):
        [time, values, low, high] = data
        self.figure.set_canvas(self.canvas)
        self.axes.clear()
        self.axes.set_ylabel("Voltage")
        self.axes.set_xlabel("Time (ms)")
        self.axes.set_title("Waveform")
        self.axes.grid(alpha = 0.5)
        self.axes.plot(time, values)
        self.axes.axvspan(low, high, color='red', alpha=0.25)
        self.canvas.draw()
        self.dataToExport = values
        

    # Must update this 
    def updateStatus(self):
        self.statusBar.SetStatusText("file loaded! Using info from {}".format(self.currentFile))

    # Displays About Dialog 
    def About(self, evt):
        text = """
        A project for ME-396P @ UT Austin. 
        
        Built by Knights of Ni!: 
        
        Rahmat Ashari
        Colin Campell
        Peter Wang
        """
                
        dlg = wx.MessageDialog(self, text, "Haptic Waveform Designer", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    #export current waveform as .wav file
    def onExportAs(self, event):
        with wx.FileDialog(self, "Save .wav file", wildcard="WAV files (*.wav)|*.wav",
                        style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

            # the user changed their mind
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     

            # save the current contents in the file
            pathname = fileDialog.GetPath()
            try:
                wavWrite(str(pathname), 44100, self.dataToExport) # in 1 data every 1 milisecond
            except IOError:
                wx.LogError("Cannot export current data in file {}.".format(pathname))

    #save current waveform segments as file (JSON)
    def onSaveAs(self, event):
        with wx.FileDialog(self, "Save workflow", wildcard="Waveform files (*.wvfm)|*.wvfm", 
                        style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

            # the user changed their mind
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     

            # save the current contents in the file
            pathname = fileDialog.GetPath()
            fileToSave = self.waveSegment
            try:
                with open(pathname, "w") as file: 
                    json.dump(fileToSave, file, indent = 4, sort_keys = False)
            except IOError:
                wx.LogError("Cannot save current data in file {}.".format(pathname))

    #load waveform file (JSON)
    def onOpen(self, event):
        with wx.FileDialog(self, "Open workflow", wildcard="Waveform files (*.wvfm)|*.wvfm",
                        style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return 

            pathname = fileDialog.GetPath()
            try:
                self.currentFile = pathname
                with open(pathname, 'r') as file:
                    self.loadedInfo = json.load(file)
                    pub.sendMessage("sendLoadData", data = self.loadedInfo)
                self.updateStatus()
            except IOError:
                wx.LogError("something went wrong lol")

# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    frame = myApp()
    frame.Show()
    app.MainLoop()
