from typing import List


async def get_available_properties(
    location, check_in, check_out, num_guests
) -> List[dict]:
    ### example db query...........

    # SELECT * FROM listings
    # WHERE listings.location ILIKE '%' || :location || '%'
    #   AND listings.max_guests >= :num_guests
    #   AND listings.status = 'active'
    #   AND listings.id NOT IN (
    #       SELECT listing_id FROM bookings
    #       WHERE status = 'confirmed'
    #         AND check_in < :request_check_out
    #         AND check_out > :request_check_in
    #   )

    return [{}]


async def get_full_detail_by_list_id(listing_id) -> dict:
    ## exapmle db query..
    #
    # SELECT * FROM listings WHERE id = listing_id
    return {}


async def create_booking_into_db(
    listing_id: str,
    reference: str,
    guest_name: str,
    guest_email: str,
    guest_phone: str,
    check_in: str,
    check_out: str,
    num_guests: int,
) -> str:

    ##inster into db and return the reference id...

    return ""
