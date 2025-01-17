import fastapi
import pydantic
import uvicorn
import requests
import yaml
import unittest
import pytest


print("FastAPI version:", fastapi.__version__)
print("Pydantic version:", pydantic.__version__)
print("Uvicorn version:", uvicorn.__version__)
print("Requests version:", requests.__version__)
print("PyYAML version:", yaml.__version__)
print("unittest version:", unittest.__version__)
print("pytest version:", pytest.__version__)