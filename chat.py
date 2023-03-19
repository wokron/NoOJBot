import os

from bot import NoOJBot

if __name__ == "__main__":
    os.environ["OPENAI_API_KEY"] = "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"

    bot = NoOJBot("E:/Study/code/java/NoOJ-Metrics-Kit/src/main/java/")

    while True:
        input_str = input("User:")

        if input_str.lower() == "quit" or input_str.lower() == "q":
            break

        print(bot(input_str))

    print("quit success")
