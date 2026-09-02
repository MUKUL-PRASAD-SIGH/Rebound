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
import { EmptyState, formatCurrency, Icon, StatusPill, titleCase } from "../ui";

function statusTone(status: string | undefined): "good" | "neutral" | "warn" {
  if (status === "recovered") return "good";
  if (status === "stopped") return "neutral";
  return "warn";
}

export default function CaseDetailPage() {
  const { id } = useParams();
  const [caseRow, setCaseRow] = useState<CaseRow | null>(null);
  const [audit, setAudit] = useState<AuditEvent[]>([]);
  const [lastDecide, setLastDecide] = useState<DecideResult | null>(null);
  const [lastExecute, setLastExecute] = useState<ExecuteResult | null>(null);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState<"decide" | "decide-execute" | "execute" | null>(null);

  const refresh = useCallback(async () => {
    if (!id) return;
    setError("");
    try {
      const [caseResult, auditResult] = await Promise.all([getCase(id), getCaseAudit(id)]);
      setCaseRow(caseResult);
      setAudit(auditResult);
    } catch (requestError) {
      setError(String(requestError));
    }
  }, [id]);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  async function onDecide(autoExecute: boolean) {
    if (!id) return;
    setBusy(autoExecute ? "decide-execute" : "decide");
    setError("");
    try {
      const result = await decideCase(id, autoExecute);
      setLastDecide(result);
      if (result.executed) setLastExecute(null);
      await refresh();
    } catch (requestError) {
      setError(String(requestError));
    } finally {
      setBusy(null);
    }
  }

  async function onExecute() {
    if (!id) return;
    setBusy("execute");
    setError("");
    try {
      setLastExecute(await executeCase(id));
      await refresh();
    } catch (requestError) {
      setError(String(requestError));
    } finally {
      setBusy(null);
    }
  }

  if (!id) return null;

  return (
    <section className="page-stack">
      <header className="page-header page-header--compact">
        <div>
          <Link className="back-link" to="/cases"><Icon name="arrow-right" size={15} /> Back to recovery queue</Link>
          <span className="eyebrow"><Icon name="cases" size={14} /> Case workspace</span>
          <h1>{caseRow ? <code>{caseRow.case_key}</code> : "Case detail"}</h1>
          <p>{caseRow ? "Review the decision context, then take a policy-controlled action." : "Loading decision context…"}</p>
        </div>
        {caseRow ? <StatusPill tone={statusTone(caseRow.status)}>{titleCase(caseRow.status)}</StatusPill> : null}
      </header>

      {error ? <div className="notice notice--error"><Icon name="warning" size={18} /><span>{error}</span></div> : null}

      {caseRow ? (
        <>
          <section className="case-summary">
            <div className="case-amount">
              <span>Revenue at risk</span>
              <strong>{formatCurrency(caseRow.amount_paise)}</strong>
              <small>{titleCase(caseRow.currency)} · {titleCase(caseRow.method)}</small>
            </div>
            <dl className="detail-grid">
              <div><dt>Failure signal</dt><dd>{titleCase(caseRow.failure_class)}</dd></div>
              <div><dt>Attempt</dt><dd>#{caseRow.attempt_n}</dd></div>
              <div><dt>Customer</dt><dd>{caseRow.customer_ref ?? "—"}</dd></div>
              <div><dt>Tenure</dt><dd>{caseRow.tenure_days ?? "—"} days</dd></div>
              <div><dt>Latest action</dt><dd>{titleCase(caseRow.latest_decision_action)}</dd></div>
              <div><dt>Gate outcome</dt><dd>{titleCase(caseRow.latest_gate_result)}</dd></div>
            </dl>
          </section>

          <div className="case-workspace">
            <section className="card decision-card">
              <div className="section-heading">
                <div>
                  <span className="eyebrow eyebrow--muted">Policy-controlled action</span>
                  <h2>Decide the next best step</h2>
                </div>
                <span className="decision-card__badge"><Icon name="shield" size={15} /> Guardrails on</span>
              </div>
              <p className="section-copy">Rebound scores this case, proposes a bounded action, and enforces confidence, value, and retry limits before execution.</p>
              <div className="action-buttons">
                <button className="button button--ghost" disabled={busy !== null} onClick={() => void onDecide(false)} type="button">
                  {busy === "decide" ? <Icon className="spin" name="refresh" size={16} /> : <Icon name="spark" size={16} />}
                  {busy === "decide" ? "Deciding…" : "Preview decision"}
                </button>
                <button className="button button--primary" disabled={busy !== null} onClick={() => void onDecide(true)} type="button">
                  {busy === "decide-execute" ? <Icon className="spin" name="refresh" size={16} /> : <Icon name="play" size={16} />}
                  {busy === "decide-execute" ? "Running…" : "Decide & execute"}
                </button>
                <button className="text-button" disabled={busy !== null} onClick={() => void onExecute()} type="button">
                  {busy === "execute" ? "Executing…" : "Execute latest"} <Icon name="arrow-right" size={15} />
                </button>
              </div>

              {lastDecide ? (
                <div className="decision-result">
                  <div className="decision-result__head"><Icon name="check" size={17} /><strong>Decision recorded</strong><StatusPill tone={lastDecide.gate_result === "allow" ? "good" : "warn"}>{titleCase(lastDecide.gate_result)}</StatusPill></div>
                  <p><code>{titleCase(lastDecide.proposed_action)}</code><Icon name="arrow-right" size={15} /><code>{titleCase(lastDecide.gated_action)}</code></p>
                  <dl><div><dt>Expected value</dt><dd>{lastDecide.ev.toFixed(1)}</dd></div><div><dt>Confidence</dt><dd>{(lastDecide.confidence * 100).toFixed(0)}%</dd></div><div><dt>Reason</dt><dd>{titleCase(lastDecide.gate_reason)}</dd></div></dl>
                  <small>{lastDecide.rationale}</small>
                </div>
              ) : null}

              {lastExecute ? (
                <div className="execution-result"><Icon name="check" size={17} /><span>Executed <code>{titleCase(lastExecute.action)}</code> in <code>{lastExecute.mode}</code> mode.</span></div>
              ) : null}
            </section>

            <aside className="card policy-card">
              <span className="eyebrow eyebrow--muted">Why the policy matters</span>
              <h2>Safe by default</h2>
              <div className="policy-card__item"><Icon name="shield" size={17} /><span><strong>Value floor</strong><small>Negative EV routes stop, not spend.</small></span></div>
              <div className="policy-card__item"><Icon name="warning" size={17} /><span><strong>Human escalation</strong><small>High-value uncertainty is surfaced.</small></span></div>
              <div className="policy-card__item"><Icon name="audit" size={17} /><span><strong>Audit evidence</strong><small>Every decision is traceable below.</small></span></div>
            </aside>
          </div>

          <section className="card data-card audit-card">
            <div className="table-toolbar">
              <div><span className="eyebrow eyebrow--muted">Append-only record</span><h2>Case audit trail</h2></div>
              <span className="record-count">{audit.length} events</span>
            </div>
            {audit.length ? (
              <div className="table-scroll">
                <table className="data-table audit-table">
                  <thead><tr><th>Timestamp</th><th>Event</th><th>Recorded context</th></tr></thead>
                  <tbody>{audit.map((event) => (
                    <tr key={event.id}>
                      <td className="time-cell">{new Date(event.created_at).toLocaleString()}</td>
                      <td><span className="event-label"><span className="event-label__dot" />{titleCase(event.kind)}</span></td>
                      <td><code className="payload-code">{JSON.stringify(event.payload)}</code></td>
                    </tr>
                  ))}</tbody>
                </table>
              </div>
            ) : <EmptyState detail="Run a preview or an execution to create the first traceable decision event." icon="audit" title="No events for this case yet" />}
          </section>
        </>
      ) : !error ? <EmptyState detail="Fetching the latest case state and its decision history." icon="refresh" title="Loading case workspace" /> : null}
    </section>
  );
}
