"""
Superklasse av `System()` som simulerer systemet, med nødvendige funksjoner også de arvede
"""

from .system import System
from .graftegner import GrafTegner

class Simulator(System):
  """
  Simulatoren er superklasse av klassen `System`, som betyr den har all informasjon, og metoder som `System` klassen

  Simulatoren brukes til (duh...) å simulere systemet over tid

  Metodene er generelle, så ALLE variabler lenger ned i strukturen kan endres og fortsatt fungere i denne klassen. 
  Metodene er de som faktisk simulerer hele systemet, med regulator, varmetap og alt.
  """
  def __init__(self) -> None:
    """
    Konstruktør og init (initialize/oppstart) av System-subklassen
    """
    super().__init__()
    self.tid = 0 #sekunder, brukes kun for plotting (sørger for ingen overlapp mellom forskjellige simulasjoner til `simuler()`)
    self.temperatur_graf = GrafTegner('Temperatur')
    self.effekt_graf = GrafTegner('Effekt')

  def simuler_tidssteg(self, tid):
    """ Simulerer varmeendring i en gitt tidsperiode, der variablene ikke endres """
    Q_varmetap = self.rom.varmeoverførings_koeffisient * self.rom.areal() * (self.rom.temperatur - self.rom.ute_temperatur) * tid
    Q_effekt = self.varme_element.effekt * tid
    forskjell_Q = Q_effekt - Q_varmetap
    forskjell_temperatur = forskjell_Q / (self.rom.masse() * self.rom.varmekapasitet_luft)
    self.rom.temperatur += forskjell_temperatur
    # print(f'Δtemp: {forskjell_temperatur:.3f}, temp: {self.rom.temperatur:.3f}, ønsket temp: {self.rom.ønsket_temperatur}, ute temp: {self.rom.ute_temperatur}')

  def simuler(self, tids_intervall, total_tid):
    """
    Simulerer systemet over tid
    
    Bruker mindre tidsintervaller får at regulatoren kan fungere, og fremme mer realistiske verdier
    """
    #sikre idioti
    tids_intervall = abs(tids_intervall)
    total_tid = abs(total_tid)
    # "intern" tid som kun brukes for å stoppe while løkken etter den totale tiden er gått
    simulerings_tid = 0
    while simulerings_tid < total_tid:
      #henter og bruker regulator outputen, samt simulerer tidssteget til neste iterasjon av løkken
      regulator_output = self.regulator.beregn_output(self.hent_ønsket_temperatur(), self.hent_temperatur(), tids_intervall)
      self.sett_effekt(regulator_output)
      self.simuler_tidssteg(tids_intervall)
      
      #legge til data til graftegner(e)
      self.temperatur_graf.x_verdier.append(self.tid)
      self.temperatur_graf.y_verdier.append(self.hent_temperatur())
      self.temperatur_graf.y2_verdier.append(self.hent_ønsket_temperatur())
      self.effekt_graf.x_verdier.append(self.tid)
      self.effekt_graf.y_verdier.append(self.varme_element.effekt)

      #endre tid for loop og klasse
      simulerings_tid += tids_intervall
      self.tid        += tids_intervall