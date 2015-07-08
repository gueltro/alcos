from wallet import *

def cli_load_wallet():
    wallet = load(get_wallet_path())
    return wallet

def cli_get_promise():
    print "Type the promise that you want to sign in your alcos: "
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

def generic_object_parse(wallet, target_object):
    ##Show a file
    if os.path.isfile(str(target_object)):
        return generic_object_parse(wallet,load(target_object))

    ##Show a python object
    if isinstance(target_object, Alcos):
        return target_object 

    if isinstance(target_object, Wallet):
        return target_object 

    if isinstance(target_object, Face):
        return target_object

    ##get an object from hash
    if isinstance(target_object, str):
    	maybe_alcos = wallet.get_alcos_from_name(target_object) 
    	if isinstance(maybe_alcos, Alcos):
        	return maybe_alcos
    return None

##execption of leading cli rule beacuse I don't think it should be here
def generic_show(wallet, target_object):
    target_object = generic_object_parse(wallet, target_object) 
    
    if target_object != None:
        target_object.pretty_print()
   




##Functions connected with cli interface

def cli_iou(arguments):
    ##Append an IOU tag to the beginning of the promise
    iou_tag = "IOU: "
    if arguments["-p"] == None:
        arguments["-p"] = iou_tag + cli_get_promise()
    else:
        arguments["-p"] =  iou_tag + arguments["-p"]
    wallet = cli_load_wallet() 
    cli_create_alcos(arguments)
    ##Append the new created alcos to the arguments,
    ##such that cli_create_alcos can consume it (hack) 
    arguments["<alcos>"] = wallet.get_past()[-1]
    cli_offer_alcos(arguments)


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
    alcos = generic_object_parse(wallet,alcos_name) 
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
    wallet = cli_load_wallet()
    output_file_path = arguments["<output-file>"]
    target_object = arguments["<object>"]
    target_object = generic_object_parse(wallet, target_object)
    if target_object == None:
        ##Your wallet is the default export value
        target_object  = wallet.face 

    store(target_object, output_file_path)
   

def cli_import_info(arguments):
    output_file_path = arguments["<input-file>"]
    wallet = cli_load_wallet()

    target_object = load(output_file_path)

    if isinstance(target_object, Face):
        new_face = target_object
        ##Import gpg info
        wallet.gpg.import_keys(new_face.public_key)
        print "Importing " + str(len(new_face.get_past())) +  " new alcos. (with possible duplicates) from " + str(face.get_name()) 
        ##Import info from past
        for alcos in new_face.get_past():
            wallet.add_to_past(alcos)

    if isinstance(target_object,Alcos):
        alcos = target_object
        print "Adding the following alcos to past"
        alcos.pretty_print()
        wallet.add_to_past(alcos)
    store(wallet,get_wallet_path()) 

def cli_show(arguments):
    wallet = cli_load_wallet()
    if arguments["issued_promises"]:
        wallet.show_issued_alcos()
    
    if arguments["owed_promises"]:
        wallet.show_owed_alcos()

    if arguments["past"]:
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
    else:
        wallet.pretty_print()
