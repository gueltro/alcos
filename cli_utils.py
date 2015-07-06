from wallet import *

def cli_load_wallet():
    wallet = load(get_wallet_path())
    return wallet

def cli_get_promise():
    promise = raw_input()  
    return promise

def cli_get_alcos(alcos_name):
    ##Import the alcos to offer, either from file or from alcos name
    if os.path.isfile(alcos):
        alcos = load(wallet,alcos)
    else:
        alcos = wallet.get_alcos_from_name(alcos_name)

    assert isinstance(alcos, Alcos) ,\
        "This is not an alcos. You must supply a valid  name for the alcos or the path location of an alcos file."
    
    return alcos

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

def cli_offer_alcos(arguments):
    alcos_name = arguents["alcos"]
    wallet = cli_load_wallet() 
    alcos = cli_get_alcos(alcos_name) 
    wallet.offer_alcos_to_key_id(alcos,receiver)

def cli_accept_alcos(arguments):
    alcos_name = arguents["alcos"]
    wallet = cli_load_wallet() 
    alcos = cli_get_alcos(alcos_name) 
    wallet.accept_alcos(alcos)
   

def cli_export_info(arguments):
    output_file_path = arguments["output-file"]
    wallet = cli_load_wallet()
    store(wallet.face, output_file_path)

def cli_import_info(arguments):
    output_file_path = arguments["output-file"]
    wallet = cli_load_wallet()
    new_face = load(output_file_path)

    assert isinstance(new_face, Face),\
            "Imported object does not contain the information about an alcos identity"

    ##Import gpg info
    wallet.gpg.import_keys(new_face.public_key)

    ##Import info from past
    wallet.face.past += new_face.past

def cli_show_issued_promises():
    wallet = cli_load_wallet()
    wallet.show_issued_promises()

def cli_show_owed_promises():
    wallet = cli_load_wallet()
    wallet.show_owed_promises()

