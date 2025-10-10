"use strict";
/**
 * Simple Calculator Module
 * This file intentionally contains syntax errors (missing semicolons)
 * for demonstration purposes in the bug fix automation demo.
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.Calculator = void 0;
class Calculator {
    /**
     * Adds two numbers
     */
    add(a, b) {
        return a + b; // Missing semicolon
    }
    /**
     * Subtracts b from a
     */
    subtract(a, b) {
        return a - b; // Missing semicolon
    }
    /**
     * Multiplies two numbers
     */
    multiply(a, b) {
        return a * b; // Missing semicolon
    }
    /**
     * Divides a by b
     * @throws Error if b is zero
     */
    divide(a, b) {
        if (b === 0) {
            throw new Error("Cannot divide by zero"); // Missing semicolon
        }
        return a / b; // Missing semicolon
    }
    /**
     * Calculates the power of a number
     */
    power(base, exponent) {
        return Math.pow(base, exponent); // Missing semicolon
    }
    /**
     * Calculates the square root
     * @throws Error if number is negative
     */
    squareRoot(num) {
        if (num < 0) {
            throw new Error("Cannot calculate square root of negative number"); // Missing semicolon
        }
        return Math.sqrt(num); // Missing semicolon
    }
}
exports.Calculator = Calculator;
// Usage example
const calc = new Calculator(); // Missing semicolon
console.log("5 + 3 =", calc.add(5, 3)); // Missing semicolon
console.log("10 - 4 =", calc.subtract(10, 4)); // Missing semicolon
console.log("6 * 7 =", calc.multiply(6, 7)); // Missing semicolon
//# sourceMappingURL=calculator.js.map