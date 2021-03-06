# DUTH's econometric/SVR web tool

DUTH's economic web tool allows simulating illustrative policy interventions. It gives users the opportunity to assess whether a policy intervention has a positive impact on the city's economy. Results are also disentangled by production sector. More information can be found in Deliverable D4.2 - Visualization widget for presenting insights about the economic activity in spatio-temporal terms (https://zenodo.org/record/3385986)

The user can use the select list in order to choose a city for the analysis, then select a economic scenario and set a value for the simulation. After the user press the "Run the model" button, the econometric analysis model will present the results in a array. In the array the user can be informed whether the policy intervention she/he chose has a positive impact on the city's economy or not. The results are also presented grouped by production sectors (e.g. Regional Employment, Regional Gross Domestic Product etc.).

Pilot city scenarios:

| Pilot city  | Description |
| ---- | ----------- |
| Antalya  | TBC |
| Antwerp  | Floods affect economic activity through disruption of the industry production (manufacturing sector) or through disruption of harbor companies’ activities as Antwerp’s harbor is one of Europe’s largest harbor. |
| Cork  | The future development of Camden Fort Meagher as a tourism destination may increase tourism spending in the area. |
| Thessaloniki  | The new parking system in Thessaloniki eases the proximity to the city center where most shops and services are located. This may increase the number of visitors coming from nearby cities, which in turn may increase retail sales. The new parking system also generates increased revenues which may invested by the municipality to improve city’s infrastructures (construction). |


## Technical Information

These instructions will get you a copy of the project up and running on your local machine for testing purposes. See deployment for notes on how to deploy the project on a live system.

#### Description of the folders:

* [economic_usr](economics_usr/): contains the python cgi service including all the econometric models (in MATLAB executable format). This folder should be copied in the "/usr/lib/economics" folder in the local machine. (see "Installing" section for more)
* [economic_var](economic_var/): contains all the necessary visualizations for the user dashboard (css/javascript libraries, econometric scenarios on json format). This folder should be copied in the "/var/www/html/economics" folder in the local machine. (see "Installing" section for more)


### Prerequisites

- Ubuntu Server LTS (16.04) (used in developement)
- or a alternative debian based distro

- Apache KAFKA - topics created:
```
ALL_ECO_ECONOMETRIC_USERINPUT_ONCALL
ALL_ECO_ECONOMETRIC_RESULTS_ONCALL
ALL_ECO_SVR_USERINPUT_ONCALL
ALL_ECO_SVR_RESULTS_ONCALL
```

### Installing

1.a. Install Apache2 and enable cgi mod
```
sudo apt-get install apache2
sudo a2enmod cgi
sudo service apache2 restart
```

1.b. Install python - pandas - xlrd - openpyxl (to read input/output xlsx )
```
sudo apt-get install python
sudo apt-get install python-pandas
sudo apt-get install python-xlrd
sudo apt-get install python-openpyxl
sudo pip install kafka
sudo pip install kafka-python
sudo pip install elasticsearch
```

1.c. Download/Install MATLAB R2018a Runtime (to run matlab exe)

```
mkdir ~/Downloads
cd Downloads && wget http://ssd.mathworks.com/supportfiles/downloads/R2018a/deployment_files/R2018a/installers/glnxa64/MCR_R2018a_glnxa64_installer.zip
sudo mkdir -p /usr/local/MATLAB/MATLAB_Runtime/v94
unzip MCR_R2018a_glnxa64_installer.zip
sudo ./install -mode silent -agreeToLicense yes
```

* Installation directory /usr/local/MATLAB/MATLAB_Runtime/v94/

1.d. Copy files in directories
```
sudo mv economics_usr /usr/lib/economics
sudo mv economics_vaw /var/www/html/economics
```

1.e. Enable 'cleaning /tmp/' cronjob

```
sudo crontab -e
```

Paste the cronjob within the file
```
0 0 * * * /home/user/rm_CUTLER_tmp.sh >/dev/null 2>&1
```
