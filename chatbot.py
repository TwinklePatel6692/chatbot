from dotenv import load_dotenv

load_dotenv() 

from langchain_mistralai import ChatMistralAI
from langchain.messages import AIMessage, SystemMessage, HumanMessage
model = ChatMistralAI(
    model="mistral-small-2506",
    temperature = 0.9
)
massages = [
    SystemMessage(content="You are intelligent")
]
print("----------type 0 to Exit the Application----------")
while True:
    
    prompt = input("you: ")
    massages.append(HumanMessage(content=prompt))
    if prompt == "0":
        break
    response = model.invoke(massages)
    massages.append(AIMessage(content=response.content))

    print("Bot :",response.content)


print(massages)
