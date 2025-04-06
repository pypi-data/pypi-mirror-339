from typing import Any, Dict, List, Optional, get_type_hints  # Imports needed for type hints and general utility
from langchain_core.language_models import BaseChatModel  # Base class for chat models
from langchain_core.messages import AIMessage, BaseMessage  # Message classes for handling conversation
from langchain_core.outputs import ChatGeneration, ChatResult  # Classes for generation and result objects
from pydantic import Field  # For data validation and settings management
import requests  # HTTP library for API requests
import json  # For JSON serialization and deserialization
import inspect  # Utility to inspect function signatures


class ChatLilypad(BaseChatModel):
    """Custom chat model using the Lilypad API with tool binding."""
    model: str = Field(alias="model_name")  # Alias for specifying the model's name
    api_key: str = Field(alias="api_key")  # Alias for specifying the API key
    temperature: float = 0.6  # Controls response randomness (higher = more random)
    api_url: str = "https://anura-testnet.lilypad.tech/api/v1/chat/completions"  # API endpoint
    tools: list = []  # List to store tool-related configurations

    def _parse_tool_calls(self, response_json: dict) -> Optional[List[dict]]:
        """
        Parse the tool calls from the API's response.
        Extracts information on tools triggered in the chat generation process.
        """
        if "choices" in response_json and response_json["choices"]:  # Check if 'choices' exist in the response
            raw_tool_calls = response_json["choices"][0]["message"].get("tool_calls", [])  # Extract tool call details
            tool_calls = []
            for raw_tool_call in raw_tool_calls:
                args = raw_tool_call["function"]["arguments"]  # Get tool arguments
                try:
                    args_dict = json.loads(args) if isinstance(args, str) else args  # Parse arguments to a dictionary
                except json.JSONDecodeError:
                    args_dict = {}  # Default to empty dictionary if parsing fails
                tool_calls.append({
                    "name": raw_tool_call["function"]["name"],  # Name of the tool
                    "args": args_dict,  # Tool arguments
                    "id": raw_tool_call["id"],  # Tool ID
                    "type": "tool_call",  # Identifier for tool call type
                })
            return tool_calls
        return []

    def bind_tools(self, tools, tool_choice=None):
        """
        Bind external tools to the model.
        Tools allow for extending functionality with custom functions.
        """
        temp = []  # Temporary list to store formatted tools
        for tool in tools:
            types = get_type_hints(tool.func)  # Get type hints for the tool's function
            args = list(inspect.signature(tool.func).parameters.keys())  # Extract argument names
            arg_types = [types[arg].__name__ for arg in args if arg in types]  # Extract argument types
            temp_properties = {arg: {"type": arg_types[i]} for i, arg in enumerate(args) if len(arg_types) > i}
            temp.append({
                "type": "function",  # Specify tool type as function
                "function": {
                    "name": tool.name,  # Tool name
                    "description": tool.description,  # Tool description
                    "parameters": {
                        "type": "object",  # Define parameter structure
                        "properties": temp_properties,  # Add argument types
                        "required": args,  # Mark required arguments
                    },
                    "tool_choice": tool_choice,  # Add tool choice option
                },
            })
        # Create a copy of the model to assign tools
        new_model = ChatLilypad(
            model_name=self.model,
            api_key=self.api_key,
            temperature=self.temperature,
            api_url=self.api_url,
        )
        new_model.tools = temp  # Bind the tools to the new model
        return new_model

    def _generate(self, messages: List[BaseMessage], stop: Optional[List[str]] = None, **kwargs: Any) -> ChatResult:
        """
        Generate responses using the Lilypad API.
        Handles conversation inputs, communicates with the API, and parses outputs.
        """
        # Prepare messages in the API-expected format
        custom_messages = [{"role": "user" if msg.type == "human" else msg.type, "content": msg.content} for msg in messages]
        payload = {
            "model": self.model,  # Model configuration
            "messages": custom_messages,  # Message list
            "stream": False,  # Whether to use streaming responses
            "temperature": self.temperature,  # Response randomness
            "tools": self.tools,  # Tool configuration
        }
        headers = {
            "Content-Type": "application/json",  # Set content type
            "Accept": "application/json",  # Accept JSON response
            'Authorization': f"Bearer {self.api_key}",  # API authentication header
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=payload)  # Make API request
            response.raise_for_status()  # Raise exception if request fails
            response_json = response.json()  # Parse the API response to JSON
            result = response_json["choices"][0]["message"]["content"]  # Extract response content
            tool_calls = self._parse_tool_calls(response_json)  # Parse tool call information
            message = AIMessage(content=result, tool_calls=tool_calls)  # Create an AI message object
            generation = ChatGeneration(message=message)  # Wrap it in a generation object
            return ChatResult(generations=[generation])  # Return the final result

        except requests.exceptions.RequestException as e:  # Handle request errors
            message = AIMessage(content=f"Error connecting to API: {e}")
            generation = ChatGeneration(message=message)
            return ChatResult(generations=[generation])

        except (KeyError, IndexError, json.JSONDecodeError) as e:  # Handle response parsing errors
            message = AIMessage(content=f"Error parsing API response: {e}")
            generation = ChatGeneration(message=message)
            return ChatResult(generations=[generation])

    @property
    def _llm_type(self) -> str:
        """Return the type of the language model."""
        return "lilypad-chat-model"

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """Return identifying parameters of the model."""
        return {
            "model": self.model,
            "temperature": self.temperature,
            "api_url": self.api_url,
            "api_key": self.api_key,
        }
        
