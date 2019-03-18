$(function () {
	$('[data-toggle="popover"]').popover()
})

function loading() {
	var x = document.getElementById("loading");
	if (x.style.display === "none") {
		x.style.display = "block";
	} else {
		x.style.display = "none";
	}
}

function reset_dynamics() {
	$(".dynamics").remove();
	$("#scenario option").remove();
	$("#scenario").append('<option selected value="base">Please choose from above</option>');
	$("#svr-text").html("");
	$("#svr_scenario-text").html("");
}

$(function() {
	$("#select_all").click(function() {
		//Show all results' table
		$('.table_em tbody').find('tr').show();
		//Reset drop down list colors
		$("#result_parameters > option").each(function () {
			$(this).attr('class', 'form-control green-dark');
		});
	});

	$("#unselect_all").click(function() {
		//Show all results' table
		$('.table_em tbody').find('tr').hide();
		//$('.table_em tbody').find('tr:has(td)').hide();
		//Reset drop down list colors
		$("#result_parameters > option").each(function () {
			$(this).attr('class', 'form-control red-dark'); 
		});
	});
});

$(function () {
	//  th_year = $('.table_em thead').find('th').eq(1).text()
	$('.table_em thead').find('th').hide();
	$('.table_em thead').find('th').eq(1).html('Ten years ahead simulation');
	//  $('.table_em thead').find('th').eq(1).html('Ten years ahead: ' + th_year);
	//  $('.table_em thead').find('th').eq(1).html('Ten years ahead simulation');
	//Add secondary headers for sector category name
	//  $('<tr id="sectortitle1" class="active"><th colspan="3">Output by production sector</th></tr>').insertBefore($('.table_em tbody tr:nth(0)'))
	//  $('<tr id="sectortitle2" class="active"><th colspan="3">Employment by production sector</th></tr>').insertBefore($('.table_em tbody tr:nth(6)'))
	//  $('<tr id="sectortitle3" class="active"><th colspan="3">Aggregate impact</th></tr>').insertBefore($('.table_em tbody tr:nth(12)'))

	$('.table_em tbody').find('tr').hide();
	var row_id = 1;
	$('.table_em tr').each(function () {
		if ($(this).find("th").text().length == 0)
		{
			$(this).attr('id', row_id);
			row_id += 1;
		}
		var element = parseFloat($(this).find('td').eq(1).text());
		if (element <= -3.00) {
			$(this).find('td').eq(1).addClass('red-dark').html(element + '%');
			$(this).find('td').eq(2).css('text-align', 'center').html("<i class='fa fa-arrow-down red-dark'></i>")
		}
		else if (element <= -1.50) {
			$(this).find('td').eq(1).addClass('red').html(element + '%');
			$(this).find('td').eq(2).css('text-align', 'center').html("<i class='fa fa-arrow-down red'></i>")
		}
		else if (element < 0.00) {
			$(this).find('td').eq(1).addClass('red-light').html(element + '%');
			$(this).find('td').eq(2).css('text-align', 'center').html("<i class='fa fa-arrow-down red-light'></i>")
		}
		else if (element == 0.00) {
			$(this).find('td').eq(1).addClass('grey').html(element + '%');
			$(this).find('td').eq(2).css('text-align', 'center').html("<i class='fa fa-minus grey'></i>")
		}
		else if (element <= 1.50) {
			$(this).find('td').eq(1).addClass('green-light').html(element + '%');
			$(this).find('td').eq(2).css('text-align', 'center').html("<i class='fa fa-arrow-up green-light'></i>")
		}
		else if (element <= 3.00) {
			$(this).find('td').eq(1).addClass('green').html(element + '%');
			$(this).find('td').eq(2).css('text-align', 'center').html("<i class='fa fa-arrow-up green'></i>")
		}
		else {
			$(this).find('td').eq(1).addClass('green-dark').html(element + '%');
			$(this).find('td').eq(2).css('text-align', 'center').html("<i class='fa fa-arrow-up green-dark'></i>")
		}
	});
});

// on select econometric model town, fill the scenario list
$(function() {
	//on('change' works on mobile too
	$("#towns").on('change', function() {
		reset_dynamics();

		var $dropdown = $(this);
		$.getJSON("/economics/scenarios/towns.json", function(data) {
			var key = $dropdown.val();
			var vals = [];

			switch(key) {
				case 'thessaloniki':
					$('#city_image').show();
					$('#city_image').attr("src","/economics/static/images/thessaloniki.jpeg");
					$('#scenario-text').html("The new parking system in Thessaloniki eases the proximity to the city center where most shops and services are located. This may increase the number of visitors coming from nearby cities, which in turn may increase retail sales. The new parking system also generates increased revenues which may invested by the municipality to improve city’s infrastructures (construction).");
					$('#svr-text').html("<div class='alert alert-info'>Click <strong><a href='model_svr.py' target='_blank'>here</a></strong> on the forecast estimations regarding revenues per sector for the new parking system in  Thessaloniki</div>")
					vals = data.Thessaloniki.split(',');
					break;
				case 'cork':
					$('#city_image').show();
					$('#city_image').attr("src","/economics/static/images/cork.jpg");
					$('#scenario-text').html("The future development of Camden Fort Meagher as a tourism destination may increase tourism spending in the area.");
					$('#svr-text').html("<div class='alert alert-info'>Check <strong><a href='model_svr.py' target='_blank'>here</a></strong> on the forecast estimations regarding revenues and the number of visitors for Camden Fort Meagher in Cork</div>")
					vals = data.Cork.split(',');
					break;
				case 'antwerp':
					$('#city_image').show();
					$('#city_image').attr("src","/economics/static/images/antwerp.jpeg");
					$('#scenario-text').html("Floods affect economic activity through disruption of the industry production (manufacturing sector) or through disruption of harbor companies’ activities as Antwerp’s harbor is one of Europe’s largest harbor.");
					vals = data.Antwerp.split(',');
					break;
				case 'antalya':
					$('#city_image').show();
					$('#city_image').attr("src","/economics/static/images/antalya.jpg");
					$('#scenario-text').html("Antalya");
					vals = data.Antalya.split(',');
					break;
				case 'base':
					$('#city_image').hide();
					vals = ['Please select from above'];
					break;
			}
			var $secondChoice = $("#scenario");
			$secondChoice.empty();
			if (key != 'base') {
				$secondChoice.append("<option selected id='base'>Please select from list</option>");
			}
			$.each(vals, function(index, value) {
				$secondChoice.append("<option id="+ value +">" + value + "</option>");
			});
		});
	});
});


$(function() {
	$("#scenario").on('change', function() {

		var $country = $("#towns");
		var $scenario = $(this);
		$(".dynamics").remove();

		if ($scenario.val() !== "Please select from list")
		{
			//  $('<h3 class="dynamics">User Input</h3>').appendTo('#dynamic_elements');

			$.getJSON("/economics/scenarios/" + $country.val() + "/" + $scenario.val()  + ".json", function(data) {
				$.each(data, function(index, value) {
					var element_title = value.split('/')[0]
					var max_value = value.split('/')[2]
					var min_value = value.split('/')[1]

					//add elements based on scenario
					$('<div class="form-group dynamics"><label for=' + index + '>' + element_title + '</label><input type="number" class="form-control" id=' + index  + ' name=' + index + ' max=' + max_value + ' min=' + min_value  +' value="1"></div>').appendTo('#dynamic_elements');
					//      $('<div class="form-group dynamics"><label for=' + index + '>' + element_title + '</label><input type="number" class="form-control" id=' + index  + ' name=' + index + ' max=' + max_value + ' min=' + min_value  +' value=1 onClick="if(this.value==0){getElementById(submit_form).disabled = true;"}></div>').appendTo('#dynamic_elements');
				});
			});
	  }//IF
	});
});

$(function() {
	$("#result_parameters").click(function() {
		var $row_id = $(this).val();
		if ($('#'+$row_id+'').is(':visible')) {
			$('#'+$row_id+'').hide();
			$('#result_parameters :selected').toggleClass('red-dark green-dark');
		}
		else {
			$('#'+$row_id+'').show();
			$('#result_parameters :selected').toggleClass('green-dark red-dark');
		}
	});
});

$(function () {
	$( ".table_svr_cork" ).each(function() {
		$(this).find('thead').find('th').eq(0).html('Working Period of Camden Fort Meagher');
		$(this).find('thead').find('th').eq(1).html('Expected Revenues');
		$(this).find('thead').find('th').eq(2).html('Expected number of visitors');
		$(this).find('tbody').find('th').eq(0).html('First year of operation');
		$(this).find('tbody').find('th').eq(1).html('Second year of operation');
	});
});

$(function () {
	$( ".table_svr_thess" ).each(function() {
		$(this).find('thead').find('th').eq(0).html('No');
		$(this).find('thead').find('th').eq(1).html('Sector');
		$(this).find('thead').find('th').eq(2).html('Expected revenues');
	});
});

// SVR model, on select town, create file inputs
$(function () {
//on('change' works on mobile too
$("#svr_towns").on('change', function() {
		reset_dynamics();

		var $dropdown = $(this);
		var key = $dropdown.val();

		switch(key) {
			case 'thessaloniki':
				var $dynamic_elements = $("#dynamic_elements");
				$('#svr_scenario-text').html("According to the selected city, the model implements forecasts based on preloaded data. In the case of Thessaloniki, the preloaded data are daily revenues of the 26 sectors from the existing parking system for the period 11 Nov 2017 to 31 December 2018. The user can upload different data, using the following links.")
				$dynamic_elements.append("<div class='form-group dynamics'><label for='userinputfile_revenue'>Revenue file (csv):</label><input type='file' id='userinputfile_revenue' name='userinputfile_revenue' accept='.csv'></div><p class='dynamics'>The sectoral revenues file for Thessaloniki should follow <a href='/economics/static/files/thes_svr_revenue_template.csv' download>this</a> template (in .csv format).</p>");
				$dynamic_elements.append("<div class='form-group dynamics'><label for='userinputfile_sector'>Sector file (txt):</label><input type='file' id='userinputfile_sector' name='userinputfile_sector' accept='.txt'></div><p class='dynamics'>The names of the parking sectors file should follow <a href='/economics/static/files/thes_svr_sectors_template.txt' download>this</a> template (in .txt format).</p>");
				$('#svr_city_image').show();
				$('#svr_city_image').attr("src","/economics/static/images/thess_svr.jpg");
				break;
			case 'cork':
				var $dynamic_elements = $("#dynamic_elements");
				$('#svr_scenario-text').html("According to the selected city, the model implements forecasts based on preloaded data. When the city of Cork is selected, the preloaded data are the daily number of visitors and the daily revenues of Fort Mitchell in Spike Island for the period 04 April 2017 to 10 February 2019, a touristic attraction nearby Camden Fort Meagher and of the same thematic content.")
				$dynamic_elements.append("<div class='form-group dynamics'><label for='userinputfile_revenue'>Revenue file (csv):</label><input type='file' id='userinputfile_revenue' name='userinputfile_revenue' accept='.csv'></div><p class='dynamics'>The daily revenues file for Camden Fort Meagher should follow <a href='/economics/static/files/cork_svr_revenue_template.csv' download>this</a> template (in .csv format).</p>");
				$dynamic_elements.append("<div class='form-group dynamics'><label for='userinputfile_visitors'>Visitors file (csv):</label><input type='file' id='userinputfile_visitors' name='userinputfile_visitors' accept='.csv'></div><p class='dynamics'>The daily number of visitors file for Camden Fort Meagher should follow <a href='/economics/static/files/cork_svr_visitors_template.csv' download>this</a> template (in .csv format).</p>");
				$('#svr_city_image').show();
				$('#svr_city_image').attr("src","/economics/static/images/cork_svr.jpg");
				break;
			case 'base':
				$('#svr_city_image').hide();
				break;
		}
	});
});

$(function () {
	$('.table_svr_thess tr').each(function () {
		var element = parseInt($(this).find('td').eq(1).text().replace(/,/g, ''))//.toFixed(2);
		element = element.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
	//	alert(element);
		$(this).find('td').eq(1).html(element+"€")
		$(this).find('td').eq(1).css({'text-align':'center'});
	});
});


$(function () {
	$('.table_svr_cork tr').each(function () {
		var element0 = parseInt($(this).find('td').eq(0).text().replace(/,/g, ''))//.toFixed(2);
		var element1 = parseInt($(this).find('td').eq(1).text().replace(/,/g, ''))//.toFixed(2);

		element0 = element0.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
		element1 = element1.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");

		$(this).find('td').eq(0).html(element0 + "€")
		$(this).find('td').eq(1).html(element1)


		$(this).find('td').eq(0).css({'text-align':'center'});
		$(this).find('td').eq(1).css({'text-align':'center'});
	});
});


