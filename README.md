# Hive scale development

#### *Project Status*: 
- *version 0 Completed*
- *version 1 Active*

## Executive Summary:

With my engineering and IT background, I created a data-driven hive weight measurement system to monitor the weight of the hive and the ambient temperature using an online dashboard. The tool helps to optimize the timing of honey harvesting, thereby improving product quality and increasing volume. In the off-season, the tool helps detect anomalies such as disease outbreaks, providing a quick financial return on investment.

## 1) Project Objective

The aim of the project is the complete design and implementation of a hive mass measurement system, including hardware, electronics and software.

For beekeepers, knowing the weight of the hives and the weather data back in time provides a lot of information. This allows them to see whether the bees are healthy, whether they are collecting pollen properly and when it is necessary to harvest the honey produced from the hive. It is useful to monitor the hive weight continuously during the flowering period, when there are rapid changes, so an automated system was needed.

<img src="https://images.unsplash.com/photo-1622057003191-47ee813ad88b?q=80&w=2146&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" align="center" width="500">

During the project, a stand-alone system was developed with a web dashboard interface where the hive's mass and weather data can be monitored continuously.

## 2) Project Implementation

The project was composed of several main components, here I present the basic concepts and solutions.


<img src="https://github.com/rolandnagy-ds/hive-scale/assets/81804897/533516cd-534a-433c-a877-13c8401a4451" align="center" width="500">

#### Hardware

A hive balance consists mainly of a weighing unit and its associated processing electronics. 

The weighing unit consists of a 300 kg load cell with an HX711 signal processing module. The digitized signal coming out of it is connected to an ATmega328 microcontroller IC. No data storage is done locally, but the measurement data is directly transmitted to a web server. To do this I use a mobile internet connection with a generic SIM card. The connection between the microcontroller and the SIM card is provided by a SIM800L GPRS module, which communicates using generic AT commands.

The system is powered from a conventional 230V AC mains supply, so a transformer unit has been added to provide 15V DC for the data acquisition modules.


#### Software

Coming soon


## 3) Project Results

The device was successfully installed in a working apiary and has been working well ever since. The data collected can be monitored through a simple online dashboard interface, which also provides the possibility to download historical data.

The system has provided a quick financial return, based on the following aspects:
- The harvesting time can be fully optimised, resulting in better quality and increasing volumes of product. This was a difficult task before, as the optimal date is highly dependent on several factors, for example, the weather. Furthermore, the bees cannot be disturbed by opening the hive, so it is useful to have an external measuring device.
- The system can be used to monitor the movement patterns of bees and indicate any anomalies that occur. It can be used, for example, to detect diseases so that the necessary intervention can be carried out quickly, reducing losses.

## Details

### Methods Used
* Data Visualization
* Complex system development
* API usage
* Web app development
* (v1: Predictive Modeling)

### Technologies
* Python
* Dash
* HTML
* (v1: PostGres, MySql)

### Needs of this project

- development of hardware components
  - mechanical components
  - electronical components with PCB
- data exploration
- data processing/cleaning
- app/ dashboard development
- writeup/reporting
- setting up data communication

### Partner

Community of local beekeepers

## Contact
* Feel free to contact team leads with any questions or if you are interested in contributing!
