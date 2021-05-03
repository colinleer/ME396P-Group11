import wx
import matplotlib
import matplotlib.pyplot as plt
from pubsub import pub

matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure

import os
import json

#local imports
import lra_model  

class lra_panel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent = parent)
        self.frame = parent  

        pub.subscribe(self.update_drive_waveform, 'update_waveform_data')

        self.lra_models = []
        self.lra_data = []
        for filename in os.listdir('./lra'):
            if filename.endswith(".lra"):
                path = os.path.join('./lra',filename)
                try:
                    with open(path, 'r') as file:
                        lra_info = json.load(file)
                        self.lra_models.append(lra_info['name'])
                        self.lra_data.append(lra_info)
                        
                    
                except IOError:
                    wx.LogError("something went wrong lol")

        title_text = wx.StaticText(self, label = 'LRA Parameters')

        lra_label = wx.StaticText(self, label = 'Model')
        self.lra_value = wx.Choice(self, choices = self.lra_models)
        self.lra_value.SetSelection(0)
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
        plot_btn.Bind(wx.EVT_BUTTON, self.plot_impedance)
        
        sim_btn = wx.Button(self, label = 'Simulate Response')
        sim_btn.Bind(wx.EVT_BUTTON, self.simulate_response)

        grid = wx.GridSizer(2, 7, 10)

        grid.AddMany([  lra_label, self.lra_value,
                        m_label, self.m_value,
                        Cm_label, self.Cm_value,
                        Rm_label, self.Rm_value, 
                        Le_label, self.Le_value, 
                        Re_label, self.Re_value, 
                        Bl_label, self.Bl_value])     

        coeffToSend = [self.m_value.GetValue(), self.Cm_value.GetValue(), self.Rm_value.GetValue(), self.Le_value.GetValue(), self.Re_value.GetValue(), self.Bl_value.GetValue()]
        pub.sendMessage("LRACoeff", data = coeffToSend)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        main_sizer.Add(title_text)
        main_sizer.Add(grid, 0, wx.TOP, 10)
        main_sizer.Add(plot_btn, 1, wx.TOP | wx.EXPAND, 10)
        main_sizer.Add(sim_btn, 1, wx.TOP | wx.EXPAND, 10)

        self.SetSizer(main_sizer) 



        self.load_lra(None)


    def load_lra(self, evt):
        sel = self.lra_value.GetSelection()

        if sel is not -1:
            self.lra = lra_model.linear_resonant_actuator(self.lra_data[sel])
        else:
            self.lra = test_lra()


        self.m_value.SetValue(str(self.lra.m))
        self.Cm_value.SetValue(str(self.lra.Cm)) 
        self.Rm_value.SetValue(str(self.lra.Rm))
        self.Le_value.SetValue(str(self.lra.Le))
        self.Re_value.SetValue(str(self.lra.Re))
        self.Bl_value.SetValue(str(self.lra.Bl))


    def update_drive_waveform(self, data):
        [time, voltage, low, high] = data
        self.lra.set_driving_function(time, voltage)
        

    def plot_impedance(self, evt):
        data = self.lra.get_impedance_spectrum()

        dlg = ImpedancePlotDialog(data)
        ret = dlg.ShowModal()    
        dlg.Destroy()

    def simulate_response(self, evt):
        
        time, displacement, t_f = self.lra.calculate_response()
        

        dlg = ResponsePlotDialog([time,displacement, t_f])
        ret = dlg.ShowModal()
        dlg.Destroy()

class ImpedancePlotDialog(wx.Dialog):

    def __init__(self, data, title="LRA Model", parent=None):
        wx.Dialog.__init__(self, parent=parent, title=title)
        pnl = wx.Panel(self)
        pnl.SetBackgroundColour('white')

        [freq, Ze] = data

        # Plot 
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)

        self.canvas = FigureCanvas(pnl, -1, self.figure)
        self.axes.grid(alpha = 0.5)

        
        self.figure.set_canvas(self.canvas)
        self.axes.clear()
        self.axes.set_ylabel("Ze (Ohms)")
        self.axes.set_xlabel("Frequency (Hz)")
        self.axes.set_title("LRA Impedance Spectrum")
        self.axes.grid(alpha = 0.5)
        self.axes.loglog( freq, abs(Ze))
        self.canvas.draw()

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.canvas, 0, wx.ALL, 10)
        sizer.Add(self.CreateStdDialogButtonSizer ( wx.OK ), 0, wx.ALIGN_RIGHT)

        sizer.SetSizeHints(self)
        pnl.SetSizerAndFit(sizer)
        self.Center()

class ResponsePlotDialog(wx.Dialog):

    def __init__(self, data, title="LRA Response", parent=None):
        wx.Dialog.__init__(self, parent=parent, title=title)
        pnl = wx.Panel(self)
        pnl.SetBackgroundColour('white')

        [time, disp, t_f] = data

        # Plot 
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)

        self.canvas = FigureCanvas(pnl, -1, self.figure)
        self.axes.grid(alpha = 0.5)

        
        self.figure.set_canvas(self.canvas)
        self.axes.clear()
        self.axes.set_ylabel("Displacement ($\mu$m)")
        self.axes.set_xlabel("Time (ms)")
        self.axes.set_title("LRA Response")
        self.axes.grid(alpha = 0.5)
        self.axes.plot( time * 1e3, disp * 1e6)
        self.axes.axvspan(0, t_f*1000, color='green', alpha=0.25)
        self.canvas.draw()

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.canvas, 0, wx.ALL, 10)
        sizer.Add(self.CreateStdDialogButtonSizer ( wx.OK ), 0, wx.ALIGN_RIGHT)

        # pnl.SetSizer(sizer)
        sizer.SetSizeHints(self)
        pnl.SetSizerAndFit(sizer)
        self.Center()


class LRA_Frame(wx.Frame):
    def __init__(self):

        wx.Frame.__init__(self, None)
        panel = lra_panel(self)
        self.Show()

if __name__ == "__main__":


    app = wx.App(False)
    frame = LRA_Frame()
    app.MainLoop()
