"""
Kommandolinjebasert grensernitt (CLI) som lar brukeren selv styre systemet, som å vise/skjule grafer samt simulere
"""

import matplotlib.pyplot as plt
from .simulator import Simulator

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