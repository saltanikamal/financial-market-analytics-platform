"use client";

import { useEffect, useRef } from "react";
import { createChart } from "lightweight-charts";

type Candle = {
  date: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume?: number;
};

export default function CandleChart({
  data,
}: {
  data: Candle[];
}) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const container = containerRef.current;

    if (!container) {
      return;
    }

    if (!Array.isArray(data) || data.length === 0) {
      return;
    }

    // Clear any previous chart instance
    container.innerHTML = "";

    const chart = createChart(container, {
      width: container.clientWidth || 900,
      height: 500,

      layout: {
        background: {
          color: "#0f172a",
        },
        textColor: "#ffffff",
      },

      grid: {
        vertLines: {
          color: "#1f2937",
        },
        horzLines: {
          color: "#1f2937",
        },
      },

      rightPriceScale: {
        borderColor: "#334155",
      },

      timeScale: {
        borderColor: "#334155",
        timeVisible: true,
        secondsVisible: false,
      },

      crosshair: {
        vertLine: {
          color: "#64748b",
        },
        horzLine: {
          color: "#64748b",
        },
      },
    });

    /*
     * Your installed lightweight-charts version uses:
     *
     * chart.addCandlestickSeries()
     *
     * Do NOT import CandlestickSeries.
     */
    const candleSeries = chart.addCandlestickSeries({
      upColor: "#22c55e",
      downColor: "#ef4444",
      borderUpColor: "#22c55e",
      borderDownColor: "#ef4444",
      wickUpColor: "#22c55e",
      wickDownColor: "#ef4444",
    });

    // ------------------------------------------
    // DATA CLEANING
    // ------------------------------------------

    const seen = new Set<string>();

    const cleaned = data
      .map((d) => {
        // lightweight-charts accepts YYYY-MM-DD strings
        // as valid Time values.
        const date = String(d.date).split("T")[0];

        return {
          time: date,
          open: Number(d.open),
          high: Number(d.high),
          low: Number(d.low),
          close: Number(d.close),
        };
      })

      // Remove invalid records
      .filter((d) => {
        return (
          /^\d{4}-\d{2}-\d{2}$/.test(d.time) &&
          Number.isFinite(d.open) &&
          Number.isFinite(d.high) &&
          Number.isFinite(d.low) &&
          Number.isFinite(d.close)
        );
      })

      // Remove duplicate dates
      .filter((d) => {
        if (seen.has(d.time)) {
          return false;
        }

        seen.add(d.time);

        return true;
      })

      // Chart requires ascending chronological order
      .sort((a, b) => {
        return a.time.localeCompare(b.time);
      });

    console.log(
      "CLEANED CANDLES:",
      cleaned.length
    );

    // Load cleaned data into the candlestick series
    candleSeries.setData(cleaned);

    // Fit all available candles into the chart
    chart.timeScale().fitContent();

    // ------------------------------------------
    // RESPONSIVE RESIZE
    // ------------------------------------------

    const resizeObserver = new ResizeObserver(() => {
      if (!container) {
        return;
      }

      const width = container.clientWidth;

      if (width > 0) {
        chart.applyOptions({
          width,
        });
      }
    });

    resizeObserver.observe(container);

    // ------------------------------------------
    // CLEANUP
    // ------------------------------------------

    return () => {
      resizeObserver.disconnect();
      chart.remove();
    };
  }, [data]);

  return (
    <div
      ref={containerRef}
      style={{
        width: "100%",
        height: 500,
      }}
    />
  );
}
