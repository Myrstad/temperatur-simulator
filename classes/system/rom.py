"""
Har `Rom` klassen som lagrer variabler til `System` om info om rommet
"""

class Rom(object):
  """
  Holder all informasjonen om rommet som blir brukt selv og av andre klasser

  Informasjon som
   * dimensjoner, dvs. lengde, høyde, dybde
   * temperaturer, i celcius [C]
   * areal(), volum() og masse() som metoder
  """
  def __init__(self, dimensjoner = (5,6,1), start_temperatur = 10, ute_temperatur = 4, ønsket_temperatur = 20) -> None:
    """
    Konstruktør

    * `dimensjoner`:        - 3 posetive numeriske verdier
    * `start_temperatur`:   - rimelig tallverdi eks. [-50, 50]
    * `ute_temperatur`:     - rimelig tallverdi eks. [-30, 30]
    * `ønsket_temperatur`:  - rimelig tallverdi eks. [0,   30]
    
    """
    self.lufttetthet = 1.2                  #kg/m³
    self.varmeoverførings_koeffisient = 0.5 #W/(m²·K)
    self.varmekapasitet_luft = 1005         #J/(kg·°C)
    self.dimemsjoner = dimensjoner          #[s,s,s] (s-strekning[meter])
    
    #temperraturer i grader celcius [C]
    self.temperatur = start_temperatur
    self.ute_temperatur = ute_temperatur
    self.ønsket_temperatur = ønsket_temperatur
  
  def volum(self) -> float|int:
    """ Regner og returner antall kubikkmeter [m³] i rommet """
    l,h,b = self.dimemsjoner
    return l * h * b
  
  def areal(self) -> float|int:
    """ Regner og returner overflaten i rommet i kvadratmeter [m²] """
    l,h,b = self.dimemsjoner
    return 2*l*h + 2*l*b + 2*h*b
  
  def masse(self) -> float:
    """ Regner og returner massen [kg] til luften i rommet """
    return self.volum() * self.lufttetthet