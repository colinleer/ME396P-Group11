import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import json


class linear_resonant_actuator():

    def __init__(self, parameters):
        self.m = parameters.get('m', 1)
        self.Cm = parameters.get('Cm', 1)
        self.Rm = parameters.get('Rm', 1)
        self.Bl = parameters.get('Bl', 1)
        self.Re = parameters.get('Re', 1)
        self.Le = parameters.get('Le', 1)

        self.drive_t = np.array([])
        self.drive_v = np.array([])



    def get_impedance_spectrum(self):
        #define freq range
        f = np.logspace(1,4,1000) 
        om = 2*np.pi*f

        Vin = 1

        #define impedances
        Zm = 1j * om * self.m
        Zc = (1j * om * self.Cm)**-1
        Zr = self.Rm

        Zmech = Zm + Zc + Zr
        Ze = self.Re + 1j*om*self.Le + self.Bl**2 / Zmech

        return f, Ze
    
    def force(self, t):
        if t< np.amax(self.drive_t):
            V = np.interp(t, self.drive_t, self.drive_v)
            tau = self.Le / self.Re 
            I = (V / self.Re) * (1 - np.exp(-t/tau))
            F = self.Bl * I
            return F
        else:
            return 0

    def lra_system(self, x, t):

        xd0 = x[1] # x' = v
        xd1 = ( self.force(t) - x[1]*self.Rm - x[0]/self.Cm ) / self.m
        return [xd0, xd1]

    def calculate_response(self, time, voltage):
        x_0 = [0,0]
        self.drive_t = time/1000
        self.drive_v = voltage
        t_f = np.amax(self.drive_t)
        t = np.linspace(0, 5*t_f, 10000)

        x = odeint(self.lra_system, x_0, t)

        disp = x[:,0]
        vel = x[:,1]

        return t, disp, t_f


    

class test_lra(linear_resonant_actuator):

    def __init__(self):
        self.parameters = { 'm': 2.61e-3, 
                            'Cm': .0005,
                            'Rm': .25,
                            'Bl': 2,
                            'Re': 6,
                            'Le': 0.1e-3, 
                            'name': 'Test LRA'
                            }
        super().__init__(self.parameters)


if __name__ == "__main__":
    lra = test_lra()
    lra.calculate_response()
    
    fig, ax = plt.subplots(1)
    ax2 = ax.twinx()
    ax.set_xlabel('Time')
    ax.set_ylabel('Displacement')

    ax.plot(t, disp, 'b-', label='x')
    ax2.plot(t, vel, 'g-', label='v')
    ax.legend()
    ax2.legend(loc='lower right')
    plt.show()


