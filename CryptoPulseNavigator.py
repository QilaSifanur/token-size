import requests
import time
import sys

API_URL = "https://api.coingecko.com/api/v3/simple/price"

def fetch_price(crypto, fiat="usd"):
    try:
        response = requests.get(API_URL, params={
            "ids": crypto,
            "vs_currencies": fiat
        })
        response.raise_for_status()
        return response.json()[crypto][fiat]
    except Exception as e:
        print(f"Ошибка при получении цены: {e}")
        return None

def detect_pulse(crypto, fiat="usd", interval=5, threshold=0.5):
    print(f"Отслеживание '{crypto}' в паре с '{fiat}'. Интервал: {interval} сек.")
    last_price = fetch_price(crypto, fiat)
    if last_price is None:
        sys.exit(1)
    print(f"Начальная цена: {last_price} {fiat.upper()}")

    while True:
        time.sleep(interval)
        current_price = fetch_price(crypto, fiat)
        if current_price is None:
            continue
        change = ((current_price - last_price) / last_price) * 100
        if abs(change) >= threshold:
            direction = "выросла" if change > 0 else "упала"
            print(f"Цена {direction} на {change:.2f}%: {current_price} {fiat.upper()}")
        last_price = current_price

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python CryptoPulseNavigator.py <crypto_id> [fiat] [interval] [threshold]")
        sys.exit(1)
    crypto = sys.argv[1]
    fiat = sys.argv[2] if len(sys.argv) > 2 else "usd"
    interval = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    threshold = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
    detect_pulse(crypto, fiat, interval, threshold)
