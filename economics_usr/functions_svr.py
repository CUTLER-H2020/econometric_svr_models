"""
Written by Karypidis Paris Alexandros
Democritus University of Thrace (DUTH)
2018 within CUTLER H2020 Project
Python 3.5

Desc: Helpers for model_svr.py
"""

import pandas as pd

def save_uploaded_file (fileitem, upload_dir, userID, filetype):
    # Test if the file was uploaded
    if fileitem.filename:
        # strip leading path from file name
        # to avoid directory traversal attacks
        #fn = os.path.basename(fileitem.filename)
        if filetype == "sector":
                filedirectory = upload_dir + filetype + str(userID) + ".txt"
        else:
                filedirectory = upload_dir + filetype + str(userID) + ".csv"
        open(filedirectory, 'wb').write(fileitem.file.read())
#        print 'The file "' + filedirectory + '" was uploaded successfully'
#    else:
#        print 'No file was uploaded'

def copy_template_file(type, town, userID, fileextension):
#    print "Running model with with default inputs"
    from shutil import copyfile

    src_filename = "templates/" + town + "_svr_" + type + "_template" + "." + fileextension
    dst_filename = "/tmp/" + type + "" + str(userID) + "." + fileextension
#    print src_filename, dst_filename
    copyfile(src_filename, dst_filename)
#    print dst_filename


def copy_template_result_files(town, userID):
    from shutil import copyfile
#    print "Copying result files"
    if town == "cork":
        #copy default revenue values results file
        src_filename = "templates/cork_svr_revenue_results.csv"
        dst_filename = "/tmp/cork_svr_revenue" + str(userID) + ".csv"
#       print src_filename, dst_filename
        copyfile(src_filename, dst_filename)
        #copy default visitors values results file
        src_filename = "templates/cork_svr_visitors_results.csv"
        dst_filename = "/tmp/cork_svr_visitors" + str(userID) + ".csv"
        copyfile(src_filename, dst_filename)
    elif town == "thessaloniki":
        #copy default revenue values results file
        src_filename = "templates/thes_svr_final_results.csv"
        dst_filename = "/tmp/final_thes" + str(userID) + ".csv"
        copyfile(src_filename, dst_filename)


#userID, number of columns, "numbers" - TBC
def check_file(userID, user_input_value, town):
    import numbers

    if town == "cork":
        user_file = "/tmp/" + user_input_value + str(userID) + ".csv"
#        print "Checking file: " + user_file
        userfile = pd.read_csv(user_file, header=None)
#        print userfile.shape

        if userfile.shape[1] > 1 or userfile.shape[0] > 1000:
            print "<div class='alert alert-danger'><a href='#' class='close' data-dismiss='alert'>&times;</a><strong>Error:</strong> Your '" + user_input_value + "' file exceeds the permitted data limit. Your file should be up to 1x1000 (columns x rows).</div>"

            return False
        for index, row in userfile.iterrows():
            if not isinstance(row[0], numbers.Number):
                print "<div class='alert alert-danger'><a href='#' class='close' data-dismiss='alert'>&times;</a><strong>Error:</strong> Your '" + user_input_value  + "' file might contain non numeric values. Please consider removing any non numeric values.</div>"
                return False

    elif town == "thessaloniki":
        if user_input_value == "revenue":
            user_file = "/tmp/" + user_input_value + str(userID) + ".csv"
#            print "Checking file: " + user_file
            userfile = pd.read_csv(user_file, header=None)
#            print userfile.shape

            if userfile.shape[1] > 50 or userfile.shape[0] > 1000:
                print "<div class='alert alert-danger'><a href='#' class='close' data-dismiss='alert'>&times;</a><strong>Error:</strong> Your '" + user_input_value + "' file exceeds the permitted data limit. Your file should be up to 30x1000 (columns x rows).</div>"
                return False
            for index, row in userfile.iterrows():
                for cols in range (userfile.shape[1]):
                    if not isinstance(row[cols], numbers.Number):
                        print "<div class='alert alert-danger'><a href='#' class='close' data-dismiss='alert'>&times;</a><strong>Error:</strong> Your '" + user_input_value  + "' file might contain non numeric values. Please consider removing any non numeric values.</div>"
                        return False

        elif user_input_value == "sector":
            user_file = "/tmp/" + user_input_value + str(userID) + ".txt"
#            print "Checking file: " + user_file
            userfile = pd.read_csv(user_file, sep=",", header=None)
            if userfile.shape[1] > 1 or userfile.shape[0] > 50:
                print "<div class='alert alert-danger'><a href='#' class='close' data-dismiss='alert'>&times;</a><strong>Error:</strong> Your '" + user_input_value + "' file exceeds the permitted data limit. Your file should be up to 1x30 (columns x rows).</div>"
                return False
            for index, row in userfile.iterrows():
                if not isinstance(row[0], basestring):
                    print "<div class='alert alert-danger'><a href='#' class='close' data-dismiss='alert'>&times;</a><strong>Error:</strong> Your '" + user_input_value  + "' file might contain non categorical values. Please consider removing any non categorical values.</div>"
                    return False


#    print "File Check ok"
    return True


def print_output_SVR(userID, town):

    #html tags
    popover_text = "CUTLER forecast model uses data from Thessaloniki&#39;s existing parking system and from Fort Mitchell in Spike Island, a touristic attraction nearby Camden Fort Meagher and of the same thematic content used as a proxy. All estimations are based on the Support Vector Regression method coupled with the linear and the RBF kernel after parameter fine-tuning. When it comes to the parking system in Thessaloniki, the estimations are provided for the following year, while for Camden Fort Meagher estimations are provided for the first and the second year of operation."
    print "<h5 class='list-group-item list-group-item-success'><strong>CUTLER forecast model executed successfully.</strong>"
    print "<span type='button' data-toggle='popover' data-placement='bottom' title='Learn more' data-content='" + popover_text + "'><i class='fa fa-info-circle'></i></span>"
    print "</h5>"
    print "<br>"

    #userID = 123
    #Read results' CSVs
    if town == "cork":
        outputs = ['/tmp/cork_svr_revenue' + str(userID) + '.csv', '/tmp/cork_svr_visitors' + str(userID) + '.csv']
        outputs_names = ["Revenues", "Visitors"]

        print "<h5>The table reports the expected revenues and the expected number of visitors for Camden Fort Meagher in Cork, for the first and the second year of operation.</h5>"
        try:
#           print "<h5><strong>" + outputs_names[index] + "</strong></h5>"
            output_filename_revenues = pd.read_csv("/tmp/cork_svr_revenue" + str(userID) + '.csv')
        except Exception as er:
            print er
            print "<div class='alert alert-danger'><a href='#' class='close' data-dismiss='alert'>&times;</a><strong>Error:</strong> Result files not found - Please contact platform administrator</div>"
        try:
#           print "<h5><strong>" + outputs_names[index] + "</strong></h5>"
            output_filename_visitors = pd.read_csv("/tmp/cork_svr_visitors" + str(userID) + '.csv')
        except Exception as er:
            print er
            print "<div class='alert alert-danger'><a href='#' class='close' data-dismiss='alert'>&times;</a><strong>Error:</strong> Result files not found - Please contact platform administrator</div>"

        output_filename_revenues = output_filename_revenues.dropna()
        output_filename_revenues = output_filename_revenues.drop(output_filename_revenues.columns[[1]], axis=1) #drop NaN rows
        output_filename_revenues = output_filename_revenues.drop(output_filename_revenues.index[-1]) #drop last row

        output_filename_visitors = output_filename_visitors.dropna() #drop NaN rows
        output_filename_visitors = output_filename_visitors.drop(output_filename_visitors.columns[[1]], axis=1) #drop second (1) column
        output_filename_visitors = output_filename_visitors.drop(output_filename_visitors.index[-1]) #drop last row

        pd.options.display.float_format = '{:,.2f}'.format #show only two digits
        pd.set_option('display.max_colwidth', -1)

        concatenated_df = pd.concat([output_filename_revenues, output_filename_visitors], axis=1) #, ignore_index=False)
        print concatenated_df.to_html(index=True, classes=['table_svr_cork', 'table', 'table-bordered', 'table-hover'])

    elif town == "thessaloniki":
        print "<h5>The table reports the expected revenues per sector of the new parking system in Thessaloniki, for the following year.</h5>"
        try:
#           print "<h5><strong>" + outputs_names[index] + "</strong></h5>"
            output_filename = pd.read_csv('/tmp/final_thes' + str(userID) + '.csv', names='0')
        except Exception as er:
            print er
            print "<div class='alert alert-danger'><a href='#' class='close' data-dismiss='alert'>&times;</a><strong>Error:</strong> Result files not found - Please contact platform administrator</div>"
        else:
            output_filename = output_filename.dropna() #drop NaN rows
            pd.options.display.float_format = '{:,.2f}'.format #show only two digits
            pd.set_option('display.max_colwidth', -1)

            user_sectors = pd.read_csv("/tmp/sector" + str(userID) + ".txt", names=["Sectors"])
            concatenated_df = pd.concat([user_sectors, output_filename], axis=1) #, ignore_index=False)
            concatenated_df.index += 1
            print concatenated_df.to_html(index=True, classes=['table_svr_thess', 'table', 'table-bordered', 'table-hover'])

    return concatenated_df
