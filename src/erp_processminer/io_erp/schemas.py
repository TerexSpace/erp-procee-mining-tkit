"""
Defines data classes for common ERP documents to provide a structured,
type-hinted representation of raw ERP data.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class PurchaseOrderItem:
    """Represents a single item within a purchase order."""
    po_number: str
    item_number: int
    material: str
    quantity: float
    unit: str
    price: float

@dataclass
class PurchaseOrderHeader:
    """Represents the header of a purchase order."""
    po_number: str
    vendor: str
    creation_date: datetime
    created_by: str

@dataclass
class GoodsReceipt:
    """Represents a goods receipt document."""
    gr_number: str
    po_number: str
    receipt_date: datetime
    quantity: float
    item_number: int

@dataclass
class Invoice:
    """Represents an invoice document."""
    invoice_number: str
    po_number: str
    invoice_date: datetime
    amount: float
    status: str
    clearing_date: Optional[datetime] = None