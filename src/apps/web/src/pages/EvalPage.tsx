import { useEffect, useState } from "react";
import { listEvalRuns, runEval } from "../api";
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

const policyPresentation: Record<string, { name: string; description: string }> = {
  baseline_a: { name: "Fixed strategy", description: "Baseline A" },
  baseline_b: { name: "Heuristic strategy", description: "Baseline B" },
  rebound: { name: "Rebound", description: "Expected-value policy" },
};

export default function EvalPage() {
  const [latest, setLatest] = useState<EvalSummary | null>(null);
  const [list, setList] = useState<EvalListItem[]>([]);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function refreshList() {
    setList(await listEvalRuns<EvalListItem[]>());
  }

  useEffect(() => {
    refreshList().catch((requestError: unknown) => setError(String(requestError)));
  }, []);

  async function runEvaluation() {
    setBusy(true);
    setError("");
    try {
      setLatest((await runEval()) as EvalSummary);
      await refreshList();
    } catch (requestError) {
      setError(String(requestError));
    } finally {
      setBusy(false);
    }
  }

  const policies = latest?.policies ?? {};
  const policyEntries = Object.entries(policies);
  const rebound = policies.rebound;
  const lift = latest?.lift_value;
  const liftIsPositive = (lift ?? 0) > 0;
  const differenceMessage = lift === undefined
    ? "—"
    : lift > 0
      ? `${formatCurrency(lift)} above fixed strategy`
      : lift < 0
        ? `${formatCurrency(Math.abs(lift))} below fixed strategy`
        : "Matched fixed strategy";
  const bestPolicy = policyEntries.reduce<[string, (typeof policyEntries)[number][1]] | null>(
    (best, current) => !best || current[1].net_value > best[1].net_value ? current : best,
    null,
  );

  return (
    <section className="page-stack">
      <header className="page-header eval-header">
        <div>
          <span className="eyebrow"><Icon name="chart" size={14} /> Insights</span>
          <h1>Insights</h1>
          <p>Measure recovery performance and compare decision strategies on the same simulated portfolio.</p>
        </div>
        <button className="button button--primary" disabled={busy} onClick={() => void runEvaluation()} type="button">
          {busy ? <Icon className="spin" name="refresh" size={16} /> : <Icon name="play" size={16} />}
          {busy ? "Running evaluation…" : "Run evaluation"}
        </button>
      </header>

      {error ? <div className="notice notice--error"><Icon name="warning" size={18} /><span>{error}</span></div> : null}

      {latest && rebound ? (
        <>
          <section className="eval-headline">
            <div className="eval-headline__metric">
              <span className="eyebrow">Portfolio performance</span>
              <strong>{formatCurrency(rebound.net_value)}</strong>
              <p><Icon name="chart" size={16} /> Simulated net value · Rebound</p>
            </div>
            <div className="eval-headline__context">
              <div><span>Cases evaluated</span><code>{rebound.cases}</code></div>
              <div><span>Recovery rate</span><code>{(rebound.recovery_rate * 100).toFixed(1)}%</code></div>
              <div><span>Stopped by policy</span><code>{(rebound.stop_rate * 100).toFixed(0)}%</code></div>
              <div><span>Run reference</span><code>{latest.eval_run_id?.slice(0, 8)}</code></div>
              <StatusPill tone="warn">SIMULATED OUTPUT</StatusPill>
            </div>
            <p className="eval-headline__note"><Icon name="shield" size={16} />{latest.honest_note}</p>
          </section>

          <section className="strategy-section">
            <div className="strategy-heading">
              <div><span className="eyebrow eyebrow--muted">Strategy comparison</span><h2>Same portfolio. Same simulated outcomes.</h2></div>
              <div className="difference-banner">
                <span>Difference vs fixed strategy</span>
                <strong className={liftIsPositive ? "positive-value" : "neutral-value"}>{differenceMessage}</strong>
              </div>
            </div>
            <div className="policy-grid">
              {policyEntries.map(([name, policy]) => {
                const presentation = policyPresentation[name] ?? { name: titleCase(name), description: "Comparison policy" };
                return (
                  <article className={`policy-metric${name === "rebound" ? " policy-metric--rebound" : ""}`} key={name}>
                    <div className="policy-metric__head">
                      <div><span className="policy-metric__name">{presentation.name}</span><p>{presentation.description}</p></div>
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
                );
              })}
            </div>
          </section>

          <section className="policy-insights">
            <div className="section-heading"><div><span className="eyebrow eyebrow--muted">Policy insights</span><h2>What this simulated run shows</h2></div></div>
            <div className="policy-insights__grid">
              <div><span>Best simulated strategy</span><strong>{bestPolicy ? (policyPresentation[bestPolicy[0]]?.name ?? titleCase(bestPolicy[0])) : "—"}</strong></div>
              <div><span>Rebound recovery rate</span><strong>{(rebound.recovery_rate * 100).toFixed(1)}%</strong></div>
              <div><span>Rebound stop rate</span><strong>{(rebound.stop_rate * 100).toFixed(0)}%</strong></div>
            </div>
          </section>
        </>
      ) : (
        <section className="card eval-empty">
          <div className="eval-empty__visual"><Icon name="chart" size={30} /><span /><span /><span /></div>
          <div><span className="eyebrow eyebrow--muted">No active result</span><h2>Measure a simulated portfolio</h2><p>Run the same outcome draw across each strategy to compare policy choices fairly.</p></div>
        </section>
      )}

      <section className="card data-card">
        <div className="table-toolbar">
          <div><span className="eyebrow eyebrow--muted">Evaluation history</span><h2>Past evaluation runs</h2></div>
          <span className="record-count">{list.length} recorded</span>
        </div>
        {list.length ? (
          <div className="table-scroll">
            <table className="data-table">
              <thead><tr><th>Completed</th><th>Batch reference</th><th>Difference vs fixed strategy</th><th><span className="sr-only">Status</span></th></tr></thead>
              <tbody>{list.map((run) => (
                <tr key={run.eval_run_id}>
                  <td className="time-cell">{run.created_at ? new Date(run.created_at).toLocaleString() : "—"}</td>
                  <td><code>{run.batch_id}</code></td>
                  <td className={run.lift_value !== null && run.lift_value > 0 ? "positive-value currency-cell" : "currency-cell"}>{formatCurrency(run.lift_value)}</td>
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
