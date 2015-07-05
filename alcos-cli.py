from wallet import *
from docopt import docopt

__doc__ = """ alcos-cli

Usage:
  alcos-cli.py create-alcos [-p promise] [-i promise-file] 
  alcos-cli.py offer <alcos>
  alcos-cli.py accept <alcos>
  alcos-cli.py show_issued_promises
  alcos-cli.py show_owed_promise

Options:
  -h --help     Show this screen.
  -p specify promise from a string
  -i specify promise from an input file
  -o OUTPUT-FILE      specify output file [default: ./alcos.pkl]  
  --quiet      print less text
  --verbose    print more text

"""

if __name__ == '__main__':
        if check_if_setup():
            arguments = docopt(__doc__)
            print(arguments)
        else:
            print "You do not have a wallet right now!"
            want_new_setup = raw_input("Do you want to setup a new wallet? (Y = Yes, Everything else = No): ") 
            if want_new_setup == "Y":
                create_wallet()
             
