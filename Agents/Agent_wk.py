import os
import sys
import asyncio
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver


# Get the parent directory of the current script's directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from Model_Prompts.Instruction import (
    travel_prompt, Destination_prompt,
    budget_prompt, timeline_prompt,
    vendor_prompt, supervised_prompt
)

from Utils.utills import (
    travel_tool, search_venues,
    schedule_time, search_vendor,
    calculate_budget,web_search
)

class WeddingAgentSystem:

    def __init__(self) -> None:
        load_dotenv()

        self.GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        self.GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

        if not self.GROQ_API_KEY or not self.GOOGLE_API_KEY:
            raise ValueError("API key is not found")

        self.model = init_chat_model(
            model="groq:llama-3.1-8b-instant"
        )
        #self.model= init_chat_model(model="gemini-robotics-er-1.5-preview")

    def travel_agent(self):
        return create_agent(
            model=self.model,
            tools=[web_search],
            system_prompt=travel_prompt
        )

    def venue_agent(self):
        return create_agent(
            model=self.model,
            tools=[web_search],
            system_prompt=Destination_prompt
        )

    def budget_agent(self):
        return create_agent(
            model=self.model,
            tools=[calculate_budget],
            system_prompt=budget_prompt
        )

    def vendor_agent(self):
        return create_agent(
            model=self.model,
            tools=[web_search],
            system_prompt=vendor_prompt
        )

    def timeline_agent(self):
        return create_agent(
            model=self.model,
            tools=[schedule_time],
            system_prompt=timeline_prompt
        )

    async def supervised_agent(self, user_query: str):
        super_agent = create_agent(
            model=self.model,
            tools=[
                calculate_budget,
                travel_tool,
                search_venues,
                search_vendor,
                schedule_time
            ],
            system_prompt=supervised_prompt,
            checkpointer=InMemorySaver()
        )
        thread ={"configurable": {"thread_id": "2"}}
        result = await super_agent.ainvoke(
            {
                "messages": [
                    HumanMessage(content=user_query)
                ]
            },
            config= thread,
            
        )

        return result["messages"][-1].content



if __name__ == "__main__":
    import asyncio

    system = WeddingAgentSystem()

    user_query = input("Enter your wedding requirements: ")

    response = asyncio.run(system.supervised_agent(user_query))
    print("\nFinal Wedding Plan:\n")
    print(response)

