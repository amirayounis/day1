from langgraph.checkpoint.sqlite import SqliteSaver  
from langchain.agents import create_agent
from langchain.messages import HumanMessage
import sqlite3
connection=sqlite3.connect("test.sql")
chat = create_agent(
    "gpt-4.1",
    checkpointer=SqliteSaver(conn=connection)     # --store -->memory/fast /non persistant
)

chat.invoke({
    "messages":[
        HumanMessage(content="what is the capital of moon ")
    ]
},{
    "configurable":{
        "threed_id":
    }
}
)