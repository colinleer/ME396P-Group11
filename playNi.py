import wx
import wx.media as wxmedia


class mainFrame(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(mainFrame, self).__init__(*args, **kwargs)  
        self.basicGUI()

    def basicGUI(self):
        # menu bar
        menuBar = wx.MenuBar()
        fileMenu = wx.Menu()
        aboutMenu = fileMenu.Append(wx.ID_ANY, "&About")
        exitMenu = fileMenu.Append(wx.ID_ANY, "&Exit")
        menuBar.Append(fileMenu, "&File")
        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.About, aboutMenu)
        self.Bind(wx.EVT_MENU, self.Quit, exitMenu)

        # play button
        buttonPlay = wx.Button(self, wx.ID_ANY, "play", (10,10))
        self.Bind(wx.EVT_BUTTON, self.playNi, buttonPlay)

        self.Show(True)

    def playNi(self, e):
        self.soundMedia = wxmedia.MediaCtrl(self)
        if self.soundMedia.Load('/Users/rahmatashari/Desktop/wxptest/ni.wav'):
            self.soundMedia.Play()

    def About(self, e):
        dlg = wx.MessageDialog( self, "Yo", "YEET", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def Quit(self, e):
        self.Close()

app = wx.App()
mainFrame(None, title = "Knights of Ni! Demo v.1.0.0", size = (400, 300))
app.MainLoop()
