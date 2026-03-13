# Prompt: Step 01/11 — UNIT TEST

---

## Chain Context

| Field | Value |
|-------|-------|
| **Invoked By** | `00_master_prompt.md` |
| **Step** | 01 of 11 |
| **Previous Step** | *(first step)* |
| **Next Step** | `02_..._prompt.md` |

Once this step is complete, output: `✅ Step 01 complete — [one-line summary]` and proceed to Step 02.

---

## Purpose
Generate JUnit5 + Mockito unit tests for OrderController

## Conditional Trigger
> Class OrderController is a rest_controller with 6 testable methods

## Target Classes
OrderController

---

## Hard Rules (Mandatory)
- **[UT-H1]** Use JUnit5 (@Test, @BeforeEach, @AfterEach, @DisplayName) — no JUnit4.
- **[UT-H2]** Use Mockito (@Mock, @InjectMocks, @ExtendWith(MockitoExtension.class)) for all dependencies.
- **[UT-H3]** Follow Arrange-Act-Assert (AAA) pattern in every test method.
- **[UT-H4]** Use @DisplayName with descriptive English sentences for every test.
- **[UT-H5]** Test class name must be OrderControllerTest.
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
Class: OrderController
Package: com.example.orderservice.controller
Component Type: rest_controller
Dependencies: OrderService orderService
Methods (6):
  - public ResponseEntity<OrderResponse> createOrder(OrderRequest request)
    Javadoc: Create a new order.

@param request the order creation request with item details
@return the created order with HTTP 201...
  - public ResponseEntity<OrderResponse> getOrder(Long orderId)
    Javadoc: Get an order by its unique identifier.

@param orderId the unique order ID
@return the order details
@throws ResourceNot...
  - public ResponseEntity<List<OrderResponse>> getAllOrders(String status, int page, int size)
    Javadoc: Get all orders with optional filtering by status.

@param status optional order status filter
@param page page number (z...
  - public ResponseEntity<OrderResponse> updateOrder(Long orderId, OrderRequest request)
    Javadoc: Update an existing order.

@param orderId the order ID to update
@param request the updated order data
@return the updat...
  - public ResponseEntity<Void> deleteOrder(Long orderId)
    Javadoc: Delete an order by ID.

@param orderId the order ID to delete
@return HTTP 204 No Content on success
@throws ResourceNot...
  - public ResponseEntity<OrderResponse> cancelOrder(Long orderId)
    Javadoc: Cancel an active order.

@param orderId the order ID to cancel
@return the cancelled order with updated status
@throws I...

## Dependencies to Mock
- OrderService orderService (injected via constructor)

## Requirements

### Mandatory (Hard Rules)
🔴 [UT-H1] Use JUnit5 (@Test, @BeforeEach, @AfterEach, @DisplayName) — no JUnit4.
🔴 [UT-H2] Use Mockito (@Mock, @InjectMocks, @ExtendWith(MockitoExtension.class)) for all dependencies.
🔴 [UT-H3] Follow Arrange-Act-Assert (AAA) pattern in every test method.
🔴 [UT-H4] Use @DisplayName with descriptive English sentences for every test.
🔴 [UT-H5] Test class name must be OrderControllerTest.
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
- Produce a single compilable Java test file: `OrderControllerTest.java`
- Package: `com.example.orderservice.controller`
- Include all necessary imports
- Cover AT MINIMUM:
  - 1 happy-path test per public method
  - 1 null-input test per nullable parameter
  - 1 boundary test per numeric parameter
  - 1 exception test per declared exception

## Test Structure Template
```java
@ExtendWith(MockitoExtension.class)
@DisplayName("OrderController Unit Tests")
class OrderControllerTest {

    @Mock
    private DependencyType dependencyName;

    @InjectMocks
    private OrderController orderController;

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
