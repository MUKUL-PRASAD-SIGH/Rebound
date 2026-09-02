import { useEffect, useState } from "react";
import { formatCurrency, Icon, StatusPill, titleCase } from "../ui";

type EvalSummary = {
  eval_run_id?: string;
  lift_value?: number;
  lift_value_label?: string;
  honest_note?: string;
  policies?: Record<
    string,
    {
      recovery_rate: number;
      recovered_value: number;
      intervention_cost: number;
      net_value: number;
      stop_rate: number;
      escalation_rate: number;
      simulated_share: number;
      cases: number;
      recovered: number;
    }
  >;
};

type EvalListItem = {
  eval_run_id: string;
  batch_id: string;
  lift_value: number | null;
  created_at: string | null;
};

const API = import.meta.env.VITE_API_URL ?? "";

const policyDescriptions: Record<string, string> = {
  baseline_a: "Fixed recovery ladder",
  baseline_b: "Alternate heuristic",
  rebound: "Expected-value policy",
};

export default function EvalPage() {
  const [latest, setLatest] = useState<EvalSummary | null>(null);
  const [list, setList] = useState<EvalListItem[]>([]);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function refreshList() {
    const response = await fetch(`${API}/api/v1/eval/runs`);
    if (!response.ok) throw new Error(`Could not load evaluation history (${response.status})`);
    setList(await response.json());
  }

  useEffect(() => {
    refreshList().catch((requestError: unknown) => setError(String(requestError)));
  }, []);

  async function runEvaluation() {
    setBusy(true);
    setError("");
    try {
      const response = await fetch(`${API}/api/v1/eval/runs`, { method: "POST", body: "{}" });
      if (!response.ok) throw new Error(await response.text());
      setLatest((await response.json()) as EvalSummary);
      await refreshList();
    } catch (requestError) {
      setError(String(requestError));
    } finally {
      setBusy(false);
    }
  }

  const liftIsPositive = (latest?.lift_value ?? 0) >= 0;

  return (
    <section className="page-stack">
      <header className="page-header eval-header">
        <div>
          <span className="eyebrow"><Icon name="chart" size={14} /> Evaluation lab</span>
          <h1>Prove the decision advantage.</h1>
          <p>Compare Rebound against fixed and heuristic baselines on the same simulated cases and random draws.</p>
        </div>
        <button className="button button--primary" disabled={busy} onClick={() => void runEvaluation()} type="button">
          {busy ? <Icon className="spin" name="refresh" size={16} /> : <Icon name="play" size={16} />}
          {busy ? "Running evaluation…" : "Run fresh evaluation"}
        </button>
      </header>

      {error ? <div className="notice notice--error"><Icon name="warning" size={18} /><span>{error}</span></div> : null}

      {latest ? (
        <>
          <section className="eval-headline">
            <div className="eval-headline__metric">
              <span className="eyebrow">Incremental net value</span>
              <strong className={liftIsPositive ? "positive-value" : "negative-value"}>{formatCurrency(latest.lift_value)}</strong>
              <p><Icon name={liftIsPositive ? "activity" : "warning"} size={16} /> Rebound versus Baseline A</p>
            </div>
            <div className="eval-headline__context">
              <div><span>Evaluation label</span><code>{latest.lift_value_label}</code></div>
              <div><span>Run reference</span><code>{latest.eval_run_id?.slice(0, 8)}</code></div>
              <StatusPill tone="warn">SIMULATED OUTPUT</StatusPill>
            </div>
            <p className="eval-headline__note"><Icon name="shield" size={16} />{latest.honest_note}</p>
          </section>

          <section className="policy-grid">
            {latest.policies && Object.entries(latest.policies).map(([name, policy]) => (
              <article className={`policy-metric${name === "rebound" ? " policy-metric--rebound" : ""}`} key={name}>
                <div className="policy-metric__head">
                  <div><span className="policy-metric__name">{titleCase(name)}</span><p>{policyDescriptions[name] ?? "Comparison policy"}</p></div>
                  {name === "rebound" ? <StatusPill tone="good">REBOUND</StatusPill> : null}
                </div>
                <strong>{formatCurrency(policy.net_value)}</strong>
                <span className="policy-metric__caption">net simulated value</span>
                <div className="policy-metric__stats">
                  <div><span>Recovery</span><b>{(policy.recovery_rate * 100).toFixed(1)}%</b></div>
                  <div><span>Cost</span><b>{formatCurrency(policy.intervention_cost)}</b></div>
                  <div><span>Stop rate</span><b>{(policy.stop_rate * 100).toFixed(0)}%</b></div>
                </div>
              </article>
            ))}
          </section>
        </>
      ) : (
        <section className="card eval-empty">
          <div className="eval-empty__visual"><Icon name="chart" size={30} /><span /><span /><span /></div>
          <div><span className="eyebrow eyebrow--muted">No active result</span><h2>Run an apples-to-apples comparison</h2><p>The same random outcome draw is shared by all policies, so the difference is attributable to the decision strategy.</p></div>
        </section>
      )}

      <section className="card data-card">
        <div className="table-toolbar">
          <div><span className="eyebrow eyebrow--muted">Historical record</span><h2>Past evaluation runs</h2></div>
          <span className="record-count">{list.length} recorded</span>
        </div>
        {list.length ? (
          <div className="table-scroll">
            <table className="data-table">
              <thead><tr><th>Completed</th><th>Batch reference</th><th>Incremental lift</th><th><span className="sr-only">Status</span></th></tr></thead>
              <tbody>{list.map((run) => (
                <tr key={run.eval_run_id}>
                  <td className="time-cell">{run.created_at ? new Date(run.created_at).toLocaleString() : "—"}</td>
                  <td><code>{run.batch_id}</code></td>
                  <td className={run.lift_value !== null && run.lift_value >= 0 ? "positive-value currency-cell" : "currency-cell"}>{formatCurrency(run.lift_value)}</td>
                  <td><StatusPill tone="neutral">SIMULATED</StatusPill></td>
                </tr>
              ))}</tbody>
            </table>
          </div>
        ) : <div className="table-empty">No runs recorded yet. Seed a batch first, then run an evaluation.</div>}
      </section>
    </section>
  );
}
