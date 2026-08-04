"use client";

import { useEffect, useRef, useState } from "react";
import { createChart } from "lightweight-charts";

const BASE_URL = "http://127.0.0.1:8000";
const SYMBOLS = ["AAPL", "MSFT", "NVDA", "SPY"];

type Prediction = {
  symbol: string;
  current_price: number;
  predicted_price: number;
  difference: number;
  percent_change: number;
  signal: "BUY" | "SELL" | "HOLD";
  model_used: string;
};

export default function Page() {
  const [selected, setSelected] = useState("AAPL");
  const [pred, setPred] = useState<Record<string, Prediction>>({});
  const [ohlc, setOhlc] = useState<Record<string, any>>({});

  const chartRef = useRef<any>(null);
  const candleRef = useRef<any>(null);
  const ma7Ref = useRef<any>(null);
  const ma20Ref = useRef<any>(null);

  // ---------------- FETCH ----------------
  const fetchPred = async (symbol: string) => {
    const res = await fetch(`${BASE_URL}/predict/${symbol}`);
    return res.json();
  };

  const fetchOHLC = async (symbol: string) => {
    const res = await fetch(`${BASE_URL}/analytics/ohlc/${symbol}`);
    return res.json();
  };

  // ---------------- LOAD ----------------
  const load = async () => {
    const results = await Promise.all(
      SYMBOLS.map(async (s) => ({
        symbol: s,
        pred: await fetchPred(s),
        ohlc: await fetchOHLC(s),
      }))
    );

    const p: any = {};
    const o: any = {};

    results.forEach((r) => {
      p[r.symbol] = r.pred;
      o[r.symbol] = r.ohlc;
    });

    setPred(p);
    setOhlc(o);
  };

  // ---------------- INIT CHART ----------------
  useEffect(() => {
    const container = document.getElementById("chart");
    if (!container) return;

    const chart = createChart(container, {
      width: container.clientWidth,
      height: 500,
      layout: {
        background: { color: "#0f172a" },
        textColor: "#e5e7eb",
      },
      grid: {
        vertLines: { color: "#1f2937" },
        horzLines: { color: "#1f2937" },
      },
    });

    candleRef.current = chart.addCandlestickSeries();
    ma7Ref.current = chart.addLineSeries({ color: "#3b82f6" });
    ma20Ref.current = chart.addLineSeries({ color: "#f59e0b" });

    chartRef.current = chart;

    return () => chart.remove();
  }, []);

  // ---------------- SAFE NORMALIZER ----------------
  const normalize = (raw: any) => {
    if (!raw) return [];
    if (Array.isArray(raw)) return raw;
    if (Array.isArray(raw.data)) return raw.data;
    if (Array.isArray(raw.ohlc)) return raw.ohlc;
    if (Array.isArray(raw.result)) return raw.result;
    return [];
  };

  // ---------------- UPDATE CHART ----------------
  useEffect(() => {
    const raw = ohlc[selected];
    if (!raw || !candleRef.current) return;

    const data = normalize(raw);
    if (data.length === 0) return;

    // candles
    const candles = data.map((d: any) => ({
      time: d.time,
      open: Number(d.open),
      high: Number(d.high),
      low: Number(d.low),
      close: Number(d.close),
    }));

    candleRef.current.setData(candles);

    // MA7
    const ma7 = data
      .filter((d: any) => d.ma7 != null)
      .map((d: any) => ({
        time: d.time,
        value: Number(d.ma7),
      }));

    ma7Ref.current?.setData(ma7);

    // MA20
    const ma20 = data
      .filter((d: any) => d.ma20 != null)
      .map((d: any) => ({
        time: d.time,
        value: Number(d.ma20),
      }));

    ma20Ref.current?.setData(ma20);
  }, [selected, ohlc]);

  useEffect(() => {
    load();
  }, []);

  const p = pred[selected];

  return (
    <div className="min-h-screen bg-slate-950 text-white p-6">

      {/* HEADER */}
      <div className="flex justify-between mb-4">
        <h1 className="text-2xl font-bold">
          📊 Trading Dashboard
        </h1>

        <div className="flex gap-2">
          {SYMBOLS.map((s) => (
            <button
              key={s}
              onClick={() => setSelected(s)}
              className={`px-3 py-1 rounded ${
                selected === s ? "bg-blue-600" : "bg-slate-800"
              }`}
            >
              {s}
            </button>
          ))}
        </div>
      </div>

      {/* SIGNAL */}
      <div className="mb-4 p-3 bg-slate-900 rounded">
        <p>
          Signal:{" "}
          <span className="font-bold text-green-400">
            {p?.signal || "..."}
          </span>
        </p>
        <p>Price: {p?.current_price}</p>
        <p>Prediction: {p?.predicted_price}</p>
      </div>

      {/* CHART */}
      <div id="chart" className="bg-slate-900 rounded" />
    </div>
  );
}
