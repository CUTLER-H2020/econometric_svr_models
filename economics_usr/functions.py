"""
Written by Karypidis Paris Alexandros
Democritus University of Thrace (DUTH)
2018 within CUTLER H2020 Project
Python 3.5

Desc: Helpers for model.py
"""

def check_input(input):
    if not input or not isinstance(input, str):
        return 0
    else:
        try:
            input_F = int(input)
        except ValueError:
            return o
        #return a number
        return input_F

def create_input(form, userID):

    import pandas as pd
    from parameters import parameters

    #get town name - scenario name
    if form.getvalue('towns'):
        town = form.getvalue('towns')

    if form.getvalue('scenario'):
        scenario = form.getvalue('scenario')

    # Get data from fields
    #circulate the form.keys and update parameters dictionary accrodingly
    for key in form.keys():
        for keys in key.split("-"):
            if keys in parameters:
                parameters[keys]['value'] = check_input(form.getvalue(key))

    #read and write a input.xlxs (based on template.xlsx)
    try:
        #relative path
        input_df = pd.read_excel("templates/template.xlsx", sheet_name=None)
    except Exception as er:
        print "Template file not found - (%s)" % (er)

    user_input = {}
    for index, row in input_df.iterrows():
        if index in parameters:
            row[1] = parameters[index]['value']
    return input_df

    '''
    import csv
    import math
    import numpy as np

    input_filename = '/tmp/input' + str(userID) + '.csv'
    with open(input_filename, 'w') as csv_file:
        writer = csv.writer(csv_file)
        for index, row in input_df.iterrows():
	    if str(index) != 'nan' and str(index) in parameters:
                print parameters[index]['value']
                writer.writerow([parameters[index]['value']])
    '''

def print_output(userID):

    import pandas as pd
    from parameters import output_parameters

    #Read results' csv
    #change directory - static directories
    #output_df = pd.read_excel("/home/paris/Desktop/Output.xlsx") #open xlxs to find file shape
    output_filename = '/tmp/Output' + str(userID) + '.csv'
    try:
        output_df = pd.read_csv(output_filename)
    except Exception as er:
	print er
#        print "Results file not found - Please contact platform administrator"
    else:

        output_df = output_df.dropna() #drop NaN rows
        #multiply last column with 100 to get percentage
        output_df[output_df.columns[1]] = output_df[output_df.columns[1]].apply(lambda x: x*100)
        output_df.insert(2, " ", " ") #create a column to show the arrows
        pd.options.display.float_format = '{:,.2f}'.format #show only two digits
        pd.set_option('display.max_colwidth', -1)

        #map output parameter number with output parameter name (matlab xlswrite can't write strings without excel)
        for index, row in output_df.iterrows():
            # change if needed 'Sectoral Num'
            output_df.loc[index,'0'] = output_parameters[row[0]]['name']

	# add a popover near title
        popover_text = "CUTLER economic model provides results in terms of long-run percentage deviations from the baseline, which captures the economy in the absence of policy interventions. For example, if the simulation shows a manufacturing sales impact of 0.2% for a city, the interpretation is that policy intervention shifted city's manufacturing sales upwards by 0.2% compared to an identical economy without policy intervention. The simulation is therefore meant to isolate the pure policy effect."
        print "<h5 class='list-group-item list-group-item-success'><strong>CUTLER economic model executed successfully. Please check below the results.</strong>"
        print "<span type='button' data-toggle='popover' data-placement='bottom' title='Learn more' data-content='%s'><i class='fa fa-info-circle'></i></span>" % (popover_text)
        print "</h5>"
	print "<br>"

        #print a dropdown list with every output parameter
        print '<label for="countries">Estimated impact by variable of interest:</label>'
        print '<a href="#" id="select_all">Select all</a>'
        print '/'
        print '<a href="#" id="unselect_all">Unselect all</a>'

	print '<select id="result_parameters" class="form-control">'
#        print '<option value="1" class="red-dark">Output by production sector</option>'
#        print '<option value="2" class="red-dark">Employment by production sector</option>'
#        print '<option value="3" class="red-dark">Consumption per capita</option>'
#        print '<option value="4" class="red-dark">Disposable income per capita</option>'
#        print '<option value="5" class="red-dark">GDP per capita</option>'
#        print '</select><br>'

        row_id = 1;
        for index, row in output_df.iterrows():
            print '<option value="%s" class="red-dark"> %s</option>' % (row_id, row[0])
            row_id += 1
        print '</select><br>'

        #keep this or do not read col.1
#        output_df = output_df.drop(output_df.columns[0], axis=1)

        print output_df.to_html(index=False, classes=['table_em', 'table', 'table-bordered', 'table-hover'])
        print "<br>"


def print_selected_input(form):

    from parameters import parameters

    print "<h4 class='list-group-item active'>Selected parameters</h4>"
    print '<ul class="list-group">'

    #get town name - scenario name
    if form.getvalue('towns'):
        print "<a class='list-group-item list-group-item-action'><h5>Town: %s</h5></a>" % (str(form.getvalue('towns')).capitalize())

    if form.getvalue('scenario'):
        print "<a class='list-group-item list-group-item-action'><h5>Scenario: %s</h5></a>" % (str(form.getvalue('scenario')))

    for key in form.keys():
        for keys in key.split("-"):
            if keys in parameters:
                print "<a class='list-group-item list-group-item-action'><h5>%s: %s</h5></a>" % (parameters[keys]['name'], str(form[key].value))
    print '</ul>'

def print_highcharts_diagrams(town, userID):

    if town == "base":
        return False
    elif town == "antalya":
        unit = "Turkish Lira"
    else:
        unit = "Thousands Euros"

    print "<div class='container'>"
    print "<div class='row' style='height: 50px;'>"

    print "<ul class='nav nav-tabs nav-justified' id='myTab'>"
    print "<li class='active'><a data-target='#first' data-toggle='tab'>Regional GDP</a></li>"
    print "<li><a data-target='#second' data-toggle='tab'>Aggregate Consumption</a></li>"
    print "<li><a data-target='#third' data-toggle='tab'>Disposable Income</a></li>"
    print "</ul>"

    print "<div class='tab-content'>"
    print "<div class='tab-pane active' id='first'>"
    print "<div id='highcharts_regional_gdp'></div>"
    filename = "/tmp/regional_gdp" + str(userID) + ".txt"
    print_diagram(filename, "Regional GDP", unit, "regional_gdp")
    print "</div>"

    print "<div class='tab-pane' id='second'>"
    print "<div id='highcharts_aggregate_consumption'></div>"
    filename = "/tmp/aggregate_consumption" + str(userID) + ".txt"
    print_diagram(filename, "Aggregate Consumption", unit, "aggregate_consumption")
    print "</div>"

    print "<div class='tab-pane' id='third'>"
    print "<div id='highcharts_disposable_income'></div>"
    filename = "/tmp/disposable_income" + str(userID) + ".txt"
    print_diagram(filename, "Disposable Income", unit, "disposable_income")
    print "</div>"

    #closes tabs
    print "</div>"
    print "</div>"


def print_diagram(filename, title, unit, type):
#parameters - userID, type of chart
    file = open(filename, "r")
    content = file.readlines()
    file.close()
    #remove every \n char from content and find starting point
    startingPoint = content[0].split("-")[0]
    content = [line.replace("\n", "")[5:] for line in content]
    numbers = map(float, content) #map content to float

    print "<script>"
    print "Highcharts.setOptions({lang: {thousandsSep: '.'}})"

    print "Highcharts.chart('highcharts_"+ type +"', {"
    print "title: {text: null},"
#    print "subtitle: {text: 'Source: thesolarfoundation.com'},"
    print "yAxis: {title: {text: '"+unit+"'}},"
    print "xAxis: {title: {text: 'Time (years)'}},"
    print "legend: {layout: 'vertical',align: 'right',verticalAlign: 'middle'},"
#    print "tooltip: {formatter: function () {return 'Year: <b>' + this.x +'</b><br>"+ title +": <b>' + this.y + '</b>';}},"
    print "tooltip: {pointFormat: '"+title+" {point.y:,.0f}'},"

    print "plotOptions: {"
#    print "series: {label: {connectorAllowed: false}, color: '#FF0000', pointStart: " + str(startingPoint) + "}"
    print "series: {color: '#FF0000', pointStart: " + str(startingPoint) + "}"
    print "},"

    print "series: [{name: '" + title + "',data:"
    print  numbers
    print ","
    print "zoneAxis: 'x',zones: [{value: 2015, color: '#7cb5ec'}, {dashStyle: 'dot'}]"

    print "}],"
    print "responsive: {rules: [{condition: {maxWidth: 500},chartOptions: {legend: {layout: 'horizontal',align: 'center',verticalAlign: 'bottom'}}}]}"

    print "})"
    print "</script>"


def print_diagrams(town):

    if town == "base":
	return False

    print "<br>"
    print "<!-- Kibana visualization iframes-->"
    print "<div class='container'>"
    print "<div class='row' style='height: 50px;'>"

    if town == "antalya":
        print "<ul class='nav nav-tabs nav-justified' id='myTab'>"
        print "<li class='active'><a data-target='#first' data-toggle='tab'>Annual growth rate (per thousand)</a></li>"
        print "<li><a data-target='#second' data-toggle='tab'>GDP per capita ($)</a></li>"
        print "<li><a data-target='#third' data-toggle='tab'>Number of house sales (first sale)</a></li>"
        print "<li><a data-target='#fourth' data-toggle='tab'>Number of overnights of foreigners</a></li>"
        print "<li><a data-target='#fifth' data-toggle='tab'>Total exports (thousand $)</a></li>"
        print "<li><a data-target='#sixth' data-toggle='tab'>Total imports (thousand $)</a></li>"
        print "<li><a data-target='#seventh' data-toggle='tab'>Total number of enterprises</a></li>"
        print "</ul>"

        print "<div class='tab-content'>"
        print "<div class='tab-pane active' id='first'>"
	iframe = '<iframe src="http://snf-859370.vm.okeanos.grnet.gr:5601/app/kibana#/visualize/edit/6e71c470-2292-11e9-9237-5f30eb781b9f?embed=true&_g=(refreshInterval%3A(pause%3A!t%2Cvalue%3A0)%2Ctime%3A(from%3A\'2008-01-28T11%3A13%3A17.422Z\'%2Cmode%3Aabsolute%2Cto%3A\'2018-01-28T11%3A28%3A17.423Z\'))" height="600" width="100%" style="border: none;"></iframe>'
        print iframe
        print "</div>"

        print "<div class='tab-pane' id='second'>"
	iframe = '<iframe src="http://snf-859370.vm.okeanos.grnet.gr:5601/app/kibana#/visualize/edit/b5622af0-2292-11e9-9237-5f30eb781b9f?embed=true&_g=(refreshInterval%3A(pause%3A!t%2Cvalue%3A0)%2Ctime%3A(from%3A\'2003-01-28T11%3A14%3A55.915Z\'%2Cmode%3Aabsolute%2Cto%3A\'2018-01-28T11%3A29%3A55.915Z\'))" height="600" width="100%" style="border: none;"></iframe>'
        print iframe
        print "</div>"

        print "<div class='tab-pane' id='third'>"
	iframe = '<iframe src="http://snf-859370.vm.okeanos.grnet.gr:5601/app/kibana#/visualize/edit/f9223910-2292-11e9-9237-5f30eb781b9f?embed=true&_g=(refreshInterval%3A(pause%3A!t%2Cvalue%3A0)%2Ctime%3A(from%3A\'2012-01-28T11%3A16%3A14.233Z\'%2Cmode%3Aabsolute%2Cto%3A\'2019-01-28T11%3A31%3A14.233Z\'))" height="600" width="100%" style="border: none;"></iframe>'
        print iframe
        print "</div>"

        print "<div class='tab-pane' id='fourth'>"
	iframe = '<iframe src="http://snf-859370.vm.okeanos.grnet.gr:5601/app/kibana#/visualize/edit/4039d6a0-2293-11e9-9237-5f30eb781b9f?embed=true&_g=(refreshInterval%3A(pause%3A!t%2Cvalue%3A0)%2Ctime%3A(from%3A\'2001-01-28T11%3A19%3A11.990Z\'%2Cmode%3Aabsolute%2Cto%3A\'2018-01-28T11%3A34%3A11.991Z\'))" height="600" width="100%" style="border: none;"></iframe>'
        print iframe
        print "</div>"

        print "<div class='tab-pane' id='fifth'>"
	iframe = '<iframe src="http://snf-859370.vm.okeanos.grnet.gr:5601/app/kibana#/visualize/edit/2b464340-2294-11e9-9237-5f30eb781b9f?embed=true&_g=(refreshInterval%3A(pause%3A!t%2Cvalue%3A0)%2Ctime%3A(from%3A\'2011-01-28T11%3A20%3A43.130Z\'%2Cmode%3Aabsolute%2Cto%3A\'2018-01-28T11%3A35%3A43.130Z\'))" height="600" width="100%" style="border: none;"></iframe>'
        print iframe
        print "</div>"

        print "<div class='tab-pane' id='sixth'>"
	iframe = '<iframe src="http://snf-859370.vm.okeanos.grnet.gr:5601/app/kibana#/visualize/edit/5f6130e0-2294-11e9-9237-5f30eb781b9f?embed=true&_g=(refreshInterval%3A(pause%3A!t%2Cvalue%3A0)%2Ctime%3A(from%3A\'2001-06-05T17%3A57%3A55.758Z\'%2Cmode%3Aabsolute%2Cto%3A\'2018-05-07T19%3A09%3A23.392Z\'))" height="600" width="100%" style="border: none;"></iframe>'
        print iframe
        print "</div>"

        print "<div class='tab-pane' id='seventh'>"
	iframe = '<iframe src="http://snf-859370.vm.okeanos.grnet.gr:5601/app/kibana#/visualize/edit/9e948af0-2294-11e9-9237-5f30eb781b9f?embed=true&_g=(refreshInterval%3A(pause%3A!t%2Cvalue%3A0)%2Ctime%3A(from%3A\'2008-01-28T11%3A22%3A37.020Z\'%2Cmode%3Aabsolute%2Cto%3A\'2017-01-28T11%3A37%3A37.020Z\'))" height="600" width="100%" style="border: none;"></iframe>'
        print iframe
        print "</div>"
	#closes tabs
        print "</div>"

    elif town == "antwerp":
        print "<ul class='nav nav-tabs nav-justified' id='myTab'>"
        print "<li class='active'><a data-target='#first' data-toggle='tab'>Total population of the metropolitan area (persons)</a></li>"
        print "<li><a data-target='#second' data-toggle='tab'>GDP per capita ($)</a></li>"
        print "<li><a data-target='#third' data-toggle='tab'>Unemployment as a share of the labour force (%)</a></li>"
        print "</ul>"

        print "<div class='tab-content'>"
        print "<div class='tab-pane active' id='first'>"
	iframe = '<iframe src="http://snf-859370.vm.okeanos.grnet.gr:5601/app/kibana#/visualize/edit/5386a9c0-2290-11e9-9237-5f30eb781b9f?embed=true&_g=(refreshInterval%3A(pause%3A!t%2Cvalue%3A0)%2Ctime%3A(from%3A\'2002-06-05T17%3A57%3A55.758Z\'%2Cmode%3Aabsolute%2Cto%3A\'2018-05-07T19%3A09%3A23.392Z\'))" height="600" width="100%" style="border: none;"></iframe>'
        print iframe
        print "</div>"

        print "<div class='tab-pane' id='second'>"
	iframe = '<iframe src="http://snf-859370.vm.okeanos.grnet.gr:5601/app/kibana#/visualize/edit/fa4a93d0-228f-11e9-9237-5f30eb781b9f?embed=true&_g=(refreshInterval%3A(pause%3A!t%2Cvalue%3A0)%2Ctime%3A(from%3A\'2004-01-28T11%3A30%3A56.282Z\'%2Cmode%3Aabsolute%2Cto%3A\'2018-01-28T11%3A45%3A56.282Z\'))" height="600" width="100%" style="border: none;"></iframe>'
        print iframe
        print "</div>"

        print "<div class='tab-pane' id='third'>"
	iframe = '<iframe src="http://snf-859370.vm.okeanos.grnet.gr:5601/app/kibana#/visualize/edit/4b27e9a0-2291-11e9-9237-5f30eb781b9f?embed=true&_g=(refreshInterval%3A(pause%3A!t%2Cvalue%3A0)%2Ctime%3A(from%3A\'2003-06-05T17%3A57%3A55.758Z\'%2Cmode%3Aabsolute%2Cto%3A\'2018-05-07T19%3A09%3A23.392Z\'))" height="600" width="100%" style="border: none;"></iframe>'
        print iframe
        print "</div>"

	#closes tabs
        print "</div>"

    elif town == "cork":
        print "<ul class='nav nav-tabs nav-justified' id='myTab'>"
        print "<li class='active'><a data-target='#first' data-toggle='tab'>Average Monthly Rent Report</a></li>"
        print "<li><a data-target='#second' data-toggle='tab'>Business Demography</a></li>"
        print "<li><a data-target='#third' data-toggle='tab'>Disposable Income per Person (Euro)</a></li>"
        print "<li><a data-target='#fourth' data-toggle='tab'>House Prices (Euro)</a></li>"
        print "</ul>"

        print "<div class='tab-content'>"
        print "<div class='tab-pane active' id='first'>"
        iframe = '<iframe src="http://snf-859370.vm.okeanos.grnet.gr:5601/app/kibana#/visualize/edit/67410130-228c-11e9-9237-5f30eb781b9f?embed=true&_g=(refreshInterval%3A(pause%3A!t%2Cvalue%3A0)%2Ctime%3A(from%3A\'2007-06-05T17%3A57%3A55.758Z\'%2Cmode%3Aabsolute%2Cto%3A\'2018-05-07T19%3A09%3A23.392Z\'))" height="600" width="100%" style="border: none;"></iframe>'
#	iframe = '<iframe src="http://snf-859370.vm.okeanos.grnet.gr:5601/app/kibana#/visualize/edit/67410130-228c-11e9-9237-5f30eb781b9f?embed=true&_g=(refreshInterval%3A(pause%3A!t%2Cvalue%3A0)%2Ctime%3A(from%3A\'2007-06-05T17%3A57%3A55.758Z\'%2Cmode%3Aabsolute%2Cto%3A\'2018-05-07T19%3A09%3A23.392Z\'))" height="600" width="100%" style="border: none;"></iframe>'
        print iframe
        print "</div>"

        print "<div class='tab-pane' id='second'>"
	iframe = '<iframe src="http://snf-859370.vm.okeanos.grnet.gr:5601/app/kibana#/visualize/edit/cdf126d0-228c-11e9-9237-5f30eb781b9f?embed=true&_g=(refreshInterval%3A(pause%3A!t%2Cvalue%3A0)%2Ctime%3A(from%3A\'2007-06-05T17%3A57%3A55.758Z\'%2Cmode%3Aabsolute%2Cto%3A\'2017-05-07T19%3A09%3A23.392Z\'))" height="600" width="100%" style="border: none;"></iframe>'
#	iframe = '<iframe src="http://snf-859370.vm.okeanos.grnet.gr:5601/app/kibana#/visualize/edit/cdf126d0-228c-11e9-9237-5f30eb781b9f?embed=true&_g=(refreshInterval%3A(pause%3A!t%2Cvalue%3A0)%2Ctime%3A(from%3A\'2007-06-05T17%3A57%3A55.758Z\'%2Cmode%3Aabsolute%2Cto%3A\'2017-05-07T19%3A09%3A23.392Z\'))" height="600" width="100%" style="border: none;"></iframe>'
        print iframe
        print "</div>"

        print "<div class='tab-pane' id='third'>"
	iframe = '<iframe src="http://snf-859370.vm.okeanos.grnet.gr:5601/app/kibana#/visualize/edit/0ea68d00-228d-11e9-9237-5f30eb781b9f?embed=true&_g=(refreshInterval%3A(pause%3A!t%2Cvalue%3A0)%2Ctime%3A(from%3A\'1999-06-05T17%3A57%3A55.758Z\'%2Cmode%3Aabsolute%2Cto%3A\'2016-05-07T19%3A09%3A23.392Z\'))" height="600" width="100%" style="border: none;"></iframe>'
        print iframe
        print "</div>"

        print "<div class='tab-pane' id='fourth'>"
	iframe = '<iframe src="http://snf-859370.vm.okeanos.grnet.gr:5601/app/kibana#/visualize/edit/51727720-228d-11e9-9237-5f30eb781b9f?embed=true&_g=(refreshInterval%3A(pause%3A!t%2Cvalue%3A0)%2Ctime%3A(from%3A\'1974-06-05T17%3A57%3A55.758Z\'%2Cmode%3Aabsolute%2Cto%3A\'2017-05-07T19%3A09%3A23.392Z\'))" height="600" width="100%" style="border: none;"></iframe>'
        print iframe
        print "</div>"

	#closes tabs
        print "</div>"

    elif town == "thessaloniki":
        print "<ul class='nav nav-tabs nav-justified' id='myTab'>"
        print "<li class='active'><a data-target='#first' data-toggle='tab'>Total population of the metropolitan area (persons)</a></li>"
        print "<li><a data-target='#second' data-toggle='tab'>GDP per capita (US$)</a></li>"
        print "<li><a data-target='#third' data-toggle='tab'>Unemployment as a share of the labour force (%)</a></li>"
        print "</ul>"

        print "<div class='tab-content'>"
        print "<div class='tab-pane active' id='first'>"
	iframe = '<iframe src="http://snf-859370.vm.okeanos.grnet.gr:5601/app/kibana#/visualize/edit/7a2081a0-228b-11e9-9237-5f30eb781b9f?embed=true&_g=(refreshInterval%3A(pause%3A!t%2Cvalue%3A0)%2Ctime%3A(from%3A\'2002-01-28T10%3A33%3A52.736Z\'%2Cmode%3Aabsolute%2Cto%3A\'2018-01-28T10%3A48%3A52.736Z\'))" height="600" width="100%" style="border: none;"></iframe>'
        print iframe
        print "</div>"

        print "<div class='tab-pane' id='second'>"
	iframe = '<iframe src="http://snf-859370.vm.okeanos.grnet.gr:5601/app/kibana#/visualize/edit/0ec01a60-228b-11e9-9237-5f30eb781b9f?embed=true&_g=(refreshInterval%3A(pause%3A!t%2Cvalue%3A0)%2Ctime%3A(from%3A\'2004-01-28T10%3A33%3A29.039Z\'%2Cmode%3Aabsolute%2Cto%3A\'2019-01-28T10%3A48%3A29.039Z\'))" height="600" width="100%" style="border: none;"></iframe>'
        print iframe
        print "</div>"

        print "<div class='tab-pane' id='third'>"
	iframe = '<iframe src="http://snf-859370.vm.okeanos.grnet.gr:5601/app/kibana#/visualize/edit/f0ce9620-228b-11e9-9237-5f30eb781b9f?embed=true&_g=(refreshInterval%3A(pause%3A!t%2Cvalue%3A0)%2Ctime%3A(from%3A\'2003-06-05T17%3A57%3A55.758Z\'%2Cmode%3Aabsolute%2Cto%3A\'2019-05-07T19%3A09%3A23.392Z\'))" height="600" width="100%" style="border: none;"></iframe>'
        print iframe
        print "</div>"

	#closes tabs
        print "</div>"

    print "</div>"
    print "</div>"
