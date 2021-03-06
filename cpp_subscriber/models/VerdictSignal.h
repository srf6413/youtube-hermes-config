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

#ifndef YOUTUBE_HERMES_CONFIG_SUBSCRIBER_MODELS_VERDICTSIGNAL_H
#define YOUTUBE_HERMES_CONFIG_SUBSCRIBER_MODELS_VERDICTSIGNAL_H

#include <string>
#include <vector>
#include "google/cloud/spanner/timestamp.h"

namespace youtube_hermes_config_subscriber {

class VerdictSignal {
 public:

  explicit VerdictSignal(){}

  std::string life_cycle_id_;
  google::cloud::spanner::v1::Timestamp create_time_;
  std::string queue_id_;
  int SLA_min_;
};

}  // namespace youtube_hermes_config_subscriber

#endif  // YOUTUBE_HERMES_CONFIG_SUBSCRIBER_MODELS_VERDICTSIGNAL_H

/*
LifeCycleId	STRING(MAX)	No
CreateTime	TIMESTAMP	No
QueueId	STRING(MAX)	No
SLA_min	INT64	No
*/