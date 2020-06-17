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

#include "absl/memory/memory.h"
#include "client.h"
#include "config_type.pb.h"
#include "google/pubsub/v1/pubsub.grpc.pb.h"

#include "mock_message.h"
#include "processor.h"

void Debug();
void Start();

int main() {
  Start();
  // Debug();
}

// Creates a Client that polls pubsub and Runs it 
// passing the MessageProcessor function as a callback
void Start() {
  using google::pubsub::v1::PubsubMessage;
  using yoututbe::hermes::config::cppsubscriber::Client;
  using yoututbe::hermes::config::cppsubscriber::MessageProcessor;
  std::string link = "projects/google.com:youtube-admin-pacing-server/subscriptions/CppBinary";

  Client *client = new Client(link);
  client->Run(MessageProcessor<PubsubMessage>);

  // Keep the program alive for atleast 5 minutes
  std::this_thread::sleep_for(std::chrono::seconds(60 * 5));

  // Currently it takes around 30 seconds for the stream object in the client 
  // to close after calling this Stop method
  client->Stop();
  
  client->JoinThread();
  std::cout << "Program Terminating" << std::endl;
}

void Debug() {}