import logging

logger = logging.getLogger(__name__)

def notify_low_stock(variant_id: int, stock_quantity: int):
    """
    Hook for Later
    - Send email
    - Send admin notification
    Push to Slack/Discord
    """
    logger.warning(
        f"[LOW STOCK] variant{variant_id} is low on stock: {stock_quantity}."
    )
