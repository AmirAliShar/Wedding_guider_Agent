from langchain.tools import tool, ToolRuntime
from langchain.messages import HumanMessage

from tavily import TavilyClient
from typing import Dict, Any
import os 
from dotenv import load_dotenv
load_dotenv()

TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
tavily= TavilyClient()

@tool
def web_search(query:str)-> Dict[str,Any]:
    """Use for web Search"""

    return tavily.search(query)


@tool
async def travel_tool(runtime: ToolRuntime) -> str:
    """
    Handles guest/vendor travel from origin to destination.
    """

    from Agents.Agent_wk import travel_agent

    origin = runtime.state.get("origin")
    destination = runtime.state.get("destination")

    if not origin or not destination:
        return "Travel not required: origin or destination missing."

    query = f"""
    Plan travel from {origin} to {destination}.
    Include flights, buses, or local vehicles if required.
    """

    result = await travel_agent.ainvoke(
        {"messages": [HumanMessage(content=query)]}
    )

    return result["messages"][-1].content

@tool
async def search_venues(runtime: ToolRuntime) -> str:
    """
    Finds and suggests wedding venues.
    """

    from Agents.Agent_wk import venue_agent

    destination = runtime.state.get("destination")
    guest_count = runtime.state.get("guest_count")

    if not destination or not guest_count:
        return "Venue search skipped: missing destination or guest count."

    query = f"""
    Find wedding venues in {destination}
    suitable for {guest_count} guests.
    """

    result = await venue_agent.ainvoke(
        {"messages": [HumanMessage(content=query)]}
    )

    return result["messages"][-1].content

@tool
async def calculate_budget(runtime: ToolRuntime) -> str:
    """
    Allocates and validates wedding budget.
    """

    from Agents.Agent_wk import budget_agent

    total_budget = runtime.state.get("budget")
    guest_count = runtime.state.get("guest_count")
    destination = runtime.state.get("destination")

    if not total_budget or not guest_count:
        return "Budget calculation skipped: missing budget or guest count."

    query = f"""
    Allocate a wedding budget of {total_budget} PKR
    for {guest_count} guests in {destination}.
    """

    result = await budget_agent.ainvoke(
        {"messages": [HumanMessage(content=query)]}
    )

    return result["messages"][-1].content

@tool
async def search_vendor(runtime: ToolRuntime) -> str:
    """
    Finds and recommends wedding vendors.
    """

    from Agents.Agent_wk import vendor_agent

    destination = runtime.state.get("destination")
    guest_count = runtime.state.get("guest_count")

    if not destination or not guest_count:
        return "Vendor search skipped: missing inputs."

    query = f"""
    Recommend wedding vendors in {destination}
    for {guest_count} guests.
    Include catering, decor, and photography.
    """

    result = await vendor_agent.ainvoke(
        {"messages": [HumanMessage(content=query)]}
    )

    return result["messages"][-1].content

@tool
async def schedule_time(runtime: ToolRuntime) -> str:
    """
    Creates a wedding-day timeline.
    """

    from Agents.Agent_wk import timeline_agent

    destination = runtime.state.get("destination")
    event_type = runtime.state.get("event_type", "Wedding")

    query = f"""
    Create a detailed timeline for a {event_type}
    event in {destination}.
    Include setup, ceremony, and teardown.
    """

    result = await timeline_agent.ainvoke(
        {"messages": [HumanMessage(content=query)]}
    )

    return result["messages"][-1].content

