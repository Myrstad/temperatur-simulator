import matplotlib.pyplot as plt

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
      plt.plot([x/60**2 for x in self.x_verdier], self.y2_verdier, linestyle="dashed")
    plt.grid()

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

class CLI(object):
  """
  Kommandolinjebasert brukergrensersnitt for simulasjonen av systemet
  """
  HJELP_MELD = 'avslutt: eller s/slutt for å avslutte\nhjelp: eller h/info for denne dialogen\nsimuler: eller s/sim for å simulere en periode\nvis: eller graf/v viser graf(er)\nskjul: eller lukk/l lukker graf(ene)\nreset: eller klarer/k/clear fjerner graf-linjen(e)'
  VELKOMMEN_MELD = 'Velkommen til CLI-verktøyet for temperatur simulasjonen til Myrstad.\nSkriv `q`  eller `quit` for å gå ut av CLI-et.\nSkriv `hjelp` for informasjon om programmet\nSkriv `sim` for å starte\n'
  SLUTT_MELD = 'Ferdig å kjøre programmet, avslutter'
  SIMULER_MELD = 'Skriv inn informasjon for simulasjonen:'
  SIMULER_ETTER_MELD = 'Skriv `graf` eller `vis` for å vise fram grafen'
  VIS_MELD = 'Viser graf(er) i eget vindu'
  LUKK_MELD = 'Lukker graf(ene) fra pyplot'
  KLARER_MELD = 'Fjerner data for graftegneren, lag en ny simulasjon får å vise fram noe'
  INGEN_KOMMANDO_MELD = 'Kommandoen finnes ikke, skriv `hjelp` om du sitter fast'

  def __init__(self) -> None:
    """ Kontruktør """
    self.simulasjon = Simulator()
    self.første_gang = True
    plt.ion()
    plt.close()
    pass

  def hent_input(self, typ = float, melding = '?') -> type:
    """ Sørger for at input() metoden henter riktig datatype """
    ferdig = False
    verdi = None
    while not ferdig:
      try:
        inp = input(melding)
        verdi = typ(inp)
        ferdig = True
      except:
        print(f'Prøv igjen, er ikke type {typ}')

    return verdi
  
  def hoved_loop(self):
    """ Løkke for selve hovedprogrammet """
    while True:
      if self.første_gang:
        self.første_gang = False
        print(CLI.VELKOMMEN_MELD)
      
      kommando = input('kommando? ').strip().lower()

      if kommando in ['h', 'hjelp', 'info']:
        print(CLI.HJELP_MELD)
      
      elif kommando in ['q', 'quit', 'exit', 'slutt', 'avslutt']:
        print(CLI.SLUTT_MELD)
        break
      
      elif kommando in ['instillinger', 'settings']:
        print('ikke implementert enda')

      elif kommando in ['s', 'sim', 'simuler']:
        print(CLI.SIMULER_MELD)
        start_temp = self.hent_input(float, 'Start temperatur? ')
        ønsket_temp = self.hent_input(float, 'Ønsket temperatur? ')
        ute_temp = self.hent_input(float, 'Ute temperaturen? ')
        tid = self.hent_input(float, 'Hvor mange timer skal simuleres? ') * 60**2
        dt = self.hent_input(float, 'Tidsintervall (anbefalt 60) i sekunder? ')
        self.simulasjon.endre_rommet(
          temperatur=start_temp,
          ute_temperatur=ute_temp,
          ønsket_temperatur=ønsket_temp,
        )
        self.simulasjon.simuler(dt, tid)
        print(CLI.SIMULER_ETTER_MELD)

      elif kommando in ['v', 'vis', 'graf']:
        print(CLI.VIS_MELD)
        self.simulasjon.temperatur_graf.tegn_graf()
        self.simulasjon.effekt_graf.tegn_graf()
      
      elif kommando in ['l', 'lukk', 'skjul']:
        print(CLI.LUKK_MELD)
        plt.close('all')

      elif kommando in ['k', 'klarer', 'clear', 'reset']:
        print(CLI.KLARER_MELD)
        self.simulasjon.regulator.integral = 0
        for graf in [self.simulasjon.effekt_graf, self.simulasjon.temperatur_graf]:
          graf.x_verdier = []
          graf.y_verdier = []
          graf.y2_verdier = []
        plt.close('all')

      else:
        print(CLI.INGEN_KOMMANDO_MELD)
      print()

if __name__ == '__main__':
  # sim = Simulator()
  # sim.sett_ønsket_temperatur(18)
  # sim.simuler(60, 60*180)
  # sim.sett_ønsket_temperatur(22)
  # sim.simuler(60, 60*180)
  # sim.sett_ønsket_temperatur(16)
  # sim.simuler(60, 60*180)
  # sim.temperatur_graf.tegn_graf()
  # sim.effekt_graf.tegn_graf()
  # sim.endre_regulatoren(Kp=1000)
  cli = CLI()
  cli.hoved_loop()