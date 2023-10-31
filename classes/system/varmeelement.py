"""
Har `VarmeElement` klassen som lagrer variabler til `System` om info om varmeelementet
"""

class VarmeElement(object):
  """
  Har informasjonen om varmeelementet, som effekt, min-max effekt og en metode for å sette effekten innenfor min og max

  Kjekt å vite at negativ minimum effekt betyr i praksis air-conditioning
  """
  def __init__(self, minimum_effekt = 0, maksimum_effekt = 1000) -> None:
    """
    Konstruktør

    Setter effekt, minimums og maksimums effekt, alle i watt[W]
    """
    self.minimum_effekt = minimum_effekt
    self.maksimum_effekt = maksimum_effekt
    self.effekt = 0

  def sett_effekt(self, watt) -> None:
    """ Metode for å sette effekten til varmeelementet, holder effekten automatisk innenfor min-max omerådet """
    self.effekt = watt
    if watt > self.maksimum_effekt:
      self.effekt = self.maksimum_effekt
    if watt < self.minimum_effekt:
      self.effekt = self.minimum_effekt