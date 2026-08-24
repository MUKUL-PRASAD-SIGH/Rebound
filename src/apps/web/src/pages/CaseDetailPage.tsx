import { useCallback, useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import {
  decideCase,
  executeCase,
  getCase,
  getCaseAudit,
  type AuditEvent,
  type CaseRow,
  type DecideResult,
  type ExecuteResult,
} from "../api";

export default function CaseDetailPage() {
  const { id } = useParams();
  const [caseRow, setCaseRow] = useState<CaseRow | null>(null);
  const [audit, setAudit] = useState<AuditEvent[]>([]);
  const [lastDecide, setLastDecide] = useState<DecideResult | null>(null);
  const [lastExecute, setLastExecute] = useState<ExecuteResult | null>(null);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  const refresh = useCallback(async () => {
    if (!id) return;
    setError("");
    try {
      const [c, a] = await Promise.all([getCase(id), getCaseAudit(id)]);
      setCaseRow(c);
      setAudit(a);
    } catch (e) {
      setError(String(e));
    }
  }, [id]);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  async function onDecide(autoExecute: boolean) {
    if (!id) return;
    setBusy(true);
    setError("");
    try {
      const r = await decideCase(id, autoExecute);
      setLastDecide(r);
      if (r.executed) setLastExecute(null);
      await refresh();
    } catch (e) {
      setError(String(e));
    } finally {
      setBusy(false);
    }
  }

  async function onExecute() {
    if (!id) return;
    setBusy(true);
    setError("");
    try {
      const r = await executeCase(id);
      setLastExecute(r);
      await refresh();
    } catch (e) {
      setError(String(e));
    } finally {
      setBusy(false);
    }
  }

  if (!id) return null;

  return (
    <section className="panel">
      <p className="note">
        <Link to="/cases">← Cases</Link>
      </p>
      <h1>Case detail</h1>
      {error ? <p className="note">{error}</p> : null}

      {caseRow ? (
        <dl className="meta">
          <div>
            <dt>Key</dt>
            <dd>
              <code>{caseRow.case_key}</code>
            </dd>
          </div>
          <div>
            <dt>Status</dt>
            <dd>{caseRow.status}</dd>
          </div>
          <div>
            <dt>Amount</dt>
            <dd>₹{(caseRow.amount_paise / 100).toFixed(2)}</dd>
          </div>
          <div>
            <dt>Failure</dt>
            <dd>{caseRow.failure_class}</dd>
          </div>
          <div>
            <dt>Latest action</dt>
            <dd>{caseRow.latest_decision_action ?? "—"}</dd>
          </div>
          <div>
            <dt>Gate</dt>
            <dd>{caseRow.latest_gate_result ?? "—"}</dd>
          </div>
        </dl>
      ) : (
        <p className="note">Loading…</p>
      )}

      <div className="row" style={{ marginBottom: "1.25rem" }}>
        <button type="button" disabled={busy} onClick={() => void onDecide(false)}>
          Decide
        </button>
        <button type="button" disabled={busy} onClick={() => void onDecide(true)}>
          Decide + execute
        </button>
        <button type="button" disabled={busy} onClick={() => void onExecute()}>
          Execute latest
        </button>
      </div>

      {lastDecide ? (
        <div className="note" style={{ marginBottom: "1rem" }}>
          Proposed <code>{lastDecide.proposed_action}</code> → gated{" "}
          <code>{lastDecide.gated_action}</code> ({lastDecide.gate_result}: {lastDecide.gate_reason}
          ). EV={lastDecide.ev.toFixed(1)} · conf={lastDecide.confidence.toFixed(2)}
          <br />
          {lastDecide.rationale}
        </div>
      ) : null}

      {lastExecute ? (
        <div className="note" style={{ marginBottom: "1rem" }}>
          Executed <code>{lastExecute.action}</code> mode=<code>{lastExecute.mode}</code>
        </div>
      ) : null}

      <h2 style={{ fontSize: "1.1rem", marginTop: "1.5rem" }}>Audit trail</h2>
      <table>
        <thead>
          <tr>
            <th>Time</th>
            <th>Kind</th>
            <th>Payload</th>
          </tr>
        </thead>
        <tbody>
          {audit.map((e) => (
            <tr key={e.id}>
              <td>{new Date(e.created_at).toLocaleString()}</td>
              <td>
                <code>{e.kind}</code>
              </td>
              <td>
                <code style={{ whiteSpace: "pre-wrap", fontSize: "0.75rem" }}>
                  {JSON.stringify(e.payload)}
                </code>
              </td>
            </tr>
          ))}
          {!audit.length ? (
            <tr>
              <td colSpan={3}>No audit events yet — run Decide.</td>
            </tr>
          ) : null}
        </tbody>
      </table>
    </section>
  );
}
