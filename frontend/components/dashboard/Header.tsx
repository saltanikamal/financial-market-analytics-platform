"use client";

import { useEffect, useState } from "react";

interface HeaderProps {
  title?: string;
}

type BackendStatus = "checking" | "connected" | "offline";

const API_BASE = "http://127.0.0.1:8000";

export default function Header({
  title = "Financial Intelligence Dashboard",
}: HeaderProps) {
  const [status, setStatus] =
    useState<BackendStatus>("checking");

  useEffect(() => {
    let active = true;

    async function checkBackend() {
      try {
        const response = await fetch(
          `${API_BASE}/`,
          {
            cache: "no-store",
          }
        );

        if (!active) return;

        setStatus(
          response.ok
            ? "connected"
            : "offline"
        );
      } catch {
        if (!active) return;

        setStatus("offline");
      }
    }

    checkBackend();

    const interval = setInterval(
      checkBackend,
      30000
    );

    return () => {
      active = false;
      clearInterval(interval);
    };
  }, []);

  const statusConfig = {
    checking: {
      label: "Checking Backend",
      dot: "bg-amber-400",
    },
    connected: {
      label: "Backend Connected",
      dot: "bg-emerald-400",
    },
    offline: {
      label: "Backend Offline",
      dot: "bg-red-400",
    },
  };

  const currentStatus =
    statusConfig[status];

  return (
    <header className="mb-8">
      <div className="flex flex-col gap-4 border-b border-slate-800 pb-6 md:flex-row md:items-end md:justify-between">

        <div>
          <div className="mb-2 flex items-center gap-2">
            <span className="h-2 w-2 rounded-full bg-emerald-400" />

            <span className="text-xs font-semibold uppercase tracking-[0.18em] text-emerald-400">
              Market Analytics Platform
            </span>
          </div>

          <h1 className="text-3xl font-bold tracking-tight text-white md:text-4xl">
            {title}
          </h1>

          <p className="mt-2 max-w-2xl text-sm text-slate-400 md:text-base">
            Market data, technical indicators, and machine learning
            predictions in a unified analytics dashboard.
          </p>
        </div>

        <div className="rounded-lg border border-slate-800 bg-slate-900 px-4 py-3">

          <p className="text-[10px] font-semibold uppercase tracking-wider text-slate-500">
            Platform Status
          </p>

          <div className="mt-1 flex items-center gap-2">

            <span
              className={`h-2 w-2 rounded-full ${currentStatus.dot}`}
            />

            <span className="text-sm font-medium text-slate-300">
              {currentStatus.label}
            </span>

          </div>

        </div>

      </div>
    </header>
  );
}
