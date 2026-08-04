"use client";

import { useEffect, useRef, useState } from "react";
import { createChart } from "lightweight-charts";

const API_BASE = "http://localhost:8000";

const STOCKS = [
  "AAPL", "MSFT", "NVDA", "AMZN", "GOOGL",
  "META", "TSLA", "SPY", "QQQ", "IWM",
  "AMD", "NFLX", "JPM", "V", "BRK.B"
];

export default function Dashboard() {
  const containerRef = useRef<HTMLDivElement>(null);

  const chartRef = useRef<any>(null);
  const candleRef = useRef<any>(null);
  const ma7Ref = useRef<any>(null);
  const ma20Ref = useRef<any>(null);

  const [symbol, setSymbol] = useState("AAPL");

  const [signal, setSignal] = useState<"BUY" | "SELL" | "HOLD">("HOLD");
  const [latestPrice, setLatestPrice] = useState<number | null>(null);

  // ---------------------------
  // INIT CHART
  // ---------------------------
  useEffect(() => {
    if (!containerRef.current) return;

    const el = containerRef.current;

    const chart = createChart(el, {
      width: el.clientWidth || 900,
      height: 650,
      layout: {
        background: { color: "#0f172a" },
        textColor: "#e2e8f0",
      },
      grid: {
        vertLines: { color: "#1e293b" },
        horzLines: { color: "#1e293b" },
      },
      timeScale: {
        timeVisible: true,
        secondsVisible: false,
      },
    });

    chartRef.current = chart;

    candleRef.current = chart.addCandlestickSeries({
      upColor: "#22c55e",
      downColor: "#ef4444",
      borderVisible: false,
      wickUpColor: "#22c55e",
      wickDownColor: "#ef4444",
    });

    ma7Ref.current = chart.addLineSeries({
      color: "#f59e0b",
      lineWidth: 2,
    });

    ma20Ref.current = chart.addLineSeries({
      color: "#3b82f6",
      lineWidth: 2,
    });

    const resizeObserver = new ResizeObserver(() => {
      if (!containerRef.current || !chartRef.current) return;
      chartRef.current.applyOptions({
        width: containerRef.current.clientWidth,
      });
    });

    resizeObserver.observe(el);

    return () => {
      resizeObserver.disconnect();
      chart.remove();
    };
  }, []);

  // ---------------------------
  // LOAD DATA
  // ---------------------------
  useEffect(() => {
    if (!candleRef.current) return;

    async function load() {
      try {
        const res = await fetch(`${API_BASE}/analytics/ohlc/${symbol}`);

        if (!res.ok) {
          console.error("API error:", res.status, await res.text());
          return;
        }

        const data = await res.json();

        if (!Array.isArray(data) || data.length === 0) return;

        // ---------------------------
        // SAFE CANDLE FIX
        // ---------------------------
        const candles = data.map((d, i) => {
          const close = Number(d.close_price);

          const open = Number(d.open_price ?? close);

          const prevClose =
            i > 0 ? Number(data[i - 1].close_price) : close;

          const high = Number(
            d.high_price ?? Math.max(open, close, prevClose)
          );

          const low = Number(
            d.low_price ?? Math.min(open, close, prevClose)
          );

          return {
            time: String(d.date).split("T")[0],
            open: isNaN(open) ? close : open,
            high: isNaN(high) ? close * 1.01 : high,
            low: isNaN(low) ? close * 0.99 : low,
            close: isNaN(close) ? 0 : close,
          };
        });

        candleRef.current.setData(candles);

        // ---------------------------
        // MA7
        // ---------------------------
        ma7Ref.current.setData(
          data
            .filter((d) => d.ma7 != null)
            .map((d) => ({
              time: String(d.date).split("T")[0],
              value: Number(d.ma7),
            }))
        );

        // ---------------------------
        // MA20
        // ---------------------------
        ma20Ref.current.setData(
          data
            .filter((d) => d.ma20 != null)
            .map((d) => ({
              time: String(d.date).split("T")[0],
              value: Number(d.ma20),
            }))
        );

        // ---------------------------
        // BUY / SELL / HOLD SIGNAL
        // ---------------------------
        const last = data[data.length - 1];

        if (last?.ma7 && last?.ma20) {
          const ma7 = Number(last.ma7);
          const ma20 = Number(last.ma20);

          setLatestPrice(Number(last.close_price));

          if (ma7 > ma20) setSignal("BUY");
          else if (ma7 < ma20) setSignal("SELL");
          else setSignal("HOLD");
        }

        setTimeout(() => {
          chartRef.current?.timeScale().fitContent();
        }, 100);

      } catch (err) {
        console.error("Fetch failed:", err);
      }
    }

    load();
  }, [symbol]);

  // ---------------------------
  // UI
  // ---------------------------
  return (
    <div className="p-6 bg-slate-950 text-white min-h-screen">

      <h1 className="text-2xl font-bold mb-4">
        Financial Intelligence Dashboard
      </h1>

      {/* SIGNAL CARD */}
      <div
        className={`p-4 rounded-lg mb-4 w-fit font-bold text-lg
        ${
          signal === "BUY"
            ? "bg-green-600"
            : signal === "SELL"
            ? "bg-red-600"
            : "bg-yellow-500"
        }`}
      >
        Signal: {signal}
        {latestPrice && (
          <div className="text-sm font-normal">
            Price: ${latestPrice.toFixed(2)}
          </div>
        )}
      </div>

      {/* STOCK SELECT */}
      <select
        className="bg-slate-800 p-2 rounded mb-4"
        value={symbol}
        onChange={(e) => setSymbol(e.target.value)}
      >
        {STOCKS.map((s) => (
          <option key={s} value={s}>
            {s}
          </option>
        ))}
      </select>

      {/* LEGEND */}
      <div className="flex gap-4 mb-4 text-sm">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 bg-yellow-400 rounded"></div>
          MA7
        </div>

        <div className="flex items-center gap-2">
          <div className="w-3 h-3 bg-blue-500 rounded"></div>
          MA20
        </div>

        <div className="flex items-center gap-2">
          <div className="w-3 h-3 bg-green-500 rounded"></div>
          Candles
        </div>
      </div>

      {/* CHART */}
      <div
        ref={containerRef}
        className="w-full h-[650px] bg-slate-900 rounded-lg"
      />
    </div>
  );
}
