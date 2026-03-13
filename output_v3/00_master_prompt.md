# MASTER ORCHESTRATOR PROMPT

> **Role:** Root of the nested prompt hierarchy — invokes all child prompts sequentially.
> **Project:** orderservice
> **Child Prompts:** 11

---

You are a senior software engineer, QA lead, and architect working on the **orderservice** Spring Boot microservice.

You are executing a full, automated test and documentation generation session. This master prompt is the **root of a nested prompt hierarchy** — it drives 11 child prompts in order. Work through every step sequentially without skipping.

---

## Project Summary

**Project:** orderservice
**Total Classes:** 8 &nbsp;|&nbsp; **Controllers:** 1 &nbsp;|&nbsp; **Services:** 1 &nbsp;|&nbsp; **Repositories:** 1

### Feature Matrix
| Feature | Detected |
|---------|----------|
| REST Controllers   | Yes (1) |
| Database / JPA     | Yes (JPA) |
| Messaging          | Kafka |
| Security           | No |
| Caching            | Yes |
| Validation         | Yes |
| Exception Handling | Yes |
| Scheduling         | No |

### Component Inventory
| Class | Type | Endpoints | Dependencies |
|-------|------|-----------|--------------|
| OrderController | rest_controller | 6 endpoint(s) | OrderService |
| Order | entity | — | — |
| OrderStatus | unknown | — | — |
| GlobalExceptionHandler | exception_handler | — | — |
| ResourceNotFoundException | unknown | — | String, Throwable |
| OrderEventProducer | component | — | KafkaTemplate<String, Object> |
| OrderRepository | repository | — | — |
| OrderService | service | — | OrderRepository, OrderMapper, OrderEventProducer |

---

## Global Rules (Apply to ALL Steps)

### Mandatory
🔴 [GL-H1] Use Java 17+ features and idioms throughout all generated code.
🔴 [GL-H2] All generated Java files must be fully compilable without modification.
🔴 [GL-H3] Process sub-tasks strictly in the order listed in the Invocation Chain.
🔴 [GL-H4] After each step output: ✅ Step N complete — [one-line summary].
🔴 [GL-H5] Do not skip any step, even if output seems similar to a previous step.
🔴 [GL-H6] Each child prompt file contains full details, hard rules, and templates for its step.

### Recommended
🟡 [GL-S1] After all steps complete, produce a final summary table: Step | Output | Status.
🟡 [GL-S2] If a step fails or must be skipped, explain why before moving to the next.
🟡 [GL-S3] Keep each step's output in a clearly labelled section.

---

## Invocation Chain — 11 Child Prompts

Execute each child prompt **in the order listed below**. For full rules and code templates, open the corresponding file.

| Step | File | Type | Purpose | Target |
|------|------|------|---------|--------|
| 01 | `01_unit_test_prompt.md` | Unit Test | Generate JUnit5 + Mockito unit tests for OrderController | OrderController |
| 02 | `02_unit_test_prompt.md` | Unit Test | Generate JUnit5 + Mockito unit tests for GlobalExceptionHandler | GlobalExceptionHandler |
| 03 | `03_unit_test_prompt.md` | Unit Test | Generate JUnit5 + Mockito unit tests for OrderEventProducer | OrderEventProducer |
| 04 | `04_unit_test_prompt.md` | Unit Test | Generate JUnit5 + Mockito unit tests for OrderRepository | OrderRepository |
| 05 | `05_unit_test_prompt.md` | Unit Test | Generate JUnit5 + Mockito unit tests for OrderService | OrderService |
| 06 | `06_integration_test_prompt.md` | Integration Test | Generate REST API integration tests for OrderController | OrderController |
| 07 | `07_integration_test_prompt.md` | Integration Test | Generate database integration tests for OrderRepository | OrderRepository |
| 08 | `08_e2e_test_prompt.md` | E2E Test | Generate end-to-end tests for orderservice | OrderController |
| 09 | `09_documentation_prompt.md` | Documentation | Generate comprehensive Markdown documentation for orderservice | OrderController, Order (+6 more) |
| 10 | `10_c4_architecture_prompt.md` | C4 Architecture | Generate C4 architecture diagrams (PlantUML) for orderservice | OrderController, Order (+6 more) |
| 11 | `11_run_arguments_prompt.md` | Run Arguments | Generate runtime execution arguments for orderservice | Project-level |

---

## Inline Sub-Task Summaries

The summaries below give you enough context to understand each step. Always open the child file for the complete rules and templates before generating output.

### Step 01 — Generate JUnit5 + Mockito unit tests for OrderController
> **File:** `01_unit_test_prompt.md` &nbsp;|&nbsp; **Trigger:** Class OrderController is a rest_controller with 6 testable methods

**Hard Rules (10)** *(top 3 shown)*:
  - 🔴 [UT-H1] Use JUnit5 (@Test, @BeforeEach, @AfterEach, @DisplayName) — no JUnit4.
  - 🔴 [UT-H2] Use Mockito (@Mock, @InjectMocks, @ExtendWith(MockitoExtension.class)) for all dependencies.
  - 🔴 [UT-H3] Follow Arrange-Act-Assert (AAA) pattern in every test method.
  - *(+7 more hard rules in child file)*

**Soft Rules:** 7 additional recommendations in child file.

**First Execution Step:** 1. Read the source class and identify all public methods

### Step 02 — Generate JUnit5 + Mockito unit tests for GlobalExceptionHandler
> **File:** `02_unit_test_prompt.md` &nbsp;|&nbsp; **Trigger:** Class GlobalExceptionHandler is a exception_handler with 3 testable methods

**Hard Rules (10)** *(top 3 shown)*:
  - 🔴 [UT-H1] Use JUnit5 (@Test, @BeforeEach, @AfterEach, @DisplayName) — no JUnit4.
  - 🔴 [UT-H2] Use Mockito (@Mock, @InjectMocks, @ExtendWith(MockitoExtension.class)) for all dependencies.
  - 🔴 [UT-H3] Follow Arrange-Act-Assert (AAA) pattern in every test method.
  - *(+7 more hard rules in child file)*

**Soft Rules:** 7 additional recommendations in child file.

**First Execution Step:** 1. Read the source class and identify all public methods

### Step 03 — Generate JUnit5 + Mockito unit tests for OrderEventProducer
> **File:** `03_unit_test_prompt.md` &nbsp;|&nbsp; **Trigger:** Class OrderEventProducer is a component with 4 testable methods

**Hard Rules (10)** *(top 3 shown)*:
  - 🔴 [UT-H1] Use JUnit5 (@Test, @BeforeEach, @AfterEach, @DisplayName) — no JUnit4.
  - 🔴 [UT-H2] Use Mockito (@Mock, @InjectMocks, @ExtendWith(MockitoExtension.class)) for all dependencies.
  - 🔴 [UT-H3] Follow Arrange-Act-Assert (AAA) pattern in every test method.
  - *(+7 more hard rules in child file)*

**Soft Rules:** 7 additional recommendations in child file.

**First Execution Step:** 1. Read the source class and identify all public methods

### Step 04 — Generate JUnit5 + Mockito unit tests for OrderRepository
> **File:** `04_unit_test_prompt.md` &nbsp;|&nbsp; **Trigger:** Class OrderRepository is a repository with 5 testable methods

**Hard Rules (10)** *(top 3 shown)*:
  - 🔴 [UT-H1] Use JUnit5 (@Test, @BeforeEach, @AfterEach, @DisplayName) — no JUnit4.
  - 🔴 [UT-H2] Use Mockito (@Mock, @InjectMocks, @ExtendWith(MockitoExtension.class)) for all dependencies.
  - 🔴 [UT-H3] Follow Arrange-Act-Assert (AAA) pattern in every test method.
  - *(+7 more hard rules in child file)*

**Soft Rules:** 7 additional recommendations in child file.

**First Execution Step:** 1. Read the source class and identify all public methods

### Step 05 — Generate JUnit5 + Mockito unit tests for OrderService
> **File:** `05_unit_test_prompt.md` &nbsp;|&nbsp; **Trigger:** Class OrderService is a service with 7 testable methods

**Hard Rules (10)** *(top 3 shown)*:
  - 🔴 [UT-H1] Use JUnit5 (@Test, @BeforeEach, @AfterEach, @DisplayName) — no JUnit4.
  - 🔴 [UT-H2] Use Mockito (@Mock, @InjectMocks, @ExtendWith(MockitoExtension.class)) for all dependencies.
  - 🔴 [UT-H3] Follow Arrange-Act-Assert (AAA) pattern in every test method.
  - *(+7 more hard rules in child file)*

**Soft Rules:** 7 additional recommendations in child file.

**First Execution Step:** 1. Read the source class and identify all public methods

### Step 06 — Generate REST API integration tests for OrderController
> **File:** `06_integration_test_prompt.md` &nbsp;|&nbsp; **Trigger:** REST controller OrderController has 6 endpoints

**Hard Rules (8)** *(top 3 shown)*:
  - 🔴 [IT-H1] Use @SpringBootTest for full context or @WebMvcTest for controller-only tests.
  - 🔴 [IT-H2] Use @AutoConfigureMockMvc and MockMvc for REST API tests.
  - 🔴 [IT-H3] Use @DataJpaTest with @AutoConfigureTestDatabase for repository tests.
  - *(+5 more hard rules in child file)*

**Soft Rules:** 5 additional recommendations in child file.

**First Execution Step:** 1. Identify the component type and its external dependencies

### Step 07 — Generate database integration tests for OrderRepository
> **File:** `07_integration_test_prompt.md` &nbsp;|&nbsp; **Trigger:** Repository OrderRepository accesses database layer

**Hard Rules (8)** *(top 3 shown)*:
  - 🔴 [IT-H1] Use @SpringBootTest for full context or @WebMvcTest for controller-only tests.
  - 🔴 [IT-H2] Use @AutoConfigureMockMvc and MockMvc for REST API tests.
  - 🔴 [IT-H3] Use @DataJpaTest with @AutoConfigureTestDatabase for repository tests.
  - *(+5 more hard rules in child file)*

**Soft Rules:** 5 additional recommendations in child file.

**First Execution Step:** 1. Identify the component type and its external dependencies

### Step 08 — Generate end-to-end tests for orderservice
> **File:** `08_e2e_test_prompt.md` &nbsp;|&nbsp; **Trigger:** Project has 1 controllers with 6 endpoints

**Hard Rules (6)** *(top 3 shown)*:
  - 🔴 [E2E-H1] Use @SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT).
  - 🔴 [E2E-H2] Use TestRestTemplate or WebTestClient for real HTTP calls.
  - 🔴 [E2E-H3] Test complete user flows — not isolated units.
  - *(+3 more hard rules in child file)*

**Soft Rules:** 3 additional recommendations in child file.

**First Execution Step:** 1. Map all endpoints into user-facing scenarios

### Step 09 — Generate comprehensive Markdown documentation for orderservice
> **File:** `09_documentation_prompt.md` &nbsp;|&nbsp; **Trigger:** Project has 8 classes across 6 packages

**Hard Rules (7)** *(top 3 shown)*:
  - 🔴 [DOC-H1] Use Markdown format with proper heading hierarchy (# → ## → ### → ####).
  - 🔴 [DOC-H2] Include these sections: Overview, Architecture, Components, API Reference, Configuration, Build & Run.
  - 🔴 [DOC-H3] Document every REST endpoint with method, path, request/response body, and status codes.
  - *(+4 more hard rules in child file)*

**Soft Rules:** 5 additional recommendations in child file.

**First Execution Step:** 1. Analyze project structure and identify main packages

### Step 10 — Generate C4 architecture diagrams (PlantUML) for orderservice
> **File:** `10_c4_architecture_prompt.md` &nbsp;|&nbsp; **Trigger:** Project has 8 classes with inter-component dependencies

**Hard Rules (7)** *(top 3 shown)*:
  - 🔴 [C4-H1] Use PlantUML syntax with C4-PlantUML library (!include C4_*).
  - 🔴 [C4-H2] Generate Context diagram (System → External Systems).
  - 🔴 [C4-H3] Generate Container diagram (showing application containers and data stores).
  - *(+4 more hard rules in child file)*

**Soft Rules:** 4 additional recommendations in child file.

**First Execution Step:** 1. Identify the system boundary and external actors

### Step 11 — Generate runtime execution arguments for orderservice
> **File:** `11_run_arguments_prompt.md` &nbsp;|&nbsp; **Trigger:** Project analysis completed — run arguments always generated

**Hard Rules (6)** *(top 3 shown)*:
  - 🔴 [RUN-H1] Provide CLI commands using `java -jar` format.
  - 🔴 [RUN-H2] Include Spring profile activation (--spring.profiles.active=).
  - 🔴 [RUN-H3] Include essential JVM parameters (-Xms, -Xmx, -XX:+UseG1GC).
  - *(+3 more hard rules in child file)*

**Soft Rules:** 4 additional recommendations in child file.

**First Execution Step:** 1. Identify required environment variables from configuration

---

## Session Execution Instructions

```
FOR i = 01 TO 11:
  1. Open child file listed in Step i of the Invocation Chain
  2. Read all Hard Rules and Soft Rules in that file
  3. Generate the required output (Java file / Markdown / PlantUML)
  4. Output: ✅ Step i complete — [one-line description of what was produced]
  5. GOTO Step i+1
END FOR
```

After Step 11, produce a final session summary:

```
## Session Complete — orderservice
| Step | Child File | Output Artifact | Status |
|------|-----------|-----------------|--------|
| 01   | ...       | ...             | ✅     |
...
```

**Begin with Step 01 now.**


---

*Generated by MD Agent Prompt Orchestrator — Master Prompt*
