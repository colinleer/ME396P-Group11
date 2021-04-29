import wx
import matplotlib.pyplot as plt
#local imports
import lra_model  

class lra_panel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent = parent)
        self.frame = parent  
        # self.SetBackgroundColour('blue')

        self.lra_models = ['Jawha J6', 'Nidec Sprinter R']

        title_text = wx.StaticText(self, label = 'LRA Parameters')

        lra_label = wx.StaticText(self, label = 'Model')
        self.lra_value = wx.Choice(self, choices = self.lra_models)
        self.lra_value.Bind(wx.EVT_CHOICE, self.load_lra)

        m_label = wx.StaticText(self, label = 'Mass')
        self.m_value = wx.TextCtrl(self, style = wx.TE_READONLY)

        Cm_label = wx.StaticText(self, label = 'Compliance')
        self.Cm_value = wx.TextCtrl(self, style = wx.TE_READONLY)

        Rm_label = wx.StaticText(self, label = 'Damping')
        self.Rm_value = wx.TextCtrl(self, style = wx.TE_READONLY)

        Le_label = wx.StaticText(self, label = 'Inductance')
        self.Le_value = wx.TextCtrl(self, style = wx.TE_READONLY)

        Re_label = wx.StaticText(self, label = 'Resistance')
        self.Re_value = wx.TextCtrl(self, style = wx.TE_READONLY)

        Bl_label = wx.StaticText(self, label = 'Sensitivity')
        self.Bl_value = wx.TextCtrl(self, style = wx.TE_READONLY)

        plot_btn = wx.Button(self, label = 'Plot Model')
        plot_btn.Bind(wx.EVT_BUTTON, self.plot_response)
        
        sim_btn = wx.Button(self, label = 'Simulate Response')

        grid = wx.GridSizer(2, 7, 10)

        grid.AddMany([  lra_label, self.lra_value,
                        m_label, self.m_value,
                        Cm_label, self.Cm_value,
                        Rm_label, self.Rm_value, 
                        Le_label, self.Le_value, 
                        Re_label, self.Re_value, 
                        Bl_label, self.Bl_value])     

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        main_sizer.Add(title_text)
        main_sizer.Add(grid, 0, wx.TOP, 10)
        main_sizer.Add(plot_btn, 1, wx.TOP | wx.EXPAND, 10)
        main_sizer.Add(sim_btn, 1, wx.TOP | wx.EXPAND, 10)

        self.SetSizer(main_sizer) 

        self.load_lra(None)


    def load_lra(self, evt):
        name = self.lra_models[self.lra_value.GetSelection()]

        if name == 'Jawha J6':
            self.lra = lra_model.jahwa_j6()
        elif name == 'Nidec Sprinter R':
            self.lra = lra_model.nidec_sprinter_r()


        self.m_value.SetValue(str(self.lra.m))
        self.Cm_value.SetValue(str(self.lra.Cm)) 
        self.Rm_value.SetValue(str(self.lra.Rm))
        self.Le_value.SetValue(str(self.lra.Le))
        self.Re_value.SetValue(str(self.lra.Re))
        self.Bl_value.SetValue(str(self.lra.Bl))

    def plot_response(self, evt):
        [freq,Z] = self.lra.get_impedance_spectrum()
        fig, ax = plt.subplots(1)
        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Ze (ohms)')

        line1, = ax.loglog(freq, abs(Z), label='LRA')
        plt.show()



class LRA_Frame(wx.Frame):
    def __init__(self):

        wx.Frame.__init__(self, None)
        panel = lra_panel(self)
        self.Show()

if __name__ == "__main__":


    app = wx.App(False)
    frame = LRA_Frame()
    app.MainLoop()