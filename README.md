# YouTube Hermes Config Automation

## **Project Goal:**
The objective of this system is to replace preexisting YouTube Hermes configuration tools with a user friendly UI for Eng /Ops members and vendor management to make configuration change requests. The UI must automatically send all new configuration change requests to the backend.  This UI must have the ability to provide the user with responses received from the backend, such as images and text files. <br/><br/>

## Overview:<br/>
With the new system, Eng/Ops members and vendor management personnel are able to create and edit Pacing system configuration change requests from the familiar Buganizer UI, instead of using the old QueueConfiguration UI.
Users will start from either the EnqueueRules UI, the RoutingTargetsUI or the QueueInfo UI. When they choose a configuration that they would like to change, a new Buganizer issue draft is opened with the pre-existing configuration data already filled out. They then just have to change the fields that they would like to change and then create the bug.<br/> <br/>
Here are the fields common to each configuration type:<br/>
* Title<br/>
* Priority<br/>
* Type<br/>
* Assignee<br/>
* CC<br/>
* Description<br/>
* Severity<br/>
* Found in <br/>
* In prod<br/>
* Reporter<br/>
* Verifier<br/>
* Targeted to<br/>
* Blocked by<br/>
* Blocking<br/>

And here are the unique advanced fields for each configuration type:<br/>

#### Enqueue Rules<br/>
* Certified By<br/>
* Discovered on<br/>
* Effort Days<br/>
* Effort Obsolete<br/>
* Impact Statement<br/>
* In PRD<br/>
* Stack Rank<br/>
* Start Date<br/>
* Target Date<br/>

#### Routing Targets<br/>
* Queue Id<br/>
* Add Queues to Route To<br/>
* Remove Queues to Route To<br/>
* Queue Info<br/>
* Queue Id<br/>
* MDB group name<br/>
* Ops Owner<br/>
* GVO Owner<br/>
* Tech Owner<br/>
* Is Dashboard Queue<br/>
* Reviews per Item<br/>
* Fragment Name<br/>
* Item Expiry (Min)<br/>
* Is Experimental Review Enabled<br/>
* Experimental Probability<br/>


Once the bug is created, the request is automatically sent to the backend where it is processed and compared to historical traffic data, and an impact analysis response is generated. If the request was invalid, Buganizer receives and prints a message detailing why the change request was invalid.  If the request was valid, then an impact analysis graph is created and included along with a detailed response of the impact that these changes will have. If applicable, anyone listed under the CC field will be notified of the change.
<br/><br/>

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

   TODO: Include the commands to install these

3. Create a virtualenv. For more info: https://virtualenv.pypa.io/

        $ virtualenv env
        $ source env/bin/activate

4. Install the dependencies needed to run the program. For more info: https://pip.pypa.io/

        $ pip install bs4
        $ pip install --upgrade google-cloud-pubsub
        $ pip install selenium

TODO: add any more necessary dependencies
        
**Set Environment Variables**

        $ export PROJECT='[PROJECT_ID]'
        $ export GOOGLE_APPLICATION_CREDENTIALS=~=/Downloads/[SERVICE_ACCOUNT_JSON_KEY]
    
**Set up Protocol Buffer**

 First view instructions and download the protocol buffer compiler at : https://developers.google.com/protocol-buffers
 

        $ protoc -I=. --python_out=python_publisher/config_change_request/ ./config_change.proto




**Download Chrome Driver:**<br/>
Download the Chromedriver here https://chromedriver.chromium.org/downloads to whatever directory you would like.
