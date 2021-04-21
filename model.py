import numpy as np
import matplotlib.pyplot as plt

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

        


class test_lra(mass_spring_damper):

    def __init__(self):
        self.parameters = { 'm': 1.61e-3, 
                            'Cm': .0003,
                            'Rm': .001,
                            'Bl': 1.12,
                            'Re': 4.3,
                            'Le': 0.1e-3
                            }
        super().__init__(self.parameters)




if __name__ == "__main__":
    lra = test_lra()
    [freq,Z] = lra.get_impedance_spectrum()
    fig, ax = plt.subplots(1)
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Ze (ohms)')

    line1, = ax.loglog(freq, abs(Z), label='LRA')
    plt.show()