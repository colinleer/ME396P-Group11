import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint


class mass_spring_damper():

    def __init__(self, parameters):
        self.m = parameters.get('m', 1)
        self.Cm = parameters.get('Cm', 1)
        self.Rm = parameters.get('Rm', 1)
        self.Bl = parameters.get('Bl', 1)
        self.Re = parameters.get('Re', 1)
        self.Le = parameters.get('Le', 1)



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

    def get_resonance(self):
        pass
    
    def force(self, t):
        if t<.010:
            return np.sin(2*np.pi*150*t)
        else:
            return 0

    def lra_system(self, x, t):

        xd0 = x[1] # x' = v
        xd1 = ( self.force(t) - x[1]*self.Rm - x[0]/self.Cm ) / self.m
        return [xd0, xd1]

    def calculate_response(self):
        x_0 = [0,0]
        t = np.linspace(0, .5, 10000)

        x = odeint(self.lra_system, x_0, t)

        disp = x[:,0]
        vel = x[:,1]

        fig, ax = plt.subplots(1)
        ax2 = ax.twinx()
        ax.set_xlabel('time')
        ax.set_ylabel('x')

        ax.plot(t, disp, 'b-', label='x')
        ax2.plot(t, vel, 'g-', label='v')
        ax.legend()
        ax2.legend(loc='lower right')
        plt.show()


        


class jahwa_j6(mass_spring_damper):

    def __init__(self):
        self.parameters = { 'm': 1.61e-3, 
                            'Cm': .0003,
                            'Rm': .11,
                            'Bl': 1.12,
                            'Re': 9,
                            'Le': 0.1e-3
                            }
        super().__init__(self.parameters)

class nidec_sprinter_r(mass_spring_damper):

    def __init__(self):
        self.parameters = { 'm': 2.54e-3, 
                            'Cm': .0006,
                            'Rm': .004,
                            'Bl': .92,
                            'Re': 15,
                            'Le': 0.1e-3
                            }
        super().__init__(self.parameters)

class test_lra(mass_spring_damper):

    def __init__(self):
        self.parameters = { 'm': 20, 
                            'Cm': 1/2,
                            'Rm': 4,
                            'Bl': .92,
                            'Re': 15,
                            'Le': 0.1e-3
                            }
        super().__init__(self.parameters)


if __name__ == "__main__":
    lra = jahwa_j6()
    lra.calculate_response()
    # [freq,Z] = lra.get_impedance_spectrum()


