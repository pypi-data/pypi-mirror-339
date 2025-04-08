from datetime import datetime
from typing import Optional

from pydantic import Field

from settings_models._combat import SettingsModel
from settings_models.validators import timezone_validator


class PairingKey(SettingsModel):
    """
    Pairing key data and metadata
    """
    key: str = Field(..., description="Pairing key")
    created_at: datetime = Field(..., description="Creation time of pairing key")
    revision: int = Field(..., ge=0, description="Revision of pairing key")

    created_at_validator = timezone_validator("created_at")


class _Certificate(SettingsModel):
    """
    Certificate for secure communication with kiosk devices
    """
    key: str = Field(..., description="Certificate key")
    cert: str = Field(..., description="Certificate")
    fingerprint: str = Field(..., description="SHA256 certificate fingerprint")


class _Otp(SettingsModel):
    """
    OTP secret for authentication on the kiosk
    """
    secret: str = Field(..., description="OTP secret")
    interval: int = Field(..., description="OTP interval in seconds")


Otp = Optional[_Otp]
Otp.__doc__ = _Otp.__doc__
Certificate = Optional[_Certificate]
Certificate.__doc__ = _Certificate.__doc__
