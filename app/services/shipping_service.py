def calculate_shipping(state: str, total_amount: float):

    # Simple Nigeria-based logic
    if state.lower() == "abuja":
        return 2000
    elif state.lower() in ["niger", "kaduna"]:
        return 3000
    else:
        return 400