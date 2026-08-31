import { useEffect, useState } from "react";

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

export default function EvalPage() {
  const [latest, setLatest] = useState<EvalSummary | null>(null);
  const [list, setList] = useState<EvalListItem[]>([]);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function refreshList() {
    const res = await fetch(`${API}/api/v1/eval/runs`);
    if (!res.ok) throw new Error(`list ${res.status}`);
    setList(await res.json());
  }

  useEffect(() => {
    refreshList().catch((e) => setError(String(e)));
  }, []);

  async function runEval() {
    setBusy(true);
    setError("");
    try {
      const res = await fetch(`${API}/api/v1/eval/runs`, { method: "POST", body: "{}" });
      if (!res.ok) throw new Error(await res.text());
      const data = (await res.json()) as EvalSummary;
      setLatest(data);
      await refreshList();
    } catch (e) {
      setError(String(e));
    } finally {
      setBusy(false);
    }
  }

  return (
    <section className="panel">
      <h1>Eval</h1>
      <p className="lede">
        Baseline A vs Rebound on the current case batch. Headline metric: <code>lift_value</code>{" "}
        (simulated net value delta — labeled honestly).
      </p>
      <div className="row" style={{ marginBottom: "1rem" }}>
        <button type="button" disabled={busy} onClick={() => void runEval()}>
          Run eval
        </button>
      </div>
      {error ? <p className="note">{error}</p> : null}

      {latest ? (
        <>
          <dl className="meta">
            <div>
              <dt>Lift value</dt>
              <dd>{latest.lift_value ?? "—"}</dd>
            </div>
            <div>
              <dt>Label</dt>
              <dd>
                <code>{latest.lift_value_label}</code>
              </dd>
            </div>
            <div>
              <dt>Run</dt>
              <dd>
                <code>{latest.eval_run_id?.slice(0, 8)}</code>
              </dd>
            </div>
          </dl>
          <p className="note">{latest.honest_note}</p>
          <table>
            <thead>
              <tr>
                <th>Policy</th>
                <th>Recovery rate</th>
                <th>Net value</th>
                <th>Cost</th>
                <th>Stop rate</th>
                <th>Sim share</th>
              </tr>
            </thead>
            <tbody>
              {latest.policies &&
                Object.entries(latest.policies).map(([name, p]) => (
                  <tr key={name}>
                    <td>
                      <code>{name}</code>
                    </td>
                    <td>{(p.recovery_rate * 100).toFixed(1)}%</td>
                    <td>{p.net_value}</td>
                    <td>{p.intervention_cost}</td>
                    <td>{(p.stop_rate * 100).toFixed(1)}%</td>
                    <td>{(p.simulated_share * 100).toFixed(0)}%</td>
                  </tr>
                ))}
            </tbody>
          </table>
        </>
      ) : null}

      <h2 style={{ fontSize: "1.1rem", marginTop: "1.5rem" }}>Past runs</h2>
      <table>
        <thead>
          <tr>
            <th>When</th>
            <th>Batch</th>
            <th>Lift</th>
          </tr>
        </thead>
        <tbody>
          {list.map((r) => (
            <tr key={r.eval_run_id}>
              <td>{r.created_at ? new Date(r.created_at).toLocaleString() : "—"}</td>
              <td>
                <code>{r.batch_id}</code>
              </td>
              <td>{r.lift_value ?? "—"}</td>
            </tr>
          ))}
          {!list.length ? (
            <tr>
              <td colSpan={3}>No eval runs yet.</td>
            </tr>
          ) : null}
        </tbody>
      </table>
    </section>
  );
}
