import { useCallback, useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { getRecentAudit, listCases, type AuditEvent, type CaseRow } from "../api";
import { EmptyState, formatCurrency, Icon, StatusPill, titleCase } from "../ui";

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

function statusTone(status: string | undefined): "good" | "neutral" | "warn" {
  if (status === "recovered") return "good";
  if (status === "stopped") return "neutral";
  return "warn";
}

type ActivityGroup = {
  id: string;
  caseId: string;
  caseRow?: CaseRow;
  events: AuditEvent[];
};

export default function AuditPage() {
  const [events, setEvents] = useState<AuditEvent[]>([]);
  const [cases, setCases] = useState<CaseRow[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  const refresh = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const [auditEvents, caseRows] = await Promise.all([getRecentAudit(), listCases()]);
      setEvents(auditEvents);
      setCases(caseRows);
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
  const executedEvents = events.filter((event) => event.kind === "executed").length;
  const policyBlocks = events.filter((event) => event.kind === "gated" && event.payload.gate_result !== "allow").length;
  const caseById = useMemo(() => new Map(cases.map((caseRow) => [caseRow.id, caseRow])), [cases]);
  const groupedActivity = useMemo(() => {
    const groups = new Map<string, ActivityGroup>();
    for (const event of events) {
      const decisionId = typeof event.payload.decision_id === "string" ? event.payload.decision_id : "intake";
      const groupId = `${event.case_id}:${decisionId}`;
      const existing = groups.get(groupId);
      if (existing) {
        existing.events.push(event);
      } else {
        groups.set(groupId, { id: groupId, caseId: event.case_id, caseRow: caseById.get(event.case_id), events: [event] });
      }
    }
    return [...groups.values()];
  }, [caseById, events]);

  return (
    <section className="page-stack">
      <header className="page-header">
        <div>
          <span className="eyebrow"><Icon name="audit" size={14} /> Activity</span>
          <h1>Activity</h1>
          <p>A complete record of recovery decisions and execution events.</p>
        </div>
        <button className="button button--ghost" disabled={loading} onClick={() => void refresh()} type="button">
          <Icon className={loading ? "spin" : undefined} name="refresh" size={16} /> {loading ? "Refreshing…" : "Refresh activity"}
        </button>
      </header>

      <div className="summary-strip">
        <div><span>Recent events</span><strong>{events.length}</strong></div>
        <div><span>Cases tracked</span><strong>{uniqueCases}</strong></div>
        <div><span>Actions executed</span><strong>{executedEvents}</strong></div>
        <div><span>Policy blocks</span><strong>{policyBlocks}</strong></div>
      </div>

      {error ? <div className="notice notice--error"><Icon name="warning" size={18} /><span>{error}</span></div> : null}

      <section className="card activity-card">
        <div className="table-toolbar">
          <div><span className="eyebrow eyebrow--muted">Latest activity</span><h2>Recovery decision summaries</h2></div>
          <StatusPill tone="good"><span className="live-dot" /> IMMUTABLE EVENT LOG</StatusPill>
        </div>
        {groupedActivity.length ? (
          <div className="activity-list">
            {groupedActivity.map((group) => {
              const action = group.caseRow?.latest_decision_action;
              const latestEvent = group.events[0];
              return <article className="activity-group" key={group.id}>
                <header className="activity-group__head">
                  <div>
                    <Link className="case-link" to={`/cases/${group.caseId}`}><code>{group.caseRow?.case_key ?? group.caseId.slice(0, 8)}</code><Icon name="chevron-right" size={14} /></Link>
                    <span>{group.caseRow ? formatCurrency(group.caseRow.amount_paise) : "Protected case"}</span>
                  </div>
                  <StatusPill tone={statusTone(group.caseRow?.status)}>{action ? titleCase(action) : titleCase(latestEvent.kind)}</StatusPill>
                </header>
                <div className="activity-timeline">
                  {group.events.slice().reverse().map((event) => (
                    <div className="activity-event" key={event.id}>
                      <span className="event-label"><span className="event-label__dot" />{titleCase(event.kind)}</span>
                      <span className="payload-code">{eventSummary(event.payload)}</span>
                      <time>{new Date(event.created_at).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" })}</time>
                    </div>
                  ))}
                </div>
                <Link className="activity-group__link" to={`/cases/${group.caseId}`}>View full evidence <Icon name="arrow-right" size={15} /></Link>
              </article>;
            })}
          </div>
        ) : !loading && !error ? <EmptyState detail="Recovery decisions, policy gates, execution attempts, and outcomes will appear here as the queue runs." icon="audit" title="No audit events yet" /> : null}
      </section>
    </section>
  );
}
