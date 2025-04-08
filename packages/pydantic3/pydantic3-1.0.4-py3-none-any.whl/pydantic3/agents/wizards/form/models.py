"""Form wizard models."""

from typing import List, Optional, Literal
from pydantic import BaseModel, Field, HttpUrl, EmailStr


class BusinessInfo(BaseModel):
    description: Optional[str] = Field(None, description="Brief description of your business or product")
    website: Optional[HttpUrl] = Field(None, description="Your business website (if available)")
    email: Optional[EmailStr] = Field(None, description="Contact email address")
    phone: Optional[str] = Field(None, description="Contact phone number")
    industry: Optional[str] = Field(None, description="Industry (e.g. Healthcare, Fintech)")
    type: Literal["b2b", "b2c", "internal", "custom"] = Field(
        ...,
        description="Type of customer interaction (b2b, b2c, internal use, or custom)"
    )


class BusinessGoals(BaseModel):
    goals: List[str] = Field(
        ...,
        min_items=1,
        max_items=3,
        description="Main goals of the business related to the form (1 to 3 items)"
    )


class BotSettings(BaseModel):
    bot_name: Optional[str] = Field(None, description="Name of the assistant bot")
    completion_threshold: Optional[int] = Field(
        100,
        ge=50,
        le=100,
        description="Form is considered completed when this percentage is reached (50–100)"
    )
    bot_style: Optional[str] = Field(
        "friendly",
        description="Bot's communication style (e.g. formal, friendly, casual)"
    )
    use_emojis: Optional[bool] = Field(
        True,
        description="Whether the bot is allowed to use emojis in its messages"
    )
    simulate_delay: Optional[bool] = Field(
        True,
        description="Whether the bot should simulate a typing delay before responding"
    )
    welcome_message: Optional[str] = Field(
        None,
        description="Text shown to users before they start filling out the form"
    )
    completion_message: Optional[str] = Field(
        None,
        description="Text shown to users after they complete the form"
    )


class DocumentSettings(BaseModel):
    model_tier: Optional[Literal["low", "medium", "high"]] = Field(
        "medium",
        description="AI model tier used to process and analyze the form (low = basic, high = advanced)"
    )


class FormIntentRequest(BaseModel):
    business: BusinessInfo
    business_goals: BusinessGoals
    document: DocumentSettings
    bot: BotSettings
    notes: Optional[str] = Field(None, description="Any additional thoughts or wishes")
