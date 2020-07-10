# YouTube Hermes Config Automation
## C++ Pubsub Subscriber
 
## Functionality:<br/>
This program creates and runs a pubsub client object which subscribes to a PubSub topic and calls a callback function whenever it receives a new message.
 
### Todo: add and elaborate on Impact Analysis component and PubSub Response Component.
<br/><br/>
 
**Setup Instructions:**
-------------------------------------------------------------------------------
 
**Authentication:**
 
This program requires authentication to be set up. Refer to the
`Authentication Getting Started Guide` for instructions on how to set up
credentials for applications.
 
*Authentication Getting Started Guide:*
   https://cloud.google.com/docs/authentication/getting-started
  
<br/>
 
**Install Dependencies**
 
Clone the project repository
 
	$ git clone https://github.com/viktries-google/youtube-hermes-config

<br>

Install `bazel` a build tool used to build and run this project and its dependencies
  *Installing Bazel:* https://docs.bazel.build/versions/master/install.html
 
## Installing bazel on Ubuntu
	$ sudo apt update && sudo apt install bazel
 
## Installing bazel on Mac os with Homebrew
	$ brew install bazel
 
 
<br><br>
      
## Set Environment Variables, or use gcloud from terminal to login
### Setting environment variables and google service account json key.
 
	$ export PROJECT='[PROJECT_ID]'
	
	$ export GOOGLE_APPLICATION_CREDENTIALS=~=/Downloads/[SERVICE_ACCOUNT_JSON_KEY]
 
<br>
 
#### Installing & Logging into gcloud from terminal
1. *Installing gcloud:* https://cloud.google.com/sdk/install
2. *Using gcloud to set the project and login to authorize:* https://cloud.google.com/sdk/gcloud/reference/auth/login
 
## Install gcloud on Linux
	$ curl https://sdk.cloud.google.com
	
	$ bash install.sh
 
## Installing on Mac os
Download and follow instructions here. https://cloud.google.com/sdk/docs/quickstart-macos
 
## Login & set project
	$ gcloud auth login
	
	$ gcloud config set project google.com:youtube-admin-pacing-server
 
<br/>
<br/>
 
**Run**
-------------------------------------------------------------------------------
 
**Run Instructions:**
 
From terminal make sure you are in the `/cpp_subscriber` folder
 
	$ cd cpp_subscriber
Run with bazel.
 
	$ bazel run :main
 
**Run Unit Test:**
	$ bazel test :unit_test
<br>
   ***note:***
 
On Mac os to run unit tests, use command.
 
	$ bazel test --copt -DGRPC_BAZEL_BUILD :unit_test
      
<br><br>
 
**Program Architecture**
-------------------------------------------------------------------------------
 
The program is composed of the following components.
 
- PubSub Subscriber
- MessageProssesor
- Impact Analysis
- PubSub Publisher (Impact Analysis Response)
 
```
[PubSub Subscriber] -> [Message Processor] -> [Impact Analysis] -> [PubSub Publisher]
 
[Historical Spanner DB] -> [Impact Analysis]
```
<br>

# Component Roles
## PubSub Subscriber (Client)
The clients job is to subscribe to a specified pubsub topic in order to receive configuration change requests. The cloud PubSub topic will receive messages from the pubsub publisher containing a serialized ConfigChangeRequest protobuf object.
 
 
## Message Processor
The Message Processor component is in charge of taking the PubSub Message, extracting the serialized string, deserializing the ConfigChangeRequest object, and passing it to the Impact Analysis Component.
 
## Impact Analysis
The Impact analysis component is responsible for receiving a ConfigChangeRequest object, connecting to the Historical Spanner Database to get historical video traffic, and calculating the impact on the system with the requested configuration changes. The Impact Analysis will pass an ImpactAnalysisResult object to the Publisher Component.
 
## PubSub Publisher
The PubSub Publisher component is responsible for receiving a ImpactAnalysisResult object, serializing it, and publishing it as a message to the specified pubsub topic as a response to the original configuration change request.

