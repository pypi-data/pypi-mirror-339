# Natural Programming with Python

A minimalistic natural programming inspired library for easy integration of LLMs into Python in a more pythonic way.

## Installation

```bash
pip install naturalpy
```

## Overview

`naturalpy` provides a seamless way to integrate LLM calls into your Python code using simple decorators. It transforms your functions into natural language interfaces to AI models, handling all the complexity of API calls and response parsing.
It uses type annotations and docstrings to convert function calls into structured LLM queries and properly typed responses.

## Features

- Simple `@natural` decorator syntax
- Uses function docstrings as prompts
- Parameter substitution with `${param_name}` syntax
- Automatic response parsing based on return type annotations
- Supports complex return types
- Configurable model parameters (temperature, max tokens, etc.)

## Supported Types
- Any Pydantic model
- Primitive types: str, int, float, bool 
- Collection types: List, Dict 
- Type composition: Union, Literal, Optional

## Quick Start

First, set your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY=your-api-key-here
```

Then, use the `@natural` decorator in your code:

```python
from naturalpy import natural
from typing import List

@natural
def generate_ideas(topic: str, count: int) -> List[str]:
    """
    Generate ${count} creative ideas related to ${topic}.
    Each idea should be innovative and practical.
    """

# Call like a normal function
ideas = generate_ideas("sustainable urban gardening", 3)
print(ideas)  # ['Vertical hydroponic systems for balconies', ...]
```

## Advanced Usage

### Returning Complex Types

The `@natural` decorator supports a variety of return types:

```python
from naturalpy import natural
from typing import List
from pydantic import BaseModel

# Example of a Pydantic model
class MovieRecommendation(BaseModel):
    title: str
    year: int
    director: str
    why_recommended: str

@natural
def recommend_movie(genres: List[str], mood: str) -> MovieRecommendation:
    """
    Recommend a movie that matches these genres: ${genres}
    The viewer is in a ${mood} mood.
    """

movies = recommend_movie(["action", "comedy"], "happy")
print(movies)

# Example of a complex return type
class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str

class Person(BaseModel):
    name: str
    age: int
    addresses: List[Address]

@natural
def get_people_data(inp: str) -> List[Person]:
    """
    Extract: ${inp}
    """

data = get_people_data("John Smith is 35 years old. He has homes at 123 Main St, Springfield, IL 62704 and 456 Oak Ave, Chicago, IL 60601.")
print(data)
```

### Classification

```python
from naturalpy import natural
from typing import Literal

@natural
def classifier(text: str, classes: List[str]) -> Literal["BILLING", "SHIPPING", "RETURN", "EXCHANGE"]:
    """
    Classify the following text: "${text}"

    Give me a label from the following classes:
    ${classes}
    """
```

### Union, Literal, Optional Types
```python
from naturalpy import natural
from typing import Union, Literal
from pydantic import BaseModel

class UserQuery(BaseModel):
    type: Literal["user"]
    username: str


class SystemQuery(BaseModel):
    type: Literal["system"]
    command: str


Query = Union[UserQuery, SystemQuery]

@natural
def parse(query: str) -> Query:
    """
    Parse the following query: "${query}"
    
    The query can be either a user query or a system command.
    """

result = parse("user lookup jsmith")
print(result)
```

### Customizing LLM Parameters

You can customize the LLM parameters by passing them to the decorator:

```python
@natural(
    model="gpt-4o-2024-08-06",
    temperature=0.9,
    max_tokens=500
)
def write_story(plot: str, style: str) -> str:
    """
    Write a short story based on this plot:
    ${plot}
    
    Write in the style of ${style}.
    """
```

## Error Handling

The decorator includes robust error handling:

- Missing docstring: `ValueError` is raised if a function has no docstring
- Missing return type: `TypeError` is raised if a function has no return type annotation
- Invalid parameter references: `RuntimeError` is raised if the docstring references parameters that don't exist
- API or parsing errors: `RuntimeError` is raised with details about the failure

## How It Works

1. The decorator extracts the function's docstring and uses it as a prompt
2. It substitutes `${parameter_name}` placeholders with actual argument values
3. It determines the expected return type from the function's annotations
4. It calls the OpenAI API with the assembled prompt
5. The response is parsed according to the expected type using instructor
6. The parsed result is returned from the function call

## Limitations
- Currently only supports OpenAI API (Will add support for other LLMs in the future)
- Currently only support synchronous calls (Will add support for async calls in the future)
- No support for streaming responses (Will add support for streaming in the future)
- No support for tool calls (Will add support for tool calls in the future)

## Requirements

- Python 3.11+
- OpenAI API key

## Dependencies
- OpenAI
- Pydantic
- Instructor

## License

MIT License
