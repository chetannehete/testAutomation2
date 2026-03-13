# Prompt: Step 09/11 — DOCUMENTATION

---

## Chain Context

| Field | Value |
|-------|-------|
| **Invoked By** | `00_master_prompt.md` |
| **Step** | 09 of 11 |
| **Previous Step** | `08_..._prompt.md` |
| **Next Step** | `10_..._prompt.md` |

Once this step is complete, output: `✅ Step 09 complete — [one-line summary]` and proceed to Step 10.

---

## Purpose
Generate comprehensive Markdown documentation for orderservice

## Conditional Trigger
> Project has 8 classes across 6 packages

## Target Classes
OrderController, Order, OrderStatus, GlobalExceptionHandler, ResourceNotFoundException, OrderEventProducer, OrderRepository, OrderService

---

## Hard Rules (Mandatory)
- **[DOC-H1]** Use Markdown format with proper heading hierarchy (# → ## → ### → ####).
- **[DOC-H2]** Include these sections: Overview, Architecture, Components, API Reference, Configuration, Build & Run.
- **[DOC-H3]** Document every REST endpoint with method, path, request/response body, and status codes.
- **[DOC-H4]** Include a data flow diagram (Mermaid syntax) showing how data moves through layers.
- **[DOC-H5]** Document all configuration properties with their types and defaults.
- **[DOC-H6]** Include a table of service responsibilities (Service → What it does → Dependencies).
- **[DOC-H7]** Write for mixed audience: junior devs, senior engineers, architects, QA engineers.

## Soft Rules (Recommended)
- **[DOC-S1]** Add sequence diagrams for complex multi-service flows.
- **[DOC-S2]** Include code examples for key configurations.
- **[DOC-S3]** Add a 'Getting Started' quick-start section.
- **[DOC-S4]** Document error codes and their meanings.
- **[DOC-S5]** Include a glossary of domain terms.

---

## Execution Steps
1. Analyze project structure and identify main packages
2. Describe the high-level architecture and layer interactions
3. Create a component inventory with responsibilities
4. Document all REST API endpoints in tabular format
5. Describe the data model and entity relationships
6. List all configuration properties with defaults
7. Generate Mermaid data flow diagrams
8. Write build and run instructions
9. Document error handling patterns

---

## Prompt Template

You are a principal software architect. Generate comprehensive technical documentation in Markdown for the following Spring Boot microservice.

## Project Information
Project: orderservice
Total Classes: 8
Controllers: 1
Services: 1
Repositories: 1
Entities: 1
Packages: com.example.orderservice.controller, com.example.orderservice.entity, com.example.orderservice.exception, com.example.orderservice.messaging, com.example.orderservice.repository, com.example.orderservice.service

Feature Flags:
  Database: Yes (JPA)
  REST API: Yes
  Messaging: Kafka
  Security: No
  Scheduling: No
  Caching: Yes
  Validation: Yes
  Feign Client: No
  Circuit Breaker: No

Components:
  - [rest_controller] OrderController (6 endpoints) (1 dependencies)
  - [entity] Order
  - [unknown] OrderStatus
  - [exception_handler] GlobalExceptionHandler
  - [unknown] ResourceNotFoundException (2 dependencies)
  - [component] OrderEventProducer (1 dependencies)
  - [repository] OrderRepository
  - [service] OrderService (3 dependencies)


## Requirements

### Mandatory (Hard Rules)
🔴 [DOC-H1] Use Markdown format with proper heading hierarchy (# → ## → ### → ####).
🔴 [DOC-H2] Include these sections: Overview, Architecture, Components, API Reference, Configuration, Build & Run.
🔴 [DOC-H3] Document every REST endpoint with method, path, request/response body, and status codes.
🔴 [DOC-H4] Include a data flow diagram (Mermaid syntax) showing how data moves through layers.
🔴 [DOC-H5] Document all configuration properties with their types and defaults.
🔴 [DOC-H6] Include a table of service responsibilities (Service → What it does → Dependencies).
🔴 [DOC-H7] Write for mixed audience: junior devs, senior engineers, architects, QA engineers.

### Recommended (Soft Rules)
🟡 [DOC-S1] Add sequence diagrams for complex multi-service flows.
🟡 [DOC-S2] Include code examples for key configurations.
🟡 [DOC-S3] Add a 'Getting Started' quick-start section.
🟡 [DOC-S4] Document error codes and their meanings.
🟡 [DOC-S5] Include a glossary of domain terms.

## Required Document Structure

```
# {Project Name} — Technical Documentation

## 1. Overview
   - Purpose and scope
   - Key technologies used

## 2. Architecture
   - High-level architecture description
   - Layer diagram (Controller → Service → Repository → Database)
   - Data flow (Mermaid diagram)

## 3. Components
   - Table: Component | Type | Responsibility | Dependencies
   - Detailed description of each service class

## 4. API Reference
   - Table: Method | Path | Request Body | Response | Status Codes
   - Detailed endpoint documentation

## 5. Data Model
   - Entity descriptions
   - Relationship diagram (if applicable)

## 6. Configuration
   - Application properties table
   - Spring profiles
   - Environment variables

## 7. Build & Run
   - Prerequisites
   - Build commands
   - Run commands with profiles
   - Docker support (if applicable)

## 8. Error Handling
   - Error response format
   - Common error codes
```

Generate the complete documentation now.


---

*Generated by MD Agent Prompt Orchestrator*
