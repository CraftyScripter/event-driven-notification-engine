# Event Driven Notification Engine - Learning & Build Journal

## Goal

Mera objective sirf notification service banana nahi hai.

Mujhe ye concepts deeply samajhne hain:

* Event Driven Architecture
* RabbitMQ
* Message Queues
* Event Contracts
* Schema Validation
* Event Routing
* Handler Pattern
* Provider Pattern
* Idempotency
* Retry Mechanisms
* Dead Letter Queues
* Production Grade Microservice Design

---

# Learning Rule

Har step me:

1. Pehle problem samjho
2. Fir architecture decision lo
3. Fir folder/file identify karo
4. Fir implementation karo

Kabhi bhi direct code nahi.

Question:

```text
Ye file kyu exist karti hai?
```

Jab answer clear ho tabhi code likhna hai.

---

# Final Architecture

```text
Producer Service
      │
      ▼
   RabbitMQ
      │
      ▼
   Consumer
      │
      ▼
 Schema Validation
      │
      ▼
    Registry
      │
      ▼
    Handler
      │
      ▼
Notification Service
      │
      ▼
   Provider
      │
      ▼
 User
```

---

# Current Folder Structure

```text
notification-service/

├── main.py
│
├── core/
│   ├── config.py
│   ├── database.py
│   ├── enums.py
│   └── constants.py
│
├── consumers/
│
├── events/
│   ├── schemas/
│   ├── handlers/
│   └── registry.py
│
├── notifications/
│   ├── providers/
│   └── templates/
│
└── tests/
```

---

# What Has Been Decided

## Event Structure

Every event follows:

```json
{
  "event_id": "...",
  "event_type": "...",
  "timestamp": "...",
  "source": "...",
  "data": {}
}
```

Reason:

* Common contract
* Validation
* Routing
* Debugging
* Tracing

---

## Event Naming Convention

Chosen format:

```text
auth.otp_sent
auth.password_reset_requested

order.created
order.shipped

payment.completed
```

Reason:

Domain driven naming.

---

## Notification Channel

Chosen approach:

```text
sms
email
push
whatsapp
```

Stored as Enum.

Reason:

Avoid magic strings.

---

## OTP Event Design

Payload:

```json
{
  "event_id": "evt_001",
  "event_type": "auth.otp_sent",
  "timestamp": "...",
  "source": "auth-service",
  "data": {
    "channel": "sms",
    "recipient": "+919999999999",
    "otp": "123456"
  }
}
```

Reason:

Notification service should decide provider.

Producer should only decide channel.

---

# Files Implemented

## core/enums.py

Purpose:

Central place for:

* EventType
* NotificationChannel

Status:

Completed

---

## events/schemas/base.py

Purpose:

Base contract for every event.

Responsibilities:

* event_id validation
* event_type validation
* timestamp validation
* source validation
* data container

Status:

Completed

---

## events/schemas/otp.py

Purpose:

OTP specific event schema.

Responsibilities:

Validate:

* channel
* recipient
* otp

Status:

Completed

---

# Current Learning Position

Next File:

```text
events/registry.py
```

Problem to solve:

```text
Consumer received an event.

How does it know which handler to execute?
```

Architecture Decision:

Registry Pattern

```text
EventType
      ↓
 Handler
```

Example:

```text
auth.otp_sent
      ↓
OtpHandler

order.created
      ↓
OrderCreatedHandler
```

---

# Future Learning Order

## Step 1

events/registry.py

Learn:

* Registry Pattern
* Event Routing

---

## Step 2

events/handlers/base.py

Learn:

* Common Handler Contract
* Polymorphism

---

## Step 3

events/handlers/otp_handler.py

Learn:

* Business Logic Layer
* Handler Responsibility

---

## Step 4

notifications/service.py

Learn:

* Service Layer
* Channel Routing

---

## Step 5

notifications/providers/base.py

Learn:

* Provider Abstraction
* Strategy Pattern

---

## Step 6

notifications/providers/sms_provider.py

Learn:

* Actual Notification Delivery

---

## Step 7

consumers/rabbitmq_consumer.py

Learn:

* Queue Consumption
* Event Processing Flow

---

## Step 8

consumers/startup.py

Learn:

* Application Startup Lifecycle

---

## Phase 2

Additional Events:

* Order Created
* Order Shipped
* Payment Completed

---

## Phase 3

Templates

Learn:

* Template Rendering
* Dynamic Notifications

---

## Phase 4

Idempotency

Learn:

* Duplicate Detection
* Event Tracking

---

## Phase 5

Retry Mechanism

Learn:

* Exponential Backoff
* Failure Recovery

---

## Phase 6

Dead Letter Queue

Learn:

* Poison Messages
* Failure Isolation

---

## Phase 7

Production Hardening

Learn:

* Structured Logging
* Monitoring
* Metrics
* Security

