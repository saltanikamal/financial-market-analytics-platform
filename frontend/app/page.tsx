"use client";

import { useEffect, useState } from "react";
import Header from "@/components/dashboard/Header";
import CandleChart from "@/components/charts/CandleChart";

const API_BASE = "http://127.0.0.1:8000";

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

type Prediction = {
  symbol: string;
  model_used: string;
  model_version: string;
  prediction_class: number;
  signal: Signal;
  probability: number;
  confidence: number;
  confidence_level: string;
  probability_margin: number;
  probabilities: {
    bearish: number;
    neutral: number;
    bullish: number;
  };
  current_price: number;
  metrics?: {
    accuracy?: number;
    precision?: number;
    recall?: number;
    f1?: number;
    roc_auc?: number | null;
  };
};

function signalClasses(signal: Signal) {
  if (signal === "BUY") {
    return {
      background: "bg-emerald-500/15",
      border: "border-emerald-500/30",
      text: "text-emerald-400",
      badge: "bg-emerald-500/20",
    };
  }

  if (signal === "SELL") {
    return {
      background: "bg-red-500/15",
      border: "border-red-500/30",
      text: "text-red-400",
      badge: "bg-red-500/20",
    };
  }

  return {
    background: "bg-amber-500/15",
    border: "border-amber-500/30",
    text: "text-amber-400",
    badge: "bg-amber-500/20",
  };
}

function probabilityWidth(value: number) {
  return `${Math.max(0, Math.min(100, value * 100))}%`;
}

export default function Dashboard() {
  const [symbol, setSymbol] = useState("AAPL");

  const [signal, setSignal] =
    useState<Signal>("HOLD");

  const [latestPrice, setLatestPrice] =
    useState<number | null>(null);

  const [prediction, setPrediction] =
    useState<Prediction | null>(null);

  const [dataMessage, setDataMessage] =
    useState("");

  const [chartData, setChartData] =
    useState<Candle[]>([]);

  const [loadingPrediction, setLoadingPrediction] =
    useState(false);

  const [loadingChart, setLoadingChart] =
    useState(false);

  // ==========================================
  // LOAD MARKET DATA
  // ==========================================

  useEffect(() => {
    async function loadChart() {
      setLoadingChart(true);

      try {
        const response = await fetch(
          `${API_BASE}/analytics/ohlc/${symbol}`
        );

        if (!response.ok) {
          setDataMessage(
            `Unable to load market data for ${symbol}.`
          );

          setChartData([]);
          setLatestPrice(null);

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

        const candles: Candle[] = data
          .map((d: any) => ({
            date: String(d.date).split("T")[0],
            open: Number(d.open),
            high: Number(d.high),
            low: Number(d.low),
            close: Number(d.close),
          }))
          .filter(
            (d: Candle) =>
              Number.isFinite(d.open) &&
              Number.isFinite(d.high) &&
              Number.isFinite(d.low) &&
              Number.isFinite(d.close)
          );

        setChartData(candles);

        const last = data[data.length - 1];

        if (last) {
          setLatestPrice(Number(last.close));

          const lastMA7 = Number(last.ma7);
          const lastMA20 = Number(last.ma20);

          if (
            Number.isFinite(lastMA7) &&
            Number.isFinite(lastMA20)
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
          `Error loading market data for ${symbol}:`,
          error
        );

        setDataMessage(
          `Unable to connect to the backend for ${symbol}.`
        );

        setChartData([]);
        setLatestPrice(null);
        setSignal("HOLD");
      } finally {
        setLoadingChart(false);
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
      setLoadingPrediction(true);

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

        const result: Prediction =
          await response.json();

        setPrediction(result);
      } catch (error) {
        console.error(
          `Error loading ML prediction for ${symbol}:`,
          error
        );

        setPrediction(null);
      } finally {
        setLoadingPrediction(false);
      }
    }

    loadPrediction();
  }, [symbol]);

  const predictionStyles = prediction
    ? signalClasses(prediction.signal)
    : signalClasses("HOLD");

  return (
    <main className="min-h-screen bg-slate-950 text-white">
      <div className="mx-auto max-w-7xl px-6 py-8">

        {/* ========================================
            HEADER
        ======================================== */}

        <Header />

        {/* ========================================
            CONTROL BAR
        ======================================== */}

        <div className="mb-6 flex flex-col gap-4 rounded-xl border border-slate-800 bg-slate-900/70 p-5 md:flex-row md:items-center md:justify-between">

          <div>
            <p className="text-sm font-medium text-slate-400">
              Market Watchlist
            </p>

            <p className="mt-1 text-sm text-slate-500">
              Select a symbol to analyze market conditions
              and ML predictions.
            </p>
          </div>

          <select
            className="w-full rounded-lg border border-slate-700 bg-slate-800 px-4 py-3 text-sm font-semibold text-white outline-none transition hover:border-slate-500 focus:border-blue-500 md:w-56"
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
        </div>

        {/* ========================================
            TOP SUMMARY
        ======================================== */}

        <div className="mb-6 grid grid-cols-1 gap-5 md:grid-cols-3">

          {/* PRICE */}

          <div className="rounded-xl border border-slate-800 bg-slate-900 p-5">
            <p className="text-sm text-slate-400">
              Current Price
            </p>

            <div className="mt-2 text-3xl font-bold">
              {latestPrice !== null
                ? `$${latestPrice.toFixed(2)}`
                : "—"}
            </div>

            <p className="mt-2 text-xs text-slate-500">
              Latest available market price
            </p>
          </div>

          {/* MARKET SIGNAL */}

          <div
            className={`rounded-xl border p-5 ${signalClasses(signal).background} ${signalClasses(signal).border}`}
          >
            <p className="text-sm text-slate-400">
              Technical Market Signal
            </p>

            <div
              className={`mt-2 text-3xl font-bold ${signalClasses(signal).text}`}
            >
              {signal}
            </div>

            <p className="mt-2 text-xs text-slate-500">
              Based on MA7 vs MA20
            </p>
          </div>

          {/* ML SIGNAL */}

          <div
            className={`rounded-xl border p-5 ${predictionStyles.background} ${predictionStyles.border}`}
          >
            <p className="text-sm text-slate-400">
              ML Prediction
            </p>

            {loadingPrediction ? (
              <div className="mt-2 text-2xl font-bold text-slate-400">
                Loading...
              </div>
            ) : prediction ? (
              <>
                <div
                  className={`mt-2 text-3xl font-bold ${predictionStyles.text}`}
                >
                  {prediction.signal}
                </div>

                <p className="mt-2 text-xs text-slate-500">
                  Confidence{" "}
                  {prediction.confidence.toFixed(2)}%
                </p>
              </>
            ) : (
              <div className="mt-2 text-2xl font-bold text-slate-500">
                N/A
              </div>
            )}
          </div>
        </div>
        {/* ========================================
            SIGNAL COMPARISON
        ======================================== */}

        <div className="mb-6 rounded-xl border border-slate-800 bg-slate-900 p-6">

          <div className="mb-5">
            <h2 className="text-lg font-semibold">
              Signal Comparison
            </h2>

            <p className="mt-1 text-sm text-slate-500">
              Compare the technical market signal with the machine learning prediction.
            </p>
          </div>

          <div className="grid grid-cols-1 gap-5 md:grid-cols-2">

            {/* TECHNICAL SIGNAL */}

            <div className="rounded-lg bg-slate-800 p-5">

              <p className="text-xs font-medium uppercase tracking-wide text-slate-500">
                Technical Analysis
              </p>

              <div
                className={`mt-2 text-2xl font-bold ${
                  signalClasses(signal).text
                }`}
              >
                {signal}
              </div>

              <p className="mt-2 text-sm text-slate-500">
                Based on MA7 vs MA20
              </p>

            </div>

            {/* ML SIGNAL */}

            <div className="rounded-lg bg-slate-800 p-5">

              <p className="text-xs font-medium uppercase tracking-wide text-slate-500">
                Machine Learning
              </p>

              {prediction ? (
                <>
                  <div
                    className={`mt-2 text-2xl font-bold ${
                      predictionStyles.text
                    }`}
                  >
                    {prediction.signal}
                  </div>

                  <p className="mt-2 text-sm text-slate-500">
                    Confidence{" "}
                    {prediction.confidence.toFixed(2)}%
                  </p>
                </>
              ) : (
                <div className="mt-2 text-2xl font-bold text-slate-500">
                  N/A
                </div>
              )}

            </div>

          </div>

          {/* AGREEMENT STATUS */}

          {prediction && (
            <div className="mt-5 rounded-lg border border-slate-700 bg-slate-950 p-4">

              {signal === prediction.signal ? (
                <div>
                  <p className="font-semibold text-emerald-400">
                    Signals Agree
                  </p>

                  <p className="mt-1 text-sm text-slate-500">
                    Technical analysis and the ML model currently indicate the same market direction.
                  </p>
                </div>
              ) : (
                <div>
                  <p className="font-semibold text-amber-400">
                    Signals Diverge
                  </p>

                  <p className="mt-1 text-sm text-slate-500">
                    Technical analysis and the ML model currently indicate different market directions.
                  </p>
                </div>
              )}

            </div>
          )}

        </div>
        {/* ========================================
            ML DETAILS
        ======================================== */}

        <div className="mb-6 grid grid-cols-1 gap-5 lg:grid-cols-2">

          {/* MODEL SUMMARY */}

          <div className="rounded-xl border border-slate-800 bg-slate-900 p-6">

            <div className="mb-5 flex items-center justify-between">
              <div>
                <h2 className="text-lg font-semibold">
                  Machine Learning Prediction
                </h2>

                <p className="mt-1 text-sm text-slate-500">
                  Classification model output
                </p>
              </div>

              {prediction && (
                <span
                  className={`rounded-full px-3 py-1 text-xs font-semibold ${predictionStyles.badge} ${predictionStyles.text}`}
                >
                  {prediction.confidence_level}
                </span>
              )}
            </div>

            {loadingPrediction ? (
              <p className="text-slate-400">
                Loading prediction...
              </p>
            ) : prediction ? (
              <div className="grid grid-cols-2 gap-4">

                <div className="rounded-lg bg-slate-800 p-4">
                  <p className="text-xs text-slate-500">
                    Signal
                  </p>

                  <p
                    className={`mt-1 text-xl font-bold ${predictionStyles.text}`}
                  >
                    {prediction.signal}
                  </p>
                </div>

                <div className="rounded-lg bg-slate-800 p-4">
                  <p className="text-xs text-slate-500">
                    Confidence
                  </p>

                  <p className="mt-1 text-xl font-bold">
                    {prediction.confidence.toFixed(2)}%
                  </p>
                </div>

                <div className="rounded-lg bg-slate-800 p-4">
                  <p className="text-xs text-slate-500">
                    Probability
                  </p>

                  <p className="mt-1 text-xl font-bold">
                    {prediction.probability.toFixed(4)}
                  </p>
                </div>

                <div className="rounded-lg bg-slate-800 p-4">
                  <p className="text-xs text-slate-500">
                    Probability Margin
                  </p>

                  <p className="mt-1 text-xl font-bold">
                    {prediction.probability_margin.toFixed(4)}
                  </p>
                </div>

              </div>
            ) : (
              <p className="text-slate-500">
                No ML prediction available.
              </p>
            )}

            {prediction && (
              <div className="mt-5 border-t border-slate-800 pt-4">

                <div className="flex justify-between text-sm">
                  <span className="text-slate-500">
                    Model
                  </span>

                  <span className="font-medium uppercase">
                    {prediction.model_used}
                  </span>
                </div>

                <div className="mt-2 flex justify-between text-sm">
                  <span className="text-slate-500">
                    Model Version
                  </span>

                  <span className="font-mono text-xs text-slate-300">
                    {prediction.model_version}
                  </span>
                </div>

                <div className="mt-2 flex justify-between text-sm">
                  <span className="text-slate-500">
                    Prediction Class
                  </span>

                  <span>
                    {prediction.prediction_class}
                  </span>
                </div>

              </div>
            )}
          </div>

          {/* PROBABILITY BREAKDOWN */}

          <div className="rounded-xl border border-slate-800 bg-slate-900 p-6">

            <h2 className="text-lg font-semibold">
              Probability Breakdown
            </h2>

            <p className="mt-1 text-sm text-slate-500">
              Model probability distribution across signals
            </p>

            {prediction ? (
              <div className="mt-6 space-y-5">

                {/* BEARISH */}

                <div>
                  <div className="mb-2 flex justify-between text-sm">
                    <span className="text-slate-400">
                      Bearish
                    </span>

                    <span className="font-semibold text-red-400">
                      {(prediction.probabilities.bearish * 100).toFixed(2)}%
                    </span>
                  </div>

                  <div className="h-2 overflow-hidden rounded-full bg-slate-800">
                    <div
                      className="h-full rounded-full bg-red-500"
                      style={{
                        width: probabilityWidth(
                          prediction.probabilities.bearish
                        ),
                      }}
                    />
                  </div>
                </div>

                {/* NEUTRAL */}

                <div>
                  <div className="mb-2 flex justify-between text-sm">
                    <span className="text-slate-400">
                      Neutral
                    </span>

                    <span className="font-semibold text-amber-400">
                      {(prediction.probabilities.neutral * 100).toFixed(2)}%
                    </span>
                  </div>

                  <div className="h-2 overflow-hidden rounded-full bg-slate-800">
                    <div
                      className="h-full rounded-full bg-amber-500"
                      style={{
                        width: probabilityWidth(
                          prediction.probabilities.neutral
                        ),
                      }}
                    />
                  </div>
                </div>

                {/* BULLISH */}

                <div>
                  <div className="mb-2 flex justify-between text-sm">
                    <span className="text-slate-400">
                      Bullish
                    </span>

                    <span className="font-semibold text-emerald-400">
                      {(prediction.probabilities.bullish * 100).toFixed(2)}%
                    </span>
                  </div>

                  <div className="h-2 overflow-hidden rounded-full bg-slate-800">
                    <div
                      className="h-full rounded-full bg-emerald-500"
                      style={{
                        width: probabilityWidth(
                          prediction.probabilities.bullish
                        ),
                      }}
                    />
                  </div>
                </div>

              </div>
            ) : (
              <p className="mt-6 text-slate-500">
                Probability data unavailable.
              </p>
            )}
          </div>
        </div>

        {/* ========================================
            MODEL METRICS
        ======================================== */}

        {prediction?.metrics && (
          <div className="mb-6 rounded-xl border border-slate-800 bg-slate-900 p-6">

            <div className="mb-5">
              <h2 className="text-lg font-semibold">
                Model Performance
              </h2>

              <p className="mt-1 text-sm text-slate-500">
                Registered evaluation metrics for the selected model
              </p>
            </div>

            <div className="grid grid-cols-2 gap-4 md:grid-cols-5">

              <Metric
                label="Accuracy"
                value={prediction.metrics.accuracy}
              />

              <Metric
                label="Precision"
                value={prediction.metrics.precision}
              />

              <Metric
                label="Recall"
                value={prediction.metrics.recall}
              />

              <Metric
                label="F1"
                value={prediction.metrics.f1}
              />

              <Metric
                label="ROC AUC"
                value={prediction.metrics.roc_auc}
              />

            </div>
          </div>
        )}

        {/* ========================================
            MARKET DATA
        ======================================== */}

        <div className="rounded-xl border border-slate-800 bg-slate-900 p-5">

          <div className="mb-5 flex items-center justify-between">

            <div>
              <h2 className="text-lg font-semibold">
                {symbol} Price Chart
              </h2>

              <p className="mt-1 text-sm text-slate-500">
                Historical OHLC market data
              </p>
            </div>

            {loadingChart && (
              <span className="text-xs text-slate-500">
                Loading...
              </span>
            )}

          </div>

          {dataMessage && (
            <div className="mb-5 rounded-lg border border-red-500/20 bg-red-500/10 p-4 text-sm text-red-400">
              {dataMessage}
            </div>
          )}

          {chartData.length > 0 ? (
            <CandleChart data={chartData} />
          ) : (
            !loadingChart && (
              <div className="flex h-[500px] items-center justify-center text-slate-500">
                No chart data available for {symbol}.
              </div>
            )
          )}
        </div>

        {/* ========================================
            FOOTER
        ======================================== */}

        <div className="mt-6 border-t border-slate-800 pt-5 text-center text-xs text-slate-600">
          Financial Intelligence Platform · Market analytics,
          technical indicators, and machine learning predictions
        </div>

      </div>
    </main>
  );
}

// ==========================================
// METRIC COMPONENT
// ==========================================

function Metric({
  label,
  value,
}: {
  label: string;
  value?: number | null;
}) {
  const valid =
    value !== undefined &&
    value !== null &&
    Number.isFinite(value);

  return (
    <div className="rounded-lg bg-slate-800 p-4">
      <p className="text-xs text-slate-500">
        {label}
      </p>

      <p className="mt-1 text-lg font-semibold">
        {valid
          ? `${(value * 100).toFixed(2)}%`
          : "N/A"}
      </p>
    </div>
  );
}
