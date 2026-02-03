# 🚀 AsyncCheckout
### *A Distributed Event-Driven Order Orchestration System*

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2+-092e20?logo=django)](https://www.djangoproject.com/)
[![Celery](https://img.shields.io/badge/Worker-Celery-green?logo=celery)](https://docs.celeryq.dev/)
[![Redis](https://img.shields.io/badge/Broker-Redis-red?logo=redis)](https://redis.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📌 Project Overview

**AsyncCheckout** is a high-reliability backend engine designed to handle the "What happens after you click buy" logic in modern e-commerce. Unlike traditional systems that make users wait for every process to finish, this project implements an **Event-Driven Architecture** to handle payments, inventory, and notifications in the background.

The core focus of this project is **reliability**. It demonstrates how to handle partial system failures, network timeouts, and data consistency in a distributed environment using industry-standard patterns.

---

## 🛠️ Tech Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Backend** | **Django / DRF** | API Management & Business Logic |
| **Task Queue** | **Celery** | Asynchronous Background Processing |
| **Message Broker** | **Redis** | Task distribution and queuing |
| **Database** | **PostgreSQL** | Transactional data storage |
| **Reliability** | **Saga Pattern** | Managing distributed consistency |

---

## 🧠 Architectural Concepts

This project bridges the gap between simple CRUD apps and distributed systems by implementing the following theories:

| Concept | Implementation Logic |
| :--- | :--- |
| **Asynchronous Flow** | Offloads long-running tasks (Payment/Mail) so the UI remains non-blocking. |
| **Idempotency** | Uses unique `idempotency_key` (UUID) to ensure no double-charges on retries. |
| **Retry Logic** | Implements exponential backoff to recover from temporary 3rd-party API failures. |
| **Compensating Trans.** | Automatically triggers "undo" actions (e.g., Refund) if a later step fails. |

---

## 🔄 The Workflow (The Saga Pattern)

1.  **Order API**: User POSTs an order. System creates a `PENDING` record and returns `202 Accepted`.
2.  **Payment Worker**: Background task attempts to process payment via a mock gateway.
3.  **Inventory Worker**: If payment succeeds, stock is reserved. If it fails, order is marked `FAILED`.
4.  **Notification Worker**: Once inventory is locked, a confirmation email is triggered.
5.  **Failure Handling**: If inventory is out of stock *after* payment, a **Refund Task** is automatically queued to ensure data consistency.

---

## 🚀 Key Features

- [x] **Non-blocking API Design**: High-performance request handling.
- [x] **Fault-Tolerant Workers**: Celery workers configured with custom retry limits.
- [x] **Idempotent Transactions**: Guards against duplicate orders and double payments.
- [x] **State Machine Tracking**: Real-time order status updates from `PENDING` to `COMPLETED`.

---

## ⚙️ Installation & Setup

### 1. Prerequisites
* Python 3.10+
* Redis Server (running on localhost:6379)
* PostgreSQL

### 2. Clone the Repository
```bash
git clone [https://github.com/Arkvos/AsyncCheckout.git](https://github.com/Arkvos/AsyncCheckout.git)
cd AsyncCheckout
