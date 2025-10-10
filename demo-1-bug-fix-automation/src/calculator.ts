/**
 * Simple Calculator Module
 * This file intentionally contains multiple types of bugs:
 * - Missing semicolons (syntax errors)
 * - Typo/syntax error (compilation error)
 * - Missing return statement (logical error)
 * for demonstration purposes in the bug fix automation demo.
 */

export class Calculator {
  /**
   * Adds two numbers
   */
  add(a: number, b: number): number {
    return a + b;
  }

  /**
   * Subtracts b from a
   */
  subtract(a: number, b: number): number {
    return a - b  // Missing semicolon (syntax error)
  }

  /**
   * Multiplies two numbers
   */
  multiply(a: number, b: number): number {
    return a * b;
  }

  /**
   * Divides a by b
   * @throws Error if b is zero
   */
  divide(a: number, b: number): number {
    if (b === 0) {
      throw new Error("Cannot divide by zero");
    }
    return a / b;
  }

  /**
   * Calculates the power of a number
   */
  power(base: number, exponent: number): number {
    const result = Math.pow(base, exponent)  // Missing semicolon (syntax error)
    // Missing return statement (logical error - function must return a value)
  }

  /**
   * Calculates the square root
   * @throws Error if number is negative
   */
  squareRoot(num: number): number {
    if (num < 0) {
      throw new Error("Cannot calculate square root of negative number");
    }
    retrun Math.sqrt(num);  // Typo: "retrun" instead of "return" (compilation error)
  }
}

// Usage example
const calc = new Calculator();
console.log("5 + 3 =", calc.add(5, 3));
console.log("10 - 4 =", calc.subtract(10, 4));
console.log("6 * 7 =", calc.multiply(6, 7));
