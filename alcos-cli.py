from docopt import docopt
from cli_utils import *

__doc__ = """ alcos-cli

Usage:
  alcos-cli.py promise [-p promise-string] [-i promise-file] [-o output-file]
  alcos-cli.py offer <alcos>  <receiver>  [-o output-file]
  alcos-cli.py accept <alcos> 
  alcos-cli.py export <output-file>
  alcos-cli.py import <input-file>
  alcos-cli.py show <object>
  alcos-cli.py show (issued_promises | owed_promises | known_promises | keys | public_key | private_key) [wallet | face] 

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

            if arguments["promise"]:
                cli_create_alcos(arguments)
            
            if arguments["offer"]:
                cli_offer_alcos(arguments)

            if arguments["accept"]:
                cli_accept_alcos(arguments)

            if arguments["export"]:
                cli_export_info(arguments)

            if arguments["import"]:
                cli_import_info(arguments)
    
            if arguments["show"]:
                cli_show(arguments)


        else:
            print "You do not have a wallet right now!"
            want_new_setup = raw_input("Do you want to setup a new wallet? (Y = Yes, Everything else = No): ") 
            if want_new_setup == "Y":
                create_wallet()
             

