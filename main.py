
import importlib

PROVIDERS = {
    "1": "providers.openai_provider",
    "2": "providers.groq_provider"
}


def select_provider():

    print("\n===== SELECT AI PROVIDER =====")
    print("1. OpenAI")
    print("2. Groq")

    choice = input("\nSelect provider: ").strip()

    module_name = PROVIDERS.get(choice)

    if module_name is None:
        print("Invalid provider selection.")
        return None

    try:
        provider_module = importlib.import_module(module_name)

        return provider_module.ask_assistant

    except ImportError as error:
        print("Provider import error:", error)
        return None

    except AttributeError:
        print("Provider must define ask_assistant().")
        return None


def main():

    ask_assistant = select_provider()

    if ask_assistant is None:
        return

    print("\nWeather Assistant Started!")
    print("Type 'exit' to stop.")

    while True:

        question = input("\nYou: ").strip()

        if question.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        if not question:
            continue

        try:
            answer = ask_assistant(question)
            print("\nAssistant:", answer)

        except Exception as error:
            print("\nError:", error)


if __name__ == "__main__":
    main()
