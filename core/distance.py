# Already implemented inside Device model – kept here for clarity
def estimate_distance(rssi: int, tx_power: float = -59.0, n: float = 2.0) -> float:
    return round(10 ** ((tx_power - rssi) / (10 * n)), 1)