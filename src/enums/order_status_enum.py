from enum import Enum

class EnumOrderStatus(Enum):
    PENDING = "PENDING" # The order has just been created
    PAID = "PAID" # The order has been paid for
    CANCELLED = "CANCELLED" # The order was cancelled by the client (from a pending state). We free the products and nothing to be done on the financial line.
    CANCELLED_AFTER_PAYMENT = "CANCELLED_AFTER_PAYMENT" # The order was cancelled by the client (from a paid state). We free the products, cancel the financial lines, initiate a refund and store the refund. 
    PAYMENT_ERROR='PAYMENT_ERROR' # The user tried to pay but encountered an error, here we won't free the products and will allow the cron job to do it's work. The user can still come back to pay for the order or cancel it. On the front-end we can tell the user that he has one day to pay for the product. We will just change the status of the order to payment error. 
    CANCELLED_AUTOMATICALLY='CANCELLED_AUTOMATICALLY' # The cron job cancelled the order automatically. We free the products. 

# Maybe work on an admin route to retry a failed refund if a client complains. 
# Work on uploading pictures of products while creating them. 
# Work on rating products of a seller as a client. 
# Containerize the app. 