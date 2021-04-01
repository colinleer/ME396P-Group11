import wx
import wx.adv

class mainFrame(wx.Frame):
    

    def __init__(self, *args, **kwargs):
        super(mainFrame, self).__init__(*args, **kwargs)  

        #### Set files to use later

        self.filename = "./inc/ni.wav"
        self.sound_names = ['Ni!', 'Ekke Ekke Ekke Ekke Ptang Zoo Boing!', 'Noo']
        self.sound_files = ['ni.wav', 'ekke.wav', 'noo.wav']

        #### Create gui

        self.i_Ni_t_GUI()
        self.Show()

    def i_Ni_t_GUI(self):
        pass
        #### Create and populate menu bar

        # menuBar = wx.MenuBar()
        # fileMenu = wx.Menu()
        # aboutMenu = fileMenu.Append(wx.ID_ANY, "&About")
        # exitMenu = fileMenu.Append(wx.ID_ANY, "&Exit")
        # menuBar.Append(fileMenu, "&File")
        # self.SetMenuBar(menuBar)

        #### Create button and choice controls ####

        # play_button = wx.Button(self, wx.ID_ANY, "play") # pos = (10,10)
        # self.choice_list = wx.Choice(self, choices = self.sound_names) # pos = (10,40)
        # image = wx.StaticBitmap(self, -1, wx.Bitmap("./inc/img.png", wx.BITMAP_TYPE_ANY))

        #### Create and populate sizers

        # main_sizer = wx.BoxSizer(wx.VERTICAL)
        # control_sizer = wx.StaticBoxSizer(wx.HORIZONTAL, self)

        # main_sizer.Add(control_sizer, 0, wx.ALIGN_CENTER, 0)
        # main_sizer.Add(image, 0, wx.ALIGN_CENTER, 0)
        
        # control_sizer.Add(self.choice_list)
        # control_sizer.Add(play_button)

        #### Set Sizer and Show Frame

        # self.SetSizerAndFit(main_sizer)
        # self.Center()


        #### Bind events to callback functions

        # self.Bind(wx.EVT_BUTTON, self.play_sound, play_button)   #### Button Click
        # self.Bind(wx.EVT_CHOICE, self.load_sound, self.choice_list) #### Choice Selection
        # self.Bind(wx.EVT_MENU, self.About, aboutMenu) #### File>About
        # self.Bind(wx.EVT_MENU, self.Quit, exitMenu) #### File>Quit
        # self.Bind(wx.EVT_CLOSE, self.Quit) #### Window close event

        #### Initialize choice and soundfile

        # self.choice_list.SetSelection(0)
        # self.load_sound(None)


    #### Callback function definitions
    #### Note the 'event' input which lets you access info about what event triggered the callback

    #### Callback function for EVT_CHOICE event
    #### Loads selected .wav file 

    def load_sound(self, event):
        selection = self.choice_list.GetCurrentSelection()
        self.filename = "./inc/{}".format(self.sound_files[selection])
        self.sound = wx.adv.Sound(self.filename)
        print('Loaded: ' + self.sound_files[selection])

    #### Callback function for EVT_BUTTON event binded to play_button ###
    #### Plays the audio file
    
    def play_sound(self, event):
        if self.sound.IsOk():
            self.sound.Play(wx.adv.SOUND_ASYNC)
            print('Play')
        else:
            wx.MessageBox("File Load Error", "Error")

    #### Callback for file>about

    def About(self, event):
        text = """
        Rahmat Ashari
        Colin Campbell
        Peter Wang"""
                
        dlg = wx.MessageDialog( self, text, "Knights of Ni! are:", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    #### Callback for window close and file>quit

    def Quit(self, event):
        self.sound = wx.adv.Sound('./inc/shrub.wav')
        if self.sound.IsOk():
            self.sound.Play(wx.adv.SOUND_ASYNC)

        answer = wx.MessageBox("Bring me a shrubbery!!!", "You want to leave?",
                       wx.YES_NO , self)

        if answer == wx.YES:
            #### Close window and end program
            self.Destroy()
        else:
            self.load_sound(None) 

    


if __name__ == '__main__':
    app = wx.App()
    mainFrame(None, title = "Knights of Ni! Demo v.1.0.0")
    app.MainLoop()
