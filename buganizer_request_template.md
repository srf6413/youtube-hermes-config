# Template for Buganizer Configuration Change Request

This documents describes and shows examples of the three different templates to create a configuration change request to change the configurations shown below

- Enqueue Rule
- Routing Rule
- Queue Info
<br><br>

# Template Format
The first line of each template specifies the type of configuration change request
```html
Configuration: <TypeOfChange>
```
\<TypeOfChange> must be one of: EnqueueRule, RoutingRule, or QueueInfo
<br><br>

When defining a change the first two lines specifies the Method, and QueueId
```html
Configuration: <TypeOfChange>

Method: <TypeOfMethod>
QueueId: <QueueId>
```
\<TypeOfMethod> must be one of: EnqueueRule, RoutingRule, or QueueInfo
<br><br>
The QueueId specifies which queue the change is being applied to.

An empty line should separate the first line and the rest of the definition of the change. 
It's possible to request multiple configuration changes of the same type by separating the changes by an empty line, (the type of change only needs to be declared once at the very top).<br>

Below are Templates for each type of change with examples.


# EnqueueRule
## Template
```html
Configuration: EnqueueRule

Method: <Add> or <Remove>
QueueId: <QueueId>
Features: <Feature>, <Feature>, <Feature>, ...
Priority: <PriorityNumber>
```
<br>

## Example
```
Configuration: EnqueueRule

Method: Add
QueueId: 3
Features: f1, f2, f3, f4
Priority: 5

Method: Add
QueueId: 3
Features: f5, f7, f10
Priority: 3

Method: Remove
QueueId: 3
Features: f6, f11
Priority: 0
```
<br><br>


# RoutingRule
## Template
```html
Configuration: RoutingRule

Method: <Add> or <Remove>
QueueId: <QueueId>
Possible-Routes: <QueueId>, <QueueId>, <QueueId>, ...
```
<br>

## Example
```
Configuration: RoutingRule

Method: Add
QueueId: 1
Possible-Routes: 2, 3, 4, 5, 6

Method: Remove
QueueId: 1
Possible-Routes: 7
```
<br><br>


# QueueInfo
## Template
```html
Configuration: QueueInfo

Method: <Add> or <Remove>
QueueId: <QueueId>
Owners: <OwnerEmail>, <OwnerEmail>, <OwnerEmail>, ...
```
<br>

## Example
```
Configuration: QueueInfo

Method: Add
QueueId: 1
Owners: isaiah@google.com, saulo@google.com, victor@google.com

Method: Remove
QueueId: 1
Owners: sundar@google.com, larry@google.com, sergey@google.com
```
<br><br>