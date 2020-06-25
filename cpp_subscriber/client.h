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

#ifndef YOUTUBE_HERMES_CONFIG_SUBSCRIBER_CLIENT_H
#define YOUTUBE_HERMES_CONFIG_SUBSCRIBER_CLIENT_H

#include <string>
#include <thread>

#include "absl/strings/string_view.h"

#include "processor.h"
namespace youtube_hermes_config_subscriber {

class Client {
 public:
   /**
   * Constructs a `Client` object that connects to a pubsub subscription based off 
   * of the @p pubsub_subscription_link opts.
   *
   * See `Run(MessageCallback callback)` for how to start client, and pass a 
   * callback that will be triggered when the subscription received a new
   * published method.
   */
  explicit Client(absl::string_view pubsub_subscription_link)
      : is_running_(false), pubsub_subscription_link_(pubsub_subscription_link) {}

  /// No default construction. Use `Client(std::string pubsub_subscription_link)`
  Client() = delete;

  /**
   * Returns the link to the pubsub subscription the client connects to.
  */
  std::string get_pubsub_subscription_link();

  /**
   * Starts the client by running `RunThreadFunction(MessageCallback callback)` in
   * a new thread. Sets is_running_ to true, and sets *thread_ to point to the thread 
   * that was created.
   * 
   * If called when is_running_ equals true, then the method returns without
   * doing anything.
  */
  void Run(MessageCallback);// callback);

  /**
   * If the client is running then this function will cause the thread that called
   * this method to wait until the thread running the client is finished running.
   * 
   * This does not happen immediatly after `Stop()` is called, as thread_ does not
   * terminate immediatly, it terminates once the stream object created in
   * `void RunThreadFunction(MessageCallback callback)` naturally closes
   * which happens around 30 seconds after not receiveing any messages from the
   * pubsub subscription .
  */
  void JoinThread();

  /**
   * If the client is running then sets is_running_ to false which will prevent
   * the thread thats is running the pubsub subscriber from staying alive.
   * 
   * If called when is_running_ is already false then the method 
   * returns without doing anything.
   * 
  */
  void Stop();

  bool IsRunning();

 private:
  bool is_running_;
  // std::thread* thread_;
  std::unique_ptr<std::thread> thread_;
  std::string pubsub_subscription_link_;

  /**
   * The function in charge of connecting to the pubsub subscription
   * This function is called by the `Run(MessageCallback callback)` method
   * and is ran in a new thread to prevent the thread that  calls this method
   * from yeilding.
  */
  void RunThreadFunction(MessageCallback);// callback);
};

}  // namespace youtube_hermes_config_subscriber

#endif  // YOUTUBE_HERMES_CONFIG_SUBSCRIBER_CLIENT_H