def apply_discount(total: float, discount):

    if discount.percentage:
        return total - (total * discount.percentage / 100)

    if discount.fixed_amount:
        return max(0, total - discount.fixed_amount)

    return total