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

#include <chrono>
#include <iostream>
#include <memory>
#include <string>
#include <vector>
#include <string>

#include "absl/memory/memory.h"
#include "client.h"
#include "proto/config_change.pb.h"
#include "proto/impact_analysis_response.pb.h"
#include "google/pubsub/v1/pubsub.grpc.pb.h"

#include "mock_message.h"
#include "processor.h"
#include "publisher.h"

const char kSubscriptionsLink[] = "projects/google.com:youtube-admin-pacing-server/subscriptions/CppBinary";
const char kPublisherTopicLink[] = "projects/google.com:youtube-admin-pacing-server/topics/TestImpactAnalysisResponse";
const int kSecondsToKeepClientAlive = 1200;

std::string getDummyImpactAnalysis() {
  ImpactAnalysisResponse impact_analysis;
  ConfigChangeRequest* config = impact_analysis.mutable_request();
  
  RoutingRule_Change* change = config->mutable_routing_rule()->add_changes();
  change->set_method("Add");
  change->set_queue("q1");
  change->add_possible_routes("q2");
  change->add_possible_routes("q3");
  change->add_possible_routes("q4");

  //Todo add dummy queue-impact objects to impact analysis object.

  return impact_analysis.SerializeAsString();
}

int main() {
  using youtube_hermes_config_subscriber::PublishMessage;
  std::cout<<getDummyImpactAnalysis()<<std::endl;
  PublishMessage(getDummyImpactAnalysis(), kPublisherTopicLink);
  return 0;
}

int main2() {

  // Creates a Client that polls pubsub and Runs it 
  // passing the MessageProcessor function as a callback.
  using google::pubsub::v1::PubsubMessage;
  using youtube_hermes_config_subscriber::Client;
  using youtube_hermes_config_subscriber::MessageProcessor;

  Client client = Client(kSubscriptionsLink);
  client.Run(MessageProcessor<PubsubMessage>);
  std::this_thread::sleep_for(std::chrono::seconds(kSecondsToKeepClientAlive));

  // Currently it takes around 30 seconds for the stream object in the client 
  // to close after calling this Stop method.
  // We will not need to call Stop in production,
  // in Prodoction the client will run indefinitly.
  client.Stop();
  
  client.JoinThread();
  std::cout << "Program Terminating" << std::endl;
  return 0;
}