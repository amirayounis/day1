from fastapi import FastAPI
from httpx import Client
import uuid
from dotenv import load_dotenv
import os
from typing import Any
load_dotenv()
g_api_key=os.getenv("GOOGLE_API_KEY")
open_ai_api_key=os.getenv("OPENAI_API_KEY")
app=FastAPI()
# ----------- test
@app.post("/get_reciepie")
def get_reciepie(ingeridiants:str):
    recepi="any thing"   # --->llm
    return {
        "response":recepi
    }
@app.post("/test_gemini_ai")
def gemini():
    headers={
            "x-goog-api-key": g_api_key
        }
    client=Client(headers=headers,base_url="https://generativelanguage.googleapis.com/v1beta/interactions",
                      timeout=3000)
    response=client.post("",json={
            "model":"gemini-3.8-flash",
            "input":"what is js in 10 words"
        })    
    return {
            "response":response.json()["steps"][-1]["content"][0]["text"]
        }
conversation_id=""
@app.post("/start_conversation")
def start_conversation():
    global conversation_id
    global history
    conversation_id=str(uuid.uuid4())
    history[conversation_id]=[]
last_res_id=None
history:dict[str,dict[str,Any]]={}
@app.post("/test_open_ai")
def open_ai(prompt:str):
    global conversation_id
    global last_res_id
    headers={
        "Authorization": f"Bearer {open_ai_api_key}"
    }
    history[conversation_id].append({
        "role":"user",            # -->g--"type":"user_input"
        "content":[
            {
                "type":"input_text",   
                "text":prompt
            }
        ]
    })
    client=Client(base_url="https://api.openai.com/v1/",
                  headers=headers
                  , timeout=3000)
    response=client.post("responses",json={
        "model":"gpt-4.1",
        "input":history[conversation_id],
        "temperature":1.2,
        "max_output_tokens":1000,
        "instructions":"""
you are a helpful creative chef who provides innovative and delicious recipes based on the ingredients given.
given a list of ingredients, you will generate a unique recipe that incorporates those ingredients in a creative way.
every recipe should include a title, a list of ingredients, and step-by-step instructions for preparation.
do not answer any irrelevant questions or provide information unrelated to cooking or recipes.
"""
    })
    response.raise_for_status()
    ai_message=response.json()["output"][0]["content"][0]["text"]
    history[conversation_id].append({
        "role":"assistant",            # -->g--"type":"model_output"
        "content":[
            {
                "type":"output_text",                 
                "text":ai_message
            }
        ]
    })
    last_res_id=response.json()["id"]
    return {
        "id":response.json()["id"],
        "response":ai_message,
        "history":history[conversation_id]
    }