from enum import Enum
import json
import math
from typing import Sequence

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
from mcp.shared.exceptions import McpError

from pydantic import BaseModel


class MathTools(str, Enum):
    COMPARE = "compare"
    SUM = "sum"
    PRODUCT = "product"
    SUBTRACT = "subtract"
    DIVIDE = "divide"
    QUOTIENT = "quotient"
    REMAINDER = "remainder"
    POWER = "power"
    SQRT = "sqrt"
    PERCENTAGE = "percentage"
    MAX = "max"
    MIN = "min"
    AVERAGE = "average"
    MEDIAN = "median"
    MODE = "mode"
    RANGE = "range"


class MathResult(BaseModel):
    result: str
    operation: str
    numbers: list[float]


class MathInput(BaseModel):
    numbers: list[float]
    operation: str


class MathServer:
    def operate(self, input: MathInput) -> MathResult:
        """Perform a math operation on the input"""

        match input.operation:
            case MathTools.COMPARE.value:
                sorted_input = sorted(input.numbers)
                result = str.join(" < ", [str(i) for i in sorted_input])
            case MathTools.SUBTRACT.value:
                assert len(input.numbers) == 2, "Operation subtract requires two inputs"
                result = input.numbers[0] - input.numbers[1]
            case MathTools.DIVIDE.value:
                assert len(input.numbers) == 2, "Operation divide requires two inputs"
                assert input.numbers[1] != 0, "Division by zero"
                result = input.numbers[0] / input.numbers[1]
            case MathTools.POWER.value:
                assert len(input.numbers) == 2, "Operation power requires two inputs"
                result = input.numbers[0] ** input.numbers[1]
            case MathTools.SQRT.value:
                assert len(input.numbers) == 1, "Operation sqrt requires one input"
                assert input.numbers[0] >= 0, "Square root of negative number"
                result = math.sqrt(input.numbers[0])
            case MathTools.PERCENTAGE.value:
                sum_of_numbers = sum(input.numbers)
                percentages = [i / sum_of_numbers * 100 for i in input.numbers]
                result = str.join(", ", [str(i) + "%" for i in percentages])
            case MathTools.SUM.value:
                result = sum(input.numbers)
            case MathTools.PRODUCT.value:
                result = math.prod(input.numbers)
            case MathTools.QUOTIENT.value:
                assert len(input.numbers) == 2, "Operation quotient requires two inputs"
                assert input.numbers[1] != 0, "Division by zero"
                result = input.numbers[0] // input.numbers[1]
            case MathTools.REMAINDER.value:
                assert (
                    len(input.numbers) == 2
                ), "Operation remainder requires two inputs"
                assert input.numbers[1] != 0, "Division by zero"
                result = input.numbers[0] % input.numbers[1]
            case MathTools.MAX.value:
                result = max(input.numbers)
            case MathTools.MIN.value:
                result = min(input.numbers)
            case MathTools.AVERAGE.value:
                result = sum(input.numbers) / len(input.numbers)
            case MathTools.MEDIAN.value:
                sorted_input = sorted(input.numbers)
                n = len(sorted_input)
                if n % 2 == 0:
                    result = (sorted_input[n // 2 - 1] + sorted_input[n // 2]) / 2
                else:
                    result = sorted_input[n // 2]
            case MathTools.MODE.value:
                from collections import Counter

                counts = Counter(input.numbers)
                mode_value = counts.most_common(1)[0][0]
                result = mode_value
            case MathTools.RANGE.value:
                result = max(input.numbers) - min(input.numbers)
            case _:
                raise ValueError(f"Unknown operation: {input.operation}")

        return MathResult(
            result=result,
            operation=input.operation,
            input=input.numbers,
        )


async def serve() -> None:
    server = Server("mcp-math")
    math_server = MathServer()

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """List available math tools."""
        return [
            Tool(
                name=MathTools.COMPARE.value,
                description="Compare a list of numbers, returning a string of the numbers in ascending order separated by '<'",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "numbers": {
                            "type": "array",
                            "items": {"type": "number"},
                            "description": "A list of numbers to compare",
                        }
                    },
                    "required": ["numbers"],
                },
            ),
            Tool(
                name=MathTools.SUBTRACT.value,
                description="Subtract two numbers, returning the difference",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "numbers": {
                            "type": "array",
                            "items": {"type": "number"},
                            "description": "Two numbers in a list, subtract the second from the first",
                        }
                    },
                    "required": ["numbers"],
                },
            ),
            Tool(
                name=MathTools.DIVIDE.value,
                description="Divide two numbers, returning the result",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "numbers": {
                            "type": "array",
                            "items": {"type": "number"},
                            "description": "Two numbers in a list, divide the first by the second",
                        }
                    },  
                    "required": ["numbers"],
                },
            ),
            Tool(
                name=MathTools.SUM.value,
                description="Sum a list of numbers",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "numbers": {
                            "type": "array",
                            "items": {"type": "number"},
                            "description": "A list of numbers to sum",
                        }
                    },
                    "required": ["numbers"],
                },
            ),
            Tool(
                name=MathTools.PRODUCT.value,
                description="Multiply a list of numbers",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "numbers": {
                            "type": "array",
                            "items": {"type": "number"},
                            "description": "A list of numbers to multiply",
                        }
                    },
                    "required": ["numbers"],
                },
            ),
            Tool(
                name=MathTools.QUOTIENT.value,
                description="Divide two numbers, returning the quotient",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "numbers": {
                            "type": "array",
                            "items": {"type": "number"},
                            "description": "Two numbers in a list, divided the first by the second and returning the quotient",
                        }
                    },
                    "required": ["numbers"],
                },
            ),
            Tool(
                name=MathTools.REMAINDER.value,
                description="Find the remainder of two numbers",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "numbers": {
                            "type": "array",
                            "items": {"type": "number"},
                            "description": "Two numbers in a list, find the remainder of the first divided by the second",
                        }
                    },
                    "required": ["numbers"],
                },
            ),
            Tool(
                name=MathTools.POWER.value,
                description="Raise a number to the power of another number",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "numbers": {
                            "type": "array",
                            "items": {"type": "number"},
                            "description": "Two numbers in a list, raise the first to the power of the second",
                        }
                    },  
                    "required": ["numbers"],
                },
            ),
            Tool(
                name=MathTools.SQRT.value,
                description="Find the square root of a number",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "numbers": {
                            "type": "array",
                            "items": {"type": "number"},
                            "description": "A number to find the square root of",
                        }
                    },
                    "required": ["numbers"],
                },
            ),
            Tool(
                name=MathTools.PERCENTAGE.value,
                description="Convert a list of numbers to percentages",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "numbers": {
                            "type": "array",
                            "items": {"type": "number"},
                            "description": "A list of numbers to convert to percentages",
                        }
                    },
                    "required": ["numbers"],
                },
            ),
            Tool(
                name=MathTools.MAX.value,
                description="Find the maximum number in a list",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "numbers": {
                            "type": "array",
                            "items": {"type": "number"},
                            "description": "A list of numbers to find the maximum of",
                        }
                    },
                    "required": ["numbers"],
                },
            ),
            Tool(
                name=MathTools.MIN.value,
                description="Find the minimum number in a list",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "numbers": {
                            "type": "array",
                            "items": {"type": "number"},
                            "description": "A list of numbers to find the minimum of",
                        }
                    },
                    "required": ["numbers"],
                },
            ),
            Tool(
                name=MathTools.AVERAGE.value,
                description="Find the average of a list of numbers",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "numbers": {
                            "type": "array",
                            "items": {"type": "number"},
                            "description": "A list of numbers to find the average of",
                        }
                    },
                    "required": ["numbers"],
                },
            ),
            Tool(
                name=MathTools.MEDIAN.value,
                description="Find the median of a list of numbers",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "numbers": {
                            "type": "array",
                            "items": {"type": "number"},
                            "description": "A list of numbers to find the median of",
                        }
                    },
                    "required": ["numbers"],
                },
            ),
            Tool(
                name=MathTools.MODE.value,
                description="Find the most common number in a list",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "numbers": {
                            "type": "array",
                            "items": {"type": "number"},
                            "description": "A list of numbers to find ",
                        }
                    },
                    "required": ["numbers"],
                },
            ),
            Tool(
                name=MathTools.RANGE.value,
                description="Find the range of a list of numbers",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "numbers": {
                            "type": "array",
                            "items": {"type": "number"},
                            "description": "A list of numbers to find the range of",
                        }
                    },
                    "required": ["numbers"],
                },
            ),
        ]

    @server.call_tool()
    async def call_tool(
        name: str, arguments: dict
    ) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        """Handle tool calls for math queries."""
        try:
            input = MathInput(**arguments)
            input.operation = name
            result = math_server.operate(input)    

            return [
                TextContent(type="text", text=json.dumps(result.model_dump(), indent=2))
            ]

        except Exception as e:
            raise ValueError(f"Error processing mcp-server-math query: {str(e)}")

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options)
