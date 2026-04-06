from pydantic import BaseModel
from typing import Optional

# ── INPUT ──────────────────────────────────────
class ConferenceInput(BaseModel):
    category: str           # "AI", "Web3", "ClimateTech"
    geography: str          # "India", "USA", "Europe", "Singapore"
    audience_size: int
    budget_usd: Optional[int] = None
    duration_days: int = 1

# ── AGENT OUTPUTS ───────────────────────────────
class Sponsor(BaseModel):
    name: str
    industry: str
    relevance_score: float
    reason: str
    outreach_email: str

class SponsorAgentOutput(BaseModel):
    sponsors: list[Sponsor]

# --- Person 2 defines content, but YOU define the shape ---

class Speaker(BaseModel):
    name: str
    title: str
    company: str
    influence_score: float
    suggested_topic: str
    bio_summary: str

class SpeakerAgentOutput(BaseModel):
    speakers: list[Speaker]

class Exhibitor(BaseModel):
    name: str
    category: str       # "startup", "enterprise", "tools"
    description: str

class ExhibitorAgentOutput(BaseModel):
    exhibitors: list[Exhibitor]

class Venue(BaseModel):
    name: str
    city: str
    capacity: int
    price_per_day_usd: int
    past_events: list[str]
    notes: str

class VenueAgentOutput(BaseModel):
    venues: list[Venue]

class PricingTier(BaseModel):
    tier_name: str
    price_usd: int
    expected_conversions: int

class PricingAgentOutput(BaseModel):
    tiers: list[PricingTier]
    predicted_attendance: int
    predicted_revenue_usd: int
    breakeven_attendance: int

class CommunityPromotion(BaseModel):
    community_name: str
    platform: str
    niche: str
    message_draft: str
    recommended_post_date: str

class GTMAgentOutput(BaseModel):
    promotions: list[CommunityPromotion]
    gtm_summary: str

class AgendaSlot(BaseModel):
    day: int
    start_time: str
    end_time: str
    session_title: str
    speaker_name: str
    room: str

class OpsAgentOutput(BaseModel):
    agenda: list[AgendaSlot]
    conflicts_detected: list[str]
    rooms_used: list[str]

# ── FINAL OUTPUT ────────────────────────────────
class ConferencePlan(BaseModel):
    input: ConferenceInput
    sponsors: SponsorAgentOutput
    speakers: SpeakerAgentOutput
    exhibitors: ExhibitorAgentOutput
    venues: VenueAgentOutput
    pricing: PricingAgentOutput
    gtm: GTMAgentOutput
    agenda: OpsAgentOutput