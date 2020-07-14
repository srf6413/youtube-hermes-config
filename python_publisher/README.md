# YouTube Hermes Config Automation

## **Project Goal:**
*Replace the YouTube Hermes configuration tools with Buganizer driven automation.* <br/><br/>

## Functionality:<br/>
Running this program will continuously scrape all Buganizer issues under a specified componentid, looking for valid templates in the reporter's comments on each issue. If a template is valid, it will then be parsed into a Protocol Buffer object, serialized and published in a Pub/Sub message through the specified topic.<br/><br/>

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
        
2. Install `pip` and `virtualenv`. Refer to `Python Development Environment Setup Guide` for Google Cloud Platform for instructions.

   *Python Development Environment Setup Guide:* https://cloud.google.com/python/setup

3. Create a virtualenv. For more info: https://virtualenv.pypa.io/

        $ virtualenv env
        $ source env/bin/activate

4. Install the dependencies needed to run the program. For more info: https://pip.pypa.io/

        $ pip install bs4
        $ pip install --upgrade google-cloud-pubsub
        $ pip install selenium
        
**Set Environment Variables**

        $ export PROJECT='[PROJECT_ID]'
        $ export GOOGLE_APPLICATION_CREDENTIALS=~=/Downloads/[SERVICE_ACCOUNT_JSON_KEY]
    
**Set up Protocol Buffer**

 First view instructions and download the protocol buffer compiler at : https://developers.google.com/protocol-buffers
 

        $ cd publisher/config_change_request
        $ protoc -I=. --python_out=python_publisher/config_change_request/ ./config_change.proto




**Download Chrome Driver:**<br/>
Download the Chromedriver here https://chromedriver.chromium.org/downloads to whatever directory you would like.




<br/>
<br/>

**Configuration**
-------------------------------------------------------------------------------

**Edit constants.py:**<br/>
Project ID: *The Project ID of the Project*<br/>
Pub/Sub Topic Name: *The name of the Pub/Sub Topic* <br/>
Buganizer Url: *The URL containing one or more Buganizer issues under a componentid.*<br/>
Path to project: *Path to the root directory of your project.* <br/>
Path to Chrome driver: *Path to the Chromedriver.*<br/>
Path to Chrome profile: *Path to the Chrome profile you would like to use. Visit chrome://version if you are unsure*<br/>
Configuration Specifier: *The specifier for all templates for the configuration type. Default = 'Configuration: '*<br/>
EnqueueRule Commands Count: *The number of nessary arguments for a EnqueueRule Change Request. Default = 4*<br/>
EnqueueRule Method Specifier: *The EnqueueRule template's specifier for method. Default = 'Method: '*<br/>
EnqueueRule Queue Specifier: *The EnqueueRule template's specifier for queue. Default = 'Queue: '*<br/>
EnqueueRule Features Specifier: *The EnqueueRule template's specifier for features. Default = 'Features: '*<br/>
EnqueueRule Priority Specifier: *The EnqueueRule template's specifier for priority. Default = 'Priority: '*<br/>
RoutingRule Commands Count: *The number of nessary arguments for a RoutingRule Change Request. Default = 3*<br/>
RoutingRule Method Specifier: *The RoutingRule template's specifier for method. Default = 'Method: '*<br/>
RoutingRule Queue Specifier: *The RoutingRule template's specifier for queue. Default = 'Queue: '*<br/>
RoutingRule Possible-Routes Specifier: *The RoutingRule template's specifier for possible routes. Default = 'Possible-Routes: '*<br/>
QueueInfo Commands Count: *The number of nessary arguments for a QueueInfo Change Request. Default = 3*<br/>
QueueInfo Method Specifier: *The QueueInfoe template's specifier for method. Default = 'Method: '*<br/>
QueueInfo Queue Specifier: *The QueueInfo template's specifier for queue. Default = 'Queue: '*<br/>
QueueInfo Owners Specifier: *The QueueInfo template's specifier for owners. Default = 'Owners: '*<br/>

**Run**
-------------------------------------------------------------------------------

**Run Instructions:**

        $ python3 main.py


**Note:** The first time you run the project each 24hr period you will be brought to MOMA Single Sign on. Select the 'Use Security Code' option and generate a security code at go/sc to log in. Once you are logged in and see Buganizer, close the browser and re-reun main.py.

**Logs**
-------------------------------------------------------------------------------


**Error Logging** Each time main.py is run, a new timestamped log file is created in the logs/ directory. Any system error messages will be printed in this log file.

