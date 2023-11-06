"""
Lagrer data og bruker pyplot fra matplotlib til å tegne grafer, fra lagret data
"""

import matplotlib.pyplot as plt

class GrafTegner(object):
  """
  Graf tegneren lagrer x og y (evt to stk y) verdier

  Og har metoden for å bruke pyplot til å tegne grafen i en GUI
  """
  def __init__(self, navn) -> None:
    """
    Konstruktør

    navn: brukes til vindu navn (og potensielt samle flere enn 2 grafer i et vindu [tror jeg...])
    """
    self.x_verdier = []
    self.y_verdier = []
    self.y2_verdier= []
    self.navn = navn
  
  def tegn_graf(self):
    """ Metode for å "plotte", men ikke vise selve grafen """
    plt.figure(self.navn)
    plt.plot([x/60**2 for x in self.x_verdier], self.y_verdier)
    if self.y2_verdier != []:
      plt.plot([x/60**2 for x in self.x_verdier], self.y2_verdier, linestyle="dashed", label="Ønsket temperatur")
    plt.grid()
    plt.xlabel('x - tid [time]')
    if self.navn == 'Effekt':
      plt.ylabel('y - effekt [watt]')
    else:
      plt.ylabel('y - temperatur [celcius]')
  
  def reset_data(self):
    self.x_verdier = []
    self.y_verdier = []
    self.y2_verdier= []

  def endre_navn(self, navn):
    self.navn = navn