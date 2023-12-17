import openai

openai.api_key = "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"

memory = []

while True:
    inp = input("User: ")
    if (inp == 'exit'):
        break
    memory.append(inp)
    completion = openai.Completion.create(
        model="text-davinci-002",
        prompt="The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nUser: " + "\nUser: ".join(memory) + "\nAssistant:",
        temperature=0.7,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    message = completion.choices[0].text.strip()
    memory.append(message)
    print("Assistant:", message)
