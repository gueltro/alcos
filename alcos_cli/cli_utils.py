##Sorcery to get alcos_core (How do you do this better?)
import sys
import os
def parent(path):
    return os.path.abspath(os.path.join(path, os.pardir))
this_folder = parent(__file__)
parent_folder = parent(this_folder)
alcos_core_folder =  parent_folder + "/alcos_core"
sys.path.append(alcos_core_folder)
from wallet import *
from parser import *

def save(wallet):
    store(wallet,get_wallet_path())

def cli_load_wallet():
    wallet = load(get_wallet_path())
    return wallet

def cli_get_promise():
    print "Type the promise that you want to sign in your alcos: "
    promise = raw_input()  
    return promise

##execption of leading cli rule beacuse I don't think it should be here
def generic_show(wallet, target_input):
    parser = Parser()
    target_object = parser.parse(wallet, target_input) 
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
    cli_create_alcos(arguments)
    ##Append the new created alcos to the arguments,
    ##such that cli_create_alcos can consume it (hack) 

    wallet = cli_load_wallet() 
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
    save(wallet)

def cli_offer_alcos(arguments):
    alcos_name = arguments["<alcos>"]
    receiver = arguments["<receiver>"]
    wallet = cli_load_wallet() 
    parser = Parser()
    alcos = parser.parse(wallet,alcos_name) 
    wallet.offer_alcos_to_key_id(alcos,receiver)
    
    ##Save the alcos to file if requested. Such a file could be used as an offer
    output_file_path =  arguments["-o"]
    if output_file_path != None:
        store(alcos,output_file_path)
    save(wallet)

def cli_accept_alcos(arguments):
    alcos_name = arguments["<alcos>"]
    wallet = cli_load_wallet() 
    parser = Parser() 
    alcos = parser.parse(alcos_name) 
    wallet.accept_alcos(alcos)
    save(wallet)

def cli_export_info(arguments):
    wallet = cli_load_wallet()
    output_file_path = arguments["<output-file>"]
    target_object = arguments["<object>"]
    parser = Parser() 
    target_object = parser.parse(wallet, target_object)
    if target_object is None:
        ##Your face is the default export value
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
        print "Importing " + str(len(new_face.get_past())) +  " new alcos. (with possible duplicates) from " + str(new_face.get_name()) 
        ##Import info from past
        for alcos in new_face.get_past():
            wallet.add_to_past(alcos)

    if isinstance(target_object,Alcos):
        alcos = target_object
        print "Adding the following alcos to past"
        alcos.pretty_print()
        wallet.add_to_past(alcos)
    save(wallet)

def cli_show(arguments):
    wallet = cli_load_wallet()
    
    ##Did the user specify what to show?
    possible_commands = set(["past","keys","issued_promises","owed_promises"])   
    
    ##Check if the user supplied one of the hard-coded commands           
    is_show_from_command = max(map(lambda command: arguments[command], possible_commands)) 
    
    ##Check if the user supplied an identifier for some python object
    this_object = arguments["<object>"] 
    is_show_from_input = not (this_object is None)

    if is_show_from_command:
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
    
    if is_show_from_input:
        generic_show(wallet, this_object)  

    if (not is_show_from_command) and (not is_show_from_input):
        wallet.pretty_print()



