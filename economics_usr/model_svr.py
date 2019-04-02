#!/usr/bin/python
"""
Written by Karypidis Paris Alexandros
Democritus University of Thrace (DUTH)
2018 within CUTLER H2020 Project
Python 3.5

Desc: The model_svr.py file handles the user input for DUTH's SVR analysis
"""

# Import modules for CGI handling 
import cgi, cgitb; cgitb.enable()
import time, os
import pandas as pd
#from functions import check_input, create_input, print_output, print_$
from functions_svr import *
from parameters import parameters
from kafka_functions import user_input_producer_SVR, user_input_consumer_SVR


#Print header
with open("templates/header.html") as file:
    print file.read()

#Print upper_text
#with open("templates/svr_upper_text.html") as file:
#    print file.read()

#check if city is selected
form = cgi.FieldStorage()

print "<div class='container'>"
print "<div class='row'>"

#Print form with city field
with open("templates/svr_form.html") as file:
    print file.read()


# check if submit is pressed
if "submit_form" in form:

    # create input
    #create a unique 9-Digits user ID
    from random import randint
    userID = randint(000000000, 999999999)
#    print userID
#    userID = 123

    print "<div class='col-8 col-xl-8 col-lg-8'>"
    if form.getvalue('svr_towns') and form.getvalue('svr_towns') != "base":
        town = form.getvalue('svr_towns')
	if town == "cork":
	    user_inputs = {"userinputfile_revenue": "revenue", "userinputfile_visitors": "visitors"}
	elif town == "thessaloniki":
	    user_inputs = {"userinputfile_revenue": "revenue", "userinputfile_sector": "sector"}

	default_files_counter = 0
	rejected = False

        for user_input_key, user_input_value in user_inputs.iteritems():
            if form.getvalue(user_input_key,):
#               print "Running model with revenue user input"
                save_uploaded_file(form[user_input_key], "/tmp/", userID, user_input_value)
   	        if not check_file(userID, user_input_value, town):
	            print "<div class='alert alert-danger'><a href='#' class='close' data-dismiss='alert'>&times;</a><strong>Error:</strong> There was a problem with the '" + user_input_value + "' file you uploaded! Please use consider using a template file instead.</div>"
          	    rejected = True
	    # else use the default file
    	    else:
		default_files_counter += 1
		if user_input_value == "sector":
	            copy_template_file(user_input_value, town, userID, "txt")
		else:
	            copy_template_file(user_input_value, town, userID, "csv")
        if not rejected:
            # kafka_functions.py - send a message that a new user up
            user_input_producer_SVR(userID)
            if user_input_consumer_SVR(userID, default_files_counter, town):
                print_output_SVR(userID, town)
    else:
        print "<div class='alert alert-danger'><a href='#' class='close' data-dismiss='alert'>&times;</a><strong>Error:</strong> There was a problem uploading your files, please try again later</div>"
    print "</div>"


#Print body
with open("templates/body.html") as file:
    print file.read()



