#include <vector>

#include "config_type.pb.h"
#include "gtest/gtest.h"

#include "mock_message.h"
#include "processor.h"

TEST(MessageProcessor, EnqueueRuleTest) {
  using yoututbe::hermes::config::cppsubscriber::MessageProcessor;
  using yoututbe::hermes::config::cppsubscriber::MockMessage;

  // Create ConfigChangeRequest object for MockMessage to serialize to string
  ConfigChangeRequest config;
  EnqueueRule* enqueue_rule = new EnqueueRule();
  EnqueueRule_Change* change = enqueue_rule->add_changes();

  change->set_method("Add");
  change->set_queue("q1");
  change->add_features("f1");
  change->add_features("f2");
  change->add_features("f3");
  change->set_priority(1);

  config.set_allocated_enqueue_rule(enqueue_rule);

  // Create MockMessage and obtain deserialized config request from MessageProcessor function
  MockMessage message = MockMessage(config);
  ConfigChangeRequest* config_change_request = MessageProcessor<MockMessage>(message);
  EnqueueRule_Change enqueue = config_change_request->enqueue_rule().changes(0);

  EXPECT_EQ(config_change_request->has_enqueue_rule(), true);
  EXPECT_EQ(config_change_request->has_routing_rule(), false);
  EXPECT_EQ(config_change_request->has_queue_info(), false);
  EXPECT_EQ(enqueue.method(), "Add");
  EXPECT_EQ(enqueue.queue(), "q1");
  EXPECT_EQ(enqueue.features(0), "f1");
  EXPECT_EQ(enqueue.features(1), "f2");
  EXPECT_EQ(enqueue.features(2), "f3");
  EXPECT_EQ(enqueue.priority(), 1);
}


TEST(MessageProcessor, RoutingRuleTest) {
  using yoututbe::hermes::config::cppsubscriber::MessageProcessor;
  using yoututbe::hermes::config::cppsubscriber::MockMessage;

  // Create ConfigChangeRequest object for MockMessage to serialize to string
  ConfigChangeRequest config;
  RoutingRule* routing_rule = new RoutingRule();
  RoutingRule_Change* change = routing_rule->add_changes();

  change->set_method("Add");
  change->set_queue("q1");
  change->add_possible_routes("q2");
  change->add_possible_routes("q3");
  change->add_possible_routes("q4");

  config.set_allocated_routing_rule(routing_rule);

  // Create MockMessage and obtain deserialized config request from MessageProcessor function
  MockMessage message = MockMessage(config);
  ConfigChangeRequest* config_change_request = MessageProcessor<MockMessage>(message);
  RoutingRule_Change routing = config_change_request->routing_rule().changes(0);

  EXPECT_EQ(config_change_request->has_routing_rule(), true);
  EXPECT_EQ(config_change_request->has_enqueue_rule(), false);
  EXPECT_EQ(config_change_request->has_queue_info(), false);
  EXPECT_EQ(routing.method(), "Add");
  EXPECT_EQ(routing.queue(), "q1");
  EXPECT_EQ(routing.possible_routes(0), "q2");
  EXPECT_EQ(routing.possible_routes(1), "q3");
  EXPECT_EQ(routing.possible_routes(2), "q4");
}

TEST(MessageProcessor, QueueInfoTest) {
  using yoututbe::hermes::config::cppsubscriber::MessageProcessor;
  using yoututbe::hermes::config::cppsubscriber::MockMessage;

  // Create ConfigChangeRequest object for MockMessage to serialize to string
  ConfigChangeRequest config;
  QueueInfo* queue_info = new QueueInfo();
  QueueInfo_Change* change = queue_info->add_changes();

  change->set_method("Add");
  change->set_queue("q1");
  change->add_owner("isaiah");
  change->add_owner("saulo");

  config.set_allocated_queue_info(queue_info);

  // Create MockMessage and obtain deserialized config request from MessageProcessor function
  MockMessage message = MockMessage(config);
  ConfigChangeRequest* config_change_request = MessageProcessor<MockMessage>(message);
  QueueInfo_Change info = config_change_request->queue_info().changes(0);

  EXPECT_EQ(config_change_request->has_queue_info(), true);
  EXPECT_EQ(config_change_request->has_routing_rule(), false);
  EXPECT_EQ(config_change_request->has_enqueue_rule(), false);
  EXPECT_EQ(info.method(), "Add");
  EXPECT_EQ(info.queue(), "q1");
  EXPECT_EQ(info.owner(0), "isaiah");
  EXPECT_EQ(info.owner(1), "saulo");
}

TEST(MessageProcessor, InvalidTest) {
  using yoututbe::hermes::config::cppsubscriber::MessageProcessor;
  using yoututbe::hermes::config::cppsubscriber::MockMessage;

  // Create Empty/Invalid ConfigChangeRequest object for MockMessage to serialize to string
  ConfigChangeRequest config;

  // Create MockMessage and obtain deserialized config request from MessageProcessor function
  MockMessage message = MockMessage(config);
  ConfigChangeRequest* config_change_request = MessageProcessor<MockMessage>(message);

  EXPECT_EQ(config_change_request, nullptr);
}