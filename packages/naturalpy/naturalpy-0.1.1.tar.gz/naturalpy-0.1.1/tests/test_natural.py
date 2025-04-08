import unittest
from typing import List, Dict
from pydantic import BaseModel

from naturalpy import natural

# Test Models
class Book(BaseModel):
    title: str
    author: str
    year: int
    genre: str


class Weather(BaseModel):
    temperature: float
    condition: str
    humidity: int
    wind_speed: float


class Recipe(BaseModel):
    name: str
    ingredients: List[str]
    steps: List[str]
    prep_time: str
    difficulty: str


class TestNaturalDecorator(unittest.TestCase):
    def test_basic_usage(self):
        """Test the most basic usage of @natural with default parameters"""

        @natural
        def get_book_recommendation(genre: str) -> Book:
            """
            Recommend a classic book in the ${genre} genre.
            Include the title, author, publication year, and genre.
            """

        book = get_book_recommendation("science fiction")

        self.assertIsInstance(book, Book)
        self.assertTrue(book.title)
        self.assertTrue(book.author)
        self.assertIsInstance(book.year, int)
        self.assertEqual(book.genre.lower(), "science fiction")

    def test_with_parameters(self):
        """Test @natural with custom parameters"""

        @natural(temperature=1.0, model="gpt-4o-2024-08-06")
        def get_weather_forecast(city: str, day: str) -> Weather:
            """
            What's the weather forecast for ${city} on ${day}?
            Provide the temperature (in Celsius), weather condition,
            humidity percentage, and wind speed in km/h.
            """

        forecast = get_weather_forecast("Tokyo", "Saturday")

        self.assertIsInstance(forecast, Weather)
        self.assertIsInstance(forecast.temperature, float)
        self.assertIsInstance(forecast.humidity, int)
        self.assertTrue(0 <= forecast.humidity <= 100)  # Valid humidity percentage

    def test_with_list_return(self):
        """Test @natural with a List return type"""

        @natural
        def get_recipes(cuisine: str, difficulty: str, count: int = 2) -> List[Recipe]:
            """
            Give me ${count} ${difficulty} recipes from ${cuisine} cuisine.
            For each recipe, provide the name, ingredients list, cooking steps,
            preparation time, and difficulty level.
            """

        recipes = get_recipes("Italian", "easy")

        self.assertIsInstance(recipes, list)
        self.assertEqual(len(recipes), 2)  # Default count parameter
        for recipe in recipes:
            self.assertIsInstance(recipe, Recipe)
            self.assertIsInstance(recipe.ingredients, list)
            self.assertIsInstance(recipe.steps, list)
            self.assertEqual(recipe.difficulty.lower(), "easy")

    def test_error_handling(self):
        """Test error handling when using @natural"""

        # Missing docstring
        with self.assertRaises(ValueError):
            @natural
            def missing_docstring(query: str) -> str:
                pass

            missing_docstring("query")

        # Missing return type
        with self.assertRaises(TypeError):
            @natural
            def missing_return_type(query: str):
                """Generate something based on ${query}"""

        # Invalid parameter substitution
        @natural
        def invalid_param(query: str) -> str:
            """Generate something based on ${invalid_param}"""

        with self.assertRaises(RuntimeError):
            invalid_param("test")


if __name__ == "__main__":
    unittest.main()
