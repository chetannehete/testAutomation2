# MD Agent — Prompt Orchestration System for Spring Boot Microservices

> **Automatically analyze Java/Spring Boot codebases and generate targeted LLM prompts for test cases, documentation, C4 architecture diagrams, and run arguments.**

## 🎯 Overview

MD Agent is a Python CLI tool that:
1. **Parses** Java source files using `javalang` AST parsing
2. **Detects** Spring Boot architectural patterns (Controllers, Services, Repositories, Messaging, etc.)
3. **Evaluates** conditional rules to determine which prompts to generate
4. **Generates** structured, deterministic LLM prompts for:
   - **Unit Tests** — JUnit5 + Mockito with AAA pattern
   - **Integration Tests** — API, Database, and Messaging
   - **E2E Tests** — Full workflow testing
   - **Documentation** — Markdown with architecture overview
   - **C4 Architecture Diagrams** — PlantUML format
   - **Run Arguments** — CLI, Docker, JVM parameters

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the full prompt orchestration system
python -m md_agent orchestrate samples/com/example/orderservice/

# Legacy: Generate basic test cases + docs
python -m md_agent generate samples/Calculator.java
```

## 📋 Commands

| Command | Description |
|---------|-------------|
| `orchestrate <path>` | **Primary.** Full Prompt Orchestration System |
| `generate <path>` | Legacy: Generate test cases + documentation |
| `testcases <path>` | Legacy: Generate test case markdown only |
| `docs <path>` | Legacy: Generate documentation markdown only |

### `orchestrate` Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--output-dir` | `-o` | `./output` | Output directory for prompt files |
| `--project-name` | `-n` | auto | Project name (auto-detected from path) |
| `--recursive` | `-r` | `True` | Scan directories recursively |

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Master Prompt Orchestrator                 │
│                                                             │
│  ┌──────────┐   ┌──────────────┐   ┌───────────────────┐   │
│  │  Java    │──▶│  Spring Boot │──▶│  Conditional Rule │   │
│  │  Parser  │   │  Detector    │   │  Evaluator        │   │
│  └──────────┘   └──────────────┘   └───────────────────┘   │
│                                            │                │
│                    ┌───────────────────────┼───────┐        │
│                    ▼           ▼           ▼       ▼        │
│              ┌──────────┐ ┌────────┐ ┌────────┐ ┌──────┐   │
│              │Unit Test │ │  Integ │ │  Doc   │ │ C4   │   │
│              │ Prompt   │ │  Test  │ │ Prompt │ │Prompt│   │
│              └──────────┘ └────────┘ └────────┘ └──────┘   │
└─────────────────────────────────────────────────────────────┘
```

## 🔍 Pattern Detection

| Pattern | How Detected | Triggers |
|---------|-------------|----------|
| REST Controller | `@RestController`, `@Controller` | API integration tests, E2E tests |
| Service | `@Service`, name ends with `Service` | Unit tests |
| Repository | `@Repository`, extends `JpaRepository` | DB integration tests |
| Entity | `@Entity`, `@Table` | Documentation |
| Kafka | `@KafkaListener`, kafka imports | Messaging integration tests |
| Security | `@EnableWebSecurity` | Auth test scenarios |
| Exception Handler | `@ControllerAdvice` | Error handling tests |

## 📁 Project Structure

```
md_agent/
├── cli.py               # CLI with orchestrate command
├── orchestrator.py       # Master Prompt Orchestrator
├── spring_detector.py    # Spring Boot pattern detector
├── prompt_templates.py   # All prompt builders
├── java_parser.py        # javalang-based Java parser
├── analyzer.py           # Legacy test case/doc generator
├── md_renderer.py        # Jinja2 markdown renderer
├── models.py             # All data models
├── mcp_server.py         # MCP protocol server
├── mcp_tools.py          # MCP tool implementations
└── templates/
    ├── test_cases.md.j2
    └── documentation.md.j2
```

## 📊 Output

After running `orchestrate`, the output directory contains:

```
output/
├── 00_orchestration_report.md    # Feature detection + execution plan
├── 01_unit_test_prompt.md        # Unit test prompts per class
├── 02_integration_test_prompt.md # API/DB/messaging test prompts
├── 03_e2e_test_prompt.md         # End-to-end test prompt
├── 04_documentation_prompt.md    # Documentation prompt
├── 05_c4_architecture_prompt.md  # C4 PlantUML prompt
└── 06_run_arguments_prompt.md    # Run args + Docker prompt
```

Each prompt file contains: **Purpose**, **Hard Rules**, **Soft Rules**, **Execution Steps**, and the **Prompt Template** ready for LLM execution.
