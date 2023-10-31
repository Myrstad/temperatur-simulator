"""
To regulatore `PIDRegulator` som er mer avansert og `AvPåRegulator` som er den enkleste tenkte regulatoren. Lagrer informasjon til `System` klassen
"""

class PIDRegulator(object):
  """
  PID-regulatoren sørger for et system jobber mot en ønsket verdi
  """
  def __init__(self, K_p = 10, K_i = 0.1, K_d = 10) -> None:
    """
    Konstruktør

    K_p: proposjonal- konstant
    K_i: integrals  - konstant
    K_d: derivasjons- konstant

    om K verdien (konstanten) er 0, betyr det at den er nullet ut / ikke gjeldene
    """
    self.K_p = K_p
    self.K_i = K_i
    self.K_d = K_d
    self.forrige_differanse = 0  #også kalt feil dvs. hvor stor feil
    self.integral = 0

  def beregn_output(self, ønsket, faktisk, dt) -> float:
    """
    Tar inn ønsket og faktisk verdi og bruker (lagrede) tidligere
    verdier via self.integral for å prøve å sette ny output skik at
    systemet får riktig ønsket verdi. Bruker forøvrig også P og D ledd.

    Returnerer et output regulatoren mener er riktig output
    """
    differanse = ønsket - faktisk
    self.integral += differanse * dt                       #integral er jo definert som summen av y(t)dt for alle t verdier
    derivert = (differanse - self.forrige_differanse) / dt #dx/dt i dette tilfellet forskjell i temperatur over tid
    
    #lager og summerer PID-leddene
    regulator_output = (self.K_p * differanse) + (self.K_i * self.integral) + (self.K_d * derivert)

    #feilen/differansen brukes til den dervierte
    self.forrige_differanse = differanse
    return regulator_output #brukes f.eks. av varmeelementet

#brukes ikke, men kan enkelt brukes med å bytte ut regulator til denne
class AvPåRegulator(object):
  """
  Av-på-regulator sørget for at et system jobber mot en ønsket verdi på enkleste måte
  brukes ikke, men kan brukes for debugging
  """
  @staticmethod
  def beregn_output(min_effekt, maks_effekt, ønsket, faktisk) -> float|int:
    """
    Metode får å "beregne" effekt, gir maks effekt om lavere enn ønsket temperatur
    mens gir minimal effekt når temperaturen overskrider ønsket temperatur
    """
    if faktisk > ønsket:
      return min_effekt
    return maks_effekt