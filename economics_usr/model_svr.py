#!/usr/bin/python
"""
Written by Karypidis Paris Alexandros
Democritus University of Thrace (DUTH)
2018 within CUTLER H2020 Project
Python 2.7
"""


# Import modules for CGI handling
import os
import cgi
import cgitb
import time
import pandas as pd
from functions_svr import *
from parameters import parameters

# enable cgitd
from typing import Any

cgitb.enable()

# Print header
with open("templates/header.html") as file:
    print file.read()

# Print upper_text
# with open("templates/svr_upper_text.html") as file:
#    print file.read()

# check if city is selected
form = cgi.FieldStorage()

print "<div class='container'>"
print "<div class='row'>"

# Print form with city field
with open("templates/svr_form.html") as file:
    print file.read()

# check if submit is pressed
if "submit_form" in form:

    # create input
    # create a unique 9-Digits user ID
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
        else:
            user_inputs = []

        default_files_counter = 0
        rejected = False
        for user_input_key, user_input_value in user_inputs.iteritems():
            if form.getvalue(user_input_key, ):
                #               print "Running model with revenue user input"
                save_uploaded_file(form[user_input_key], "/tmp/", userID, user_input_value)
                if not check_file(userID, user_input_value, town):
                    print "<div class='alert alert-danger'><a href='#' class='close' " \
                          "data-dismiss='alert'>&times;</a><strong>Error:</strong> There was a problem with the '" + \
                          user_input_value + "' file you uploaded! Please use consider using a template file " \
                                             "instead.</div> "
                    rejected = True
            # else use the default file
            else:
                default_files_counter += 1
                if user_input_value == "sector":
                    copy_template_file(user_input_value, town, userID, "txt")
                else:
                    copy_template_file(user_input_value, town, userID, "csv")
        if not rejected:

            if default_files_counter == 2:
                copy_template_result_files(town, userID)
            else:
                # if file is uploaded use it
                # MAGIC STARTS - call matlab script
                import subprocess

                subprocess.check_call(['matlab_scripts/run_matlab_script_svr.sh', town,
                                       str(userID)])  # town - selected town, userID 9digit unique session ID
            # MAGIC ENDS

            # print results
            # html tags
            popover_text = "CUTLER forecast model uses data from Thessaloniki&#39;s existing parking system and from " \
                           "Fort Mitchell in Spike Island, a touristic attraction nearby Camden Fort Meagher and of " \
                           "the same thematic content used as a proxy. All estimations are based on the Support " \
                           "Vector Regression method coupled with the linear and the RBF kernel after parameter " \
                           "fine-tuning. When it comes to the parking system in Thessaloniki, the estimations are " \
                           "provided for the following year, while for Camden Fort Meagher estimations are provided " \
                           "for the first and the second year of operation. "
            print "<h5 class='list-group-item list-group-item-success'><strong>CUTLER forecast model executed " \
                  "successfully.</strong> "
            print "<span type='button' data-toggle='popover' data-placement='bottom' title='Learn more' " \
                  "data-content='" + popover_text + "'><i class='fa fa-info-circle'></i></span> "
            print "</h5>"
            print "<br>"

            # userID = 123

            # Read results' CSVs
            if town == "cork":
                outputs = ['/tmp/cork_svr_revenue' + str(userID) + '.csv',
                           '/tmp/cork_svr_visitors' + str(userID) + '.csv']
                outputs_names = ["Revenues", "Visitors"]

                print "<h5>The table reports the expected revenues and the expected number of visitors for Camden " \
                      "Fort Meagher in Cork, for the first and the second year of operation.</h5> "
                try:
                    #  		    print "<h5><strong>" + outputs_names[index] + "</strong></h5>"
                    output_filename_revenues = pd.read_csv("/tmp/cork_svr_revenue" + str(userID) + '.csv')
                except Exception as er:
                    print er
                    print "<div class='alert alert-danger'><a href='#' class='close' " \
                          "data-dismiss='alert'>&times;</a><strong>Error:</strong> Result files not found - Please " \
                          "contact platform administrator</div> "
                try:
                    #  		    print "<h5><strong>" + outputs_names[index] + "</strong></h5>"
                    output_filename_visitors = pd.read_csv("/tmp/cork_svr_visitors" + str(userID) + '.csv')
                except Exception as er:
                    print er
                    print "<div class='alert alert-danger'><a href='#' class='close' " \
                          "data-dismiss='alert'>&times;</a><strong>Error:</strong> Result files not found - Please " \
                          "contact platform administrator</div> "

                output_filename_revenues = output_filename_revenues.dropna()
                output_filename_revenues = output_filename_revenues.drop(output_filename_revenues.columns[[1]],
                                                                         axis=1)  # drop NaN rows
                output_filename_revenues = output_filename_revenues.drop(
                    output_filename_revenues.index[-1])  # drop last row

                output_filename_visitors = output_filename_visitors.dropna()  # drop NaN rows
                output_filename_visitors = output_filename_visitors.drop(output_filename_visitors.columns[[1]],
                                                                         axis=1)  # drop second (1) column
                output_filename_visitors = output_filename_visitors.drop(
                    output_filename_visitors.index[-1])  # drop last row

                pd.options.display.float_format = '{:,.2f}'.format  # show only two digits
                pd.set_option('display.max_colwidth', -1)

                concatenated_df = pd.concat([output_filename_revenues, output_filename_visitors],
                                            axis=1)  # , ignore_index=False)
                print concatenated_df.to_html(index=True,
                                              classes=['table_svr_cork', 'table', 'table-bordered', 'table-hover'])

            elif town == "thessaloniki":
                print "<h5>The table reports the expected revenues per sector of the new parking system in " \
                      "Thessaloniki, for the following year.</h5> "
                try:
                    #   		    print "<h5><strong>" + outputs_names[index] + "</strong></h5>"
                    output_filename = pd.read_csv('/tmp/final_thes' + str(userID) + '.csv', names='0')
                except Exception as er:
                    print er
                    print "<div class='alert alert-danger'><a href='#' class='close' " \
                          "data-dismiss='alert'>&times;</a><strong>Error:</strong> Result files not found - Please " \
                          "contact platform administrator</div> "
                else:
                    output_filename = output_filename.dropna()  # drop NaN rows
                    pd.options.display.float_format = '{:,.2f}'.format  # show only two digits
                    pd.set_option('display.max_colwidth', -1)

                user_sectors = pd.read_csv("/tmp/sector" + str(userID) + ".txt", names=["Sectors"])
                concatenated_df = pd.concat([user_sectors, output_filename], axis=1)  # , ignore_index=False)
                concatenated_df.index += 1
                print concatenated_df.to_html(index=True,
                                              classes=['table_svr_thess', 'table', 'table-bordered', 'table-hover'])

    else:
        print "<div class='alert alert-danger'><a href='#' class='close' " \
              "data-dismiss='alert'>&times;</a><strong>Error:</strong> There was a problem uploading your files, " \
              "please try again later</div> "
    print "</div>"

# Print body
with open("templates/body.html") as file:
    print file.read()
