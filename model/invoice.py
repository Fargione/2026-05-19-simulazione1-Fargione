from dataclasses import dataclass
from datetime import datetime


@dataclass
class Invoice:
    InvoiceId : int
    CustomerId : int
    InvoiceDate : datetime
    BillingAddress : str
    BillingCity: str
    BillingState : str
    BillingCountry: str
    BillingPostalCode: str
    Total : int

    def __hash__(self):
        return hash(self.InvoiceId)

    def __eq__(self, other):
        return self.InvoiceId == other.InvoiceId

    def __str__(self):
        return f"{self.InvoiceId} con {self.CustomerId}"