from typing import Optional
from typing_extensions import TypedDict
from models.schemas import (
    ConferenceInput, SponsorAgentOutput, SpeakerAgentOutput,
    ExhibitorAgentOutput, VenueAgentOutput, PricingAgentOutput,
    GTMAgentOutput, OpsAgentOutput
)

class ConferenceState(TypedDict):
    # Input
    conference_input: ConferenceInput

    # Agent outputs
    sponsors: Optional[SponsorAgentOutput]
    speakers: Optional[SpeakerAgentOutput]
    exhibitors: Optional[ExhibitorAgentOutput]
    venues: Optional[VenueAgentOutput]
    pricing: Optional[PricingAgentOutput]
    gtm: Optional[GTMAgentOutput]
    agenda: Optional[OpsAgentOutput]

    # Error tracking
    errors: list[str]