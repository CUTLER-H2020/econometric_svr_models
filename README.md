# DUTH's econometric/SVR dashboard

DUTH's custom econometric and SVR model dashboards

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

- Ubuntu Server LTS (16.04) (used in developement)
- or a alternative debian based distro

- Apache KAFKA - topics created:
```
DATA_ALL_ECO_ECONOMETRIC_USERINPUT
ANLZ_ALL_ECO_ECONOMETRIC_USERINPUT
DATA_ALL_ECO_SVR_USERINPUT
ANLZ_ALL_ECO_SVR_USERINPUT
```

### Installing

#### 1. Manual

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


#### 2. Automatically

Run setup.sh on project's directory
```
./setup.sh    -> NOT YET COMPLETED
```
