"""
Written by Karypidis Paris Alexandros
Democritus University of Thrace (DUTH)
2018 within CUTLER H2020 Project
Python 2.7
"""

import pandas as pd


def save_uploaded_file(fileitem, upload_dir, userID, filetype):
    # Test if the file was uploaded
    if fileitem.filename:
        # strip leading path from file name
        # to avoid directory traversal attacks
        # fn = os.path.basename(fileitem.filename)
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
        # copy default revenue values results file
        src_filename = "templates/cork_svr_revenue_results.csv"
        dst_filename = "/tmp/cork_svr_revenue" + str(userID) + ".csv"
        #       print src_filename, dst_filename
        copyfile(src_filename, dst_filename)
        # copy default visitors values results file
        src_filename = "templates/cork_svr_visitors_results.csv"
        dst_filename = "/tmp/cork_svr_visitors" + str(userID) + ".csv"
        copyfile(src_filename, dst_filename)
    elif town == "thessaloniki":
        # copy default revenue values results file
        src_filename = "templates/thes_svr_final_results.csv"
        dst_filename = "/tmp/final_thes" + str(userID) + ".csv"
        copyfile(src_filename, dst_filename)


# userID, number of columns, "numbers" - TBC
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
                print "<div class='alert alert-danger'><a href='#' class='close' data-dismiss='alert'>&times;</a><strong>Error:</strong> Your '" + user_input_value + "' file might contain non numeric values. Please consider removing any non numeric values.</div>"
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
                for cols in range(userfile.shape[1]):
                    if not isinstance(row[cols], numbers.Number):
                        print "<div class='alert alert-danger'><a href='#' class='close' data-dismiss='alert'>&times;</a><strong>Error:</strong> Your '" + user_input_value + "' file might contain non numeric values. Please consider removing any non numeric values.</div>"
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
                    print "<div class='alert alert-danger'><a href='#' class='close' data-dismiss='alert'>&times;</a><strong>Error:</strong> Your '" + user_input_value + "' file might contain non categorical values. Please consider removing any non categorical values.</div>"
                    return False

    #    print "File Check ok"
    return True
