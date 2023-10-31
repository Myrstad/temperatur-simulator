# Klasser

## rom med omgivelser

ha et rom (med omgivelse) med følgende egenskaper

- høyde
- bredde
- dybde
- volum
- areal
- lufta sin varmekapisitet
- lufta sin masse per kubikkmeter
- start tempratur
- nå temp
- basis (ute) temp
- varmelement(er) | **klasse**

hvorfor så mange?

først og fremt får å kunne lage det realistisk, og at temperaturen naturlig faller gradvis ned til utetempraturen fordi det er realistisk og nødvendig får å ha bruk får en regulator senere i oppgaven

kunne simulere at rommet naturlig mister tempratur

## varmeelement

burde kanskje være under rommet/systemet

Eventuelle egenskaper:

- maks effekt
- effekten nå
- regulator | **klasse**

## Regulator

Egenskaper:

- kjennskap til varmeelement **klassen** eller motsatt
- tempratur
- ønsket tempratur
- PID konstanter (hvor mye de forskjellige leddene skal bety)
  - P
  - I
  - D = 0, til å begynne med

# utvikling

## 1

Simulere rommet med naturlig varmetap, med en simulering av tidsintervallet

## 2

ha et varmelement med varmeeffekt (W) funksjon: `sett_effekt(watt)`

trenger en simulator får å simulere varmen i rommet med effekt etter gitt tid, godt indervall er 60s, og en funksjon `simuler(delta_tid)` får å se hva som har skjedd etter tidsintervallet'

## 3

Regulere
