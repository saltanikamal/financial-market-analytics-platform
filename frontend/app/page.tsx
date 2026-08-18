"use client";

import { useEffect, useState } from "react";
import Header from "@/components/dashboard/Header";
import CandleChart from "@/components/charts/CandleChart";

const API_BASE = "http://localhost:8000";

const STOCKS = [
  "AAPL",
  "AMD",
  "AMZN",
  "AVGO",
  "BAC",
  "CAT",
  "COST",
  "CVX",
  "DIA",
  "GE",
  "GOOGL",
  "GS",
  "HD",
  "JNJ",
  "JPM",
  "LLY",
  "MA",
  "META",
  "MS",
  "MSFT",
  "NFLX",
  "NVDA",
  "ORCL",
  "QQQ",
  "SPY",
  "TSLA",
  "UNH",
  "V",
  "WMT",
  "XOM",
];

type Signal = "BUY" | "SELL" | "HOLD";

type Candle = {
  date: string;
  open: number;
  high: number;
  low: number;
  close: number;
};

export default function Dashboard() {
  const [symbol, setSymbol] = useState("AAPL");

  const [signal, setSignal] =
    useState<Signal>("HOLD");

  const [latestPrice, setLatestPrice] =
    useState<number | null>(null);

  const [prediction, setPrediction] =
    useState<any>(null);

  const [dataMessage, setDataMessage] =
    useState("");

  const [chartData, setChartData] =
    useState<Candle[]>([]);

  // ==========================================
  // LOAD PRICE DATA
  // ==========================================

  useEffect(() => {
    async function loadChart() {
      try {
        const response = await fetch(
          `${API_BASE}/analytics/ohlc/${symbol}`
        );

        if (!response.ok) {
          setDataMessage(
            `Unable to load market data for ${symbol}.`
          );
          setChartData([]);
          return;
        }

        const result = await response.json();

        if (!result.available) {
          setDataMessage(
            result.message ||
              `No market data available for ${symbol}.`
          );

          setChartData([]);
          setLatestPrice(null);
          setSignal("HOLD");

          return;
        }

        setDataMessage("");

        const data = result.data || [];

        const candles: Candle[] = data.map(
          (d: any) => ({
            date: String(d.date).split("T")[0],
            open: Number(d.open),
            high: Number(d.high),
            low: Number(d.low),
            close: Number(d.close),
          })
        );

        setChartData(candles);

        const last = data[data.length - 1];

        if (last) {
          setLatestPrice(Number(last.close));

          const lastMA7 = Number(last.ma7);
          const lastMA20 = Number(last.ma20);

          if (
            !Number.isNaN(lastMA7) &&
            !Number.isNaN(lastMA20)
          ) {
            if (lastMA7 > lastMA20) {
              setSignal("BUY");
            } else if (lastMA7 < lastMA20) {
              setSignal("SELL");
            } else {
              setSignal("HOLD");
            }
          } else {
            setSignal("HOLD");
          }
        }
      } catch (error) {
        console.error(
          `Error loading chart data for ${symbol}:`,
          error
        );

        setDataMessage(
          `Unable to connect to the backend for ${symbol}.`
        );

        setChartData([]);
        setLatestPrice(null);
        setSignal("HOLD");
      }
    }

    loadChart();
  }, [symbol]);

  // ==========================================
  // LOAD ML PREDICTION
  // ==========================================

  useEffect(() => {
    async function loadPrediction() {
      setPrediction(null);

      try {
        const response = await fetch(
          `${API_BASE}/predict/${symbol}`
        );

        if (!response.ok) {
          console.error(
            `No ML prediction available for ${symbol}`
          );

          setPrediction(null);
          return;
        }

        const result = await response.json();

        setPrediction(result);
      } catch (error) {
        console.error(
          `Error loading ML prediction for ${symbol}:`,
          error
        );

        setPrediction(null);
      }
    }

    loadPrediction();
  }, [symbol]);

  // ==========================================
  // DASHBOARD
  // ==========================================

  return (
    <div
      className="
        min-h-screen
        bg-slate-950
        text-white
        p-6
      "
    >
      <Header />

      <h1
        className="
          text-3xl
          font-bold
          mb-6
        "
      >
        Financial Intelligence Dashboard
      </h1>

      {/* STOCK SELECTOR */}

      <select
        className="
          bg-slate-800
          rounded
          p-2
          mb-5
        "
        value={symbol}
        onChange={(e) =>
          setSymbol(e.target.value)
        }
      >
        {STOCKS.map((stock) => (
          <option
            key={stock}
            value={stock}
          >
            {stock}
          </option>
        ))}
      </select>

      {/* MARKET SIGNAL */}

      <div
        className={`
          rounded-lg
          p-4
          mb-5
          w-fit

          ${
            signal === "BUY"
              ? "bg-green-600"
              : signal === "SELL"
              ? "bg-red-600"
              : "bg-yellow-500"
          }
        `}
      >
        <h2 className="font-bold text-lg">
          Market Signal
        </h2>

        <p>
          Signal: {signal}
        </p>

        {latestPrice !== null && (
          <p>
            Price: $
            {latestPrice.toFixed(2)}
          </p>
        )}
      </div>

      {/* ML PREDICTION */}

      <div
        className="
          bg-slate-800
          rounded-lg
          p-5
          mb-5
          w-fit
        "
      >
        <h2 className="font-bold mb-3">
          ML Prediction
        </h2>

        {prediction ? (
          <div>
            <p>
              Signal:{" "}
              {prediction.signal ?? "N/A"}
            </p>

            <p>
              Confidence:{" "}
              {prediction.confidence ?? "N/A"}
            </p>

            <p>
              Probability:{" "}
              {prediction.probability ?? "N/A"}
            </p>

            {prediction.model && (
              <p>
                Model: {prediction.model}
              </p>
            )}

            {prediction.model_version && (
              <p>
                Model Version:{" "}
                {prediction.model_version}
              </p>
            )}
          </div>
        ) : (
          <p>
            No ML prediction available for{" "}
            {symbol}
          </p>
        )}
      </div>

      {/* DATA MESSAGE */}

      {dataMessage && (
        <div
          className="
            bg-red-700
            rounded
            p-3
            mb-5
          "
        >
          {dataMessage}
        </div>
      )}

      {/* CANDLESTICK CHART */}

      <div
        className="
          w-full
          rounded-lg
          bg-slate-900
        "
      >
        <CandleChart
          data={chartData}
        />
      </div>
    </div>
  );
}
