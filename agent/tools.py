from langchain.messages import AIMessage
from langchain_core.tools import tool
from langgraph.types import Command

from dtos.tool_dtos import (
    CreateBookingInput,
    EscalateToHumanInput,
    ListingDetailsInput,
    SearchPropertiesInput,
)
from services.agent_services import (
    create_booking_into_db,
    get_available_properties,
    get_full_detail_by_list_id,
)


@tool("search_available_properties", args_schema=SearchPropertiesInput)
async def search_available_properties(
    location: str,
    check_in: str,
    check_out: str,
    num_guests: int,
) -> dict:
    """
    Search for available property listings that match the guest's criteria. Use this when the guest ask for available properties and provides a location, check-in date, check-out date, and number of guests. Queries the database to find properties in the given location that are not already booked for the requested dates and can accommodate the required number of guests.

    - Example: "Show me places in Mirpur from April 10 to April 12 for 2 guests"

    INPUT:
        location (str): City or area name in Bangladesh (e.g., "Cox's Bazar", "Sylhet", "Sreemangal")
        check_in (str): Date in 'YYYY-MM-DD' format
        check_out (str): Date in 'YYYY-MM-DD' format, must be after check_in
        num_guests (int): Number of guests (1 or more)

    Returns a list of available properties.
    """

    results = await get_available_properties(location, check_in, check_out, num_guests)

    return {
        "status": "success",
        "results": results,
    }


@tool("get_listing_details", args_schema=ListingDetailsInput)
async def get_listing_details(listing_id: str) -> dict:
    """
    Retrieve complete details of a specific property listing.

    USE THIS TOOL WHEN:
    - The guest asks for more information about a property they saw in search results
    - The guest asks about amenities, house rules, cancellation policy, or rating of a particular place
    - Example: "What are the amenities in the Seaside Villa?" or "Does that property allow pets?"

    INPUT:
        listing_id (str): UUID of the listing (obtained from search results or conversation context)
    """
    result = await get_full_detail_by_list_id(listing_id)

    return {
        "status": "success",
        "listing": result,
    }


@tool("create_booking", args_schema=CreateBookingInput)
async def create_booking(
    listing_id: str,
    guest_name: str,
    guest_email: str,
    guest_phone: str,
    check_in: str,
    check_out: str,
    num_guests: int,
) -> dict:
    """
    Create a confirmed booking for a guest. Use this only when the guest explicitly confirms they want to book a specific property. Requires the listing ID, guest name, phone number, check-in and check-out dates, and number of guests. Calculates the total price based on number of nights, inserts a new booking record with status 'confirmed', and returns a booking confirmation with a unique human-readable reference number.
    """
    reference = "demo_ref"

    db_reference = await create_booking_into_db(
        listing_id,
        reference,
        guest_name,
        guest_email,
        guest_phone,
        check_in,
        check_out,
        num_guests,
    )
    return {
        "status": "success",
        "reference": db_reference,
    }


@tool("human_handover", args_schema=EscalateToHumanInput)
async def human_handover(message: str, reason: str) -> Command:
    """
    Call this when the guest's query requires a human agent.
    Use it for: complaints, complex issues, explicit human requests,
    or situations beyond your capability.

    Args:
        reason: Why human intervention is needed, under 10 words.
        message: a friendly message informing the guest, under 20 words.
    """

    return Command(
        update={
            "messages": [AIMessage(content=message)],
            "is_human_needed": True,
            "human_handover_reason": reason,
        }
    )


TOOLS = [search_available_properties, get_listing_details, create_booking, human_handover]
