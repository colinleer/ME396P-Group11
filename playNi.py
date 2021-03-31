import wx
import wx.media as wxmedia
import wx.adv



class mainFrame(wx.Frame):
    

    def __init__(self, *args, **kwargs):
        super(mainFrame, self).__init__(*args, **kwargs)  
        self.filename = "./ni.wav"
        self.sound_choices = ['Ni!', 'Ekke Ekke Ekke Ekke Ptang Zoo Boing!', 'Noo']
        self.sound_files = ['ni.wav', 'ekke.wav', 'noo.wav']
        self.ni_GUI()

    def ni_GUI(self):
        # Create and populate menu bar
        menuBar = wx.MenuBar()
        fileMenu = wx.Menu()
        aboutMenu = fileMenu.Append(wx.ID_ANY, "&About")
        exitMenu = fileMenu.Append(wx.ID_ANY, "&Exit")
        menuBar.Append(fileMenu, "&File")
        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.About, aboutMenu)
        self.Bind(wx.EVT_MENU, self.Quit, exitMenu)
        self.Bind(wx.EVT_CLOSE, self.Quit)

        
        # Create choice list
        self.choice_list = wx.Choice(self, choices = self.sound_choices)
        self.Bind(wx.EVT_CHOICE, self.load_sound, self.choice_list)

        # Create play button
        play_button = wx.Button(self, wx.ID_ANY, "play", (10,10))
        self.Bind(wx.EVT_BUTTON, self.playNi, play_button)


        # Create and populate sizers
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        control_sizer = wx.StaticBoxSizer(wx.HORIZONTAL, self)

        main_sizer.Add(control_sizer, 0, wx.ALIGN_CENTER, 0)
        main_sizer.Add(wx.StaticBitmap(self, -1, wx.Bitmap("./img.png", wx.BITMAP_TYPE_ANY)), 0, wx.ALIGN_CENTER, 0)
        
        control_sizer.Add(self.choice_list)
        control_sizer.Add(play_button)

        # Load default soundfile
        self.choice_list.SetSelection(0)
        self.load_sound(None)

        # Show Frame
        self.SetSizerAndFit(main_sizer)
        self.Center()
        self.Show(True)

    # Callback function for EVT_CHOICE event
    # Loads selected .wav file 
    def load_sound(self, e):
        selection = self.choice_list.GetCurrentSelection()
        self.filename = "./{}".format(self.sound_files[selection])
        self.sound = wx.adv.Sound(self.filename)

    # Callback function for EVT_BUTTON event binded to play_button
    # Plays the audio file
    def playNi(self, e):
        if self.sound.IsOk():
            self.sound.Play(wx.adv.SOUND_ASYNC)
        else:
            wx.MessageBox("File Load Error", "Error")

    # Displays About Dialog 
    def About(self, e):
        text = """
        Rahmat Ashari
        Colin Campell
        Peter Wang"""
                
        dlg = wx.MessageDialog( self, text, "Knights of Ni! are:", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    # Callback for EVT_CLOSE event and file>quit
    def Quit(self, e):
        self.sound = wx.adv.Sound('./shrub.wav')
        if self.sound.IsOk():
            self.sound.Play(wx.adv.SOUND_ASYNC)

        answer = wx.MessageBox("Bring me a shrubbery!!!", "You want to leave?",
                       wx.YES_NO , self)

        if answer == wx.YES:
            self.Destroy()
    



app = wx.App()
mainFrame(None, title = "Knights of Ni! Demo v.1.0.0")
app.MainLoop()
