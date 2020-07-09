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

Files from NYC Opendata -> S3

Files Stored from S3 processed into -> Spark -> Processed Data stored into PostgreSQL

Data from PostgreSQL -> Accessed by NodeExpress API


New Data is processed and stored using Javascript's exec library in conjunction with NodeExpress API

Front-End -> Created using ReactJS in Conjunction with Tableau for table visualization


### Spark

### PostgreSQL

### Node.js and Express

### ReactJS

### Tableau


## Dataset
![Air Quality](https://data.cityofnewyork.us/Environment/Air-Quality/c3uy-2p5r)
![Mental Health Services](https://data.cityofnewyork.us/Health/Mental-Health-Service-Finder-Data/8nqg-ia7v)
![Subway Entrances](https://data.cityofnewyork.us/Transportation/Subway-Entrances/drex-xx56)
![NYPD Crime Data](https://data.cityofnewyork.us/Public-Safety/NYPD-Complaint-Data-Current-Year-To-Date-/5uac-w243)
![Vehicle Collissions Data](https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95)
![DOB Buildings Dataset](https://data.cityofnewyork.us/Housing-Development/DOB-NOW-Build-Approved-Permits/rbx6-tga4)

## File Structure

Placeholder text....

## Methodology


#### Simulated Real-Estate Data


#### Data Processing





