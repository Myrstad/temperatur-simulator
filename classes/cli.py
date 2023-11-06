"""
Kommandolinjebasert grensernitt (CLI) som lar brukeren selv styre systemet, som å vise/skjule grafer samt simulere
"""

import matplotlib.pyplot as plt
from .simulator import Simulator

class CLI(object):
  """
  Kommandolinjebasert brukergrensersnitt for simulasjonen av systemet
  """
  HJELP_MELD = 'avslutt: eller s/slutt for å avslutte\nhjelp: eller h/info for denne dialogen\nsimuler: eller s/sim for å simulere en periode\nvis: eller graf/v viser graf(er)\nskjul: eller lukk/l lukker graf(ene)\nreset: eller klarer/k/clear fjerner graf-linjen(e)\ninstillinger: eller i/settings for å endre på varibler til simulasjonen'
  VELKOMMEN_MELD = 'Velkommen til CLI-verktøyet for temperatur simulasjonen til Myrstad.\nSkriv `q`  eller `quit` for å gå ut av CLI-et.\nSkriv `hjelp` for informasjon om programmet\nSkriv `sim` for å starte\n'
  SLUTT_MELD = 'Ferdig å kjøre programmet, avslutter'
  SIMULER_MELD = 'Skriv inn informasjon for simulasjonen:'
  SIMULER_ETTER_MELD = 'Skriv `graf` eller `vis` for å vise fram grafen'
  VIS_MELD = 'Viser graf(er) i eget vindu'
  LUKK_MELD = 'Lukker graf(ene) fra pyplot'
  KLARER_MELD = 'Fjerner data for graftegneren, lag en ny simulasjon får å vise fram noe'
  INGEN_KOMMANDO_MELD = 'Kommandoen finnes ikke, skriv `hjelp` om du sitter fast'
  INSTILLINGER_MELD = 'Forskjellige ting kan endres ved behov, ja/nei er svar hvor første er standardverdi om du ikke taster inn noe'

  def __init__(self) -> None:
    """ Kontruktør """
    self.simulasjon = Simulator()
    self.første_gang = True
    plt.ion()
    plt.close()
  
  def hent_boolsk(self, default=False, melding = '?') -> bool:
    """ For å spørre brukeren spørsmålet ønsker du x svar Y/n """
    ferdig = False
    while not ferdig:
      innputt = input(melding).strip().lower()
      if innputt in ['ja', 'j', 'y', '1']:
        return True
      if innputt in ['nei', 'n']:
        return False
      if innputt == '' or innputt == None:
        return default
      print('Prøv på nytt, svar `ja` eller `nei`')

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
        print(f'Prøv igjen, er ikke gjøres om til typen {typ}')

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
      
      elif kommando in ['i', 'instillinger', 'settings']:
        print(CLI.INSTILLINGER_MELD)
        endre_rommet = self.hent_boolsk(False, 'Ønsker du å endre på rommets dimensjoner (nei/ja)? ')
        if endre_rommet:
          print(f'Dimensjoner er per nå, {self.simulasjon.rom.dimemsjoner}')
          print('Instillinger for rommets dimensjoner:')
          l = self.hent_input(melding='(tall) lengde? ')
          b = self.hent_input(melding='(tall) bredde? ')
          d = self.hent_input(melding='(tall) dybde? ')
          self.simulasjon.endre_rommet(dimensjon=(l,b,d))
        endre_regulator = self.hent_boolsk(False, 'Ønsker å endre på regulatorens konstanter (nei/ja)? ')
        if endre_regulator:

          print(f'Regulatorens ledd per nå, (P,I,D) =  {self.simulasjon.regulator.K_p, self.simulasjon.regulator.K_i, self.simulasjon.regulator.K_d}')
          print('Instillinger for regulatores PID-ledd:')
          p = self.hent_input(melding='(tall) p-ledd? ')
          i = self.hent_input(melding='(tall) i-ledd? ')
          d = self.hent_input(melding='(tall) d-ledd? ')
          self.simulasjon.endre_regulatoren(Kp=p, Ki=i, Kd=d)
        endre_varmeelement = self.hent_boolsk(False, 'Ønsker du å endre på regulatorens effekt (nei/ja)? ')
        if endre_varmeelement:
          print(f'Varmeelements minimum effekt per nå er {self.simulasjon.varme_element.minimum_effekt}W og maksimum {self.simulasjon.varme_element.maksimum_effekt}W per nå')
          print('Instillinger for varmeelementet:')
          min_watt = self.hent_input(melding='(tall) minimum effekt? ')
          maks_watt = self.hent_input(melding='(tall) maksimum effekt? ')
          self.simulasjon.endre_varmeelement(min_effekt=min_watt, maks_effekt=maks_watt)

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