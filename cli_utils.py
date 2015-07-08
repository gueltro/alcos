from wallet import *

def cli_load_wallet():
    wallet = load(get_wallet_path())
    return wallet

def cli_get_promise():
    promise = raw_input()  
    return promise

def cli_get_alcos(alcos_name):
    wallet = cli_load_wallet()
    ##Import the alcos to offer, either from file or from alcos name
    if os.path.isfile(alcos_name):
        alcos = load(alcos_name)
    else:
        alcos = wallet.get_alcos_from_name(alcos_name)

    assert isinstance(alcos, Alcos) ,\
        "This is not an alcos. You must supply a valid  name for the alcos or the path location of an alcos file."
    
    return alcos

##execption of leading cli rule beacuse I don't think it should be here
def generic_show(wallet, target_object):
    ##Show a file
    if os.path.isfile(str(target_object)):
        generic_show(wallet,load(target_object))

    ##Show a python object
    if isinstance(target_object, Alcos):
        target_object.pretty_print()

    if isinstance(target_object, Wallet):
        target_object.pretty_print()

    ##get an object from hash
    if isinstance(target_object, str):
    	maybe_alcos = wallet.get_alcos_from_name(target_object) 
    	if isinstance(maybe_alcos, Alcos):
        	maybe_alcos.pretty_print()

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
    alcos_name = arguments["<alcos>"]
    receiver = arguments["<receiver>"]
    wallet = cli_load_wallet() 
    alcos = cli_get_alcos(alcos_name) 
    wallet.offer_alcos_to_key_id(alcos,receiver)
    
    ##Save the alcos to file if requested. Such a file could be used as an offer
    output_file_path =  arguments["-o"]
    if output_file_path != None:
        store(alcos,output_file_path)
    store(wallet,get_wallet_path())

def cli_accept_alcos(arguments):
    alcos_name = arguments["<alcos>"]
    wallet = cli_load_wallet() 
    alcos = cli_get_alcos(alcos_name) 
    wallet.accept_alcos(alcos)
    store(wallet,get_wallet_path()) 

def cli_export_info(arguments):
    output_file_path = arguments["<output-file>"]
    wallet = cli_load_wallet()
    store(wallet.face, output_file_path)

def cli_import_info(arguments):
    output_file_path = arguments["<input-file>"]
    wallet = cli_load_wallet()
    new_face = load(output_file_path)

    assert isinstance(new_face, Face),\
            "Imported object does not contain the information about an alcos identity"

    ##Import gpg info
    wallet.gpg.import_keys(new_face.public_key)
    
    print "Importing " + str(len(new_face.get_past())) +  " new alcos. (with possible duplicates)"
    ##Import info from past
    for alcos in new_face.get_past():
        wallet.add_to_past(alcos)

def cli_show(arguments):
    wallet = cli_load_wallet()
    if arguments["issued_promises"]:
        wallet.show_issued_alcos()
    
    if arguments["owed_promises"]:
        wallet.show_owed_alcos()

    if arguments["known_promises"]:
        wallet.show_past()

    if arguments["keys"]:
        keys_uid =  [key["uids"] for key in wallet.gpg.list_keys()]
        print "List of the known keys"
        for uid in keys_uid:
            print uid[0]

    if arguments["public_key"]:
        print wallet.get_my_public_key()  
    
    if arguments["private_key"]:
        print wallet.get_my_private_key()  

    this_object = arguments["<object>"] 
    if this_object != None:
        generic_show(wallet,this_object) 

