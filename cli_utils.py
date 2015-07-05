from wallet import *

def cli_load_wallet():
    wallet = load(get_wallet_path())
    return wallet

def cli_create_alcos(arguments):
    wallet = cli_load_wallet() 

    ##make sure that user gives promise in a single way
    assert arguments["-i"] == None or arguments["-p"] == None ,\
        "You must import a promise from either a string or a file, not both!"

    ##Parse promise from command line
    if arguments["-p"] != None:
        promise = arguments["-p"]
    
    ##Parse promise from input file
    if arguments["-i"] != None:
        promise_file = arguments["-u"] 
        promise = open(promise_file,"r").read()

    ##If the user did not offer a promise, parse one from command line
    if arguments["-i"] == None and arguments["-p"] == None:
        print "Type the promise that you want to sign in your alcos: "
        promise = cli_get_promise()
    
    wallet.create_alcos(promise)
    new_alcos = wallet.get_past()[-1]
    print "Created new alcos: "
    print "Alcos identifier:"
    print new_alcos.name
    print "Promise stored in the new alcos: "
    print new_alcos.promise
    store(wallet,get_wallet_path())

def cli_get_promise():
    promise = raw_input()  
    return promise


def cli_show_owed_promises():
    wallet = cli_load_wallet()
    wallet.show_owed_promises()

