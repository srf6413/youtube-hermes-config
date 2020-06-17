// Copyright 2020 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#ifndef YOUTUBE_HERMES_CONFIG_CPPSUBSCRIBER_PROCESSOR_H
#define YOUTUBE_HERMES_CONFIG_CPPSUBSCRIBER_PROCESSOR_H

#include <sstream>
#include <string>
#include <thread>
#include <vector>

#include "config_type.pb.h"
#include "google/pubsub/v1/pubsub.grpc.pb.h"

namespace yoututbe {
namespace hermes {
namespace config {
namespace cppsubscriber {

typedef ConfigChangeRequest* MessageCallback(google::pubsub::v1::PubsubMessage const&);

// Constants used for logging data in MessageProcessor function
const std::string kInvalidConfigurationWarning = "Invalid ConfigChangeRequest Object. ConfigChangeRequest must have oneof (enqueue_rule, routing_rule, queue_info)";
const std::string kParsingFailedWarning = "Failed to parse ConfigChangeRequest Object from String";
const std::string kSuccessfulParsingMessage = "Successfully parsed ConfigChangeRequest from message";
const std::string kEnqueueRuleHeader = "-- Enqueue Rule --";
const std::string kRoutingRuleHeader = "-- Routing Rule --";
const std::string kQueueInfoHeader = "-- Queue Info --";

// MessageProcessor Templated function
// Message class should be a `MockMessage` or `google::pubsub::v1::PubsubMessage`
// This function logs the contents of message if there is a valid config_type
// and return the deserialized message object wrapped in a ConfigChangeRequest object 
// If Parsing the ConfigChangeRequest object then a nullptr will be returned
template <class Message>
ConfigChangeRequest* MessageProcessor(Message const& message) {
  using google::protobuf::Map;
  using std::cout;
  using std::endl;
  using std::string;
  using std::vector;

  ConfigChangeRequest* config_change_request = new ConfigChangeRequest();
  bool parsed_succesfully = config_change_request->ParseFromString(message.data());

  // If parsing failed, log error and return nullptr
  if (!parsed_succesfully) {
    cout << endl << kParsingFailedWarning << endl;
    cout << "message.data(): " << message.data() << endl;
    delete config_change_request;
    return nullptr;
  }

  cout << endl << kSuccessfulParsingMessage << endl;
  
  if (config_change_request->has_enqueue_rule()) {
    // log each EnqueueRule
    cout << kEnqueueRuleHeader << endl;
    for (int i = 0; i < config_change_request->enqueue_rule().changes_size(); ++i) {
      cout << config_change_request->enqueue_rule().changes(i).DebugString() << endl;
    }
  } else if (config_change_request->has_routing_rule()) {
    // log each RoutingRule
    cout << kRoutingRuleHeader << endl;
    for (int i = 0; i < config_change_request->routing_rule().changes_size(); ++i) {
      cout << config_change_request->routing_rule().changes(i).DebugString() << endl;
    }
  } else if (config_change_request->has_queue_info()) {
    // log each QueueInfo
    cout << kQueueInfoHeader << endl;
    for (int i = 0; i < config_change_request->queue_info().changes_size(); ++i) {
      cout << config_change_request->queue_info().changes(i).DebugString() << endl;
    }
  } else {
    // log Invalid Configuration Warning
    cout << kInvalidConfigurationWarning << endl;
    delete config_change_request;
    return nullptr;
  }
  
  return config_change_request;
}

}  // namespace cppsubscriber
}  // namespace config
}  // namespace hermes
}  // namespace yoututbe

#endif  // YOUTUBE_HERMES_CONFIG_CPPSUBSCRIBER_PROCESSOR_H