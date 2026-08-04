from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
import json
import random

# =====================================
# CONFIRM FILE IS LOADED
# =====================================
print("🚀 LOADED market_stream.py")

router = APIRouter()

# =====================================
# TEST ROUTE
# =====================================
@router.get("/ws-test")
def ws_test():
    return {
        "status": "market_stream router loaded"
    }

# =====================================
# WEBSOCKET ROUTE
# =====================================
@router.websocket("/ws/market")
async def market_ws(websocket: WebSocket):

    print("🔥 Incoming WebSocket connection")

    await websocket.accept()

    print("✅ WebSocket accepted")

    price = 300.0

    try:
        while True:

            price += random.uniform(-1, 1)

            payload = {
                "symbol": "AAPL",
                "price": round(price, 2),
                "volume": random.randint(1000, 5000)
            }

            await websocket.send_text(
                json.dumps(payload)
            )

            print("📤 Sent:", payload)

            await asyncio.sleep(1)

    except WebSocketDisconnect:
        print("🔌 Client disconnected")

    except Exception as e:
        print("❌ WebSocket error:", str(e))

    finally:
        print("🧹 WebSocket cleanup complete")
