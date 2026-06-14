# -----------------------------------------
# Project: Offline Chatbot with Voice Assistant
# Developer: Sweta Gajanan Gurmule
# File Name: offline chatbot.py
# Description: Offline ChatGPT-like AI Assistant
# -----------------------------------------
import ollama

messages = []

print("===================================")
print("Typing Chatbot Started")
print("Type 'exit' to stop")
print("===================================")

while True:
    user_input = input("\nType your question: ")

    if user_input.lower() == "exit":
        print("Closing Chatbot...")
        break

    messages.append({
        "role": "user",
        "content": user_input + ". Answer in 2-3 lines only."
    })

    response = ollama.chat(
        model="mistral",
        messages=messages,
        options={"num_predict": 50}
    )

    reply = response["message"]["content"]

    messages.append({
        "role": "assistant",
        "content": reply
    })

    print("AI:", reply)

    if len(messages) > 6:
        messages = []