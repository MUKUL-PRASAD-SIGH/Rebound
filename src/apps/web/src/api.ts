const API = import.meta.env.VITE_API_URL ?? "";

export type MetricsSummary = {
  cases_total: number;
  cases_open: number;
  cases_recovered: number;
  cases_stopped: number;
  cases_escalated: number;
  eval_runs: number;
};

export type CaseRow = {
  id: string;
  case_key: string;
  status: string;
  amount_paise: number;
  failure_class: string;
  method: string;
  attempt_n: number;
};

export async function getHealth(): Promise<{ status: string; version: string }> {
  const res = await fetch(`${API}/api/v1/health`);
  if (!res.ok) throw new Error(`health ${res.status}`);
  return res.json();
}

export async function getMetrics(): Promise<MetricsSummary> {
  const res = await fetch(`${API}/api/v1/metrics/summary`);
  if (!res.ok) throw new Error(`metrics ${res.status}`);
  return res.json();
}

export async function listCases(): Promise<CaseRow[]> {
  const res = await fetch(`${API}/api/v1/cases`);
  if (!res.ok) throw new Error(`cases ${res.status}`);
  return res.json();
}

export async function seedSynthetic(): Promise<{ inserted: number; skipped: number }> {
  const res = await fetch(`${API}/api/v1/ingest/synthetic`, { method: "POST" });
  if (!res.ok) throw new Error(`seed ${res.status}`);
  return res.json();
}
