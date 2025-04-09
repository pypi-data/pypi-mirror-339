"""
Exceptions for Payler SDK.
"""

from enum import Enum
from typing import Any, Optional, Dict, Type


class PaylerErrorCode(Enum):
    """Payler payment system error codes."""

    NONE = 0
    INVALID_AMOUNT = 1
    BALANCE_EXCEEDED = 2
    DUPLICATE_ORDER_ID = 3
    ISSUER_DECLINED_OPERATION = 4
    LIMIT_EXCEEDED = 5
    AF_DECLINED = 6
    INVALID_ORDER_STATE = 7
    ORDER_NOT_FOUND = 9
    PROCESSING_ERROR = 10
    PARTIAL_RETRIEVE_NOT_ALLOWED = 11
    GATE_DECLINED = 13
    INVALID_CARD_INFO = 14
    INVALID_CARDNUMBER = 15
    INVALID_CARDHOLDER = 16
    INVALID_CVV = 17
    API_NOT_ALLOWED = 18
    INVALID_PASSWORD = 19
    INVALID_PARAMS = 20
    SESSION_TIMEOUT = 21
    MERCHANT_NOT_FOUND = 22
    SESSION_NOT_FOUND = 24
    CARD_EXPIRED = 25
    RECURRENT_TEMPLATE_NOT_FOUND = 26
    RECURRENT_TEMPLATE_NOT_ACTIVE = 27
    NO_TRANSACTION_BY_TEMPLATE = 28

    # Recurrent payments errors (100-199)
    RECURRENT_PAYMENTS_NOT_SUPPORTED = 100
    EXPIRED_RECURRENT_TEMPLATE = 101
    RECURRENT_TEMPLATE_ANOTHER_TERMINAL = 102
    FAILED_UPDATE_ACTIVE_STATUS = 103
    TEMPLATE_ACTIVATION_REQUIRES_BANK_CONF = 104
    REFUND_OF_RECURRENT_NOT_SUPPORTED = 105
    TOO_FREQUENT_RECURRENT_PAYMENTS = 106
    RECURRENT_TEMPLATE_REWRITTEN = 107

    # Refund and charge errors (200-299)
    PARTIAL_REFUND_NOT_ALLOWED = 200
    MULTIPLE_REFUND_NOT_SUPPORTED = 201
    PARTIAL_CHARGE_NOT_ALLOWED = 202

    # Access period errors (300-399)
    EXPIRED_RETRIEVE_PERIOD = 300

    # Validation errors (400-499)
    INVALID_EXPIRY_MONTH = 400
    INVALID_EXPIRY_YEAR = 401
    INVALID_SECURE_CODE = 402
    INVALID_EMAIL = 403

    # Card status errors (500-599)
    CARD_INACTIVE = 500
    OPERATION_NOT_SUPPORTED = 501
    DECLINED_BY_CARDHOLDER = 502
    PIN_ERROR = 503
    RESTRICTED_CARD = 504
    INVALID_CARD_STATUS = 505

    # Transaction state errors (600-699)
    DUPLICATED_OPERATION = 600
    IN_PROGRESS_ERROR = 601
    PAID_EARLIER = 602
    DEAL_NOT_FOUND = 603
    INCORRECT_TRANSACTION_TYPE = 604
    TRANSACTION_NOT_TWO_STEP = 605
    ATTEMPT_NOT_FOUND = 606
    ATTEMPTS_NUMBER_EXCEEDED = 607
    THERE_IS_NEWER_ATTEMPT = 608
    EMAIL_ATTEMPTS_NUMBER_EXCEEDED = 609
    CARD_NOT_FOUND = 610
    CARD_ALREADY_SAVED = 611
    CUSTOMER_NOT_FOUND = 612

    # Configuration and settings errors (700-799)
    TEMPLATE_NOT_FOUND = 700
    RETURN_URL_NOT_SET = 701
    TERMINAL_NOT_FOUND = 702
    CURRENCY_NOT_SUPPORTED = 703
    RECEIPT_SERVICE_NOT_ENABLED = 704

    # 3DS errors (800-899)
    THREE_DS_FAIL = 800
    NO_RESULT_OF_3DS = 801
    PREPROCESS_3DS_INFO_NOT_FOUND = 802
    NOT_INVOLVED_IN_3DS = 803
    NOT_INVOLVED_IN_3DS2 = 804

    # Merchant rights and system errors (900-999)
    OPERATION_NOT_ALLOWED_TO_MERCHANT = 900
    COMPLETED_PARTIALLY = 901
    RECONCILE_ERROR = 902
    DECLINED = 903
    TEMPORARY_MALFUNCTION = 904
    UNSUPPORTED_CARD_TYPE = 905

    # Specific payment methods errors (1000+)
    EMONEY_REFUND_NOT_SUPPORTED = 1000
    CHECKOUT_METHOD_NOT_ALLOWED = 1100
    OPERATION_NOT_CONFIRMED = 1101
    AMOUNT_LIMIT_EXCEEDED = 1102


class PaylerError(Exception):
    """Base class for all Payler SDK exceptions."""

    pass


class PaylerApiError(PaylerError):
    """Error when interacting with Payler API."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response: Optional[Any] = None,
        error_code: Optional[PaylerErrorCode] = None,
    ) -> None:
        """
        Initialize API error.

        Args:
            message: Error message
            status_code: HTTP code of response, if applicable
            response: Full response from API, if available
            error_code: Specific Payler error code, if available
        """
        self.status_code = status_code
        self.response = response
        self.error_code = error_code
        super().__init__(message)


class PaylerSessionError(PaylerError):
    """Error when creating or using Payler session."""

    pass


class PaylerTransactionNotFoundError(PaylerError):
    """Error when trying to find non-existent transaction."""

    pass


class PaylerValidationError(PaylerError):
    """Error when validating incoming or outgoing data."""

    pass


class PaylerRefundError(PaylerError):
    """Error when performing refund operation."""

    pass


# Specific exceptions for different error categories


# Payment errors
class PaylerInvalidAmountError(PaylerApiError):
    """Incorrect transaction amount"""

    pass


class PaylerBalanceExceededError(PaylerApiError):
    """Card balance exceeded"""

    pass


class PaylerDuplicateOrderIdError(PaylerApiError):
    """Duplicate order ID"""

    pass


class PaylerIssuerDeclinedOperationError(PaylerApiError):
    """Issuer declined operation"""

    pass


class PaylerLimitExceededError(PaylerApiError):
    """Limit exceeded"""

    pass


class PaylerSecurityDeclinedError(PaylerApiError):
    """Security declined operation"""

    pass


class PaylerInvalidOrderStateError(PaylerApiError):
    """Operation cannot be performed due to payment state"""

    pass


class PaylerOrderNotFoundError(PaylerApiError):
    """Payment session with specified ID not found"""

    pass


class PaylerProcessingError(PaylerApiError):
    """General error when interacting with processing"""

    pass


# Card errors
class PaylerInvalidCardInfoError(PaylerApiError):
    """Incorrect card data specified"""

    pass


class PaylerInvalidCardNumberError(PaylerApiError):
    """Incorrect card number specified"""

    pass


class PaylerInvalidCardholderError(PaylerApiError):
    """Incorrect cardholder name specified"""

    pass


class PaylerInvalidCVVError(PaylerApiError):
    """Incorrect CVV specified"""

    pass


class PaylerCardExpiredError(PaylerApiError):
    """Card expiration date expired"""

    pass


class PaylerCardInactiveError(PaylerApiError):
    """Card is inactive"""

    pass


class PaylerRestrictedCardError(PaylerApiError):
    """Restricted card"""

    pass


class PaylerCardNotFoundError(PaylerApiError):
    """Card not found"""

    pass


class PaylerCardAlreadySavedError(PaylerApiError):
    """Card already saved"""

    pass


# Recurrent payments errors
class PaylerRecurrentTemplateNotFoundError(PaylerApiError):
    """Recurrent template with specified ID not found"""

    pass


class PaylerRecurrentTemplateNotActiveError(PaylerApiError):
    """Recurrent template is not active"""

    pass


class PaylerNoTransactionByTemplateError(PaylerApiError):
    """No transactions were previously executed by template"""

    pass


class PaylerRecurrentPaymentsNotSupportedError(PaylerApiError):
    """Recurrent payments not supported"""

    pass


class PaylerExpiredRecurrentTemplateError(PaylerApiError):
    """Recurrent template expiration date expired"""

    pass


# Authorization and session errors
class PaylerApiNotAllowedError(PaylerApiError):
    """This Payler API method is not allowed from the current IP address"""

    pass


class PaylerInvalidPasswordError(PaylerApiError):
    """Access denied, because the password is incorrect"""

    pass


class PaylerInvalidParamsError(PaylerApiError):
    """One of the request parameters has an incorrect value"""

    pass


class PaylerSessionTimeoutError(PaylerApiError):
    """The time allotted for the payment has expired"""

    pass


class PaylerMerchantNotFoundError(PaylerApiError):
    """Merchant description not found"""

    pass


class PaylerSessionNotFoundError(PaylerSessionError):
    """Payment session not found"""

    pass


# 3DS errors
class PaylerThreeDSFailError(PaylerApiError):
    """3D-Secure authentication not completed"""

    pass


class PaylerNotInvolvedIn3DSError(PaylerApiError):
    """Used card does not support 3D-Secure authentication"""

    pass


class PaylerNotInvolvedIn3DS2Error(PaylerApiError):
    """Card does not support 3D-Secure 2 authentication"""

    pass


# Configuration errors
class PaylerCurrencyNotSupportedError(PaylerApiError):
    """This currency is not supported"""

    pass


class PaylerTemporaryMalfunctionError(PaylerApiError):
    """Temporary system problem"""

    pass


# Refund errors
class PaylerPartialRefundNotAllowedError(PaylerRefundError):
    """Partial refund not supported"""

    pass


class PaylerMultipleRefundNotSupportedError(PaylerRefundError):
    """Subsequent refunds are not supported in automatic mode"""

    pass


# Mapping error codes to exception classes
ERROR_CODE_MAPPING: Dict[PaylerErrorCode, Type[PaylerError]] = {
    PaylerErrorCode.INVALID_AMOUNT: PaylerInvalidAmountError,
    PaylerErrorCode.BALANCE_EXCEEDED: PaylerBalanceExceededError,
    PaylerErrorCode.DUPLICATE_ORDER_ID: PaylerDuplicateOrderIdError,
    PaylerErrorCode.ISSUER_DECLINED_OPERATION: (
        PaylerIssuerDeclinedOperationError,
    ),
    PaylerErrorCode.LIMIT_EXCEEDED: PaylerLimitExceededError,
    PaylerErrorCode.AF_DECLINED: PaylerSecurityDeclinedError,
    PaylerErrorCode.INVALID_ORDER_STATE: PaylerInvalidOrderStateError,
    PaylerErrorCode.ORDER_NOT_FOUND: PaylerOrderNotFoundError,
    PaylerErrorCode.PROCESSING_ERROR: PaylerProcessingError,
    PaylerErrorCode.INVALID_CARD_INFO: PaylerInvalidCardInfoError,
    PaylerErrorCode.INVALID_CARDNUMBER: PaylerInvalidCardNumberError,
    PaylerErrorCode.INVALID_CARDHOLDER: PaylerInvalidCardholderError,
    PaylerErrorCode.INVALID_CVV: PaylerInvalidCVVError,
    PaylerErrorCode.API_NOT_ALLOWED: PaylerApiNotAllowedError,
    PaylerErrorCode.INVALID_PASSWORD: PaylerInvalidPasswordError,
    PaylerErrorCode.INVALID_PARAMS: PaylerInvalidParamsError,
    PaylerErrorCode.SESSION_TIMEOUT: PaylerSessionTimeoutError,
    PaylerErrorCode.MERCHANT_NOT_FOUND: PaylerMerchantNotFoundError,
    PaylerErrorCode.SESSION_NOT_FOUND: PaylerSessionNotFoundError,
    PaylerErrorCode.CARD_EXPIRED: PaylerCardExpiredError,
    PaylerErrorCode.RECURRENT_TEMPLATE_NOT_FOUND: (
        PaylerRecurrentTemplateNotFoundError,
    ),
    PaylerErrorCode.RECURRENT_TEMPLATE_NOT_ACTIVE: (
        PaylerRecurrentTemplateNotActiveError,
    ),
    PaylerErrorCode.NO_TRANSACTION_BY_TEMPLATE: (
        PaylerNoTransactionByTemplateError,
    ),
    PaylerErrorCode.RECURRENT_PAYMENTS_NOT_SUPPORTED: (
        PaylerRecurrentPaymentsNotSupportedError,
    ),
    PaylerErrorCode.EXPIRED_RECURRENT_TEMPLATE: (
        PaylerExpiredRecurrentTemplateError,
    ),
    PaylerErrorCode.CARD_INACTIVE: PaylerCardInactiveError,
    PaylerErrorCode.RESTRICTED_CARD: PaylerRestrictedCardError,
    PaylerErrorCode.CARD_NOT_FOUND: PaylerCardNotFoundError,
    PaylerErrorCode.CARD_ALREADY_SAVED: PaylerCardAlreadySavedError,
    PaylerErrorCode.THREE_DS_FAIL: PaylerThreeDSFailError,
    PaylerErrorCode.NOT_INVOLVED_IN_3DS: PaylerNotInvolvedIn3DSError,
    PaylerErrorCode.NOT_INVOLVED_IN_3DS2: PaylerNotInvolvedIn3DS2Error,
    PaylerErrorCode.CURRENCY_NOT_SUPPORTED: PaylerCurrencyNotSupportedError,
    PaylerErrorCode.TEMPORARY_MALFUNCTION: PaylerTemporaryMalfunctionError,
    PaylerErrorCode.PARTIAL_REFUND_NOT_ALLOWED: (
        PaylerPartialRefundNotAllowedError,
    ),
    PaylerErrorCode.MULTIPLE_REFUND_NOT_SUPPORTED: (
        PaylerMultipleRefundNotSupportedError,
    ),
}


def handle_payler_error_code(
    error_code: int, message: str, response: Optional[Any] = None
) -> PaylerError:
    """
    Converts Payler error code to the corresponding exception.

    Args:
        error_code: Payler API error code
        message: Error message
        response: Full API response, if available

    Returns:
        Corresponding PaylerError instance
    """
    try:
        payler_error_code = PaylerErrorCode(error_code)
        exception_class = ERROR_CODE_MAPPING.get(
            payler_error_code, PaylerApiError
        )
        return exception_class(
            message,
            error_code=payler_error_code,
            response=response,
        )
    except ValueError:
        return PaylerApiError(message, response=response)
