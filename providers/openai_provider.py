import json
import os
from openai import OpenAI
from dotenv import load_dotenv
from tools.weather_api import get_weather

load_dotenv()

client= OpenAI(api_key=os.getenv("OPENAI_API"))

model="gpt-4o"

tools = [
    {
        "type": "function",
        "name": "get_weather",
        "description": "get current weather for the city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "enter city name",  # ✅ inside the property
                }
            },
            "required": ["city"],
            "additionalProperties": False,  # ✅ boolean
        },
        "strict": True,
    }
]

SYSTEM_PROMPT="""
You are a helpful weather assistant.

Rules:
1. For current weather questions, call the weather tool.
2. Never invent temperature, humidity, or weather conditions.
3. Use only the returned tool data to answer.
4. If the city is missing, ask the user which city.
5. If the tool returns an error, explain it honestly.
6. Answer in simple English.
7. Include the city, temperature in Celsius, and
   other available weather details.
"""

def ask_assistant(user_prompt:str):
    
    input_items=[
        {"role":"system","content":SYSTEM_PROMPT},
        {"role":"user","content":user_prompt}
    ]
    
    result=client.responses.create(
        model=model,
        input=input_items,
        tools=tools,
        tool_choice="auto",
        temperature=0.2,
        max_output_tokens=500
        
    )
    
    while True:
        function_calls=[]
        for item in result.output:
            if item.type=="function_call":
                function_calls.append(item)
        if not function_calls:
            return result.output_text
        
        input_items.extend(result.output)
        
        for call in function_calls:
            if call.name != "get_weather":
                tool_result = {"error": "Unknown tool requested."}
            else:
                try:
                    arguments = json.loads(call.arguments)
                    city = arguments["city"]
                    tool_result=get_weather(city)
                except (json.JSONDecodeError, KeyError, TypeError):
                    tool_result = {
                            "error": "Invalid arguments supplied to the weather tool."
                        }
            input_items.append({
                "type":"function_call_output",
                "call_id":call.call_id,
                "output": json.dumps(tool_result)
            })
            
            result=client.responses.create(
                model=model,
                input=input_items,
                tools=tools,
                tool_choice="auto",
                temperature=0.2,
                max_output_tokens=500
            )
            
            
