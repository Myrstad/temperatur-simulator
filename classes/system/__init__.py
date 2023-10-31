"""
Her samles alt som trenger får å danne et system, altså en regulator, et varmeelement og et rom. Til én klasse `System`
"""

from .regulators import PIDRegulator
from .varmeelement import VarmeElement
from .rom import Rom

class System(object):
  """
  Systemet samler alle klassene på et sted, så de kan settes sammen og hente informasjon fra hverandre via System klassen 

  Har også noen metoder får å sette/hente forskjellig informasjon som er nyttig som enkelt metoder

  Metode for å endre alt innenfor rom og varmeelement, på en måte en 'instillinger' metode
  """
  def __init__(self) -> None:
    self.regulator = PIDRegulator()
    self.varme_element = VarmeElement()
    self.rom = Rom()
  
  def sett_ønsket_temperatur(self, temperatur: float|int) -> None:
    self.rom.ønsket_temperatur = temperatur

  def hent_ønsket_temperatur(self) -> float|int:
    return self.rom.ønsket_temperatur
  
  def hent_temperatur(self) -> float|int:
    return self.rom.temperatur

  def sett_effekt(self, watt: float|int) -> None:
    self.varme_element.sett_effekt(watt)

  def endre_rommet(self, *, dimensjon = None, temperatur = None, ønsket_temperatur = None, ute_temperatur = None, varmeoverførings_koeffisient = None, varmekapasitet_luft = None, lufttetthet = None):
    """
    endre rommet sine variabler i simulatoren
    
    eks. bruk: `endre_rommet(ute_temperatur=10)` merk at du må bruke keywordargument f(x=2), ikke lov med f(2) samt at trenger bare å endre de du trenger å endre og ikke alle
    """
    if dimensjon: self.rom.dimemsjoner = dimensjon
    if ønsket_temperatur: self.rom.ønsket_temperatur = ønsket_temperatur
    if temperatur: self.rom.temperatur = temperatur #kan brukes får å sette start temperatur i starten
    if ute_temperatur: self.rom.ute_temperatur = ute_temperatur
    
    #konstanter som ikke trengs å endres, men som kan får å teste forskjellige egenskaper
    if varmeoverførings_koeffisient: self.rom.varmeoverførings_koeffisient = varmeoverførings_koeffisient
    if varmekapasitet_luft: self.rom.varmekapasitet_luft = varmekapasitet_luft
    if lufttetthet: self.rom.lufttetthet = lufttetthet

  def endre_varmeelement(self, *, min_effekt = None, maks_effekt = None) -> None:
    """ endre varmeelement variabler """
    if min_effekt: self.varme_element.minimum_effekt = min_effekt
    if maks_effekt: self.varme_element.maksimum_effekt = maks_effekt

  def endre_regulatoren(self, *, Kp = None, Ki = None, Kd = None) -> None:
    """ endre regulatorens variabler """
    if type(self.regulator) == PIDRegulator:
      if Kp: self.regulator.K_p = Kp
      if Ki: self.regulator.K_i = Ki
      if Kd: self.regulator.K_d = Kd