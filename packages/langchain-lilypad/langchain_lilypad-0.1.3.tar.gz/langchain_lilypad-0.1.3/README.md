# ChatLilypad

ChatLilypad is a powerful and customizable chat model built on the `LangChain` framework. It integrates seamlessly with the Lilypad API, extending the functionality of traditional chat models through tool binding, structured output, and workflow integration. This module empowers developers to create dynamic, intelligent conversational agents tailored to their unique needs.

- [ChatLilypad](#chatlilypad)
  - [Overview](#overview)
  - [Features](#features)
  - [Setup](#setup)
    - [Prerequisites](#prerequisites)
    - [Dependencies](#dependencies)
    - [Installation](#installation)
  - [Usage](#usage)
    - [Initializing the Model](#initializing-the-model)
    - [Generating Responses](#generating-responses)
  - [Customization](#customization)
    - [Adjusting Temperature](#adjusting-temperature)
    - [Changing the API Endpoint](#changing-the-api-endpoint)
  - [Tool Integration](#tool-integration)
    - [Supported Models](#supported-models)
    - [Defining and Binding Tools](#defining-and-binding-tools)
  - [Structured Output](#structured-output)
    - [Defining Structured Output](#defining-structured-output)
    - [Example Usage](#example-usage)
  - [License](#license)


## Overview

ChatLilypad is designed to facilitate intelligent, scalable conversations by combining a custom chat model with external tools via the Lilypad API. The model supports structured responses, tool binding, and graph and workflow integration while providing high configurability for advanced use cases.

## Features

- **Lilypad Chat Model**: Dynamically generates responses using the Lilypad API.
- **Tool Integration**: Connects external tools to expand conversational capabilities.
- **High Configurability**: Allows developers to modify parameters like temperature, API endpoints, and tool configurations.
- **Structured Output**: Delivers organized, schema-defined responses for improved validation.
- **Error Handling**: Incorporates fallback mechanisms for API connectivity and parsing issues.
- **Extendable Design**: Built on `LangChain`, enabling modular development and scalability.

## Setup

### Prerequisites
To use ChatLilypad, ensure you have:
- Python 3.8 or higher
- Pip (Python package manager)
- API key for the [Lilypad API](https://anura.lilypad.tech)

### Dependencies
Required Python packages:
- `requests`: For HTTP API communication.
- `json`: For data serialization and deserialization.
- `pydantic`: For data validation and model schema definitions.
- `langchain_core`: Core classes and functionality for chat models.

Install all dependencies:
```bash
pip install requests pydantic langchain-core
```

### Installation
To install the ChatLilypad module:
```bash
pip install langchain-lilypad
```

## Usage

### Initializing the Model
Import and initialize `ChatLilypad` with your Lilypad API key and the model name:
```python
from langchain_lilypad import ChatLilypad

lilypad_model = ChatLilypad(
    model_name="your_model_name",
    api_key="your_api_key"
)
```

### Generating Responses
Send a list of messages to the model to generate intelligent responses:
```python
from langchain_core.messages import BaseMessage

messages = [
    BaseMessage(type="human", content="Tell me a joke!"),
]

response = lilypad_model.invoke(messages)
print({"messages": [response]})
```

## Customization

### Adjusting Temperature
Control the randomness of responses by modifying the `temperature` parameter:
```python
lilypad_model.temperature = 0.8
```

### Changing the API Endpoint
Connect to a custom API endpoint by updating the `api_url`:
```python
lilypad_model.api_url = "https://new-api-endpoint.com"
```

## Tool Integration

Tooling enhances ChatLilypad's capabilities by enabling seamless integration with external APIs and resources.

### Supported Models
Currently, only the following models support tooling:
- **llama3.1:8b**
- **qwen2.5:7b**
- **qwen2.5-coder:7b**
- **phi4-mini:3.8b**
- **mistral:7b**

### Defining and Binding Tools
Tools can be defined and dynamically bound to the model. For example:
```python
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_core.tools import tool

search = DuckDuckGoSearchResults(safesearch="strict", max_results=10)

@tool
def websearch(webprompt: str) -> str:
    """Performs accurate web searches based on user input."""
    return search.invoke(webprompt)

lilypad_model = lilypad_model.bind_tools([websearch])
```

Once bound, tools enable enhanced interaction during conversations.

## Structured Output

ChatLilypad supports structured output for organized and schema-compliant responses.

### Defining Structured Output
Define structured schemas using `Pydantic` models:

```python
from pydantic import BaseModel, Field
from typing import Optional

class Joke(BaseModel):
    """Joke to tell user."""
    setup: str = Field(description="The setup of the joke")
    punchline: str = Field(description="The punchline of the joke")
    rating: Optional[int] = Field(default=None, description="How funny the joke is (1-10)")
```

### Example Usage
Bind the structured schema to the model:
```python
structured_llm = lilypad_model.with_structured_output(Joke)
response = structured_llm.invoke("Tell me a joke")
print(response)
```
This ensures that generated responses conform to the `Joke` schema, improving validation and usability.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.