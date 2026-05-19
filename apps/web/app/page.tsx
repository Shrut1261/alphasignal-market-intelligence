"use client";

import { Activity, BarChart3, Brain, Newspaper, ShieldCheck } from "lucide-react";
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from "recharts";

const equityCurve = [
  { date: "Jan", alpha: 100, spy: 100 },
  { date: "Feb", alpha: 104, spy: 101 },
  { date: "Mar", alpha: 102, spy: 99 },
  { date: "Apr", alpha: 111, spy: 103 },
  { date: "May", alpha: 119, spy: 106 },
  { date: "Jun", alpha: 126, spy: 109 }
];

const sentiment = [
  { ticker: "AAPL", score: 0.62 },
  { ticker: "MSFT", score: 0.48 },
  { ticker: "JPM", score: 0.21 },
  { ticker: "NVDA", score: 0.74 },
  { ticker: "SPY", score: 0.32 }
];

const metrics = [
  { label: "Sharpe", value: "1.42" },
  { label: "Max DD", value: "-8.6%" },
  { label: "Win Rate", value: "57%" },
  { label: "Latency p95", value: "184ms" }
];

export default function DashboardPage() {
  return (
    <main className="min-h-screen bg-ink text-slate-100">
      <header className="border-b border-slate-800 bg-[#0f151c]">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
          <div>
            <h1 className="text-2xl font-semibold tracking-normal">AlphaSignal</h1>
            <p className="mt-1 text-sm text-slate-400">
              Market intelligence, ML signals, sentiment, and backtesting.
            </p>
          </div>
          <div className="flex items-center gap-2 rounded-md border border-slate-700 px-3 py-2 text-sm text-slate-300">
            <ShieldCheck className="h-4 w-4 text-positive" />
            Tested platform slice
          </div>
        </div>
      </header>

      <section className="mx-auto grid max-w-7xl gap-4 px-6 py-6 md:grid-cols-4">
        {metrics.map((metric) => (
          <div key={metric.label} className="rounded-md border border-slate-800 bg-panel p-4">
            <p className="text-sm text-slate-400">{metric.label}</p>
            <p className="mt-2 text-2xl font-semibold">{metric.value}</p>
          </div>
        ))}
      </section>

      <section className="mx-auto grid max-w-7xl gap-4 px-6 pb-8 lg:grid-cols-[1.7fr_1fr]">
        <div className="rounded-md border border-slate-800 bg-panel p-5">
          <div className="mb-4 flex items-center gap-2">
            <BarChart3 className="h-5 w-5 text-accent" />
            <h2 className="text-base font-semibold">Strategy Equity Curve</h2>
          </div>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={equityCurve}>
                <CartesianGrid stroke="#23303d" />
                <XAxis dataKey="date" stroke="#94a3b8" />
                <YAxis stroke="#94a3b8" />
                <Tooltip />
                <Area dataKey="alpha" stroke="#35c2ff" fill="#35c2ff33" />
                <Area dataKey="spy" stroke="#2dd4bf" fill="#2dd4bf22" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="rounded-md border border-slate-800 bg-panel p-5">
          <div className="mb-4 flex items-center gap-2">
            <Newspaper className="h-5 w-5 text-accent" />
            <h2 className="text-base font-semibold">Sentiment Scores</h2>
          </div>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={sentiment}>
                <CartesianGrid stroke="#23303d" />
                <XAxis dataKey="ticker" stroke="#94a3b8" />
                <YAxis stroke="#94a3b8" />
                <Tooltip />
                <Bar dataKey="score" fill="#2dd4bf" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </section>

      <section className="mx-auto grid max-w-7xl gap-4 px-6 pb-10 md:grid-cols-3">
        {[
          { icon: Activity, title: "Ingestion", text: "Yahoo and FRED adapters normalize provider data into typed schemas." },
          { icon: Brain, title: "ML Signals", text: "Leakage-safe labels and directional metrics prepare the LightGBM baseline." },
          { icon: BarChart3, title: "Backtesting", text: "Weights are lagged and transaction costs are modeled before metrics are computed." }
        ].map((item) => (
          <div key={item.title} className="rounded-md border border-slate-800 bg-panel p-5">
            <item.icon className="h-5 w-5 text-accent" />
            <h3 className="mt-4 text-base font-semibold">{item.title}</h3>
            <p className="mt-2 text-sm leading-6 text-slate-400">{item.text}</p>
          </div>
        ))}
      </section>
    </main>
  );
}
