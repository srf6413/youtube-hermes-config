# YouTube Hermes Config Automation
## C++ Pubsub Subscriber

## Functionality:<br/>
This program creates and runs a pubsub client object which subscribes to a pubsub topic and calls a callback function when ever it receives a new message.
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

1. Clone the project repository

        $ git clone https://github.com/viktries-google/youtube-hermes-config
        
2. Install `bazel` a build tool used to build and run this project and its dependencies
   *Installing Bazel:* https://docs.bazel.build/versions/master/install.html

<br><br>
        
**Set Environment Variables, or use gcloud from terminal to login**
#### setting environment variables

-        $ export PROJECT='[PROJECT_ID]'
-        $ export GOOGLE_APPLICATION_CREDENTIALS=~=/Downloads/[SERVICE_ACCOUNT_JSON_KEY]

<br>

#### logging into gcloud with terminal
1. *Installing gcloud:* https://cloud.google.com/sdk/install
2. *gcloud auth login:* https://cloud.google.com/sdk/gcloud/reference/auth/login

<br/>
<br/>

**Run**
-------------------------------------------------------------------------------

**Run Instructions:**

From terminal make sure you are in the `/cpp_subscriber` folder 

 -       $ cd cpp_subscriber
run with bazel
 -       $ bazel run :main

**Run Unit Test:**
 -       $ bazel test :unit_test

    ***note:***

    for mac os if unit test fails to build with weird gcp errors, use command

        $ bazel test --copt -DGRPC_BAZEL_BUILD :unit_test 

<br><br><br>

**Program Overview**
-------------------------------------------------------------------------------

This program creates and runs a pubsub client object which subscribes to a pubsub topic and calls a callback function when ever it receives a new message.

Currently the program is composed of two main components.

- Client
- MessageProssesor

## Client
The clients job is to subscribe to a pubsub topic. The cloud PubSub topic will receive messages from the python publisher containing a serialized protobuf object. 
When running the client a callback needs to be passed as a parameter. The client calls this callback passing the pubsub message to it whenever a new message is received from pubsub.

## Message Processor
The Message Processor is a function that is used as a callback and takes a 
PubsubMessage as an argument. The message processor deserializes a ConfigChangRequest object, console logs the object, and returns it.