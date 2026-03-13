package com.example.calculator;

import java.util.List;
import java.util.ArrayList;

/**
 * A simple arithmetic calculator with basic and advanced operations.
 *
 * Provides methods for addition, subtraction, multiplication, division,
 * and batch processing of numbers.
 *
 * @author MD Agent Demo
 * @version 1.0
 */
public class Calculator {

    /** Running total for chained operations. */
    private double memory;

    /** History of all operations performed. */
    private final List<String> history;

    /**
     * Creates a new Calculator with memory initialized to zero.
     */
    public Calculator() {
        this.memory = 0.0;
        this.history = new ArrayList<>();
    }

    /**
     * Creates a new Calculator with a given initial memory value.
     *
     * @param initialValue the starting memory value
     */
    public Calculator(double initialValue) {
        this.memory = initialValue;
        this.history = new ArrayList<>();
    }

    /**
     * Adds two integers and returns the result.
     *
     * @param a the first operand
     * @param b the second operand
     * @return the sum of a and b
     */
    public int add(int a, int b) {
        int result = a + b;
        history.add(a + " + " + b + " = " + result);
        return result;
    }

    /**
     * Subtracts the second integer from the first.
     *
     * @param a the minuend
     * @param b the subtrahend
     * @return the difference (a - b)
     */
    public int subtract(int a, int b) {
        int result = a - b;
        history.add(a + " - " + b + " = " + result);
        return result;
    }

    /**
     * Multiplies two doubles and returns the product.
     *
     * @param a the first factor
     * @param b the second factor
     * @return the product of a and b
     */
    public double multiply(double a, double b) {
        double result = a * b;
        history.add(a + " * " + b + " = " + result);
        return result;
    }

    /**
     * Divides the numerator by the denominator.
     *
     * @param numerator   the dividend
     * @param denominator the divisor (must not be zero)
     * @return the quotient
     * @throws ArithmeticException if denominator is zero
     */
    public double divide(double numerator, double denominator) throws ArithmeticException {
        if (denominator == 0) {
            throw new ArithmeticException("Division by zero");
        }
        double result = numerator / denominator;
        history.add(numerator + " / " + denominator + " = " + result);
        return result;
    }

    /**
     * Computes the factorial of a non-negative integer.
     *
     * @param n the non-negative integer
     * @return the factorial of n
     * @throws IllegalArgumentException if n is negative
     */
    public long factorial(int n) throws IllegalArgumentException {
        if (n < 0) {
            throw new IllegalArgumentException("Factorial is not defined for negative numbers");
        }
        long result = 1;
        for (int i = 2; i <= n; i++) {
            result *= i;
        }
        history.add("factorial(" + n + ") = " + result);
        return result;
    }

    /**
     * Checks if a number is even.
     *
     * @param number the number to check
     * @return true if the number is even, false otherwise
     */
    public boolean isEven(int number) {
        return number % 2 == 0;
    }

    /**
     * Sums all numbers in the given list.
     *
     * @param numbers the list of numbers to sum
     * @return the total sum
     */
    public double sumAll(List<Double> numbers) {
        double total = 0.0;
        for (Double num : numbers) {
            total += num;
        }
        history.add("sumAll(" + numbers.size() + " items) = " + total);
        return total;
    }

    /**
     * Stores a value into the calculator's memory.
     *
     * @param value the value to store
     */
    public void storeInMemory(double value) {
        this.memory = value;
        history.add("Memory stored: " + value);
    }

    /**
     * Retrieves the current memory value.
     *
     * @return the current memory value
     */
    public double recallMemory() {
        return memory;
    }

    /**
     * Clears the calculator memory and operation history.
     */
    public void clear() {
        this.memory = 0.0;
        this.history.clear();
    }

    /**
     * Returns the complete operation history as a formatted string.
     *
     * @return the operation history
     */
    public String getHistory() {
        return String.join("\n", history);
    }

    /**
     * Formats a number to the specified decimal places.
     *
     * @param value         the number to format
     * @param decimalPlaces the number of decimal places
     * @return the formatted string representation
     * @throws IllegalArgumentException if decimalPlaces is negative
     */
    public String formatNumber(double value, int decimalPlaces) throws IllegalArgumentException {
        if (decimalPlaces < 0) {
            throw new IllegalArgumentException("Decimal places cannot be negative");
        }
        return String.format("%." + decimalPlaces + "f", value);
    }
}
