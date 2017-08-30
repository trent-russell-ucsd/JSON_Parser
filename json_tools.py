#!/bin/env python2.7

import testlib
import os
import sys
import subprocess
import getopt
import ntpath
import json
from subprocess import Popen, PIPE, STDOUT

#cp -v tests/json_tools/json_tools.py test_json_tools && chmod a+x test_json_tools
###########################################################################
# Constructor for JSON_tools
###########################################################################
def Parse_Args(cfg): 
    obj = {
        'err': 0, 
        'msg': 'Good',
        'action_id': '',
        'unit_testing': False,
        'reboot': False,
        'key_set': False,
        'key_str': '',
        'key_arr': [],
        'val_set': False,
        'val_str': '',
        'file': False,
        'file_path': '',
        'dest_path': '',
        'file_name': '',
        'dir_name': '',
        'log_dir': '', 
        'timeout': '', 
        'target_ip': '',
        'src': '',
        'dest': '',
        'checkFeature': False,
        'attribute': '',
        'feature': '',
        'sysDictKey': '',
        'strict': 'OFF'
    }   

    obj['log_dir'] = cfg['log_dir']
    obj['target_ip'] = cfg['target_ip']
    obj['timeout'] = cfg['timeout'] 

    #get the Action ID number
    obj['action_id'] = os.environ.get("ACTION_ID")   
    if obj['action_id'] is None:
        obj['action_id'] = "999999"

    msg =  "--------------------------------------------------------------------------------\n"
    msg += "json_tools log: \n"
    msg += "--------------------------------------------------------------------------------\n"
    obj['msg'] = msg
    logger_lugger(obj)

    try:
        #Better way of cleaning up string. Need to pass it through as an argument to get rid of '\'; kind of a hack... :)
        str = os.environ['TESTING_AUTOTEST_ARGUMENTS']
        cmd = 'python tests/json_tools/argv.py ' + str
        p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)

        for line in p.stdout:
            line = line.rstrip()
            print line

        argv = eval(line)

        msg =  "\n-------------------------------------------------------------------------------\n"
        msg += "\nEnviornment Variable:\n"
        msg += os.environ['TESTING_AUTOTEST_ARGUMENTS']+"\n"
        msg += "\nARGV:\n"
        msg += line +"\n"
        msg += "\n-------------------------------------------------------------------------------\n"
        obj['msg'] = msg
        logger_lugger(obj)
   
        if len(argv) < 1:
            obj['msg'] = "Error: 14\nNeed command line arguments for test to function.\n"
            obj['err'] = 14
            Shut_Down( obj, True, True )

        opts, args = getopt.getopt(argv,"hruf:k:v:a:F:s:S:", ["help", "reboot", "unit", "file=", "key=", "value=", "if-attribute=", "if-feat=", "if-sysdict=", "strict="])

        if len(args) != 0:
            msg = "ERROR: 14\nSomething went wrong with your command line args.\n"
            print msg
            obj['msg'] = msg
            obj['err'] = 14
            Shut_Down( obj, True, True )

    except Exception: 
        msg = "ERROR: 12\nIllegal argument passed in the command line\n"
        #msg += sys.exc_info()[0]+"\n"
        obj['msg'] = msg
        obj['err'] = 12
        Shut_Down( obj, True, True )

    for o, a in opts:
        if o in ("-h", "--help"):
            msg = ""
            obj['msg'] = msg
            obj['err'] = 0
            Shut_Down( obj, False, True )
        elif o in ("-r", "--reboot"):
            obj['reboot'] = True
        elif o in ("-u", "--unit"):
            obj['unit_testing'] = True
        elif o in ("-f", "--file"):  
            file = a.strip()
            obj['file'] = True
            obj['file_path'] = file
            obj['dir_name'] = ntpath.dirname(file)
            obj['file_name'] = ntpath.basename(file)
        elif o in ("-k", "--key"):
            obj['key_set'] = True
            obj['key_str'] = a
        elif o in ("-v", "--value"):
            obj['val_set'] = True
            obj['val_str'] = a
        elif o in ("-a", "--if-attribute"):
            obj['checkFeature'] = True
            obj['attribute'] += "-a "+a+" "
        elif o in ("-F", "--if-feat"):
            obj['checkFeature'] = True
            obj['feature'] += "-f "+a+" "
        elif o in ("-s", "--if-sysdict"):
            obj['checkFeature'] = True
            obj['sysDictKey'] += "-s "+a+" "
        elif o in ("-S", "--strict"):
            obj['strict'] = a.upper()
        else:
            msg = "Error: 13\nUnknown argument passed in the command line...\n"
            obj['msg'] = msg
            obj['err'] = 13
            Shut_Down( obj, True, True )
    #end for

    if obj['strict'] not in ('ON', 'OFF'):
        obj['err'] = 25
        obj['msg'] = "ERROR: 25\nInvalid arg for --strict option. Only 'ON' or 'OFF' is allowed."
        Shut_Down( obj, True, True )


    return obj
#end __init__

###############################################################################
# Shut_Down:
###############################################################################
def Shut_Down( obj, show_err, show_use ):
    if show_err == True:
        ret_str = Error(obj['msg'])
        obj['msg'] += '\n'+ret_str

    if show_use == True:
        ret_str = Usage()
        obj['msg'] += '\n'+ret_str        

    print str(obj['err'])+" "+obj['msg']+"\n"+obj['log_dir'] 
    logger_lugger(obj)
    sys.exit(obj['err'])
#end

###############################################################################
# Logger Lugger will handle logging so you don't have too...
###############################################################################
def logger_lugger(obj):
    try:
        file_path = os.path.join(obj['log_dir'], 'json_tools.txt')
        file = open(file_path, 'a')
        file.write(obj['msg']+'\n')
        file.close()
        err = 0
    except:
        err = 1

    return err
#end

###############################################################################
# Error:
###############################################################################
def Error(err):
    msg = """
-------------------------------------------------------------------------------
"Uhhh... what happened?"
-------------------------------------------------------------------------------
                       u                                 
                  .  x!X                                 
                ."X M~~>                                 
               d~~XX~~~k    .u.xZ `\ \ "%                
              d~~~M!~~~?..+"~~~~~?:  "    h              
             '~~~~~~~~~~~~~~~~~~~~~?      `              
             4~~~~~~~~~~~~~~~~~~~~~~>     '              
             ':~~~~~~~~~~(X+"" X~~~~>    xHL             
              %~~~~~(X="      'X"!~~% :RMMMRMRs          
               ^"*f`          ' (~~~~~MMMMMMMMMMMx       
                 f     /`   %   !~~~~~MMMMMMMMMMMMMc     
                 F    ?      '  !~~~~~!MMMMMMMMMMMMMM.   
                ' .  :": "   :  !X""(~~?MMMMMMMMMMMMMMh  
                'x  .~  ^-+="   ? "f4!*  #MMMMMMMMMMMMMM.
                 /"               .."     `MMMMMMMMMMMMMM
                 h ..             '         #MMMMMMMMMMMM
                 f                '          @MMMMMMMMMMM
               :         .:=""     >       dMMMMMMMMMMMMM
               "+mm+=~("           RR     @MMMMMMMMMMMMM"
                       %          (MMNmHHMMMMMMMMMMMMMMF 
                      uR5         @MMMMMMMMMMMMMMMMMMMF  
                    dMRMM>       dMMMMMMMMMMMMMMMMMMMF   
                   RM$MMMF=x..=" RMRM$MMMMMMMMMMMMMMF    
                  MMMMMMM       'MMMMMMMMMMMMMMMMMMF     
                 dMMRMMMK       'MMMMMMMMMMMMMMMMM"      
                 RMMRMMME       3MMMMMMMMMMMMMMMM        
                @MMMMMMM>       9MMMMMMMMMMMMMMM~        
               'MMMMMMMM>       9MMMMMMMMMMMMMMF         
-------------------------------------------------------------------------------  
"""+str(err)+"""
-------------------------------------------------------------------------------
"""
    return msg
#end Error()


###########################################################################
# Prints help message on the screen
###########################################################################
def Usage():
    msg = '''
-------------------------------------------------------------------------------
Usage:
-------------------------------------------------------------------------------

*NOTE: All of the values for the flags need to be wrapped in 'SINGLE' 
   quotes or the program won't be able to parse out the correct values.
   'SINGLE' quotes also affect how the argument is processed and should
   be avoided in the key/value/file text.

-k or --key:    Enter a strand of keys in your JSON.
            ex: --key '["key1"]["key2"]["key3"]["key4"]'

-v or --value:  Enter a SINGLE value to be set
            ex: --value '"Foo"'

-f or --file:   Enter a file path to be edited on the Server
            ex: --file 'path/to/your/json/file.json'

-r or --reboot: Reboots the Server after JSON is edited
            ex: --reboot

-S or --strict: If strict mode is 'OFF' (default), test won't fail if it can't
                find the json file at the given path. Exits 44 if strict mode
                is 'OFF'. 
            ex: --strict 'ON'
                --strict 'OFF'
            see:


-a or --if-attribute: 
                Uses 'checkFeature' to check if the given attributes are
                present on the given Server. If an attribute is not found,
                the test will exit 44 N/A. Multiple attributes can be checked
                in one test. 
            see:


-F or --if-feat:
                Uses 'checkFeature' to check if the given features are
                present on the given Server. If a feature is not found,
                the test will exit 44 N/A. Multiple features can be checked
                in one test. 
            see:


-s or --if-sysdict:
                Uses 'checkFeature' to check if the given sysdict entries are
                present on the given Server. If an entry is not found,
                the test will exit 44 N/A. Multiple entries can be checked
                in one test. 
            see:


-h or --help:   Prints usage message and exits.
            ex: --help

-u or --unit:   Used for unit testing. Experts only...
            ex: --unit
-------------------------------------------------------------------------------

-------------------------------------------------------------------------------
EXIT CODES:
-------------------------------------------------------------------------------
0             No Errors Were Detected.
44            N/A: Test exited 'Not Available': 44
13            Unknown argument passed in the command line.
14            Missing command line args.
15            Problem transferring json file from the Server to HERE.
16            Problem transferring json file from HERE to the Server.
17            Problem reading json file. May not be a valid json structure. 
18            Couldn't check json file path. 
19            Unable to create an array of keys from dictionary.
20            Problem merging new data into json.
21            Problem writing updated json back to its file.
22            Problem with restart command in json_tools.
24            JSON file not found. Check file path in args. 
25            Invalid input for '--strict' option. Use 'ON' or 'OFF'.
26            Problem in checkFeature.
-------------------------------------------------------------------------------

    '''
    return msg
#end usage

###############################################################################
# Get an array of keys and sanitize the data; return key array
###############################################################################
def Get_Key_Arr(obj):
    obj['err'] = 0

    try:
        obj['key_str'] = obj['key_str'].replace("[", "")
        key_arr = obj['key_str'].split("]")
        key_arr.pop()
        obj['key_arr'] = key_arr
        obj['msg'] = "Key array set in obj\n"
    except:
        obj['err'] = 19
        obj['msg'] = "ERROR: 19\nProblem parsing key array\n"+str(sys.exc_info()[0])+"\n"

    logger_lugger(obj)
    return obj
#end

###############################################################################
# Checks if the src file exists on the Server
###############################################################################
def Check_File_Exists(obj):
    obj['err'] = 0
    obj['msg'] = "Attempting to check if src exists on the Server...\n"

    #Early out if unit testing... Don't want to use fileTransfer...
    if obj['unit_testing'] == True:
        return obj

    try:
        cmd = "sh runtest.sh fileTransfer -I %s -L %s -T %s -e %s" % (obj['target_ip'], obj['log_dir'], obj['timeout'], obj['src'] )
        obj['err'] = subprocess.call(cmd, shell=True)
        obj['msg'] += "Returning: "+str(obj['err'])+"\n"
        if obj['err'] != 0:
            if obj['strict'] == 'OFF':
                obj['msg'] += "N/A: 44\nfileTransfer exited "+str(obj['err'])+" when checking if the json file exists.\nFile not found\n" 
                obj['err'] = 44
            else:
                obj['msg'] += "ERROR: 24\nFile not found. Check file path in args.\n"
                obj['err'] = 24
            #end
        #end if
    except:
        obj['msg'] += "ERROR: 18\nUnable to check if json file exists.\n"+str(sys.exc_info()[0])+"\n"
        obj['err'] = 18

    logger_lugger(obj)
    return obj
#end

###############################################################################
# Transfers file from the Server using fileTransfer test
###############################################################################
def File_Transfer_From_Server(obj):
    obj['err'] = 0
    if obj['unit_testing'] == False:
        try:
            msg = "File transfer from Server...\n"
            print msg 
            cmd = "sh runtest.sh fileTransfer -I %s -L %s -T %s -r %s %s" % (obj['target_ip'], obj['log_dir'], obj['timeout'], obj['src'], obj['dest'] )
            obj['err'] = subprocess.call(cmd, shell=True)
            msg += "Returning: "+str(obj['err'])+"\n\n"
            obj[msg] = msg
        except:
            msg += "ERROR: 15\nUnable to transfer json file from the Server\n"+str(sys.exc_info()[0])+"\n"
            obj[msg] = msg
            obj['err'] = 15
    else:
        msg = "UNIT TESTING: READING from " + str(obj['src'])
        print msg
        cmd = "cp " + str(obj['src']) + " " + str(obj['dest'])
        obj['err'] = subprocess.call(cmd, shell=True)
        msg += "Returning: "+str(obj['err'])+"\n\n"

    logger_lugger(obj)        
    return obj
#end File_Transfer_From_Server()

###############################################################################
# Transfers file to the Server using fileTransfer test
###############################################################################
def File_Transfer_To_Server(obj):
    obj['err'] = 0
    if obj['unit_testing'] == False:
        try:
            msg = "File transfer to the Server...\n"       
            print msg
            cmd = "sh runtest.sh fileTransfer -I %s -L %s -T %s -s %s %s" % (obj['target_ip'], obj['log_dir'], obj['timeout'], obj['src'], obj['dest'] )
            obj['err'] = subprocess.call(cmd, shell=True)
            msg += "Returning: "+str(obj['err'])+"\n\n"
            obj['msg'] = msg
        except:
            msg += "ERROR: 16\nUnable to transfer json file to the Server\n"+str(sys.exc_info()[0])+"\n"
            obj[msg] = msg
            obj['err'] = 16
    else:
        obj['msg'] = "UNIT TESTING: Not Transfering File..."

    logger_lugger(obj)
    return obj
#end File_Transfer_To_Server()

###############################################################################
# Open and read a json file; return data in an object
###############################################################################
def Read_JSON_Data(obj):
    obj['msg'] = "Reading JSON file...\n"
    obj['err'] = 0
    try:
        #READ json file
        json_path = os.path.join(obj['log_dir'], obj['file_name'])
        json_file = open( json_path, "r" ) 
        obj['data'] = json.load(json_file)
        json_file.close()
        obj['msg'] += "Read is successful.\n\n"
    except:
        obj['msg'] = "ERROR: 17\nUnable to read json file.\n"+str(sys.exc_info()[0])+"\n"
        obj['err'] = 17

    logger_lugger(obj)
    return obj
#end

###############################################################################
# Tries to convert a string to an int, returns int or False
###############################################################################
def Try_Int(str):
    try:
        return int(str)
    except:
        return False 
#end

###############################################################################
# Tries to convert a string to a float; returns float or False
###############################################################################
def Try_Float(str):
    try:
        if '.' in str:
            return float(str)
        else:
            return False
    except:
        return False
#end

###############################################################################
# Attempts to convert a string into a json data type.
###############################################################################
def Converter( str):
    if str[0] == "\"" and str[-1] == "\"":
        obj = str[1: -1]
    elif str == '{}':
        obj = {}
    elif str == "null":
        obj = None
    elif str[0] == '[' and str[-1] == ']':
        try:
            obj = eval(str)
        except:
            obj = str
    elif str.isalpha() == True:
        try:
            obj = json.loads(str)
        except:
            obj = str
    elif type(Try_Float(str)) == float:
        obj = Try_Float(str)
    elif type(Try_Int(str)) == int:
        obj = Try_Int(str)
    else:
        obj = str

    return obj
#end Converter

###############################################################################
# Attempts to walk through the json data structure 
# and insert a value at a given key.
###############################################################################
def Merge_Dicts(obj):
    #msg = "Merging: "+obj['val_str']+"...\n"        

    arr = []
    val = Converter(obj['val_str'])
    for element in obj['key_arr']:
        arr.append(Converter(element))
    #end for

    temp = obj['data']

    length = len(arr)
    counter = 0

    for element in arr:
        if counter < length - 1:
            try:
                if type(temp[element]) == dict:
                    temp = temp[element]
                elif type(temp[element]) == list:
                    temp = temp[element]
                else:
                    temp[element] = {}
                    temp = temp[element]

            except:
                temp[element] = {}
                temp = temp[element]
        else:
            try:
                temp[element] = val
                obj['msg'] = "Merge is successful.\n"
                logger_lugger(obj)
            except:
                obj['msg'] = "ERROR: 20\nUnable to merge json file. "+ str(sys.exc_info()[0])+"\n"
                obj['err'] = 20
                return obj 
        counter += 1
    #end for

    obj['msg'] = "Merge completed...\n\n"
    logger_lugger(obj)
    return obj
#end

###############################################################################
# Write to a json file; return object
###############################################################################
def Write_JSON_Data(obj):
    obj['msg'] = "Writing to JSON file...\n"                
    try:
        #WRITE json file
        json_path = os.path.join(obj['log_dir'], obj['file_name'])
        json_file = open(json_path, "w+")
        json_dump = json.dumps(obj['data'], indent=4, sort_keys=True )
        json_dump = json_dump.replace('\n', '\r\n')
        json_file.write( json_dump )
        json_file.close()
        obj['msg'] += "Write is successful.\n\n"
    except:
        obj['msg'] = "ERROR: 21\n Unable to write data to json file.\n"+ str(sys.exc_info()[0])+"\n"
        obj['err'] = 21

    logger_lugger(obj)
    return obj

#end

###############################################################################
# Reboots the Server
###############################################################################
def Reboot_System(obj):
    obj['err'] = 0
    obj['msg'] = "Rebooting the Server\n"
    try:
        command= "sh runtest.sh reboot -I %s -L %s -T %s " % (obj['target_ip'], obj['log_dir'], obj['timeout'] )
        obj['msg'] += "Command: " + command
        obj['err'] = subprocess.call(command, shell=True)
    except:
        obj['err'] = 22
        obj['msg'] = "ERROR: 22\nProblem restarting Server with json_tools\n"+ str(sys.exc_info()[0])+"\n"

    logger_lugger(obj)
    return obj 
#end

###############################################################################
#
###############################################################################
def Check_Feature(obj):
    obj['err'] = 0

    #early out if not checking checkFeature
    if obj['checkFeature'] == False:
        return obj

    try:
        obj['msg'] = "Checking Features...\n"
        #White space is added at the end of each --if arg in Parse_Args for loop...
        cmd = "sh runtest.sh checkFeature -I "+obj['target_ip']+" -L "+str(obj['log_dir'])+" -T "+str(obj['timeout'])+" --if "+obj['feature']+obj['attribute']+obj['sysDictKey']
        obj['msg'] += "Command: " + cmd + "\n"
        obj['err'] = subprocess.call(cmd, shell=True) 
        obj['msg'] += "Returning exit code from previous command: "+str(obj['err'])
    except:
        obj['err'] = 26
        obj['msg'] = "ERROR: 26\nProblem with checkFeature\n"+ str(sys.exc_info()[0])+"\n"

    logger_lugger(obj)    
    return obj
#end

###############################################################################
# Start calling the functions to edit JSON
###############################################################################
def Start_JSON(obj):
    if obj['key_set'] == True and obj['val_set'] == True and obj['file'] == True:
        print "Away we go..."

        #------------------------------
        #SETUP src and dest for incoming...
        obj['src'] = obj['file_path']
        obj['dest'] = os.path.join(obj['log_dir'], obj['file_name'])

        #------------------------------
        # Check if JSON file exists on the Server
        obj = Check_File_Exists(obj)
        if obj['err'] != 0:
            Shut_Down( obj, True, True )

        #------------------------------
        # Run checkFeature if needed...
        obj = Check_Feature(obj)
        if obj['err'] != 0:
            Shut_Down( obj, True, True )

        #------------------------------
        #TRANSFER the file from the Server
        obj = File_Transfer_From_Server(obj)
        if obj['err'] != 0:
            Shut_Down( obj, True, True )
            
        #READ data from file
        obj = Read_JSON_Data(obj)
        if obj['err'] != 0:
            Shut_Down( obj, True, True )

        #------------------------------
        #GET the array of keys and value
        obj = Get_Key_Arr(obj)
        if obj['err'] != 0:
            Shut_Down( obj, True, True )

        #------------------------------
        #EDIT json file
        obj = Merge_Dicts(obj)
        if obj['err'] != 0:
            Shut_Down( obj, True, True )
        
        #------------------------------
        #WRITE to json file
        obj = Write_JSON_Data(obj)
        if obj["err"] != 0:
            Shut_Down( obj, True, True )

        #------------------------------
        #SWAP dest and src 
        obj['src'] = obj['dest']
        obj['dest'] = obj['dir_name']

        #------------------------------
        #TRANSFER json file
        obj = File_Transfer_To_Server(obj)
        if obj["err"] != 0:
            Shut_Down( obj, True, True )

    return obj
#end Start_JSON

def Check_ReBoot(obj):
    if obj['reboot'] == True and obj['unit_testing'] == False:
        obj['msg'] = "Attempting to reboot the Server...\n"
        obj = Reboot_System(obj)

    return obj
#end

###############################################################################
# Main method
###############################################################################
def Main():
    cfg = testlib.parse_argv(sys.argv)

    #----------------------------------
    # Parse the args
    obj = Parse_Args(cfg)
    if obj['err'] != 0:
        Shut_Down( obj, True, True )

    #----------------------------------
    # Start processing JSON
    obj = Start_JSON(obj)
    if obj['err'] != 0:
        Shut_Down( obj, True, True )

    #----------------------------------
    # Re-Boot... If needed
    obj = Check_ReBoot(obj)
    if obj['err'] != 0:
        Shut_Down( obj, True, True )

    #----------------------------------
    # Test exiting 0 without any errors... 
    obj['msg'] = 'Program Done, No Errors' 
    obj['err'] = 0

    Shut_Down( obj, False, False )
#end Main

if __name__ == "__main__" : 
    Main()

###############################################################################

