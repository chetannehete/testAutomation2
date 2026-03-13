# Prompt: Step 03/11 — UNIT TEST

---

## Chain Context

| Field | Value |
|-------|-------|
| **Invoked By** | `00_master_prompt.md` |
| **Step** | 03 of 11 |
| **Previous Step** | `02_..._prompt.md` |
| **Next Step** | `04_..._prompt.md` |

Once this step is complete, output: `✅ Step 03 complete — [one-line summary]` and proceed to Step 04.

---

## Purpose
Generate JUnit5 + Mockito unit tests for OrderEventProducer

## Conditional Trigger
> Class OrderEventProducer is a component with 4 testable methods

## Target Classes
OrderEventProducer

---

## Hard Rules (Mandatory)
- **[UT-H1]** Use JUnit5 (@Test, @BeforeEach, @AfterEach, @DisplayName) — no JUnit4.
- **[UT-H2]** Use Mockito (@Mock, @InjectMocks, @ExtendWith(MockitoExtension.class)) for all dependencies.
- **[UT-H3]** Follow Arrange-Act-Assert (AAA) pattern in every test method.
- **[UT-H4]** Use @DisplayName with descriptive English sentences for every test.
- **[UT-H5]** Test class name must be OrderEventProducerTest.
- **[UT-H6]** Each test must be independent — no shared mutable state.
- **[UT-H7]** Verify interactions using Mockito.verify() for void dependency calls.
- **[UT-H8]** Test naming convention: should_ExpectedBehavior_When_Condition().
- **[UT-H9]** Include tests for: happy path, null inputs, boundary values, and exception scenarios.
- **[UT-H10]** Use assertThrows() for exception testing, not try-catch.

## Soft Rules (Recommended)
- **[UT-S1]** Use @ParameterizedTest with @ValueSource or @MethodSource for methods with multiple valid inputs.
- **[UT-S2]** Use ArgumentCaptor when verifying complex objects passed to mocks.
- **[UT-S3]** Group tests using @Nested inner classes by method under test.
- **[UT-S4]** Add // Arrange, // Act, // Assert comments in every test.
- **[UT-S5]** Keep each test under 20 lines for readability.
- **[UT-S6]** Use factory methods or builders for complex test data.
- **[UT-S7]** Test private methods indirectly through public API.

---

## Execution Steps
1. Read the source class and identify all public methods
2. Identify all injected dependencies that need mocking
3. Create @Mock for each dependency and @InjectMocks for the class under test
4. For each public method, generate @Nested class with:
   a. Happy-path test with valid inputs
   b. Null-input tests for each nullable parameter
   c. Boundary tests for numeric parameters (0, negative, MAX_VALUE)
   d. Exception tests for each declared exception
5. Verify mock interactions with Mockito.verify()
6. Ensure all tests follow AAA pattern with @DisplayName
7. Add parametrized tests where multiple input variations make sense

---

## Prompt Template

You are a senior Java test engineer. Generate comprehensive JUnit5 unit tests with Mockito for the following Spring Boot class.

## Source Class Information
Class: OrderEventProducer
Package: com.example.orderservice.messaging
Component Type: component
Dependencies: KafkaTemplate<String, Object> kafkaTemplate
Methods (4):
  - public void publishOrderCreated(Order order)
    Javadoc: Publish an order-created event.

@param order the created order...
  - public void publishOrderUpdated(Order order)
    Javadoc: Publish an order-updated event.

@param order the updated order...
  - public void publishOrderCancelled(Order order)
    Javadoc: Publish an order-cancelled event.

@param order the cancelled order...
  - public void publishOrderDeleted(Long orderId)
    Javadoc: Publish an order-deleted event.

@param orderId the deleted order ID...

## Dependencies to Mock
- KafkaTemplate<String, Object> kafkaTemplate (injected via constructor)

## Requirements

### Mandatory (Hard Rules)
🔴 [UT-H1] Use JUnit5 (@Test, @BeforeEach, @AfterEach, @DisplayName) — no JUnit4.
🔴 [UT-H2] Use Mockito (@Mock, @InjectMocks, @ExtendWith(MockitoExtension.class)) for all dependencies.
🔴 [UT-H3] Follow Arrange-Act-Assert (AAA) pattern in every test method.
🔴 [UT-H4] Use @DisplayName with descriptive English sentences for every test.
🔴 [UT-H5] Test class name must be OrderEventProducerTest.
🔴 [UT-H6] Each test must be independent — no shared mutable state.
🔴 [UT-H7] Verify interactions using Mockito.verify() for void dependency calls.
🔴 [UT-H8] Test naming convention: should_ExpectedBehavior_When_Condition().
🔴 [UT-H9] Include tests for: happy path, null inputs, boundary values, and exception scenarios.
🔴 [UT-H10] Use assertThrows() for exception testing, not try-catch.

### Recommended (Soft Rules)
🟡 [UT-S1] Use @ParameterizedTest with @ValueSource or @MethodSource for methods with multiple valid inputs.
🟡 [UT-S2] Use ArgumentCaptor when verifying complex objects passed to mocks.
🟡 [UT-S3] Group tests using @Nested inner classes by method under test.
🟡 [UT-S4] Add // Arrange, // Act, // Assert comments in every test.
🟡 [UT-S5] Keep each test under 20 lines for readability.
🟡 [UT-S6] Use factory methods or builders for complex test data.
🟡 [UT-S7] Test private methods indirectly through public API.

## Output Format
- Produce a single compilable Java test file: `OrderEventProducerTest.java`
- Package: `com.example.orderservice.messaging`
- Include all necessary imports
- Cover AT MINIMUM:
  - 1 happy-path test per public method
  - 1 null-input test per nullable parameter
  - 1 boundary test per numeric parameter
  - 1 exception test per declared exception

## Test Structure Template
```java
@ExtendWith(MockitoExtension.class)
@DisplayName("OrderEventProducer Unit Tests")
class OrderEventProducerTest {

    @Mock
    private DependencyType dependencyName;

    @InjectMocks
    private OrderEventProducer orderEventProducer;

    @BeforeEach
    void setUp() {
        // Common setup
    }

    @Nested
    @DisplayName("methodName tests")
    class MethodNameTests {

        @Test
        @DisplayName("should return expected result when valid input provided")
        void should_ReturnExpected_When_ValidInput() {
            // Arrange
            // Act
            // Assert
        }
    }
}
```

Generate the complete test file now.


---

*Generated by MD Agent Prompt Orchestrator*
