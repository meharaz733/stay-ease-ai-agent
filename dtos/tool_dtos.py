from pydantic import BaseModel, Field

class SearchPropertiesInput(BaseModel):
    location: str = Field(description="City or area name e.g. 'Cox's Bazar', 'Sylhet'")
    check_in: str = Field(description="Check-in date in YYYY-MM-DD format")
    check_out: str = Field(description="Check-out date in YYYY-MM-DD format")
    num_guests: int = Field(description="Number of guests", ge=1, le=20)


class ListingDetailsInput(BaseModel):
    listing_id: str = Field(description="Unique identifier of the property listing")


class CreateBookingInput(BaseModel):
    listing_id: str = Field(description="ID of the property to book")
    guest_name: str = Field(description="Full name of the guest")
    guest_mail: str = Field(description="Mail address of the guest.")
    guest_phone: str = Field(description="Guest contact number")
    check_in: str = Field(description="Check-in date in YYYY-MM-DD format")
    check_out: str = Field(description="Check-out date in YYYY-MM-DD format")
    num_guests: int = Field(description="Number of guests", ge=1)

class EscalateToHumanInput(BaseModel):
    message:str = Field(description="A friendly message for informing guest")
    reason:str = Field(description="The reason human agent needed.")

