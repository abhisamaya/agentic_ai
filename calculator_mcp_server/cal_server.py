import math
from mcp.server.mcpserver import MCPServer
import json
from pathlib import Path
from datetime import datetime, timezone


cal_mcp = MCPServer(name= "Notes_MCP_Server")


# Store recent calculations in memory.
calculation_history: list[dict] = []


# -------------------------
# Helper functions
# -------------------------

def validate_number(value: float, name: str = "value") -> float:
    """Validate that an input is a finite number."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a number.")

    value = float(value)

    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite.")

    return value

def record_calculation(
    operation: str, inputs: dict, result: float
) -> str:
    """Record a successful calculation and format its result."""
    calculation_history.append({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "operation": operation,
        "inputs": inputs,
        "result": result,
    })

    # Keep the most recent 100 calculations.
    del calculation_history[:-100]

    return f"{operation} result: {result:.12g}"


# -------------------------
# Core calculator tools
# -------------------------

@cal_mcp.tool()
def add(a: float, b: float) -> str:
    """Add two numbers a and b and return their sum."""
    a = validate_number(a, "a")
    b = validate_number(b, "b")
    result = a + b

    if not math.isfinite(result):
        return "Error: The result is outside the supported numeric range."

    return record_calculation("Addition", {"a": a, "b": b}, result)


@cal_mcp.tool()
def subtract(a: float, b: float) -> str:
    """Subtract b from a and return the difference."""
    a = validate_number(a, "a")
    b = validate_number(b, "b")
    result = a - b

    if not math.isfinite(result):
        return "Error: The result is outside the supported numeric range."

    return record_calculation("Subtraction", {"a": a, "b": b}, result)


@cal_mcp.tool()
def multiply(a: float, b: float) -> str:
    """Multiply two numbers a and b and return their product."""
    a = validate_number(a, "a")
    b = validate_number(b, "b")
    result = a * b

    if not math.isfinite(result):
        return "Error: The result is outside the supported numeric range."

    return record_calculation("Multiplication", {"a": a, "b": b}, result)


@cal_mcp.tool()
def divide(a: float, b: float) -> str:
    """Divide a by b. Returns an error if b is zero."""
    a = validate_number(a, "a")
    b = validate_number(b, "b")

    if b == 0:
        return "Error: Division by zero is not allowed."

    result = a / b
    return record_calculation("Division", {"a": a, "b": b}, result)



# -------------------------
# Advanced calculator tools
# -------------------------

@cal_mcp.tool()
def power(base: float, exponent: float) -> str:
    """Raise base to exponent and return the result."""
    base = validate_number(base, "base")
    exponent = validate_number(exponent, "exponent")

    try:
        result = base ** exponent

        if isinstance(result, complex) or not math.isfinite(result):
            return "Error: The result is not a supported finite real number."

    except (ValueError, OverflowError, ZeroDivisionError):
        return "Error: The power operation is undefined or out of range."

    return record_calculation(
        "Power", {"base": base, "exponent": exponent}, result
    )


@cal_mcp.tool()
def square_root(number: float) -> str:
    """Calculate the square root of a non-negative number."""
    number = validate_number(number, "number")

    if number < 0:
        return "Error: Cannot calculate the real square root of a negative number."

    result = math.sqrt(number)
    return record_calculation("Square root", {"number": number}, result)


@cal_mcp.tool()
def percentage(value: float, percent: float) -> str:
    """Calculate percent percent of value. For example, 20 percent of 150 is 30."""
    value = validate_number(value, "value")
    percent = validate_number(percent, "percent")
    result = value * percent / 100

    if not math.isfinite(result):
        return "Error: The result is outside the supported numeric range."

    return record_calculation(
        "Percentage", {"value": value, "percent": percent}, result
    )




# -------------------------
# Resources
# -------------------------

@cal_mcp.resource("constants://math")
def get_math_constants() -> str:
    """Return common mathematical constants as JSON."""
    constants = {
        "pi": math.pi,
        "e": math.e,
        "golden_ratio": (1 + math.sqrt(5)) / 2,
    }
    return json.dumps(constants, indent=2)


@cal_mcp.resource("history://calculations")
def get_calculation_history() -> str:
    """Return the recent calculation history as JSON."""
    return json.dumps(calculation_history, indent=2)


# -------------------------
# Prompts
# -------------------------

@cal_mcp.prompt()
def solve_equation(problem: str) -> str:
    """Create a step-by-step prompt for solving a math word problem."""
    return f"""
Solve the following mathematical word problem.

Problem: {problem}

Instructions:
1. Identify the known values and the unknown.
2. Define the variables needed.
3. Translate the problem into mathematical equations.
4. Explain each solution step clearly.
5. Use the calculator tools when appropriate to verify arithmetic.
6. State the final answer with units when applicable.
7. Check whether the answer makes sense in context.
"""


@cal_mcp.prompt()
def calculation_help(topic: str = "basic arithmetic") -> str:
    """Create a helpful explanation prompt for a mathematical topic."""
    return f"""
You are a patient mathematics tutor.

Help the user understand: {topic}

Instructions:
1. Explain the concept in simple language.
2. Introduce the relevant formula, if applicable.
3. Work through a clear example step by step.
4. Use the calculator tools to verify numerical results when useful.
5. Mention common mistakes and how to avoid them.
6. End with a short practice question.
"""

