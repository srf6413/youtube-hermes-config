# YouTube Hermes Config Automation

## **Project Goal:**
The objective of this system is to replace preexisting YouTube Hermes configuration tools with a user friendly UI for Eng /Ops members and vendor management to make configuration change requests. The UI must automatically send all new configuration change requests to the backend.  This UI must have the ability to provide the user with responses received from the backend, such as images and text files. <br/><br/>

## Overview:<br/>
With the new system, Eng/Ops members and vendor management personnel are able to create and edit Pacing system configuration change requests from the familiar Buganizer UI, instead of using the old QueueConfiguration UI.
Users will start from either the EnqueueRules UI, the RoutingTargetsUI or the QueueInfo UI. When they choose a configuration that they would like to change, a new Buganizer issue draft is opened with the pre-existing configuration data already filled out. They then just have to change the fields that they would like to change and then create the bug.<br/><br/>
Once the bug is created, the request is automatically sent to CAT where it is processed and compared to historical traffic data, and an impact analysis response is generated. If the request was invalid, Buganizer receives and prints a message detailing why the change request was invalid.  If the request was valid, then an impact analysis graph is created and included along with a detailed response of the impact that these changes will have. If applicable, anyone listed under the CC field will be notified of the change.
<br/> <br/>


**Setup Instructions:**
-------------------------------------------------------------------------------

**Authentication:**

This program requires authentication to be setup. Refer to the
`Authentication Getting Started Guide` for instructions on how to set up
credentials for applications.

*Authentication Getting Started Guide:*
    https://cloud.google.com/docs/authentication/getting-started
    
<br/>

**Install Dependencies**

1. Clone the project repository in whatever directory you want to use.

        $ git clone https://github.com/viktries-google/youtube-hermes-config
        
2. Install the latest version of Python, as well as pip. Refer to `Python Development Environment Setup Guide` for Google Cloud Platform for further instructions.

   *Python Development Environment Setup Guide:* https://cloud.google.com/python/setup

        $ sudo apt update
        $ sudo apt install python3 python3-dev python3-venv
        $ wget https://bootstrap.pypa.io/get-pip.py
        $ sudo python3 get-pip.py
        $ pip --version

3. Create a virtualenv. For more info: https://virtualenv.pypa.io/

        $ cd your-project
        $ python3 -m venv venv
        $ source env/bin/activate

4. Install the dependencies needed to run the program. For more info: https://pip.pypa.io/

        $ pip install bs4
        $ pip install --upgrade google-cloud-pubsub
        $ pip install --upgrade google-cloud-spanner
        $ pip install selenium
        $ pip install matplotlib
        $ pip install pandas

**Set Environment Variables**

        $ export PROJECT='[PROJECT_ID]'
        $ export GOOGLE_APPLICATION_CREDENTIALS=~=/Downloads/[SERVICE_ACCOUNT_JSON_KEY]
    
**Set up Protocol Buffer**

 First view instructions and download the protocol buffer compiler at : https://developers.google.com/protocol-buffers
 

        $ protoc -I=. --python_out=python_publisher/config_change_request/ ./config_change.proto
        $ protoc -I=. --python_out=python_subscriber/ ./impact_analysis_response.proto

        TODO @ballah: add setup for cpp subscriber




**Download Chrome Driver:**<br/>
Download the Chromedriver here https://chromedriver.chromium.org/downloads to whatever directory you would like.

**Run**
-------------------------------------------------------------------------------

**Run Instructions:**<br/><br/>
Before running make sure to edit *python_publisher/constants.py* and *python_subscriber/constants.py* as needed. Once you are ready to run, open up three terminal windows.<br/><br/>
Window 1:

        $ cd python_subscriber
        $ python3 main.py   
<br/>
Window 2:

        $ cd cpp_subscriber
        $ TODO @ballah: add cpp subscriber run instructions 
<br/>
Window 3:

        $ cd python_publisher
        $ python3 main.py


**Note:** The first time you run the project each 24hr period you will be brought to MOMA Single Sign on. Select the 'Use Security Code' option and generate a security code at go/sc to log in. Once you are logged in you will be brought to Buganizer.