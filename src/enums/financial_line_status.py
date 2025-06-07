from enum import Enum

class EnumFinancialLineStatus(Enum):
    CREATED = 'CREATED'
    PENDING = 'PENDING'
    COLLECTED = 'COLLECTED'
    CANCELLED='CANCELLED'


