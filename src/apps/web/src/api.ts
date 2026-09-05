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
  customer_ref?: string;
  tenure_days?: number;
  currency?: string;
  source?: string;
  latest_decision_action?: string | null;
  latest_gate_result?: string | null;
  failure_code?: string | null;
};

export type AuditEvent = {
  id: string;
  case_id: string;
  kind: string;
  payload: Record<string, unknown>;
  created_at: string;
};

export type DecideResult = {
  case_id: string;
  proposed_action: string;
  gated_action: string;
  gate_result: string;
  gate_reason: string;
  rationale: string;
  confidence: number;
  ev: number;
  executed: boolean;
  attempt_id: string | null;
};

export type ExecuteResult = {
  attempt_id: string;
  action: string;
  mode: string;
  response: Record<string, unknown>;
  razorpay_payment_link_id?: string | null;
};

export type PaymentLinkRefreshResult = {
  case_id: string;
  payment_link_id: string;
  payment_link_status?: string | null;
  reconciled: boolean;
  case_status: string;
};

async function jsonOrThrow<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`${res.status}: ${text}`);
  }
  return res.json() as Promise<T>;
}

export async function getHealth(): Promise<{ status: string; version: string }> {
  return jsonOrThrow(await fetch(`${API}/api/v1/health`));
}

export async function getMetrics(): Promise<MetricsSummary> {
  return jsonOrThrow(await fetch(`${API}/api/v1/metrics/summary`));
}

export async function listCases(): Promise<CaseRow[]> {
  return jsonOrThrow(await fetch(`${API}/api/v1/cases`));
}

export async function getCase(id: string): Promise<CaseRow> {
  return jsonOrThrow(await fetch(`${API}/api/v1/cases/${id}`));
}

export async function getCaseAudit(id: string): Promise<AuditEvent[]> {
  return jsonOrThrow(await fetch(`${API}/api/v1/cases/${id}/audit`));
}

export async function seedSynthetic(): Promise<{ inserted: number; skipped: number }> {
  return jsonOrThrow(await fetch(`${API}/api/v1/ingest/synthetic`, { method: "POST" }));
}

export async function decideCase(id: string, autoExecute = false): Promise<DecideResult> {
  const q = autoExecute ? "?auto_execute=true" : "";
  return jsonOrThrow(await fetch(`${API}/api/v1/cases/${id}/decide${q}`, { method: "POST" }));
}

export async function executeCase(id: string): Promise<ExecuteResult> {
  return jsonOrThrow(await fetch(`${API}/api/v1/cases/${id}/execute`, { method: "POST" }));
}

export async function refreshPaymentLink(id: string): Promise<PaymentLinkRefreshResult> {
  return jsonOrThrow(await fetch(`${API}/api/v1/cases/${id}/refresh-payment-link`, { method: "POST" }));
}

export async function batchDecide(autoExecute = true): Promise<{ count: number }> {
  const q = autoExecute ? "?auto_execute=true" : "?auto_execute=false";
  return jsonOrThrow(await fetch(`${API}/api/v1/cases/batch/decide${q}`, { method: "POST" }));
}

export async function runEval(seed = 42): Promise<Record<string, unknown>> {
  return jsonOrThrow(
    await fetch(`${API}/api/v1/eval/runs?seed=${seed}`, { method: "POST", body: "{}" }),
  );
}
