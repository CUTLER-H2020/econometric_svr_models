"""
Written by Karypidis Paris Alexandros
Democritus University of Thrace (DUTH)
2018 within CUTLER H2020 Project
Python 3.5

Desc: The model.py file handles the user input for DUTH's econometric analysis
"""

#!/usr/bin/python

# Import modules for CGI handling 
import cgi, cgitb
import time
import pandas as pd
#from functions import check_input, create_input, print_output, print_selected_input, print_diagrams
from functions import *
from parameters import parameters
from kafka_functions import user_input_producer, user_input_consumer

#Print header
with open("templates/header.html") as file:
    print file.read()

#Print upper_text
with open("templates/upper_text.html") as file:
    print file.read()


print "<div class='container'>"
print "<div class='row'>"

#Print form
with open("templates/form.html") as file:
    print file.read()

# Create instance of FieldStorage
form = cgi.FieldStorage()
if "submit_form" in form:

    #create a unique 9-Digits user ID
    from random import randint
    userID = randint(000000000, 999999999)
#    userID = 123

    #create input.xlsx based on user input
    user_input_parameters = create_input(form, userID) # functions.py
    user_input_producer(userID, user_input_parameters) #kafka_functions.py

    #get town name - scenario name
    if form.getvalue('towns'):
        town = form.getvalue('towns')
    else:
        town = "base"

    if user_input_consumer(userID, town): #kafka_functions.py

        '''
        #MAGIC STARTS - call matlab script
        import subprocess
        try:
            subprocess.check_call(['matlab_scripts/run_matlab_script.sh', town, str(userID)]) #town - selected town, userID 9digit unique session ID
        except subprocess.CalledProcessError, e:
	    print e.output
        #MAGIC ENDS
       '''
        print "<div class='col-8 col-xl-8 col-lg-8'>"

        #read output.xlsx and print an array
        print_output(userID) # functions.py
        #print selected parameters
    #    print_selected_input(form) # functions.py

    print "</div>"
print "</div>"
print "</div>"

'''
if "submit_form" in form:
    #get town name - scenario name
    if form.getvalue('towns'):
        town = form.getvalue('towns')
    else:
        town = "base"

#    print_highcharts_diagrams(town, userID)

#    print_diagrams(town)
'''

#Print form
with open("templates/body.html") as file:
    print file.read()
