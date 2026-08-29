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

    container.innerHTML = "";

    // ------------------------------------------
    // CREATE CHART
    // ------------------------------------------

    const chart = createChart(container, {
      width: container.clientWidth || 900,
      height: 520,

      layout: {
        background: {
          color: "#0b1220",
        },
        textColor: "#94a3b8",
        fontFamily:
          "Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif",
      },

      grid: {
        vertLines: {
          color: "#172033",
        },
        horzLines: {
          color: "#172033",
        },
      },

      rightPriceScale: {
        borderColor: "#263247",
        textColor: "#94a3b8",
        scaleMargins: {
          top: 0.08,
          bottom: 0.08,
        },
      },

      timeScale: {
        borderColor: "#263247",
        timeVisible: false,
        secondsVisible: false,
        rightOffset: 5,
        barSpacing: 7,
        minBarSpacing: 3,
      },

      crosshair: {
        mode: 1,

        vertLine: {
          color: "#64748b",
          width: 1,
          style: 2,
          labelBackgroundColor: "#1e293b",
        },

        horzLine: {
          color: "#64748b",
          width: 1,
          style: 2,
          labelBackgroundColor: "#1e293b",
        },
      },

      handleScroll: {
        mouseWheel: true,
        pressedMouseMove: true,
        horzTouchDrag: true,
        vertTouchDrag: true,
      },

      handleScale: {
        axisPressedMouseMove: true,
        mouseWheel: true,
        pinch: true,
      },
    });

    // ------------------------------------------
    // CANDLE DATA CLEANING
    // ------------------------------------------

    const seen = new Set<string>();

    const cleaned = data
      .map((d) => {
        const date = String(d.date).split("T")[0];

        return {
          time: date,
          open: Number(d.open),
          high: Number(d.high),
          low: Number(d.low),
          close: Number(d.close),
        };
      })

      .filter((d) => {
        return (
          /^\d{4}-\d{2}-\d{2}$/.test(d.time) &&
          Number.isFinite(d.open) &&
          Number.isFinite(d.high) &&
          Number.isFinite(d.low) &&
          Number.isFinite(d.close)
        );
      })

      .filter((d) => {
        if (seen.has(d.time)) {
          return false;
        }

        seen.add(d.time);

        return true;
      })

      .sort((a, b) =>
        a.time.localeCompare(b.time)
      );

    // ------------------------------------------
    // CANDLE SERIES
    // ------------------------------------------

    const candleSeries =
      chart.addCandlestickSeries({
        upColor: "#22c55e",
        downColor: "#ef4444",

        borderUpColor: "#22c55e",
        borderDownColor: "#ef4444",

        wickUpColor: "#22c55e",
        wickDownColor: "#ef4444",
      });

    candleSeries.setData(cleaned);

    // ------------------------------------------
    // FIT CHART TO DATA
    // ------------------------------------------

    chart.timeScale().fitContent();

    // ------------------------------------------
    // RESPONSIVE RESIZE
    // ------------------------------------------

    const resizeObserver =
      new ResizeObserver(() => {
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
      className="w-full overflow-hidden rounded-lg"
      style={{
        width: "100%",
        height: 520,
      }}
    />
  );
}
