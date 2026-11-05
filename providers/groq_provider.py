import json 
import os
from groq import Groq
from dotenv import load_dotenv
from tools.weather_api import get_weather

load_dotenv()

client= Groq(api_key=os.getenv("GROQ_API"))

model=  "openai/gpt-oss-20b"

tools=[{
    "type":"function",
    "function":{
        "name":"get_weather",
        "description":"get the weather in city",
        "parameters":{
            "type":"object",
            "properties":{
                "city":{"type":"string"}
            },
            "required": ["city"]
        }
    }
}]

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

def execute_tool(tool_name, arguments):
    if tool_name == "get_weather":
        return get_weather(**arguments)
    return {"error": f"Tool {tool_name} not found"}

messages=[{"role":"system","content":SYSTEM_PROMPT}]
    
def ask_assistant(user_prompt:str):
    
    messages.append({"role":"user","content":user_prompt})
    
    for _ in range(5):
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        
        message = response.choices[0].message

        # No tool requested: return final answer
        if not message.tool_calls:
            return message.content or "I couldn't generate an answer."

        # Preserve the assistant's tool-call message in history
        messages.append(message.model_dump(exclude_none=True))

        # Execute each requested tool
        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            print(f"\nCalling tool: {tool_name}")
            print(f"Arguments: {arguments}")

            result =execute_tool(tool_name, arguments)

            # Return tool output to the model
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })

    return "Maximum tool-calling attempts reached."