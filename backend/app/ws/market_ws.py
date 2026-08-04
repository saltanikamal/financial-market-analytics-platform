from fastapi import APIRouter, WebSocket
import asyncio
import json
import random
from datetime import datetime

router = APIRouter()

SYMBOLS = ["AAPL", "MSFT", "NVDA", "SPY"]

# fake live price generator (we will replace with real data later)
prices = {
    "AAPL": 190,
    "MSFT": 410,
    "NVDA": 300,
    "SPY": 500,
}


@router.websocket("/ws/market")
async def market_ws(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            updates = []

            for symbol in SYMBOLS:
                change = random.uniform(-1.5, 1.5)
                prices[symbol] += change

                candle = {
                    "symbol": symbol,
                    "time": int(datetime.utcnow().timestamp()),
                    "price": round(prices[symbol], 2),
                }

                updates.append(candle)

            await websocket.send_text(json.dumps(updates))
            await asyncio.sleep(1)

    except Exception as e:
        print("WebSocket closed:", e)
