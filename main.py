""" Hovedfil som brukeren skal kjøre """

from classes.cli import CLI

if __name__ == '__main__':
  grensesnitt = CLI()
  grensesnitt.hoved_loop()