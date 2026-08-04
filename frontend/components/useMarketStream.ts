"use client";

import { useEffect, useState } from "react";

export function useMarketStream(symbol: string) {
  const [data, setData] = useState<any[]>([]);

  useEffect(() => {
    if (!symbol) return;

    const ws = new WebSocket(`ws://127.0.0.1:8000/ws/${symbol}`);

    ws.onopen = () => {
      console.log("WebSocket connected:", symbol);
    };

    ws.onmessage = (event) => {
      const candle = JSON.parse(event.data);

      setData((prev) => {
        const updated = [...prev, candle];
        return updated.slice(-200); // keep last 200 candles
      });
    };

    ws.onerror = (err) => {
      console.error("WebSocket error:", err);
    };

    ws.onclose = () => {
      console.log("WebSocket closed");
    };

    return () => ws.close();
  }, [symbol]);

  return data;
}
