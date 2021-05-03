import numpy as np
import matplotlib.pyplot as plt


class waveform():
    def __init__(self, frequency, num_cycles):
        
        self.id = id(self)
        self.f = frequency
        self.t = np.linspace(0, num_cycles/self.f, 10) #ms
        self.v = np.full(len(self.t), 1)
        self.a = 1
        self.t_0 = 0
        self.n = num_cycles
        
        
    def calculate(self):
        pass
    
    def get_data(self):
        return self.t, self.v

    def getDataExtra(self):
        return self.f, self.a
    
    def get_value(time):
        val = np.interp(time, self.t, self.v)
        return val

class sinc_wave(waveform):
    def __init__(self, frequency, num_cycles):
        super().__init__(frequency, num_cycles)
        self.calculate()
        
    
    def calculate(self):
        self.t = np.linspace(0, self.n/self.f, 1000) #ms
        self.t_0 = np.median(self.t)
        # print(self.f)
        self.v = self.a * np.sin(2 * np.pi * self.f * (self.t - self.t_0 )) / (2* np.pi * (self.t  - self.t_0))


class sine_wave(waveform):
    def __init__(self, frequency, num_cycles, amplitude = 1):
        super().__init__(frequency, num_cycles)
        self.a = amplitude
        self.calculate()
        # print(self.v)
    
    def calculate(self):
        self.t = np.linspace(0, self.n/self.f, 1000) #ms
        self.v = self.a * np.sin(2* np.pi * self.f * (self.t - self.t_0)) 




# if __name__ == "__main__":
    # sinc = sinc_wave(100, 2)
    # sine1 = sine_wave(100, .5)
    # sine2 = sine_wave(30, .5)
    # sine3 = sine_wave(250, .5)

    # waves = [sine1, sine2, sine3, sinc]
    


    # fig, ax = plt.subplots(1)
    # ax.set_xlabel('Time (s)')
    # ax.set_ylabel('Voltage (V)')

    # # line1, = ax.plot(sinc.get_data()[0], sinc.get_data()[1], label='sinc')
    # line2, = ax.plot(calculate_wvfm(waves)[0], calculate_wvfm(waves)[1], label='sine')
    
    # ax.legend()
    # plt.show()
