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
#include <stdlib.h>

#include <fstream>

#include "absl/memory/memory.h"
#include "client.h"
#include "proto/config_change.pb.h"
#include "proto/impact_analysis_response.pb.h"
// #include "config_change.pb.h"
// #include "impact_analysis_response.pb.h"
#include "google/pubsub/v1/pubsub.grpc.pb.h"

#include "mock_message.h"
#include "processor.h"
#include "publisher.h"

const char kSubscriptionsLink[] = "projects/google.com:youtube-admin-pacing-server/subscriptions/CppBinary";
const char kPublisherTopicLink[] = "projects/google.com:youtube-admin-pacing-server/topics/TestImpactAnalysisResponse";
const char kImpactFilePath[] = "/Users/isaiah/Dev/Google/youtube-hermes-config/cpp_subscriber/impact.txt";

const int kSecondsToKeepClientAlive = 1200;

int main() {

  // Creates a Client that polls pubsub and Runs it 
  // passing the MessageProcessor function as a callback.
  using google::pubsub::v1::PubsubMessage;
  using youtube_hermes_config_subscriber::Client;
  using youtube_hermes_config_subscriber::MessageProcessor;

  writeProtoToFile();
  
  Client client = Client(kSubscriptionsLink);
  client.Run(MessageProcessor<PubsubMessage>);
  // std::this_thread::sleep_for(std::chrono::seconds(kSecondsToKeepClientAlive));

  // Currently it takes around 30 seconds for the stream object in the client 
  // to close after calling this Stop method.
  // We will not need to call Stop in production,
  // in Prodoction the client will run indefinitly.
  // client.Stop();
  
  client.JoinThread();
  std::cout << "Program Terminating" << std::endl;
  return 0;
}

int writeProtoToFile() {
    using youtube_hermes_config_subscriber::PublishMessage;
    using youtube_hermes_config_subscriber::getDummyImpactAnalysis;

    ConfigChangeRequest request;
    std::string impact = getDummyImpactAnalysis(request);

    std::ofstream impactFile;
    impactFile.open (kImpactFilePath);
    impactFile << impact;

    PublishMessage(impact, kPublisherTopicLink);
}