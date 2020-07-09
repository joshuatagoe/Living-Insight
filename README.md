WIP

# Living-Insight

The goal of this project is to build a data pipeline that allows homebuyers and renters to to gain access to detailed information about potential houses and neighborhoods they are considering, so that they can make more informed decisions on where they want to live.

![Image of Demo](images/demo1.png)
![Image of Demo](images/demo2.png)

# Table of Contents
  * [Motivation](#motivation)
  * [Pipeline](#pipeline)
  * [Requirements](#requirements)
  * [Architecture](#architecture)
  * [Dataset](#dataset)
  * [File Structure](#file-structure)
  * [Methodology](#methodology)


## Motivation

Many people, when buying homes often focus on the price, or at the very most, the price and hearsay from friends and neighbors, they never really search for insight into a specific neighborhood or place, and part of the reason for that is due to the large variety of data, and disjointed it is. Living-Insight solves this problem by creating a data pipeline that connects its users to all of this data.


## Pipeline
![Pipeline](images/pipeline.png)

## Requirements
Python 3  
Ubuntu  
PySpark  

## Architecture

##### Files from NYC Opendata -> S3
Files Uploaded into S3 either manually through the AWS console, or using [uploadcsvs.py](uploadcsvs.py)

##### Files Stored from S3 processed into -> Spark -> Processed Data stored into PostgreSQL
[Process_datasets](https://github.com/JUCHY/Living-Insight/tree/master/process_datasets) contains the python scripts used to match the different datasets to specific buildings and locations. This data is also then uploaded into postgresql using the JDBC driver

##### Data from PostgreSQL -> Accessed by NodeExpress API
[Queries.js](node-postgres-api/queries.js) contains the API calls that provides the data that is visualized with the frontend
API also accepts in new data, using javascripts exec api to run a [spark job](https://github.com/JUCHY/Living-Insight/blob/master/process_datasets/integrate_data.py) and [SQL Script](https://github.com/JUCHY/Living-Insight/blob/master/process_datasets/integrate_data.sql) from the command line.

##### Front-End -> Created using ReactJS in Conjunction with Tableau for table visualization, and Google Maps API for displaying location of data points
[React](https://reactjs.org/docs/create-a-new-react-app.html) is used for the dynamic rendering of data points displayed using the [Google Maps Api](https://www.npmjs.com/package/react-google-maps). Clicking a datapoint reveals a more detailed view of that data. A [tableau](https://www.tableau.com/) visualization is dynamically rendered at the bottom of the webapp. The tableau visualization conencts to a tableau workbook craeted usnig the tableau desktop app, and stored onto the tableau online server.

### Spark
[Create cluster of EC2 instances](https://blog.insightdatascience.com/create-a-cluster-of-instances-on-aws-899a9dc5e4d0)  
[Install spark onto cluster](https://blog.insightdatascience.com/simply-install-spark-cluster-mode-341843a52b88)  
[Download JDBC for handling connection PSQL database](https://jdbc.postgresql.org/download.html)  
Install necceessary python modules:
```
pip install fastkml
pip install gmpy2
```
Submit Python Script:
```
spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --master spark://ec2-52-91-13-65.compute-1.amazonaws.com:7077 --driver-class-path /home/ubuntu/postgresql-42.2.14.jar {Path/to/Script} {command_line_args if any}
```

### PostgreSQL
[Installation](https://blog.insightdatascience.com/simply-install-postgresql-58c1e4ebf252)  
Connect to database and create user  
```
sudo -u postgres -i
psql
CREATE USER <set_username> WITH PASSWORD '<setpassword>';

```

### Node.js and Express
[Install Node.js](https://github.com/nodesource/distributions/blob/master/README.md#debinstall)  
Run:  
```
mkdir node-api-postgres
cd node-api-postgres
npm init -y
npm i express pg

```

### ReactJS
Run   
```
npx create-react-app my-app
cd my-app
npm install react-google-maps --save
```
Edit index.html in public to include script for [tableau javascript api](https://help.tableau.com/current/api/js_api/en-us/JavaScriptAPI/js_api.htm)  

### Tableau
Download [Tableau Desktop App](https://www.tableau.com/products/desktop)  
[Connect to database](https://help.tableau.com/current/pro/desktop/en-us/examples_tableauserver.htm)  
You will need to setup your EC2 security group, and permissions in your psql pg_hba.conf file for this to work out  
[Place on tableau online](https://help.tableau.com/current/pro/desktop/en-us/publish_workbooks_share.htm#:~:text=With%20the%20workbook%20open%20in,the%20project%20to%20publish%20to.)  
[Connect react app to tableau javascript api](https://www.youtube.com/watch?v=hc4UCBTACTU)  


## Dataset
[Air Quality](https://data.cityofnewyork.us/Environment/Air-Quality/c3uy-2p5r)  
[Mental Health Services](https://data.cityofnewyork.us/Health/Mental-Health-Service-Finder-Data/8nqg-ia7v)  
[Subway Entrances](https://data.cityofnewyork.us/Transportation/Subway-Entrances/drex-xx56)  
[NYPD Crime Data](https://data.cityofnewyork.us/Public-Safety/NYPD-Complaint-Data-Current-Year-To-Date-/5uac-w243)  
[Vehicle Collissions Data](https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95)  
[DOB Buildings Dataset](https://data.cityofnewyork.us/Housing-Development/DOB-NOW-Build-Approved-Permits/rbx6-tga4)  
  
## File Structure

Placeholder text....

## Methodology


#### Simulated Real-Estate Data
Data from DOBs buildings dataset is used to simulate real-estate data. [sparkprocessing.py](https://github.com/JUCHY/Living-Insight/blob/6f12c45f0a3dba79931b021ce69ef6c939028d73/process_datasets/sparkprocessing.py#L36) loops through the rows of the dataset and creates a custom rental_price for each building based off selecting a point from a gaussian distribution of the averge rent price of that borough. Only the first 1000 houses are used due to the limitations of how many google geolocation api requests I can make.


#### Data Processing





