from docopt import docopt
from cli_utils import *

__doc__ = """ alcos-cli

Usage:
  alcos-cli.py create-alcos [-p promise] [-i promise-file] [-o output-file]
  alcos-cli.py offer <alcos>  <receiver>  [-o output-file]
  alcos-cli.py accept <alcos> 
  alcos-cli.py show_issued_promises
  alcos-cli.py show_owed_promises

Options:
  -h --help     Show this screen.
  -p specify promise from a string
  -i specify promise from an input file
  -o output-file      
  --quiet      print less text
  --verbose    print more text
"""

if __name__ == '__main__':
        if check_if_setup():
            arguments = docopt(__doc__)
            print arguments

            ##Different parse based on the command

            if arguments["create-alcos"]:
                cli_create_alcos(arguments)
            
            if arguments["offer"]:
                cli_offer_alcos(arguments)

            if arguments["offer"]:
                cli_offer_alcos(arguments)
        
            if arguments["show_issued_promises"]:
                cli_show_issued_promises()

            if arguments["show_owed_promises"]:
                cli_show_owed_promises()

        else:
            print "You do not have a wallet right now!"
            want_new_setup = raw_input("Do you want to setup a new wallet? (Y = Yes, Everything else = No): ") 
            if want_new_setup == "Y":
                create_wallet()
             

