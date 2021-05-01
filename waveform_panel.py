import wx
from pubsub import pub
import wx.lib.agw.floatspin as FS
import waveform
import numpy as np

# https://www.blog.pythonlibrary.org/2011/01/04/wxpython-wx-listctrl-tips-and-tricks/


class waveform_builder(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent = parent)
        self.frame = parent  
        # self.SetBackgroundColour('red')
        
        self.waves = [] #list of aggregated waveforms
    
        # listbox ctrl
        self.list_ctrl = wx.ListCtrl(self, style=wx.LC_REPORT|wx.BORDER_SUNKEN)
        self.list_ctrl.InsertColumn(0, 'Segment')
        self.list_ctrl.InsertColumn(1, 'Frequency')
        self.list_ctrl.InsertColumn(2, 'Cycles')
        self.list_ctrl.InsertColumn(3, 'Amplitude')
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.select_wvfm)

        #waveform building buttons
        self.wvfm_type = wx.Choice(self, choices = ['sine', 'sinc'])
        self.add_btn = wx.Button(self, label= 'add')
        self.delete_btn = wx.Button(self, label = 'delete')
        self.add_btn.Bind(wx.EVT_BUTTON, self.add_wvfm)
        self.delete_btn.Bind(wx.EVT_BUTTON, self.delete_wvfm)

        title_text = wx.StaticText(self, label = 'Waveform Parameters')

        freq_label = wx.StaticText(self, label = 'Frequency')
        amp_label = wx.StaticText(self, label = 'Amplitude')

        self.freq_spin = FS.FloatSpin(self, -1, min_val=.01, max_val=1000,
                                 increment=1, value=1, agwStyle=FS.FS_LEFT)
        self.freq_spin.SetFormat("%f")
        self.freq_spin.SetDigits(2)
        self.freq_spin.Bind(FS.EVT_FLOATSPIN, self.change_frequency_spin)

        self.amp_spin = FS.FloatSpin(self, -1, min_val=-10, max_val=10,
                                 increment=0.1, value=1, agwStyle=FS.FS_LEFT)
        self.amp_spin.SetFormat("%f")
        self.amp_spin.SetDigits(2)
        self.amp_spin.Bind(FS.EVT_FLOATSPIN, self.change_amplitude_spin)

        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        list_sizer = wx.BoxSizer(wx.VERTICAL)
        control_sizer = wx.BoxSizer(wx.HORIZONTAL)
        parameter_sizer = wx.BoxSizer(wx.VERTICAL)
        parameter_grid = wx.GridSizer(2,2,10)

        control_sizer.Add(self.wvfm_type)
        control_sizer.Add(self.add_btn, 0, wx.LEFT, 5)
        control_sizer.Add(self.delete_btn, 0, wx.LEFT, 5)


        parameter_sizer.Add(title_text, 0, wx.BOTTOM|wx.TOP, 5)
        
        parameter_grid.Add(freq_label)
        parameter_grid.Add(self.freq_spin)
        parameter_grid.Add(amp_label)
        parameter_grid.Add(self.amp_spin)

        parameter_sizer.Add(parameter_grid, 0, wx.TOP, 10)

        list_sizer.Add(control_sizer)
        list_sizer.Add(self.list_ctrl, 1, wx.TOP | wx.EXPAND, 5)
        main_sizer.Add(list_sizer, 1, wx.EXPAND | wx.LEFT, 5)
        main_sizer.Add(parameter_sizer, 0 , wx.LEFT | wx.RIGHT, 60)

        self.SetSizerAndFit(main_sizer)
        pub.subscribe(self.openFile, "sendLoadData")

    def openFile(self, data):
        self.waves = []
        self.list_ctrl.DeleteAllItems()
        loadData = data 
        loadedSegment = loadData["segments"]
        loadFreqList = []
        loadAmpList = []
        for seg in loadedSegment.keys():
            loadFreqList.append(loadedSegment[seg][0])
            loadAmpList.append(loadedSegment[seg][1])

        print(loadAmpList)
        for k in range(len(loadAmpList)):
            index = len(self.waves)
            wvfm = waveform.sine_wave(loadFreqList[k], 0.5, amplitude = loadAmpList[k])
            self.waves.append(wvfm)
            self.list_ctrl.InsertItem(index, 'sine ' + str(index))
            self.list_ctrl.SetItem(index, 1, str(wvfm.f))
            self.list_ctrl.SetItem(index, 2, str(wvfm.n))
            self.list_ctrl.SetItem(index, 3, str(wvfm.a))
            
        self.update_wfvm_data()


    def build_wvfm(self):
        self.indexedWaves = []
        time = np.empty(1)
        data = np.empty(1)
        sign = 1

        for wave in self.waves:
            print(wave)
            [t, v] = wave.get_data()
            [freqGathered, ampGathered] = wave.getDataExtra()
            addTime = np.array(t + time[-1]) * 1000
            addMagnitude = np.array(sign * v)
            self.indexedWaves.append([freqGathered, ampGathered, addTime, addMagnitude])
            time = np.append(time, t + time[-1])
            data = np.append(data, v * sign)
            sign *= -1
        
        return time, data

    def add_wvfm(self, evt):
        index = len(self.waves)
        wvfm = waveform.sine_wave(150, 0.5)
        self.waves.append(wvfm)
        self.list_ctrl.InsertItem(index, 'sine ' + str(index))
        self.list_ctrl.SetItem(index, 1, str(wvfm.f))
        self.list_ctrl.SetItem(index, 2, str(wvfm.n))
        self.list_ctrl.SetItem(index, 3, str(wvfm.a))
        self.update_wfvm_data()
    
    def delete_wvfm(self, evt):
        item = self.list_ctrl.GetFirstSelected()
        self.waves.pop(item)
        self.list_ctrl.DeleteItem(item)
        self.update_wfvm_data() 

    def update_wfvm_data(self):
        [time, data ] = self.build_wvfm()
        waveSegment = {}
        for idx, wave in enumerate(self.indexedWaves):
            waveSegment["segment {}".format(idx)] = [wave[0], wave[1], wave[2].tolist(), wave[3].tolist()]
        pub.sendMessage("update_waveform_data", data = [time*1000, data])
        pub.sendMessage("waveSegmentData", data = waveSegment)

    def select_wvfm(self, evt):
        index = evt.GetIndex()
        wvfm = self.waves[index]
        self.freq_spin.SetValue(wvfm.f)
        self.amp_spin.SetValue(wvfm.a)

    def change_frequency_spin(self, evt):
        val = self.freq_spin.GetValue()
        index = self.list_ctrl.GetFirstSelected()
        wvfm = self.waves[index]
        wvfm.f = val
        wvfm.calculate()
        self.waves[index] = wvfm
        self.list_ctrl.SetItem(index, 1, str(wvfm.f))
        self.update_wfvm_data()

    def change_amplitude_spin(self, evt):
        val = self.amp_spin.GetValue()
        index = self.list_ctrl.GetFirstSelected()
        wvfm = self.waves[index]
        wvfm.a = val
        wvfm.calculate()
        self.waves[index] = wvfm
        self.list_ctrl.SetItem(index, 3, str(wvfm.a))
        self.update_wfvm_data()

class TestFrame(wx.Frame):
    def __init__(self):

        wx.Frame.__init__(self, None)
        panel = waveform_builder(self)
        self.Show()

if __name__ == "__main__":

    app = wx.App(False)
    frame = TestFrame()
    app.MainLoop()
