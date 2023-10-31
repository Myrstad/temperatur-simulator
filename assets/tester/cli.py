import matplotlib.pyplot as plt
plt.ion()

xs = [0,1,2,3,4,5]
ys = [9,3,2,1,4,2]
plt.plot(xs, ys)
plt.close()

first_run = True
while True:
  if first_run:
    first_run = False
    print('Velkommen til CLI-verktøyet for temperatur simulasjonen til Myrstad.\nSkriv `q`  eller `quit` for å gå ut av CLI-et.\nSkriv `hjelp` for informasjon om programmet\n')
  command = input('kommando? ').strip().lower()
  # print('cmd:', command)
  if command == 'hjelp' or command == 'info' or command == 'h':
    print('q: eller quit/exit for å avslutte\nhjelp: eller info for denne dialogen\nsimuler: eller sim for å simulere en periode')

  elif command == 'quit' or command == 'q' or command == 'exit':
    print('Ferdig å kjøre')
    break
  
  elif command == 'sim' or command == 'simuler':
    tid           = input('Hvor mange minutter ønsker du å simulere? ')           ; tid = float(tid)
    tidsintervall = input('Hvilket tidsintervall i sekunder ønsker du å bruke? ') ; tidsintervall = float(tidsintervall)
    temp          = input('Hvilken temperatur ønsker du? ')                       ; temp = float(temp)
    print(tid, tidsintervall, temp)
    print()
    print('Skriv `graf` eller `vis` for å vise fram grafen')
    plt.clf()
    plt.plot([1,2,3,4,5], [10,20,30,20,10])

  elif command == 'v' or command == 'vis' or command == 'graf':
    plt.clf()
    plt.plot(xs, ys)

  elif command == 'lukk' or command == 'skjul':
    plt.close()

  else:
    print("Funksjon finnes ikke, prøv på nytt eller `hjelp` får ekstra informasjon")

  print()