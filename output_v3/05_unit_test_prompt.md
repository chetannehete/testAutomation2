# Prompt: Step 05/11 — UNIT TEST

---

## Chain Context

| Field | Value |
|-------|-------|
| **Invoked By** | `00_master_prompt.md` |
| **Step** | 05 of 11 |
| **Previous Step** | `04_..._prompt.md` |
| **Next Step** | `06_..._prompt.md` |

Once this step is complete, output: `✅ Step 05 complete — [one-line summary]` and proceed to Step 06.

---

## Purpose
Generate JUnit5 + Mockito unit tests for OrderService

## Conditional Trigger
> Class OrderService is a service with 7 testable methods

## Target Classes
OrderService

---

## Hard Rules (Mandatory)
- **[UT-H1]** Use JUnit5 (@Test, @BeforeEach, @AfterEach, @DisplayName) — no JUnit4.
- **[UT-H2]** Use Mockito (@Mock, @InjectMocks, @ExtendWith(MockitoExtension.class)) for all dependencies.
- **[UT-H3]** Follow Arrange-Act-Assert (AAA) pattern in every test method.
- **[UT-H4]** Use @DisplayName with descriptive English sentences for every test.
- **[UT-H5]** Test class name must be OrderServiceTest.
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
Class: OrderService
Package: com.example.orderservice.service
Component Type: service
Dependencies: OrderRepository orderRepository, OrderMapper orderMapper, OrderEventProducer eventProducer
Methods (7):
  - public OrderResponse createOrder(OrderRequest request)
    Javadoc: Create a new order from the given request.

@param request the order request with items
@return the created order respon...
  - public OrderResponse getOrderById(Long id) throws ResourceNotFoundException
    Javadoc: Get order by ID with caching.

@param id the order ID
@return the order response
@throws ResourceNotFoundException if no...
  - public List<OrderResponse> getAllOrders(String status, int page, int size)
    Javadoc: Get all orders with optional status filter.

@param status optional status filter
@param page page number
@param size pa...
  - public OrderResponse updateOrder(Long id, OrderRequest request) throws ResourceNotFoundException
    Javadoc: Update an existing order.

@param id the order ID
@param request the update request
@return the updated order response
@...
  - public void deleteOrder(Long id) throws ResourceNotFoundException
    Javadoc: Delete an order by ID.

@param id the order ID
@throws ResourceNotFoundException if not found...
  - public OrderResponse cancelOrder(Long id) throws ResourceNotFoundException, IllegalStateException
    Javadoc: Cancel an active order.

@param id the order ID
@return the cancelled order
@throws ResourceNotFoundException if not fou...
  - public boolean isOrderOwnedByCustomer(Long orderId, Long customerId)
    Javadoc: Check if an order belongs to a specific customer.

@param orderId the order ID
@param customerId the customer ID
@return...

## Dependencies to Mock
- OrderRepository orderRepository (injected via constructor)
- OrderMapper orderMapper (injected via constructor)
- OrderEventProducer eventProducer (injected via constructor)

## Requirements

### Mandatory (Hard Rules)
🔴 [UT-H1] Use JUnit5 (@Test, @BeforeEach, @AfterEach, @DisplayName) — no JUnit4.
🔴 [UT-H2] Use Mockito (@Mock, @InjectMocks, @ExtendWith(MockitoExtension.class)) for all dependencies.
🔴 [UT-H3] Follow Arrange-Act-Assert (AAA) pattern in every test method.
🔴 [UT-H4] Use @DisplayName with descriptive English sentences for every test.
🔴 [UT-H5] Test class name must be OrderServiceTest.
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
- Produce a single compilable Java test file: `OrderServiceTest.java`
- Package: `com.example.orderservice.service`
- Include all necessary imports
- Cover AT MINIMUM:
  - 1 happy-path test per public method
  - 1 null-input test per nullable parameter
  - 1 boundary test per numeric parameter
  - 1 exception test per declared exception

## Test Structure Template
```java
@ExtendWith(MockitoExtension.class)
@DisplayName("OrderService Unit Tests")
class OrderServiceTest {

    @Mock
    private DependencyType dependencyName;

    @InjectMocks
    private OrderService orderService;

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
