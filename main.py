from fastapi import FastAPI
from httpx import Client
import uuid
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain.messages import HumanMessage
load_dotenv()
app=FastAPI()
conversation_id=""
@app.post("/start_conversation")
def start_conversation():
    global conversation_id
    global history
    conversation_id=str(uuid.uuid4())
#------------ create chatbot 
llm=init_chat_model("gpt-4.1-mini",temperature=1.5 ,max_tokens=1000,max_retries=3,timeout=3000)
chatbot=create_agent(llm ,
                      system_prompt="You are a helpful science fiction writer",
                      checkpointer=InMemorySaver())
@app.post("/chat")
def chat(prompt:str):
    global chatbot
    global conversation_id
    response=chatbot.invoke({
    "messages":[
        HumanMessage(content=prompt)
 ]
},{
  "configurable":{
    "thread_id":conversation_id
  }  
})
    return {
        "message":response["messages"][-1].content
        ,"history":response["messages"]
    }

    