import matplotlib.pyplot as plt

class Regulator:
  def __init__(self) -> None:
    pass

class VarmeElement:
  def __init__(self) -> None:
    self.effekt = 0         # effekten nå i watt
    self.min_effekt = 1000 # watt
    self.maks_effekt = 1000 # watt


class System:
  def __init__(self) -> None:
    self.start_temperatur = 4
    self.basis_temperatur = 4  # ute temperatur
    self.ønsket_temperatur = 20
    self.nå_temperatur = int(self.start_temperatur)
    self.rom_dimensjoner = (5,6,1) #høyde, bredde, dybde i meter
    self.min_effekt = 0     #W
    self.maks_effekt = 1000 #W
    self.effekt = 0         #W
  
    #varibler for fysikk
    self.rom_varmeoverføring = 0.5  #W/(m²·K)
    self.rom_luft_tetthet = 1.2     #kg/m³
    self.rom_luft_varmekapasitet = 1005 #J/(kg·°C)
    l, b, d = self.rom_dimensjoner
    self.rom_volum = l*b*d
    self.rom_areal = 2*(l*b) + 2*(l*d) + 2*(d*b)

    #variabler for regulator
    self.integral = 0

    #plotting
    self.xs = []
    self.Ws = []
    self.ys = []
    self.øys= []
    self.tid = 0


  def sett_ønsket_temperatur(self, temperatur):
    self.ønsket_temperatur = temperatur

  def sett_varmeffekt(self, watt):
    self.effekt = watt

  def simuler_tidssteg(self, delta_tid):
    Q_varmetap = self.rom_varmeoverføring * self.rom_areal * (self.nå_temperatur - self.basis_temperatur) * delta_tid
    Q_effekt = self.effekt * delta_tid
    dQ = Q_effekt - Q_varmetap
    dT = dQ / (self.rom_volum * self.rom_luft_tetthet * self.rom_luft_varmekapasitet)
    self.nå_temperatur += dT
    print(f'Δtemp: {dT:.3f}, temp: {self.nå_temperatur:.3f}, med {self.effekt:0>4} Watt i {delta_tid} sek')

  def simuler(self, tids_intervall, total_tid):
    tid = 0
    while tid < total_tid:
      # self.effekt = self.PI_regulator(tids_intervall)
      # self.effekt = self.av_på_regulator()
      self.effekt = 1000
      self.simuler_tidssteg(tids_intervall)
      self.xs.append(self.tid)
      self.ys.append(self.nå_temperatur)
      self.øys.append(self.ønsket_temperatur)
      self.Ws.append(self.effekt)
      tid+=tids_intervall
      self.tid+=tids_intervall
  
  def av_på_regulator(self) -> float:
    if self.nå_temperatur > self.ønsket_temperatur:
      return self.min_effekt
    else:
      return self.maks_effekt
  
  def PI_regulator(self, dt) -> float:
    watt = self.i_ledd(dt) + self.p_ledd()
    if watt > self.maks_effekt:
      return self.maks_effekt
    if watt < self.min_effekt:
      return self.min_effekt
    return watt

  def i_ledd(self, dt) -> float:
    differanse = self.ønsket_temperatur - self.nå_temperatur
    u_i = 1
    self.integral += differanse * dt
    watt = self.integral * u_i
    return watt

  def p_ledd(self) -> float:
    differanse = self.ønsket_temperatur - self.nå_temperatur
    u_p = 100
    watt = differanse * u_p
    return watt
  
  def d_ledd(self) -> float:
    pass
      

if __name__ == '__main__':
  plt.figure(0)
  s = System()
  s.sett_varmeffekt(1000)
  s.sett_ønsket_temperatur(22)
  s.simuler(60, 60*180)
  s.sett_ønsket_temperatur(15)
  s.simuler(60, 60*180)
  plt.plot(s.xs, s.ys)
  plt.plot(s.xs, s.øys)
  plt.figure(1)
  plt.plot(s.xs, s.Ws)
  plt.show()
  pass