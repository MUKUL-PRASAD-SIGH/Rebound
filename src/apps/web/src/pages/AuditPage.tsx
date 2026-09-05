import { useCallback, useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { getRecentAudit, type AuditEvent } from "../api";
import { EmptyState, Icon, StatusPill, titleCase } from "../ui";

const displayableContext = new Set([
  "action",
  "case_status",
  "event_type",
  "gate_result",
  "gated_action",
  "label",
  "policy_version",
  "result",
  "source",
  "value_paise",
]);

function eventSummary(payload: Record<string, unknown>): string {
  const entries = Object.entries(payload).filter(([key]) => displayableContext.has(key));
  if (!entries.length) return "Context protected";
  return entries.map(([key, value]) => `${titleCase(key)}: ${String(value)}`).join(" · ");
}

export default function AuditPage() {
  const [events, setEvents] = useState<AuditEvent[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  const refresh = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      setEvents(await getRecentAudit());
    } catch (requestError) {
      setError(String(requestError));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  const uniqueCases = useMemo(() => new Set(events.map((event) => event.case_id)).size, [events]);
  const outcomeEvents = events.filter((event) => event.kind === "outcome").length;

  return (
    <section className="page-stack">
      <header className="page-header">
        <div>
          <span className="eyebrow"><Icon name="audit" size={14} /> Decision evidence</span>
          <h1>Audit trail</h1>
          <p>An append-only record of the context, policy decisions, execution, and outcomes behind every recovery action.</p>
        </div>
        <button className="button button--ghost" disabled={loading} onClick={() => void refresh()} type="button">
          <Icon className={loading ? "spin" : undefined} name="refresh" size={16} /> {loading ? "Refreshing…" : "Refresh record"}
        </button>
      </header>

      <div className="summary-strip">
        <div><span>Recent events</span><strong>{events.length}</strong></div>
        <div><span>Cases covered</span><strong>{uniqueCases}</strong></div>
        <div><span>Outcome records</span><strong>{outcomeEvents}</strong></div>
        <div><span>Record type</span><strong className="summary-strip__text">Append-only</strong></div>
      </div>

      {error ? <div className="notice notice--error"><Icon name="warning" size={18} /><span>{error}</span></div> : null}

      <section className="card data-card audit-card">
        <div className="table-toolbar">
          <div><span className="eyebrow eyebrow--muted">Latest activity</span><h2>Recovery decision log</h2></div>
          <StatusPill tone="good"><span className="live-dot" /> IMMUTABLE HISTORY</StatusPill>
        </div>
        {events.length ? (
          <div className="table-scroll">
            <table className="data-table audit-table">
              <thead><tr><th>Timestamp</th><th>Case</th><th>Event</th><th>Recorded context</th></tr></thead>
              <tbody>{events.map((event) => (
                <tr key={event.id}>
                  <td className="time-cell">{new Date(event.created_at).toLocaleString()}</td>
                  <td><Link className="case-link" to={`/cases/${event.case_id}`}><code>{event.case_id.slice(0, 8)}</code><Icon name="chevron-right" size={14} /></Link></td>
                  <td><span className="event-label"><span className="event-label__dot" />{titleCase(event.kind)}</span></td>
                  <td><span className="payload-code">{eventSummary(event.payload)}</span></td>
                </tr>
              ))}</tbody>
            </table>
          </div>
        ) : !loading && !error ? <EmptyState detail="Recovery decisions, policy gates, execution attempts, and outcomes will appear here as the queue runs." icon="audit" title="No audit events yet" /> : null}
      </section>
    </section>
  );
}
