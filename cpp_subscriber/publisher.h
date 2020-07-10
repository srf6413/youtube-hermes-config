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

#ifndef YOUTUBE_HERMES_CONFIG_SUBSCRIBER_PUBLISHER_H
#define YOUTUBE_HERMES_CONFIG_SUBSCRIBER_PUBLISHER_H

#include <google/protobuf/stubs/statusor.h>
#include <grpc++/grpc++.h>

#include <sstream>
#include <string>
#include <thread>
#include <vector>

#include "google/pubsub/v1/pubsub.grpc.pb.h"
#include "proto/config_change.pb.h"
#include "google/pubsub/v1/pubsub.grpc.pb.h"
#include "absl/strings/string_view.h"

namespace youtube_hermes_config_subscriber {

void PublishMessage(const std::string message_data, const std::string topic) {
  using grpc::ClientContext;
  using google::pubsub::v1::Publisher;
  using google::pubsub::v1::PublishRequest;
  using google::pubsub::v1::PublishResponse;
  using google::pubsub::v1::PubsubMessage;

  auto credentials = grpc::GoogleDefaultCredentials();
  auto channel = grpc::CreateChannel("pubsub.googleapis.com", credentials);
  std::unique_ptr<Publisher::Stub> stub(Publisher::NewStub(channel));

  PublishRequest request;
  request.set_topic(topic);
  PubsubMessage message;
  message.set_data(message_data);
  *request.add_messages() = message;

  PublishResponse response;
  ClientContext clientContext;

  auto status = stub->Publish(&clientContext, request, &response);
  if (!status.ok()) {
      std::cout << "failed" + std::to_string(status.error_code()) + ": " + status.error_message() << '\n';
  }

}

}  // namespace youtube_hermes_config_subscriber

#endif  // YOUTUBE_HERMES_CONFIG_SUBSCRIBER_PUBLISHER_H