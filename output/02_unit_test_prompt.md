# Prompt: Step 02/11 — UNIT TEST

---

## Chain Context

| Field | Value |
|-------|-------|
| **Invoked By** | `00_master_prompt.md` |
| **Step** | 02 of 11 |
| **Previous Step** | `01_..._prompt.md` |
| **Next Step** | `03_..._prompt.md` |

Once this step is complete, output: `✅ Step 02 complete — [one-line summary]` and proceed to Step 03.

---

## Purpose
Generate JUnit5 + Mockito unit tests for GlobalExceptionHandler

## Conditional Trigger
> Class GlobalExceptionHandler is a exception_handler with 3 testable methods

## Target Classes
GlobalExceptionHandler

---

## Hard Rules (Mandatory)
- **[UT-H1]** Use JUnit5 (@Test, @BeforeEach, @AfterEach, @DisplayName) — no JUnit4.
- **[UT-H2]** Use Mockito (@Mock, @InjectMocks, @ExtendWith(MockitoExtension.class)) for all dependencies.
- **[UT-H3]** Follow Arrange-Act-Assert (AAA) pattern in every test method.
- **[UT-H4]** Use @DisplayName with descriptive English sentences for every test.
- **[UT-H5]** Test class name must be GlobalExceptionHandlerTest.
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
Class: GlobalExceptionHandler
Package: com.example.orderservice.exception
Component Type: exception_handler
Dependencies: None
Methods (3):
  - public ResponseEntity<Map<String, Object>> handleNotFound(ResourceNotFoundException ex)
    Javadoc: Handle resource not found exceptions.

@param ex the exception
@return 404 error response...
  - public ResponseEntity<Map<String, Object>> handleConflict(IllegalStateException ex)
    Javadoc: Handle illegal state exceptions.

@param ex the exception
@return 409 error response...
  - public ResponseEntity<Map<String, Object>> handleGeneral(Exception ex)
    Javadoc: Handle unexpected exceptions.

@param ex the exception
@return 500 error response...

## Dependencies to Mock
No dependencies to mock.

## Requirements

### Mandatory (Hard Rules)
🔴 [UT-H1] Use JUnit5 (@Test, @BeforeEach, @AfterEach, @DisplayName) — no JUnit4.
🔴 [UT-H2] Use Mockito (@Mock, @InjectMocks, @ExtendWith(MockitoExtension.class)) for all dependencies.
🔴 [UT-H3] Follow Arrange-Act-Assert (AAA) pattern in every test method.
🔴 [UT-H4] Use @DisplayName with descriptive English sentences for every test.
🔴 [UT-H5] Test class name must be GlobalExceptionHandlerTest.
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
- Produce a single compilable Java test file: `GlobalExceptionHandlerTest.java`
- Package: `com.example.orderservice.exception`
- Include all necessary imports
- Cover AT MINIMUM:
  - 1 happy-path test per public method
  - 1 null-input test per nullable parameter
  - 1 boundary test per numeric parameter
  - 1 exception test per declared exception

## Test Structure Template
```java
@ExtendWith(MockitoExtension.class)
@DisplayName("GlobalExceptionHandler Unit Tests")
class GlobalExceptionHandlerTest {

    @Mock
    private DependencyType dependencyName;

    @InjectMocks
    private GlobalExceptionHandler globalExceptionHandler;

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
