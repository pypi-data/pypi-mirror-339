"""
Data models for Payler SDK.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional


class PaylerPaymentStatuses(str, Enum):
    """Payment statuses used in Payler."""

    CREATED = "Created"
    PRE_AUTHORIZED_3DS = "PreAuthorized3DS"
    PRE_AUTHORIZED_3DS2 = "PreAuthorized3DS2"
    PRE_AUTHORIZED_3DS_METHOD = "PreAuthorized3DSMethod"
    AUTHORIZED = "Authorized"
    REVERSED = "Reversed"
    CHARGED = "Charged"
    REFUNDED = "Refunded"
    REJECTED = "Rejected"
    PENDING = "Pending"
    CREDITED = "Credited"


@dataclass
class PaylerCustomerUpdateOrCreateRequest:
    """Customer model in Payler system."""
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    address: Optional[str] = None
    document_type: Optional[str] = None
    document_seria: Optional[str] = None
    document_number: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert customer object to dictionary for Payler API.

        Returns:
            Dictionary with customer data in API format
        """
        return {
            "customer_name": self.name,
            "customer_phone": self.phone,
            "customer_email": self.email,
            "customer_fullName": self.full_name,
            "customer_address": self.address,
            "customer_documentType": self.document_type,
            "customer_documentSeria": self.document_seria,
            "customer_documentNumber": self.document_number,
        }


@dataclass
class PaylerCustomerUpdateOrCreateResponse:
    """Model of response on customer creation or update."""
    customer_id: str


@dataclass
class PaylerCustomerCard:
    """Customer card model."""
    card_id: str
    card_number: str
    recurrent_template_id: str


@dataclass
class PaylerCustomerCardListResponse:
    """Model of response on customer cards list."""

    cards: list[PaylerCustomerCard]


@dataclass
class PaylerPaymentResponse:
    """Model of payment response."""
    order_id: str
    status: str
    amount: float


@dataclass
class StartSaveCardSessionResponse:
    """Model of response on start save card session."""
    session_id: str
    order_id: str
    save_card_url: str


@dataclass
class RemoveSavedCardResponse:
    """Model of response on remove saved card."""
    changed: bool


@dataclass
class PaylerPaymentStatusResponse:
    """Model of payment status response."""
    status: str
    order_id: str
    amount: float
    recurrent_template_id: Optional[str] = None
    payment_type: Optional[str] = None
