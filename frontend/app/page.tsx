"use client";

import { useEffect, useMemo, useState } from "react";
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
      background: "bg-emerald-500/10",
      border: "border-emerald-500/25",
      text: "text-emerald-400",
      badge: "bg-emerald-500/10",
      bar: "bg-emerald-500",
    };
  }

  if (signal === "SELL") {
    return {
      background: "bg-red-500/10",
      border: "border-red-500/25",
      text: "text-red-400",
      badge: "bg-red-500/10",
      bar: "bg-red-500",
    };
  }

  return {
    background: "bg-amber-500/10",
    border: "border-amber-500/25",
    text: "text-amber-400",
    badge: "bg-amber-500/10",
    bar: "bg-amber-500",
  };
}

function percentage(value: number | null | undefined) {
  if (!Number.isFinite(value)) {
    return "—";
  }

  return `${(Number(value) * 100).toFixed(1)}%`;
}

function scorePercentage(value: number | null | undefined) {
  if (!Number.isFinite(value)) {
    return "—";
  }

  return `${Number(value).toFixed(1)}%`;
}

function probabilityWidth(value: number | null | undefined) {
  if (!Number.isFinite(value)) {
    return "0%";
  }

  return `${Math.max(
    0,
    Math.min(100, Number(value) * 100)
  )}%`;
}

export default function Dashboard() {
  const [symbol, setSymbol] = useState("AAPL");

  const [signal, setSignal] =
    useState<Signal>("HOLD");

  const [latestPrice, setLatestPrice] =
    useState<number | null>(null);

  const [previousClose, setPreviousClose] =
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
      setDataMessage("");

      try {
        const response = await fetch(
          `${API_BASE}/analytics/ohlc/${symbol}`,
          {
            cache: "no-store",
          }
        );

        if (!response.ok) {
          setDataMessage(
            `Unable to load market data for ${symbol}.`
          );

          setChartData([]);
          setLatestPrice(null);
          setPreviousClose(null);
          setSignal("HOLD");

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
          setPreviousClose(null);
          setSignal("HOLD");

          return;
        }

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
        const prior = data[data.length - 2];

        if (last) {
          const close = Number(last.close);

          setLatestPrice(
            Number.isFinite(close)
              ? close
              : null
          );

          if (prior) {
            const priorCloseValue =
              Number(prior.close);

            setPreviousClose(
              Number.isFinite(priorCloseValue)
                ? priorCloseValue
                : null
            );
          } else {
            setPreviousClose(null);
          }

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
        setPreviousClose(null);
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
          `${API_BASE}/predict/${symbol}`,
          {
            cache: "no-store",
          }
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

  const technicalStyles =
    signalClasses(signal);

  const predictionStyles = prediction
    ? signalClasses(prediction.signal)
    : signalClasses("HOLD");

  const priceChange = useMemo(() => {
    if (
      latestPrice === null ||
      previousClose === null ||
      previousClose === 0
    ) {
      return null;
    }

    return (
      ((latestPrice - previousClose) /
        previousClose) *
      100
    );
  }, [latestPrice, previousClose]);

  const signalsAgree =
    prediction !== null &&
    signal === prediction.signal;

  return (
    <main className="min-h-screen bg-slate-950 text-white">
      <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 sm:py-8">

        {/* ========================================
            HEADER
        ======================================== */}

        <Header />

        {/* ========================================
            MARKET SELECTOR
        ======================================== */}

        <section className="mb-6 rounded-2xl border border-slate-800/80 bg-slate-900/70 p-5 shadow-lg shadow-black/10">
          <div className="flex flex-col gap-5 lg:flex-row lg:items-center lg:justify-between">

            <div>
              <div className="flex items-center gap-3">
                <div className="flex h-9 w-9 items-center justify-center rounded-lg border border-blue-500/20 bg-blue-500/10">
                  <span className="text-sm font-bold text-blue-400">
                    {symbol.slice(0, 1)}
                  </span>
                </div>

                <div>
                  <p className="text-xs font-bold uppercase tracking-[0.16em] text-slate-500">
                    Selected Market
                  </p>

                  <p className="mt-1 text-lg font-bold text-white">
                    {symbol}
                  </p>
                </div>
              </div>

              <p className="mt-3 text-sm text-slate-500">
                Analyze historical price action,
                technical signals, and model output.
              </p>
            </div>

            <div className="flex flex-col gap-2 sm:flex-row sm:items-center">
              <label
                htmlFor="stock-selector"
                className="text-xs font-semibold uppercase tracking-wider text-slate-500"
              >
                Symbol
              </label>

              <select
                id="stock-selector"
                className="min-w-48 rounded-xl border border-slate-700 bg-slate-800 px-4 py-3 text-sm font-semibold text-white outline-none transition hover:border-slate-500 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
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

          </div>
        </section>

        {/* ========================================
            MARKET OVERVIEW
        ======================================== */}

        <section className="mb-6 grid grid-cols-1 gap-4 md:grid-cols-3">

          {/* PRICE */}

          <div className="rounded-2xl border border-slate-800/80 bg-slate-900/70 p-6 shadow-lg shadow-black/10">
            <div className="flex items-start justify-between">
              <div>
                <p className="text-xs font-bold uppercase tracking-[0.16em] text-slate-500">
                  Current Price
                </p>

                <p className="mt-3 text-3xl font-bold tracking-tight text-white">
                  {latestPrice !== null
                    ? `$${latestPrice.toFixed(2)}`
                    : "—"}
                </p>
              </div>

              <span className="rounded-lg bg-blue-500/10 px-3 py-1.5 text-xs font-bold text-blue-400">
                {symbol}
              </span>
            </div>

            <div className="mt-5 flex items-center justify-between border-t border-slate-800 pt-4">
              <span className="text-xs text-slate-500">
                Daily change
              </span>

              <span
                className={`text-sm font-semibold ${
                  priceChange === null
                    ? "text-slate-500"
                    : priceChange >= 0
                    ? "text-emerald-400"
                    : "text-red-400"
                }`}
              >
                {priceChange === null
                  ? "—"
                  : `${priceChange >= 0 ? "+" : ""}${priceChange.toFixed(2)}%`}
              </span>
            </div>
          </div>

          {/* TECHNICAL */}

          <div
            className={`rounded-2xl border p-6 shadow-lg shadow-black/10 ${technicalStyles.background} ${technicalStyles.border}`}
          >
            <div className="flex items-start justify-between">
              <div>
                <p className="text-xs font-bold uppercase tracking-[0.16em] text-slate-500">
                  Technical Signal
                </p>

                <p
                  className={`mt-3 text-3xl font-bold ${technicalStyles.text}`}
                >
                  {loadingChart
                    ? "..."
                    : signal}
                </p>
              </div>

              <span
                className={`rounded-lg px-3 py-1.5 text-xs font-bold ${technicalStyles.badge} ${technicalStyles.text}`}
              >
                MA7 / MA20
              </span>
            </div>

            <div className="mt-5 border-t border-slate-800/60 pt-4">
              <p className="text-xs leading-5 text-slate-500">
                Short-term trend signal derived from
                moving-average positioning.
              </p>
            </div>
          </div>

          {/* ML */}

          <div
            className={`rounded-2xl border p-6 shadow-lg shadow-black/10 ${predictionStyles.background} ${predictionStyles.border}`}
          >
            <div className="flex items-start justify-between">
              <div>
                <p className="text-xs font-bold uppercase tracking-[0.16em] text-slate-500">
                  ML Prediction
                </p>

                <p
                  className={`mt-3 text-3xl font-bold ${predictionStyles.text}`}
                >
                  {loadingPrediction
                    ? "..."
                    : prediction
                    ? prediction.signal
                    : "N/A"}
                </p>
              </div>

              {prediction && (
                <span
                  className={`rounded-lg px-3 py-1.5 text-xs font-bold ${predictionStyles.badge} ${predictionStyles.text}`}
                >
                  {prediction.confidence_level}
                </span>
              )}
            </div>

            <div className="mt-5 flex items-center justify-between border-t border-slate-800/60 pt-4">
              <span className="text-xs text-slate-500">
                Model confidence
              </span>

              <span
                className={`text-sm font-bold ${predictionStyles.text}`}
              >
                {prediction
                  ? scorePercentage(
                      prediction.confidence
                    )
                  : "—"}
              </span>
            </div>
          </div>

        </section>

        {/* ========================================
            PRICE CHART
        ======================================== */}

        <section className="mb-6 overflow-hidden rounded-2xl border border-slate-800/80 bg-slate-900/70 shadow-lg shadow-black/10">

          <div className="flex flex-col gap-4 border-b border-slate-800/80 px-6 py-5 sm:flex-row sm:items-center sm:justify-between">

            <div>
              <div className="flex items-center gap-3">
                <h2 className="text-lg font-bold text-white">
                  Price Action
                </h2>

                {loadingChart && (
                  <span className="rounded-full bg-blue-500/10 px-2.5 py-1 text-[10px] font-bold uppercase tracking-wider text-blue-400">
                    Loading
                  </span>
                )}
              </div>

              <p className="mt-1 text-sm text-slate-500">
                Historical daily candlestick data for{" "}
                <span className="font-semibold text-slate-400">
                  {symbol}
                </span>
              </p>
            </div>

            <div className="flex items-center gap-2 text-xs text-slate-500">
              <span className="h-2 w-2 rounded-full bg-emerald-500" />
              Up
              <span className="ml-3 h-2 w-2 rounded-full bg-red-500" />
              Down
            </div>

          </div>

          <div className="p-3 sm:p-5">
            {dataMessage ? (
              <div className="flex min-h-[420px] items-center justify-center rounded-xl border border-red-500/20 bg-red-500/5 px-6 text-center">
                <div>
                  <p className="font-semibold text-red-400">
                    Market data unavailable
                  </p>

                  <p className="mt-2 text-sm text-slate-500">
                    {dataMessage}
                  </p>
                </div>
              </div>
            ) : chartData.length > 0 ? (
              <CandleChart data={chartData} />
            ) : (
              <div className="flex min-h-[420px] items-center justify-center rounded-xl border border-slate-800 bg-slate-950/40">
                <p className="text-sm text-slate-500">
                  Loading market data...
                </p>
              </div>
            )}
          </div>

        </section>

        {/* ========================================
            SIGNAL COMPARISON
        ======================================== */}

        <section className="mb-6 rounded-2xl border border-slate-800/80 bg-slate-900/70 p-6 shadow-lg shadow-black/10">

          <div className="flex flex-col gap-4 border-b border-slate-800/80 pb-5 sm:flex-row sm:items-center sm:justify-between">

            <div>
              <p className="text-xs font-bold uppercase tracking-[0.16em] text-blue-400">
                Decision Layer
              </p>

              <h2 className="mt-2 text-xl font-bold text-white">
                Signal Comparison
              </h2>

              <p className="mt-1 max-w-2xl text-sm leading-6 text-slate-500">
                Compare the rule-based technical signal
                with the independent machine-learning
                classification output.
              </p>
            </div>

            {prediction && (
              <div
                className={`rounded-full border px-4 py-2 text-xs font-bold tracking-wider ${
                  signalsAgree
                    ? "border-emerald-500/20 bg-emerald-500/10 text-emerald-400"
                    : "border-amber-500/20 bg-amber-500/10 text-amber-400"
                }`}
              >
                {signalsAgree
                  ? "SIGNALS AGREE"
                  : "SIGNALS DIVERGE"}
              </div>
            )}

          </div>

          <div className="mt-6 grid grid-cols-1 gap-5 md:grid-cols-2">

            {/* TECHNICAL SIGNAL */}

            <div className="rounded-xl border border-slate-800 bg-slate-950/40 p-5">

              <div className="flex items-center justify-between">
                <div>
                  <p className="text-xs font-bold uppercase tracking-wider text-slate-500">
                    Technical Analysis
                  </p>

                  <p className="mt-1 text-xs text-slate-600">
                    MA7 compared with MA20
                  </p>
                </div>

                <span className="rounded-md bg-slate-800 px-2 py-1 text-[10px] font-bold uppercase tracking-wider text-slate-500">
                  Rule-Based
                </span>
              </div>

              <p
                className={`mt-6 text-4xl font-bold ${technicalStyles.text}`}
              >
                {signal}
              </p>

              <p className="mt-3 text-sm leading-6 text-slate-500">
                A short-term trend indication based on
                the relative position of the 7-day and
                20-day moving averages.
              </p>

            </div>

            {/* ML SIGNAL */}

            <div className="rounded-xl border border-slate-800 bg-slate-950/40 p-5">

              <div className="flex items-center justify-between">
                <div>
                  <p className="text-xs font-bold uppercase tracking-wider text-slate-500">
                    Machine Learning
                  </p>

                  <p className="mt-1 text-xs text-slate-600">
                    Three-class market classification
                  </p>
                </div>

                {prediction && (
                  <span className="rounded-md bg-slate-800 px-2 py-1 text-[10px] font-bold uppercase tracking-wider text-slate-500">
                    {prediction.model_used}
                  </span>
                )}
              </div>

              {prediction ? (
                <>
                  <p
                    className={`mt-6 text-4xl font-bold ${predictionStyles.text}`}
                  >
                    {prediction.signal}
                  </p>

                  <div className="mt-4 flex items-center justify-between">
                    <span className="text-sm text-slate-500">
                      Confidence
                    </span>

                    <span
                      className={`text-sm font-bold ${predictionStyles.text}`}
                    >
                      {scorePercentage(
                        prediction.confidence
                      )}
                    </span>
                  </div>
                </>
              ) : (
                <p className="mt-6 text-3xl font-bold text-slate-600">
                  N/A
                </p>
              )}

            </div>

          </div>

          {/* AGREEMENT MESSAGE */}

          {prediction && (
            <div
              className={`mt-5 rounded-xl border p-5 ${
                signalsAgree
                  ? "border-emerald-500/20 bg-emerald-500/5"
                  : "border-amber-500/20 bg-amber-500/5"
              }`}
            >
              <div className="flex items-start gap-4">

                <div
                  className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-full ${
                    signalsAgree
                      ? "bg-emerald-500/10 text-emerald-400"
                      : "bg-amber-500/10 text-amber-400"
                  }`}
                >
                  {signalsAgree ? "✓" : "!"}
                </div>

                <div>
                  <p
                    className={`font-bold ${
                      signalsAgree
                        ? "text-emerald-400"
                        : "text-amber-400"
                    }`}
                  >
                    {signalsAgree
                      ? "Signals currently agree"
                      : "Signals currently diverge"}
                  </p>

                  <p className="mt-1 text-sm leading-6 text-slate-500">
                    {signalsAgree
                      ? "The technical rule and ML classifier currently point in the same direction."
                      : "The technical rule and ML classifier currently point in different directions. This divergence should be treated as an analytical observation, not a trading recommendation."}
                  </p>
                </div>

              </div>
            </div>
          )}

        </section>

        {/* ========================================
            ML PROBABILITY BREAKDOWN
        ======================================== */}

        <section className="mb-6 rounded-2xl border border-slate-800/80 bg-slate-900/70 p-6 shadow-lg shadow-black/10">

          <div className="border-b border-slate-800/80 pb-5">
            <p className="text-xs font-bold uppercase tracking-[0.16em] text-violet-400">
              Model Output
            </p>

            <h2 className="mt-2 text-xl font-bold text-white">
              Prediction Probability
            </h2>

            <p className="mt-1 text-sm leading-6 text-slate-500">
              Model probabilities across the bearish,
              neutral, and bullish classes.
            </p>
          </div>

          {prediction ? (
            <div className="mt-6 space-y-5">

              {/* BEARISH */}

              <div>
                <div className="mb-2 flex items-center justify-between">
                  <span className="text-sm font-medium text-slate-300">
                    Bearish
                  </span>

                  <span className="text-sm font-bold text-red-400">
                    {percentage(
                      prediction.probabilities
                        .bearish
                    )}
                  </span>
                </div>

                <div className="h-2 overflow-hidden rounded-full bg-slate-800">
                  <div
                    className="h-full rounded-full bg-red-500 transition-all"
                    style={{
                      width:
                        probabilityWidth(
                          prediction
                            .probabilities
                            .bearish
                        ),
                    }}
                  />
                </div>
              </div>

              {/* NEUTRAL */}

              <div>
                <div className="mb-2 flex items-center justify-between">
                  <span className="text-sm font-medium text-slate-300">
                    Neutral
                  </span>

                  <span className="text-sm font-bold text-amber-400">
                    {percentage(
                      prediction.probabilities
                        .neutral
                    )}
                  </span>
                </div>

                <div className="h-2 overflow-hidden rounded-full bg-slate-800">
                  <div
                    className="h-full rounded-full bg-amber-500 transition-all"
                    style={{
                      width:
                        probabilityWidth(
                          prediction
                            .probabilities
                            .neutral
                        ),
                    }}
                  />
                </div>
              </div>

              {/* BULLISH */}

              <div>
                <div className="mb-2 flex items-center justify-between">
                  <span className="text-sm font-medium text-slate-300">
                    Bullish
                  </span>

                  <span className="text-sm font-bold text-emerald-400">
                    {percentage(
                      prediction.probabilities
                        .bullish
                    )}
                  </span>
                </div>

                <div className="h-2 overflow-hidden rounded-full bg-slate-800">
                  <div
                    className="h-full rounded-full bg-emerald-500 transition-all"
                    style={{
                      width:
                        probabilityWidth(
                          prediction
                            .probabilities
                            .bullish
                        ),
                    }}
                  />
                </div>
              </div>

            </div>
          ) : (
            <div className="mt-6 rounded-xl border border-slate-800 bg-slate-950/40 p-6">
              <p className="text-sm text-slate-500">
                {loadingPrediction
                  ? "Loading model probabilities..."
                  : "Prediction probabilities are unavailable for this symbol."}
              </p>
            </div>
          )}

        </section>

        {/* ========================================
            MODEL DETAILS
        ======================================== */}

        <section className="mb-6 rounded-2xl border border-slate-800/80 bg-slate-900/70 p-6 shadow-lg shadow-black/10">

          <div className="border-b border-slate-800/80 pb-5">
            <p className="text-xs font-bold uppercase tracking-[0.16em] text-emerald-400">
              Model Transparency
            </p>

            <h2 className="mt-2 text-xl font-bold text-white">
              Model Details
            </h2>

            <p className="mt-1 text-sm leading-6 text-slate-500">
              Metadata returned by the prediction
              service for the selected market.
            </p>
          </div>

          {prediction ? (
            <div className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">

              <div className="rounded-xl border border-slate-800 bg-slate-950/40 p-4">
                <p className="text-[10px] font-bold uppercase tracking-wider text-slate-500">
                  Model
                </p>

                <p className="mt-2 font-semibold text-slate-200">
                  {prediction.model_used}
                </p>
              </div>

              <div className="rounded-xl border border-slate-800 bg-slate-950/40 p-4">
                <p className="text-[10px] font-bold uppercase tracking-wider text-slate-500">
                  Version
                </p>

                <p className="mt-2 break-all font-mono text-xs text-slate-300">
                  {prediction.model_version}
                </p>
              </div>

              <div className="rounded-xl border border-slate-800 bg-slate-950/40 p-4">
                <p className="text-[10px] font-bold uppercase tracking-wider text-slate-500">
                  Confidence
                </p>

                <p
                  className={`mt-2 font-semibold ${predictionStyles.text}`}
                >
                  {scorePercentage(
                    prediction.confidence
                  )}
                </p>
              </div>

              <div className="rounded-xl border border-slate-800 bg-slate-950/40 p-4">
                <p className="text-[10px] font-bold uppercase tracking-wider text-slate-500">
                  Probability Margin
                </p>

                <p className="mt-2 font-semibold text-slate-200">
                  {percentage(
                    prediction.probability_margin
                  )}
                </p>
              </div>

            </div>
          ) : (
            <div className="mt-6 rounded-xl border border-slate-800 bg-slate-950/40 p-5">
              <p className="text-sm text-slate-500">
                Model metadata will appear when a
                prediction is available.
              </p>
            </div>
          )}

        </section>

        {/* ========================================
            RESPONSIBLE INTERPRETATION
        ======================================== */}

        <section className="rounded-2xl border border-blue-500/15 bg-blue-500/5 p-6">

          <div className="flex items-start gap-4">

            <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-blue-500/10 text-blue-400">
              i
            </div>

            <div>
              <h2 className="font-bold text-blue-300">
                How to interpret this dashboard
              </h2>

              <p className="mt-2 text-sm leading-6 text-slate-400">
                Technical signals and machine-learning
                predictions are analytical outputs from
                this portfolio project. They are not
                financial advice or guarantees of future
                market performance. Model confidence
                represents the model's output, not the
                probability that a trade will be profitable.
              </p>

              <p className="mt-3 text-sm leading-6 text-slate-500">
                The dashboard intentionally separates
                rule-based technical analysis from the
                independent ML classification so that
                agreement and divergence can be evaluated
                transparently.
              </p>
            </div>

          </div>

        </section>

        {/* ========================================
            FOOTER
        ======================================== */}

        <footer className="mt-8 border-t border-slate-800/80 pt-5 text-center">
          <p className="text-xs text-slate-600">
            Financial Intelligence Dashboard ·
            Market analytics · Technical analysis ·
            Machine learning
          </p>
        </footer>

      </div>
    </main>
  );
}
