from typing import Dict, Any

from langchain_core.prompts import ChatPromptTemplate

from eventforge.agents.base.base_agent import BaseAgent
from eventforge.models.pricing_model import PricingModel, suggest_base_price
from eventforge.utils.logging import get_logger
from eventforge.models.schemas import ConferenceInput, PricingAgentOutput
from eventforge.utils.llm_client import get_llm

logger = get_logger(__name__)


class PricingAgent(BaseAgent):

    def __init__(self):
        super().__init__("pricing_agent")

        self.llm = get_llm().with_structured_output(
            PricingAgentOutput, method="json_schema", strict=True
        )

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are an expert in conference pricing and revenue optimization.",
                ),
                (
                    "user",
                    """
            Conference Details:
            Category: {category}
            Geography: {geography}
            Audience Size: {audience_size}
        
            Venue Info:
            {venue_summary}
        
            MODEL SIGNALS:
            - Baseline Ticket Price: {baseline_price}
            - Predicted Attendance: {predicted_attendance}
        
            TASK:
            - Create 3 pricing tiers (basic, standard, premium)
            - Assign UNIQUE id to each tier
            - Set realistic ticket prices around baseline_price
            - Distribute conversions across tiers
        
            CONSTRAINTS:
            - Total conversions ≈ predicted_attendance
            - Total attendance <= audience_size
            - Revenue = sum(price * conversions)
            - Prices must match geography (India ≈ ₹1000–₹10000 range equivalent)
            - Avoid unrealistic spikes in premium tier
        
            OUTPUT:
            - tiers
            - predicted_revenue_usd
            """,
                ),
            ]
        )
        self.model = PricingModel()

    async def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        try:
            logger.info("PricingAgent started")

            input_data = ConferenceInput(**state["input"])

            venue_data = state["outputs"]["venue_agent"]
            sponsor_data = state["outputs"]["sponsor_agent"]
            speaker_data = state["outputs"]["speaker_agent"]

            # ---- MODEL SIGNAL ----
            baseline_price = suggest_base_price(
                input_data.geography, input_data.audience_size
            )

            predicted_attendance = self.model.predict_attendance(
                audience_size=input_data.audience_size,
                duration=input_data.duration_days,
                sponsors=len(sponsor_data.sponsors),
                speakers=len(speaker_data.speakers),
            )

            # ---- PROMPT ----
            chain = self.prompt | self.llm

            result: PricingAgentOutput = await chain.ainvoke(
                {
                    "category": input_data.category,
                    "geography": input_data.geography,
                    "audience_size": input_data.audience_size,
                    "venue_summary": str(venue_data),

                    #injected signals
                    "baseline_price": baseline_price,
                    "predicted_attendance": predicted_attendance,
                }
            )
            total_revenue = sum(
                t.price_usd * t.expected_conversions
                for t in result.tiers
            )
            result.predicted_revenue_usd = total_revenue

            # ---- ENFORCE MODEL TRUTH ----
            result.baseline_price_usd = baseline_price
            result.predicted_attendance = min(
                predicted_attendance,
                input_data.audience_size
            )

            logger.info("PricingAgent completed")

            return self._success(result)

        except Exception as e:
            logger.exception("PricingAgent failed")
            return self._fail(e)
