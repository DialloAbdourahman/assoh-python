from enum import Enum

class EnumOrderStatus(Enum):
    PENDING = "PENDING" # The order has just been created
    PAID = "PAID" # The order has been paid for
    CANCELLED = "CANCELLED" # The order was cancelled by the client (from a pending state). We free the products and nothing to be done on the financial line.
    CANCELLED_AFTER_PAYMENT = "CANCELLED_AFTER_PAYMENT" # The order was cancelled by the client (from a paid state). We free the products, cancel the financial lines, initiate a refund and store the refund. 

    PAYMENT_ERROR='PAYMENT_ERROR' # The user tried to pay but encountered an error, here we won't free the products and will allow the cron job to do it's work. The user can still come back to pay for the order or cancel it. On the front-end we can tell the user that he has one day to pay for the product. We will just change the status of the order to payment error. 
    CANCELLED_AUTOMATICALLY='CANCELLED_AUTOMATICALLY' # The cron job cancelled the order automatically. We free the products. 

# Come back to the cancel order after payment and complete the whole process (refunds and everything)
# Come back and handle the stripe payment error and allow the user to retry failed payments. 
# Work on the crone job that cancels order automatically. 
# Work on the crone job that retries refunds (No bad idea, we don't need a cron job for that. The client will just contact the admin and the admin will see what to do. This is to avoid re-refunding )