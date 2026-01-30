from typing import Optional, Dict, List
from typing_extensions import TypedDict

class WeddingState(TypedDict, total=False):
    # User Inputs
    origin: str                 # e.g. "Pakistan", "Lahore"
    destination: str            # e.g. "Karachi"
    guest_count: int            # e.g. 100
    budget: int                 # e.g. 500000
    event_type: str             # Wedding / Nikah / Walima
    event_date: Optional[str]   # "2025-03-12"

    # Budget Breakdown
    budget_allocation: Dict[str, int]
    budget_feasible: bool

    # Venue
    venue_selected: Optional[str] 
    venue_cost: Optional[int]

    # Vendors
    vendors_selected: Dict[str, str]
    vendor_costs: Dict[str, int]

    # Travel
    travel_required: bool
    travel_plan: Optional[str]
    travel_cost: Optional[int]

    # Timeline
    timeline: Optional[List[str]]

    # Supervisor Meta
    missing_fields: List[str]
    conflicts: List[str]
