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
        const response = await fetch(`${API_BASE}/`, {
          cache: "no-store",
        });

        if (!active) {
          return;
        }

        setStatus(
          response.ok
            ? "connected"
            : "offline"
        );
      } catch {
        if (!active) {
          return;
        }

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
      label: "Checking",
      dot: "bg-amber-400",
      ring: "ring-amber-400/20",
    },
    connected: {
      label: "System Online",
      dot: "bg-emerald-400",
      ring: "ring-emerald-400/20",
    },
    offline: {
      label: "Backend Offline",
      dot: "bg-red-400",
      ring: "ring-red-400/20",
    },
  };

  const currentStatus = statusConfig[status];

  return (
    <header className="mb-8">
      <div className="rounded-2xl border border-slate-800/80 bg-slate-900/70 px-6 py-6 shadow-xl shadow-black/10 backdrop-blur-sm md:px-8 md:py-7">

        <div className="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">

          {/* ---------------------------------------
              BRAND / TITLE
          --------------------------------------- */}

          <div>
            <div className="mb-3 flex items-center gap-3">

              <div className="flex h-8 w-8 items-center justify-center rounded-lg border border-blue-500/20 bg-blue-500/10">
                <div className="h-2.5 w-2.5 rounded-full bg-blue-400 shadow-lg shadow-blue-400/40" />
              </div>

              <span className="text-xs font-bold uppercase tracking-[0.2em] text-blue-400">
                Market Analytics Platform
              </span>

            </div>

            <h1 className="text-3xl font-bold tracking-tight text-white md:text-4xl">
              {title}
            </h1>

            <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-400 md:text-base">
              Market data, technical indicators, and machine
              learning predictions in a unified analytics
              environment.
            </p>
          </div>

          {/* ---------------------------------------
              SYSTEM STATUS
          --------------------------------------- */}

          <div className="flex items-center gap-4 rounded-xl border border-slate-800 bg-slate-950/60 px-5 py-4">

            <div
              className={`flex h-10 w-10 items-center justify-center rounded-full bg-slate-900 ring-4 ${currentStatus.ring}`}
            >
              <span
                className={`h-2.5 w-2.5 rounded-full ${currentStatus.dot}`}
              />
            </div>

            <div>
              <p className="text-[10px] font-bold uppercase tracking-[0.16em] text-slate-500">
                Platform Status
              </p>

              <div className="mt-1 flex items-center gap-2">
                <span
                  className={`h-1.5 w-1.5 rounded-full ${currentStatus.dot}`}
                />

                <span className="text-sm font-semibold text-slate-200">
                  {currentStatus.label}
                </span>
              </div>

              <p className="mt-1 text-[11px] text-slate-500">
                API health monitored automatically
              </p>
            </div>

          </div>

        </div>

        {/* ---------------------------------------
            DIVIDER
        --------------------------------------- */}

        <div className="my-6 h-px bg-slate-800/80" />

        {/* ---------------------------------------
            PLATFORM CAPABILITIES
        --------------------------------------- */}

        <div className="flex flex-wrap items-center gap-x-6 gap-y-3">

          <div className="flex items-center gap-2">
            <span className="h-1.5 w-1.5 rounded-full bg-blue-400" />
            <span className="text-xs font-medium text-slate-400">
              Market Data
            </span>
          </div>

          <div className="flex items-center gap-2">
            <span className="h-1.5 w-1.5 rounded-full bg-violet-400" />
            <span className="text-xs font-medium text-slate-400">
              Technical Analysis
            </span>
          </div>

          <div className="flex items-center gap-2">
            <span className="h-1.5 w-1.5 rounded-full bg-emerald-400" />
            <span className="text-xs font-medium text-slate-400">
              Machine Learning
            </span>
          </div>

          <div className="flex items-center gap-2">
            <span className="h-1.5 w-1.5 rounded-full bg-amber-400" />
            <span className="text-xs font-medium text-slate-400">
              Real-Time API
            </span>
          </div>

        </div>

      </div>
    </header>
  );
}
