# Weather API Tool Calling Assistant

A Python CLI application that provides real-time weather information using Large Language Models (LLMs) with tool calling capabilities. It supports multiple AI providers (**OpenAI** and **Groq**) and integrates with the **OpenWeatherMap API** to fetch accurate, up-to-date weather data.

## Features

- **Multi-Provider Support:** Choose between OpenAI and Groq at runtime.
- **Function/Tool Calling:** Allows the LLM to intelligently invoke the weather lookup tool based on user prompts.
- **Robust Error Handling:** Handles missing cities, network issues, and invalid tool arguments gracefully.
- **Celsius Support:** Returns temperatures in Celsius along with humidity, feels-like temperature, and conditions.

## Project Structure

```text
weather_api/
│
├── main.py                 # Entry point, handles provider selection and chat loop
├── requirements.txt        # Project dependencies
├── .env                    # Environment variables (API keys - do not commit)
├── .gitignore              # Git ignore rules
│
├── providers/              # LLM provider integrations
│   ├── __init__.py         # Package init file
│   ├── openai_provider.py  # OpenAI integration using tool calling
│   └── groq_provider.py    # Groq integration using tool calling
│
└── tools/                  # Tool definitions
    ├── __init__.py         # Package init file
    └── weather_api.py      # OpenWeatherMap API wrapper function
```

## Prerequisites

- Python 3.10+
- An API key for [OpenWeatherMap](https://openweathermap.org/api)
- An API key for either [OpenAI](https://openai.com/) or [Groq](https://groq.com/)

## Installation & Setup

1. **Clone or navigate to the project directory:**
   ```bash
   cd weather_api
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows (Git Bash):
   source venv/Scripts/activate
   # On Windows (Command Prompt / PowerShell):
   # venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your environment variables:**
   Create a `.env` file in the root directory with the following keys:
   ```env
   OPENAI_API=your_openai_api_key_here
   GROQ_API=your_groq_api_key_here
   WEATHER_API=your_open_weather_map_api_key_here
   ```

## Usage

Run the main application:
```bash
python main.py
```

Follow the on-screen prompt to select your preferred AI provider (`1` for OpenAI, `2` for Groq), then type your weather-related questions (e.g., *"What is the weather in Tokyo?"*). Type `exit` or `quit` to end the session.
