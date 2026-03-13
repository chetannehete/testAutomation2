"""
Prompt Templates for the Nested Prompt Generation System.

Each function produces a GeneratedPrompt with:
  - Purpose
  - Hard Rules (mandatory LLM constraints)
  - Soft Rules (recommended best practices)
  - Rendered template body (the actual prompt text)
  - Conditional trigger explanation
  - Step-by-step execution plan
"""

from __future__ import annotations

from typing import List, Optional

from md_agent.models import (
    ClassInfo,
    CodebaseAnalysis,
    ComponentType,
    EndpointInfo,
    GeneratedPrompt,
    PromptRule,
    PromptType,
    SpringComponent,
)


# ═══════════════════════════════════════════════════════════════════════
#  UNIT TEST PROMPT
# ═══════════════════════════════════════════════════════════════════════

def build_unit_test_prompt(
    component: SpringComponent,
    analysis: CodebaseAnalysis,
) -> GeneratedPrompt:
    """Build a prompt for generating JUnit5 + Mockito unit tests."""

    cls = component.class_info
    deps = component.dependencies
    dep_list = ", ".join(f"{d.type} {d.field_name}" for d in deps) if deps else "None"

    # Build context — source code summary
    context_lines = [
        f"Class: {cls.name}",
        f"Package: {cls.package or 'default'}",
        f"Component Type: {component.component_type.value}",
        f"Dependencies: {dep_list}",
        f"Methods ({len(cls.methods)}):",
    ]
    for m in cls.methods:
        param_sig = ", ".join(f"{p.type} {p.name}" for p in m.parameters)
        exc_str = f" throws {', '.join(m.exceptions)}" if m.exceptions else ""
        context_lines.append(
            f"  - {' '.join(m.modifiers)} {m.return_type} {m.name}({param_sig}){exc_str}"
        )
        if m.javadoc:
            context_lines.append(f"    Javadoc: {m.javadoc[:120]}...")

    context = "\n".join(context_lines)

    # Hard Rules
    hard_rules = [
        PromptRule("UT-H1", "Use JUnit5 (@Test, @BeforeEach, @AfterEach, @DisplayName) — no JUnit4.", True),
        PromptRule("UT-H2", "Use Mockito (@Mock, @InjectMocks, @ExtendWith(MockitoExtension.class)) for all dependencies.", True),
        PromptRule("UT-H3", "Follow Arrange-Act-Assert (AAA) pattern in every test method.", True),
        PromptRule("UT-H4", "Use @DisplayName with descriptive English sentences for every test.", True),
        PromptRule("UT-H5", f"Test class name must be {cls.name}Test.", True),
        PromptRule("UT-H6", "Each test must be independent — no shared mutable state.", True),
        PromptRule("UT-H7", "Verify interactions using Mockito.verify() for void dependency calls.", True),
        PromptRule("UT-H8", "Test naming convention: should_ExpectedBehavior_When_Condition().", True),
        PromptRule("UT-H9", "Include tests for: happy path, null inputs, boundary values, and exception scenarios.", True),
        PromptRule("UT-H10", "Use assertThrows() for exception testing, not try-catch.", True),
    ]

    # Soft Rules
    soft_rules = [
        PromptRule("UT-S1", "Use @ParameterizedTest with @ValueSource or @MethodSource for methods with multiple valid inputs.", False),
        PromptRule("UT-S2", "Use ArgumentCaptor when verifying complex objects passed to mocks.", False),
        PromptRule("UT-S3", "Group tests using @Nested inner classes by method under test.", False),
        PromptRule("UT-S4", "Add // Arrange, // Act, // Assert comments in every test.", False),
        PromptRule("UT-S5", "Keep each test under 20 lines for readability.", False),
        PromptRule("UT-S6", "Use factory methods or builders for complex test data.", False),
        PromptRule("UT-S7", "Test private methods indirectly through public API.", False),
    ]

    # Build the prompt template
    template = f"""You are a senior Java test engineer. Generate comprehensive JUnit5 unit tests with Mockito for the following Spring Boot class.

## Source Class Information
{context}

## Dependencies to Mock
{_format_dependencies(deps)}

## Requirements

### Mandatory (Hard Rules)
{_format_rules(hard_rules)}

### Recommended (Soft Rules)
{_format_rules(soft_rules)}

## Output Format
- Produce a single compilable Java test file: `{cls.name}Test.java`
- Package: `{cls.package or 'default'}`
- Include all necessary imports
- Cover AT MINIMUM:
  - 1 happy-path test per public method
  - 1 null-input test per nullable parameter
  - 1 boundary test per numeric parameter
  - 1 exception test per declared exception

## Test Structure Template
```java
@ExtendWith(MockitoExtension.class)
@DisplayName("{cls.name} Unit Tests")
class {cls.name}Test {{

    @Mock
    private DependencyType dependencyName;

    @InjectMocks
    private {cls.name} {cls.name[0].lower() + cls.name[1:]};

    @BeforeEach
    void setUp() {{
        // Common setup
    }}

    @Nested
    @DisplayName("methodName tests")
    class MethodNameTests {{

        @Test
        @DisplayName("should return expected result when valid input provided")
        void should_ReturnExpected_When_ValidInput() {{
            // Arrange
            // Act
            // Assert
        }}
    }}
}}
```

Generate the complete test file now.
"""

    # Execution steps
    steps = [
        "1. Read the source class and identify all public methods",
        "2. Identify all injected dependencies that need mocking",
        "3. Create @Mock for each dependency and @InjectMocks for the class under test",
        "4. For each public method, generate @Nested class with:",
        "   a. Happy-path test with valid inputs",
        "   b. Null-input tests for each nullable parameter",
        "   c. Boundary tests for numeric parameters (0, negative, MAX_VALUE)",
        "   d. Exception tests for each declared exception",
        "5. Verify mock interactions with Mockito.verify()",
        "6. Ensure all tests follow AAA pattern with @DisplayName",
        "7. Add parametrized tests where multiple input variations make sense",
    ]

    trigger = f"Class {cls.name} is a {component.component_type.value} with {len(cls.methods)} testable methods"

    return GeneratedPrompt(
        prompt_type=PromptType.UNIT_TEST,
        purpose=f"Generate JUnit5 + Mockito unit tests for {cls.name}",
        hard_rules=hard_rules,
        soft_rules=soft_rules,
        context=context,
        template_body=template,
        target_classes=[cls.name],
        conditional_trigger=trigger,
        execution_steps=steps,
    )


# ═══════════════════════════════════════════════════════════════════════
#  INTEGRATION TEST PROMPT
# ═══════════════════════════════════════════════════════════════════════

def build_integration_test_prompt(
    component: SpringComponent,
    analysis: CodebaseAnalysis,
    test_type: str = "api",  # api | db | messaging
) -> GeneratedPrompt:
    """Build a prompt for generating Spring Boot integration tests."""

    cls = component.class_info
    features = analysis.features

    # Context varies by test type
    if test_type == "api":
        specific_context = _build_api_test_context(component)
        purpose = f"Generate REST API integration tests for {cls.name}"
        trigger = f"REST controller {cls.name} has {len(component.endpoints)} endpoints"
    elif test_type == "db":
        specific_context = _build_db_test_context(component, analysis)
        purpose = f"Generate database integration tests for {cls.name}"
        trigger = f"Repository {cls.name} accesses database layer"
    elif test_type == "messaging":
        specific_context = _build_messaging_test_context(component, features)
        purpose = f"Generate messaging integration tests for {cls.name}"
        trigger = f"Component {cls.name} uses {'Kafka' if features.has_kafka else 'RabbitMQ'} messaging"
    else:
        specific_context = ""
        purpose = f"Generate integration tests for {cls.name}"
        trigger = f"Component {cls.name} requires integration testing"

    # Hard Rules
    hard_rules = [
        PromptRule("IT-H1", "Use @SpringBootTest for full context or @WebMvcTest for controller-only tests.", True),
        PromptRule("IT-H2", "Use @AutoConfigureMockMvc and MockMvc for REST API tests.", True),
        PromptRule("IT-H3", "Use @DataJpaTest with @AutoConfigureTestDatabase for repository tests.", True),
        PromptRule("IT-H4", "Test class name must end with 'IT' (e.g., UserControllerIT).", True),
        PromptRule("IT-H5", "Use @Transactional and @Rollback for DB tests to avoid side effects.", True),
        PromptRule("IT-H6", "Use TestContainers for external dependencies (DB, Kafka, Redis) when applicable.", True),
        PromptRule("IT-H7", "Test HTTP status codes, response body, and headers for API tests.", True),
        PromptRule("IT-H8", "Use @Sql or test data setup methods for database seeding.", True),
    ]

    # Soft Rules
    soft_rules = [
        PromptRule("IT-S1", "Use @TestPropertySource to override application.properties for tests.", False),
        PromptRule("IT-S2", "Use Spring's @ActiveProfiles('test') for test-specific configuration.", False),
        PromptRule("IT-S3", "Use @Order for tests that have a natural execution sequence.", False),
        PromptRule("IT-S4", "Use @DynamicPropertySource for TestContainers port mapping.", False),
        PromptRule("IT-S5", "Add @Tag('integration') for filtering in CI/CD pipelines.", False),
    ]

    # Template
    template = f"""You are a senior Java test engineer. Generate comprehensive integration tests for the following Spring Boot component.

## Source Class Information
Class: {cls.name}
Package: {cls.package or 'default'}
Component Type: {component.component_type.value}
Test Type: {test_type.upper()} Integration Test

{specific_context}

## Requirements

### Mandatory (Hard Rules)
{_format_rules(hard_rules)}

### Recommended (Soft Rules)
{_format_rules(soft_rules)}

## Output Format
- Produce a single compilable Java test file: `{cls.name}IT.java`
- Package: `{cls.package or 'default'}`
- Include all necessary imports
- Use Spring Boot Test annotations
- Include test data setup and cleanup

Generate the complete integration test file now.
"""

    steps = [
        "1. Identify the component type and its external dependencies",
        "2. Determine which Spring Boot test slice to use (@WebMvcTest, @DataJpaTest, etc.)",
        "3. Set up TestContainers if external services are needed",
        "4. Create test data fixtures",
        "5. For API tests: test all endpoints with MockMvc",
        "6. For DB tests: test CRUD operations with assertions on DB state",
        "7. For messaging tests: test message production and consumption",
        "8. Verify error handling and edge cases",
    ]

    return GeneratedPrompt(
        prompt_type=PromptType.INTEGRATION_TEST,
        purpose=purpose,
        hard_rules=hard_rules,
        soft_rules=soft_rules,
        context=specific_context,
        template_body=template,
        target_classes=[cls.name],
        conditional_trigger=trigger,
        execution_steps=steps,
    )


# ═══════════════════════════════════════════════════════════════════════
#  E2E TEST PROMPT
# ═══════════════════════════════════════════════════════════════════════

def build_e2e_test_prompt(
    analysis: CodebaseAnalysis,
) -> GeneratedPrompt:
    """Build a prompt for generating end-to-end test scenarios."""

    features = analysis.features
    controllers = [c for c in analysis.components if c.component_type in (
        ComponentType.REST_CONTROLLER, ComponentType.CONTROLLER
    )]
    all_endpoints = []
    for c in controllers:
        for ep in c.endpoints:
            all_endpoints.append(f"{ep.http_method} {ep.path} → {c.class_info.name}.{ep.method_name}")

    endpoint_list = "\n".join(f"  - {e}" for e in all_endpoints) if all_endpoints else "  (no endpoints detected)"

    context = f"""Project: {analysis.project_name}
Total Classes: {features.total_classes}
Controllers: {features.controller_count}
Services: {features.service_count}
Repositories: {features.repository_count}
Database: {'Yes (' + ', '.join(features.database_types) + ')' if features.has_database else 'No'}
Messaging: {'Kafka' if features.has_kafka else 'RabbitMQ' if features.has_rabbitmq else 'No'}
Security: {'Yes' if features.has_security else 'No'}

Endpoints:
{endpoint_list}
"""

    hard_rules = [
        PromptRule("E2E-H1", "Use @SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT).", True),
        PromptRule("E2E-H2", "Use TestRestTemplate or WebTestClient for real HTTP calls.", True),
        PromptRule("E2E-H3", "Test complete user flows — not isolated units.", True),
        PromptRule("E2E-H4", "Include authentication setup if security is enabled.", True),
        PromptRule("E2E-H5", "Test both success and failure paths end-to-end.", True),
        PromptRule("E2E-H6", "Use TestContainers for all external dependencies.", True),
    ]

    soft_rules = [
        PromptRule("E2E-S1", "Define test scenarios as user stories (Given/When/Then).", False),
        PromptRule("E2E-S2", "Test CRUD lifecycle: Create → Read → Update → Delete.", False),
        PromptRule("E2E-S3", "Include performance assertions (response time < X ms) where relevant.", False),
    ]

    template = f"""You are a senior QA engineer. Generate comprehensive end-to-end tests for the following Spring Boot microservice.

## Project Overview
{context}

## Requirements

### Mandatory (Hard Rules)
{_format_rules(hard_rules)}

### Recommended (Soft Rules)
{_format_rules(soft_rules)}

## Test Scenarios to Cover
1. Full CRUD lifecycle for each main resource
2. Error handling (invalid inputs, not found, unauthorized)
3. Data validation flows
4. Cross-service interactions (if applicable)
{'5. Authentication and authorization flows' if features.has_security else ''}
{'6. Message publication and consumption flows' if features.has_messaging else ''}

## Output Format
- Produce a single Java test file: `{analysis.project_name}E2ETest.java`
- Use Given/When/Then comments for scenario documentation
- Include test data setup and teardown

Generate the complete E2E test file now.
"""

    steps = [
        "1. Map all endpoints into user-facing scenarios",
        "2. Define happy-path E2E flows (CRUD lifecycle)",
        "3. Define error scenarios (4xx, 5xx responses)",
        "4. Set up full application context with TestContainers",
        "5. Implement authentication if security is present",
        "6. Execute scenarios using TestRestTemplate",
        "7. Assert on HTTP responses and database state",
    ]

    return GeneratedPrompt(
        prompt_type=PromptType.E2E_TEST,
        purpose=f"Generate end-to-end tests for {analysis.project_name}",
        hard_rules=hard_rules,
        soft_rules=soft_rules,
        context=context,
        template_body=template,
        target_classes=[c.class_info.name for c in controllers],
        conditional_trigger=f"Project has {features.controller_count} controllers with {features.total_endpoints} endpoints",
        execution_steps=steps,
    )


# ═══════════════════════════════════════════════════════════════════════
#  DOCUMENTATION PROMPT
# ═══════════════════════════════════════════════════════════════════════

def build_documentation_prompt(
    analysis: CodebaseAnalysis,
) -> GeneratedPrompt:
    """Build a prompt for generating technical Markdown documentation."""

    features = analysis.features

    # Build component inventory
    component_summary = []
    for comp in analysis.components:
        cls = comp.class_info
        ep_count = len(comp.endpoints)
        dep_count = len(comp.dependencies)
        line = f"  - [{comp.component_type.value}] {cls.name}"
        if ep_count:
            line += f" ({ep_count} endpoints)"
        if dep_count:
            line += f" ({dep_count} dependencies)"
        component_summary.append(line)

    context = f"""Project: {analysis.project_name}
Total Classes: {features.total_classes}
Controllers: {features.controller_count}
Services: {features.service_count}
Repositories: {features.repository_count}
Entities: {features.entity_count}
Packages: {', '.join(features.packages[:10])}

Feature Flags:
  Database: {'Yes (' + ', '.join(features.database_types) + ')' if features.has_database else 'No'}
  REST API: {'Yes' if features.has_rest_controllers else 'No'}
  Messaging: {'Kafka' if features.has_kafka else 'RabbitMQ' if features.has_rabbitmq else 'No'}
  Security: {'Yes' if features.has_security else 'No'}
  Scheduling: {'Yes' if features.has_scheduling else 'No'}
  Caching: {'Yes' if features.has_caching else 'No'}
  Validation: {'Yes' if features.has_validation else 'No'}
  Feign Client: {'Yes' if features.has_feign_client else 'No'}
  Circuit Breaker: {'Yes' if features.has_circuit_breaker else 'No'}

Components:
{chr(10).join(component_summary)}
"""

    hard_rules = [
        PromptRule("DOC-H1", "Use Markdown format with proper heading hierarchy (# → ## → ### → ####).", True),
        PromptRule("DOC-H2", "Include these sections: Overview, Architecture, Components, API Reference, Configuration, Build & Run.", True),
        PromptRule("DOC-H3", "Document every REST endpoint with method, path, request/response body, and status codes.", True),
        PromptRule("DOC-H4", "Include a data flow diagram (Mermaid syntax) showing how data moves through layers.", True),
        PromptRule("DOC-H5", "Document all configuration properties with their types and defaults.", True),
        PromptRule("DOC-H6", "Include a table of service responsibilities (Service → What it does → Dependencies).", True),
        PromptRule("DOC-H7", "Write for mixed audience: junior devs, senior engineers, architects, QA engineers.", True),
    ]

    soft_rules = [
        PromptRule("DOC-S1", "Add sequence diagrams for complex multi-service flows.", False),
        PromptRule("DOC-S2", "Include code examples for key configurations.", False),
        PromptRule("DOC-S3", "Add a 'Getting Started' quick-start section.", False),
        PromptRule("DOC-S4", "Document error codes and their meanings.", False),
        PromptRule("DOC-S5", "Include a glossary of domain terms.", False),
    ]

    template = f"""You are a principal software architect. Generate comprehensive technical documentation in Markdown for the following Spring Boot microservice.

## Project Information
{context}

## Requirements

### Mandatory (Hard Rules)
{_format_rules(hard_rules)}

### Recommended (Soft Rules)
{_format_rules(soft_rules)}

## Required Document Structure

```
# {{Project Name}} — Technical Documentation

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
"""

    steps = [
        "1. Analyze project structure and identify main packages",
        "2. Describe the high-level architecture and layer interactions",
        "3. Create a component inventory with responsibilities",
        "4. Document all REST API endpoints in tabular format",
        "5. Describe the data model and entity relationships",
        "6. List all configuration properties with defaults",
        "7. Generate Mermaid data flow diagrams",
        "8. Write build and run instructions",
        "9. Document error handling patterns",
    ]

    return GeneratedPrompt(
        prompt_type=PromptType.DOCUMENTATION,
        purpose=f"Generate comprehensive Markdown documentation for {analysis.project_name}",
        hard_rules=hard_rules,
        soft_rules=soft_rules,
        context=context,
        template_body=template,
        target_classes=[c.class_info.name for c in analysis.components],
        conditional_trigger=f"Project has {features.total_classes} classes across {len(features.packages)} packages",
        execution_steps=steps,
    )


# ═══════════════════════════════════════════════════════════════════════
#  C4 ARCHITECTURE PROMPT
# ═══════════════════════════════════════════════════════════════════════

def build_c4_architecture_prompt(
    analysis: CodebaseAnalysis,
) -> GeneratedPrompt:
    """Build a prompt for generating C4 architecture diagrams in PlantUML."""

    features = analysis.features

    # Build dependency graph summary
    dep_lines = []
    for cls_name, deps in analysis.class_dependency_graph.items():
        if deps:
            dep_lines.append(f"  {cls_name} → {', '.join(deps)}")

    dep_graph_str = "\n".join(dep_lines) if dep_lines else "  (no dependencies detected)"

    # Component breakdown
    comp_by_type = {}
    for comp in analysis.components:
        ct = comp.component_type.value
        comp_by_type.setdefault(ct, []).append(comp.class_info.name)

    comp_breakdown = "\n".join(
        f"  {ct}: {', '.join(names)}" for ct, names in comp_by_type.items()
    )

    context = f"""Project: {analysis.project_name}
Total Classes: {features.total_classes}

Component Breakdown:
{comp_breakdown}

Dependency Graph:
{dep_graph_str}

External Systems:
  {'Database (' + ', '.join(features.database_types) + ')' if features.has_database else ''}
  {'Kafka Message Broker' if features.has_kafka else ''}
  {'RabbitMQ Message Broker' if features.has_rabbitmq else ''}
  {'External APIs (Feign Client)' if features.has_feign_client else ''}
"""

    hard_rules = [
        PromptRule("C4-H1", "Use PlantUML syntax with C4-PlantUML library (!include C4_*).", True),
        PromptRule("C4-H2", "Generate Context diagram (System → External Systems).", True),
        PromptRule("C4-H3", "Generate Container diagram (showing application containers and data stores).", True),
        PromptRule("C4-H4", "Generate Component diagram (showing internal components and their relationships).", True),
        PromptRule("C4-H5", "Use standard C4 elements: Person, System, Container, Component, Rel.", True),
        PromptRule("C4-H6", "Include descriptions for every element and relationship.", True),
        PromptRule("C4-H7", "Show data flow direction in relationships.", True),
    ]

    soft_rules = [
        PromptRule("C4-S1", "Use color coding: blue for internal, gray for external systems.", False),
        PromptRule("C4-S2", "Add technology labels to containers (e.g., 'Spring Boot', 'PostgreSQL').", False),
        PromptRule("C4-S3", "Include legends for diagram readability.", False),
        PromptRule("C4-S4", "Show deployment zones if cloud infrastructure is detectable.", False),
    ]

    template = f"""You are a software architect specializing in C4 modeling. Generate C4 architecture diagrams in PlantUML format for the following Spring Boot microservice.

## Project Information
{context}

## Requirements

### Mandatory (Hard Rules)
{_format_rules(hard_rules)}

### Recommended (Soft Rules)
{_format_rules(soft_rules)}

## Required Diagrams

### 1. Context Diagram (Level 1)
Show the system in its environment — who uses it and what external systems it connects to.

```plantuml
@startuml C4_Context
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Context.puml
' Define elements here
@enduml
```

### 2. Container Diagram (Level 2)
Show the high-level technology decisions — web app, database, message broker, etc.

```plantuml
@startuml C4_Container
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml
' Define elements here
@enduml
```

### 3. Component Diagram (Level 3)
Show internal components — controllers, services, repositories — and their relationships.

```plantuml
@startuml C4_Component
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Component.puml
' Define elements here
@enduml
```

Generate all three PlantUML diagrams now.
"""

    steps = [
        "1. Identify the system boundary and external actors",
        "2. Map external systems (databases, message brokers, APIs)",
        "3. Create Context diagram with Person and System elements",
        "4. Identify containers (Spring Boot app, data stores, brokers)",
        "5. Create Container diagram with technology labels",
        "6. Map internal components from the dependency graph",
        "7. Create Component diagram showing Controller → Service → Repository flow",
        "8. Add relationship descriptions and data flow directions",
    ]

    return GeneratedPrompt(
        prompt_type=PromptType.C4_ARCHITECTURE,
        purpose=f"Generate C4 architecture diagrams (PlantUML) for {analysis.project_name}",
        hard_rules=hard_rules,
        soft_rules=soft_rules,
        context=context,
        template_body=template,
        target_classes=[c.class_info.name for c in analysis.components],
        conditional_trigger=f"Project has {features.total_classes} classes with inter-component dependencies",
        execution_steps=steps,
    )


# ═══════════════════════════════════════════════════════════════════════
#  RUN ARGUMENTS PROMPT
# ═══════════════════════════════════════════════════════════════════════

def build_run_arguments_prompt(
    analysis: CodebaseAnalysis,
) -> GeneratedPrompt:
    """Build a prompt for generating runtime execution arguments."""

    features = analysis.features

    # Collect config properties from all configuration components
    all_config_props = []
    for comp in analysis.components:
        if comp.component_type == ComponentType.CONFIGURATION:
            all_config_props.extend(comp.config_properties)

    config_props_str = "\n".join(f"  - {p}" for p in all_config_props) if all_config_props else "  (none detected)"

    context = f"""Project: {analysis.project_name}
Database: {'Yes (' + ', '.join(features.database_types) + ')' if features.has_database else 'No'}
Messaging: {'Kafka' if features.has_kafka else 'RabbitMQ' if features.has_rabbitmq else 'No'}
Security: {'Yes' if features.has_security else 'No'}
Spring Profiles Detected: {', '.join(features.spring_profiles) if features.spring_profiles else 'none'}

Configuration Properties Found:
{config_props_str}
"""

    hard_rules = [
        PromptRule("RUN-H1", "Provide CLI commands using `java -jar` format.", True),
        PromptRule("RUN-H2", "Include Spring profile activation (--spring.profiles.active=).", True),
        PromptRule("RUN-H3", "Include essential JVM parameters (-Xms, -Xmx, -XX:+UseG1GC).", True),
        PromptRule("RUN-H4", "List all required environment variables with descriptions.", True),
        PromptRule("RUN-H5", "Provide separate commands for dev, staging, and production.", True),
        PromptRule("RUN-H6", "Include Docker run command if containerization is applicable.", True),
    ]

    soft_rules = [
        PromptRule("RUN-S1", "Include Gradle/Maven commands for building the artifact.", False),
        PromptRule("RUN-S2", "Add JMX monitoring flags for production.", False),
        PromptRule("RUN-S3", "Include health check curl commands.", False),
        PromptRule("RUN-S4", "Provide docker-compose example if multiple services are involved.", False),
    ]

    template = f"""You are a DevOps engineer. Generate runtime execution arguments and run commands for the following Spring Boot microservice.

## Project Information
{context}

## Requirements

### Mandatory (Hard Rules)
{_format_rules(hard_rules)}

### Recommended (Soft Rules)
{_format_rules(soft_rules)}

## Required Sections

### 1. Environment Variables
Table: Variable | Description | Required | Default | Example

### 2. Spring Profiles
- dev: local development settings
- staging: pre-production settings
- prod: production settings

### 3. JVM Parameters
- Memory settings
- GC configuration
- Debug flags

### 4. CLI Run Commands
```bash
# Development
java -jar ...

# Staging
java -jar ...

# Production
java -jar ...
```

### 5. Docker
```bash
docker run ...
docker-compose up ...
```

### 6. Build Commands
```bash
# Gradle
./gradlew build

# Maven
mvn clean package
```

Generate all run argument documentation now.
"""

    steps = [
        "1. Identify required environment variables from configuration",
        "2. Determine Spring profiles from codebase analysis",
        "3. Calculate appropriate JVM memory settings for the service size",
        "4. Build CLI commands for each environment",
        "5. Create Docker run commands with environment mapping",
        "6. Add build commands for Gradle/Maven",
        "7. Include health check and monitoring commands",
    ]

    return GeneratedPrompt(
        prompt_type=PromptType.RUN_ARGUMENTS,
        purpose=f"Generate runtime execution arguments for {analysis.project_name}",
        hard_rules=hard_rules,
        soft_rules=soft_rules,
        context=context,
        template_body=template,
        target_classes=[],
        conditional_trigger="Project analysis completed — run arguments always generated",
        execution_steps=steps,
    )


# ═══════════════════════════════════════════════════════════════════════
#  HELPERS
# ═══════════════════════════════════════════════════════════════════════

def _format_rules(rules: List[PromptRule]) -> str:
    """Format rules into numbered markdown list."""
    lines = []
    for r in rules:
        prefix = "🔴" if r.is_hard else "🟡"
        lines.append(f"{prefix} [{r.id}] {r.description}")
    return "\n".join(lines)


def _format_dependencies(deps) -> str:
    """Format dependency list for prompt context."""
    if not deps:
        return "No dependencies to mock."
    lines = []
    for d in deps:
        lines.append(f"- {d.type} {d.field_name} (injected via {d.injection_method})")
    return "\n".join(lines)


def _build_api_test_context(component: SpringComponent) -> str:
    """Build API-specific context for integration test prompt."""
    lines = [f"Base Path: {component.base_path or '/'}", "", "Endpoints:"]
    for ep in component.endpoints:
        lines.append(f"  {ep.http_method} {ep.path}")
        if ep.request_body_type:
            lines.append(f"    Request Body: {ep.request_body_type}")
        if ep.response_type:
            lines.append(f"    Response: {ep.response_type}")
        if ep.path_variables:
            lines.append(f"    Path Variables: {', '.join(ep.path_variables)}")
    return "\n".join(lines)


def _build_db_test_context(component: SpringComponent, analysis: CodebaseAnalysis) -> str:
    """Build database-specific context for integration test prompt."""
    lines = [
        f"Repository: {component.class_info.name}",
        f"Database Types: {', '.join(analysis.features.database_types)}",
        "",
        "Methods to test:",
    ]
    for m in component.class_info.methods:
        param_sig = ", ".join(f"{p.type} {p.name}" for p in m.parameters)
        lines.append(f"  - {m.return_type} {m.name}({param_sig})")
    return "\n".join(lines)


def _build_messaging_test_context(component: SpringComponent, features) -> str:
    """Build messaging-specific context for integration test prompt."""
    broker = "Kafka" if features.has_kafka else "RabbitMQ" if features.has_rabbitmq else "Unknown"
    lines = [
        f"Component: {component.class_info.name}",
        f"Message Broker: {broker}",
        f"Type: {component.component_type.value}",
        "",
        "Listener/Producer Methods:",
    ]
    for m in component.class_info.methods:
        if any(a in m.annotations for a in ("KafkaListener", "RabbitListener", "JmsListener")):
            lines.append(f"  - [LISTENER] {m.name}")
        elif any(a in m.annotations for a in ("SendTo",)):
            lines.append(f"  - [PRODUCER] {m.name}")
        else:
            lines.append(f"  - {m.name}")
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════
#  MASTER ORCHESTRATOR PROMPT
# ═══════════════════════════════════════════════════════════════════════

def build_master_orchestrator_prompt(
    analysis: CodebaseAnalysis,
    child_prompts: List[GeneratedPrompt],
    child_filenames: List[str],
) -> GeneratedPrompt:
    """
    Build the root/master orchestrator prompt.

    This is a single prompt that:
    1. Summarises the whole project
    2. Declares global rules that apply across every sub-task
    3. Lists every child prompt in an explicit Invocation Chain table
    4. Provides inline summaries of each child so the master is self-contained
    5. Instructs the LLM to execute child prompts sequentially and confirm each
    """
    features = analysis.features

    # ── Project feature table ─────────────────────────────────────────
    feature_rows = [
        f"| REST Controllers   | {'Yes (' + str(features.controller_count) + ')' if features.has_rest_controllers else 'No'} |",
        f"| Database / JPA     | {'Yes (' + ', '.join(features.database_types) + ')' if features.has_database else 'No'} |",
        f"| Messaging          | {'Kafka' if features.has_kafka else 'RabbitMQ' if features.has_rabbitmq else 'No'} |",
        f"| Security           | {'Yes' if features.has_security else 'No'} |",
        f"| Caching            | {'Yes' if features.has_caching else 'No'} |",
        f"| Validation         | {'Yes' if features.has_validation else 'No'} |",
        f"| Exception Handling | {'Yes' if features.has_exception_handling else 'No'} |",
        f"| Scheduling         | {'Yes' if features.has_scheduling else 'No'} |",
    ]
    feature_table = "\n".join(feature_rows)

    # ── Component inventory table ─────────────────────────────────────
    comp_rows = []
    for comp in analysis.components:
        cls = comp.class_info
        ep_str = f"{len(comp.endpoints)} endpoint(s)" if comp.endpoints else "—"
        dep_str = ", ".join(d.type for d in comp.dependencies) if comp.dependencies else "—"
        comp_rows.append(
            f"| {cls.name} | {comp.component_type.value} | {ep_str} | {dep_str} |"
        )
    comp_table = "\n".join(comp_rows)

    # ── Invocation chain table ────────────────────────────────────────
    chain_rows = []
    for i, (prompt, fname) in enumerate(zip(child_prompts, child_filenames), start=1):
        targets = ", ".join(prompt.target_classes[:2])
        if len(prompt.target_classes) > 2:
            targets += f" (+{len(prompt.target_classes) - 2} more)"
        chain_rows.append(
            f"| {i:02d} | `{fname}` | {prompt.prompt_type.value.replace('_', ' ').title()} "
            f"| {prompt.purpose} | {targets or 'Project-level'} |"
        )
    chain_table = "\n".join(chain_rows)

    # ── Inline sub-task summaries ─────────────────────────────────────
    inline_summaries = []
    for i, (prompt, fname) in enumerate(zip(child_prompts, child_filenames), start=1):
        hard_count = len(prompt.hard_rules)
        soft_count = len(prompt.soft_rules)
        first_step = prompt.execution_steps[0] if prompt.execution_steps else "—"
        hard_preview = "\n".join(
            f"  - 🔴 [{r.id}] {r.description}" for r in prompt.hard_rules[:3]
        )
        if len(prompt.hard_rules) > 3:
            hard_preview += f"\n  - *(+{len(prompt.hard_rules) - 3} more hard rules in child file)*"
        inline_summaries.append(
            f"### Step {i:02d} — {prompt.purpose}\n"
            f"> **File:** `{fname}` &nbsp;|&nbsp; "
            f"**Trigger:** {prompt.conditional_trigger}\n\n"
            f"**Hard Rules ({hard_count})** *(top 3 shown)*:\n{hard_preview}\n\n"
            f"**Soft Rules:** {soft_count} additional recommendations in child file.\n\n"
            f"**First Execution Step:** {first_step}\n"
        )
    inline_section = "\n".join(inline_summaries)

    # ── Global rules ──────────────────────────────────────────────────
    global_hard_rules = [
        PromptRule("GL-H1", "Use Java 17+ features and idioms throughout all generated code.", True),
        PromptRule("GL-H2", "All generated Java files must be fully compilable without modification.", True),
        PromptRule("GL-H3", "Process sub-tasks strictly in the order listed in the Invocation Chain.", True),
        PromptRule("GL-H4", "After each step output: ✅ Step N complete — [one-line summary].", True),
        PromptRule("GL-H5", "Do not skip any step, even if output seems similar to a previous step.", True),
        PromptRule("GL-H6", "Each child prompt file contains full details, hard rules, and templates for its step.", True),
    ]
    global_soft_rules = [
        PromptRule("GL-S1", "After all steps complete, produce a final summary table: Step | Output | Status.", False),
        PromptRule("GL-S2", "If a step fails or must be skipped, explain why before moving to the next.", False),
        PromptRule("GL-S3", "Keep each step's output in a clearly labelled section.", False),
    ]

    # ── Full master prompt template ───────────────────────────────────
    total = len(child_prompts)
    template = f"""You are a senior software engineer, QA lead, and architect working on the **{analysis.project_name}** Spring Boot microservice.

You are executing a full, automated test and documentation generation session. This master prompt is the **root of a nested prompt hierarchy** — it drives {total} child prompts in order. Work through every step sequentially without skipping.

---

## Project Summary

**Project:** {analysis.project_name}
**Total Classes:** {features.total_classes} &nbsp;|&nbsp; **Controllers:** {features.controller_count} &nbsp;|&nbsp; **Services:** {features.service_count} &nbsp;|&nbsp; **Repositories:** {features.repository_count}

### Feature Matrix
| Feature | Detected |
|---------|----------|
{feature_table}

### Component Inventory
| Class | Type | Endpoints | Dependencies |
|-------|------|-----------|--------------|
{comp_table}

---

## Global Rules (Apply to ALL Steps)

### Mandatory
{_format_rules(global_hard_rules)}

### Recommended
{_format_rules(global_soft_rules)}

---

## Invocation Chain — {total} Child Prompts

Execute each child prompt **in the order listed below**. For full rules and code templates, open the corresponding file.

| Step | File | Type | Purpose | Target |
|------|------|------|---------|--------|
{chain_table}

---

## Inline Sub-Task Summaries

The summaries below give you enough context to understand each step. Always open the child file for the complete rules and templates before generating output.

{inline_section}
---

## Session Execution Instructions

```
FOR i = 01 TO {total:02d}:
  1. Open child file listed in Step i of the Invocation Chain
  2. Read all Hard Rules and Soft Rules in that file
  3. Generate the required output (Java file / Markdown / PlantUML)
  4. Output: ✅ Step i complete — [one-line description of what was produced]
  5. GOTO Step i+1
END FOR
```

After Step {total:02d}, produce a final session summary:

```
## Session Complete — {analysis.project_name}
| Step | Child File | Output Artifact | Status |
|------|-----------|-----------------|--------|
| 01   | ...       | ...             | ✅     |
...
```

**Begin with Step 01 now.**
"""

    execution_steps = [
        "1. Orient: read the Project Summary and Feature Matrix",
        f"2. Apply Global Rules GL-H1 through GL-H6 to all {total} steps",
        f"3. Open child file for Step 01 and execute it",
        f"4. Confirm with: ✅ Step 01 complete — [summary]",
        f"5. Continue Step 02 → Step {total:02d} sequentially",
        "6. Produce the final session summary table",
    ]

    return GeneratedPrompt(
        prompt_type=PromptType.MASTER,
        purpose=f"Master orchestrator — drives {total} sequential child prompts for {analysis.project_name}",
        hard_rules=global_hard_rules,
        soft_rules=global_soft_rules,
        context=f"Project: {analysis.project_name}, {features.total_classes} classes, {total} child prompts",
        template_body=template,
        target_classes=[c.class_info.name for c in analysis.components],
        conditional_trigger="Always generated — root of the nested prompt hierarchy",
        execution_steps=execution_steps,
    )
