from dataclasses import dataclass

@dataclass
class OrderStatus:
    track_id: str
    payment_url: str
    expired_at: int
    date: int

@dataclass
class PaymentStatus:
    track_id: str
    type: str
    amount: int
    currency: str
    status: str
    mixed_payment: bool
    fee_paid_by_payer: int
    under_paid_coverage: float
    lifetime: int
    callback_url: str
    return_url: str
    email: str
    order_id: str
    description: str
    thanks_message: str
    expired_at: int
    date: int
    txs: list