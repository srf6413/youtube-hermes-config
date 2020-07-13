# Historical Traffic Database

This document describes Historical Traffic Database, provides context on the tables in the database, and contains the Spanner Schema.

The Historical Traffic DataBase stores the current state of the configuration rules, (enqueuing, routing, and queue info), as well as historical data of video life-cycles within the system.


# Database Tables
The Database is composed of the following tables:
- Queues
- EnqueueRule
- Videos
- EnqueueSignal
- RoutedSignal
- VerdictSignal


# Spanner Schema

```sql
# The queue table contains information on the routing data for each queue, the owners of the queue, the name of the queue, and the desired SLA time in minutes.

CREATE TABLE Queues (
    Id             STRING(MAX) NOT NULL,
    QueueName      STRING(MAX) NOT NULL,        # The name of the queue.
    Owners         ARRAY<STRING(MAX)> NOT NULL, # A list of the queue owners emails.
    PossibleRoutes ARRAY<INT64> NOT NULL,       # A list of Queue Ids specifying where videos in this queue can route to.
    DesiredSLA_min INT64 NOT NULL,              # The target service time for processing videos in this queue.
) PRIMARY KEY(Id);
```
<br>

```sql
# The video table stores records of the videos signaled for review and the videos features.

CREATE TABLE Videos (
    Id          STRING(MAX) NOT NULL,
    Features    ARRAY<STRING(MAX)> NOT NULL, # A List of features pertaining to the video.
    Likes       INT64 NOT NULL,              # The video's like count.
    Dislikes    INT64 NOT NULL,              # The video's dislike count.
) PRIMARY KEY(Id);
```
<br>

```sql
# The EnqueueSignal table stores historical records of when a video is enqueued, which video was enqueued, the violation the video was flagged for, which queue the video was enqueued to, and which life-cycle the signal is a part of.

CREATE TABLE EnqueueSignal (
    LifeCycleId        STRING(MAX) NOT NULL, # The Id representing which life-cycle the enqueue signal is a part of.
    VideoId            STRING(MAX) NOT NULL, # The Id for the Video this signal is link to.
    QueueMatch         INT64 NOT NULL,       # The Id of the queue that the video is being matched to.
    ViolationCategory  STRING(MAX) NOT NULL, # The violation category that the video is being reviewed for.
    CreateTime         TIMESTAMP NOT NULL,   # The timestamp of when the signal occured.
    FOREIGN KEY (VideoId) REFERENCES Videos (Id)
) PRIMARY KEY(LifeCycleId);
```
<br>

```sql
# The RoutedSignal table stores historical records of when a video was routed, which video was routed, which queue it was routed from/to, and which life-cycle the signal is a part of.

CREATE TABLE RoutedSignal (
    LifeCycleId STRING(MAX) NOT NULL, # The Id representing which life-cycle the signal is a part of.
    ToQueue     STRING(MAX) NOT NULL, # The Id of the queue the video was routed to.
    FromQueue   STRING(MAX) NOT NULL, # The Id of the queue the video was routed from.
    CreateTime  TIMESTAMP NOT NULL,   # The timestamp of when the signal occured.
) PRIMARY KEY(LifeCycleId, CreateTime);
```
<br>

```sql
# The VerdictSignal table stores historical records of when a reviewer completed their review of a video, the reviewers verdict, the SLA (the time it took for the video to be serviced), and which life-cycle the signal is a part of.

CREATE TABLE VerdictSignal (
    LifeCycleId   STRING(MAX) NOT NULL, # The Id representing which life-cycle the signal is a part of.
    CreateTime    TIMESTAMP NOT NULL,   # The timestamp of when the signal occured.
    QueueId       STRING(MAX) NOT NULL, # The Id of the queue the video was in when the review verdict was made.
    TotalSLA_min       INT64 NOT NULL,  # The total service time in minutes of the video from when it was enqueued till the verdict.
) PRIMARY KEY(LifeCycleId, CreateTime);
```
<br>

```sql
#The EnqueueRule table stores the rules that map which queue a video should be enqueued when they first enter the system based on the video's features.

CREATE TABLE EnqueueRule (
    Id         STRING(MAX) NOT NULL,
    QueueId    STRING(MAX) NOT NULL, # The queue that this enqueue rule maps to.
    Rule       STRING(MAX) NOT NULL, # The rules defining what video features match with this EnqueueRule. 
    Priority   INT64 NOT NULL,       # The priority of the EnqueueRule. A lower priority takes precedence.
    FOREIGN KEY (QueueId) REFERENCES Queues (Id)
) PRIMARY KEY(Id);
``` 
<br>    


