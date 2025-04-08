from enum import Enum
from typing import Optional

from settings_models._combat import SettingsModel, Field
from settings_models.validators import hhmm_validator


class _GateMode(str, Enum):
    """
    How the gate should behave
    """
    automatic = "automatic"
    permanent_open = "permanent_open"
    permanent_close = "permanent_close"
    standard = "standard"


class _DayMode(SettingsModel):
    """
    If day mode (everyone can enter) is enabled and at what time of day
    """
    enabled: bool
    start: str = Field("00:00", description="Start of day mode in format HH:MM local time")
    end: str = Field("00:00", description="End of day mode in format HH:MM local time")

    start_validator = hhmm_validator("start")
    end_validator = hhmm_validator("end")


GateMode = Optional[_GateMode]
GateMode.__doc__ = _GateMode.__doc__
DayMode = Optional[_DayMode]
DayMode.__doc__ = _DayMode.__doc__
