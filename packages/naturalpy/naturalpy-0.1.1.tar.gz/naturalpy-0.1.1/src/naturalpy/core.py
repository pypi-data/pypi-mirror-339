import inspect
import re
import os
from functools import wraps
from typing import get_type_hints
from openai import OpenAI
import instructor

# Initialize global OpenAI client
client = instructor.from_openai(OpenAI(api_key=os.environ.get("OPENAI_API_KEY")))

def natural(func=None, *, model="gpt-4o-2024-08-06", temperature=0.7, max_tokens=None, **extra_params):
    """
    Decorator to transform functions into natural language interfaces to LLMs.
    Can be used as @natural or @natural(model="gpt-4o", temperature=1.0)
    Args:
        func: The function to decorate
        model (str): The LLM model to use
        temperature (float): Controls randomness in generation (0-2)
        max_tokens (int, optional): Maximum number of tokens to generate
        **extra_params: Additional parameters to pass to the OpenAI API
    """

    def decorator(func):
        # Check return type at decoration time, not execution time
        type_hints = get_type_hints(func)
        return_type = type_hints.get("return", None)
        if return_type is None:
            raise TypeError("Function must have a return type annotation.")

        @wraps(func)
        def wrapper(*args, **kwargs):
            # Bind arguments
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()

            # Get prompt from docstring
            docstring = func.__doc__
            if not docstring:
                raise ValueError("Function must have a docstring as prompt.")

            prompt = docstring.strip()

            # Find all placeholders in the docstring
            placeholders = re.findall(r'\$\{([^}]+)\}', prompt)

            # Check if all placeholders are valid parameter names
            for placeholder in placeholders:
                if placeholder not in bound_args.arguments:
                    raise RuntimeError(
                        f"Invalid parameter placeholder '${{{placeholder}}}' in docstring. Available parameters: {list(bound_args.arguments.keys())}")

            # Substitute all valid placeholders
            for key, value in bound_args.arguments.items():
                prompt = re.sub(rf"\$\{{{key}\}}", str(value), prompt)

            try:
                # Build parameters with user overrides
                api_params = {
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "response_model": return_type,
                    "temperature": temperature,
                    **extra_params
                }

                # Add max_tokens if specified
                if max_tokens is not None:
                    api_params["max_tokens"] = max_tokens

                # Add any extra parameters
                api_params.update(extra_params)

                completion = client.chat.completions.create(**api_params)
                return completion
            except Exception as e:
                raise RuntimeError(f"LLM call or parsing failed: {e}")

        return wrapper

    # This handles the case where decorator is used without parentheses
    if func is not None:
        return decorator(func)
    return decorator
