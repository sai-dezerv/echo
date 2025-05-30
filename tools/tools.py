

class Tools:
    tools = []
    def __init__(self):
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_weather",
                    "description": "Get current temperature for provided coordinates in celsius.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "latitude": {"type": "number"},
                            "longitude": {"type": "number"},
                        },
                        "required": ["latitude", "longitude"],
                        "additionalProperties": False,
                    },
                    "strict": True,
                },
            }
        ]
    