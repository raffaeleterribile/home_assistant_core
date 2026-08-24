"""Constants for the AI device agent integration."""

DOMAIN = "ai_device_agent"
DEFAULT_TITLE = "AI Device Agent"

SUPPORTED_DOMAINS = {"light", "switch"}
UNSUPPORTED_DOMAIN_KEYWORDS = {
    "climate",
    "cover",
    "fan",
    "media",
    "lock",
    "camera",
}
BACKEND_UNAVAILABLE_MESSAGE = (
    "The AI device agent is temporarily unavailable. Please try again shortly."
)
