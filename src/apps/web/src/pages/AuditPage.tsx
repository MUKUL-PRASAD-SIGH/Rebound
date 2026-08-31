import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

type AuditEvent = {
  id: string;
  case_id: string;
  kind: string;
  payload: Record<string, unknown>;
  created_at: string;
};

const API = import.meta.env.VITE_API_URL ?? "";

export default function AuditPage() {
  const [events, setEvents] = useState<AuditEvent[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch(`${API}/api/v1/audit/recent`)
      .then(async (r) => {
        if (!r.ok) throw new Error(String(r.status));
        return r.json();
      })
      .then(setEvents)
      .catch((e) => setError(String(e)));
  }, []);

  return (
    <section className="panel">
      <h1>Audit</h1>
      <p className="lede">Recent audit events across cases (append-only).</p>
      {error ? <p className="note">{error}</p> : null}
      <table>
        <thead>
          <tr>
            <th>Time</th>
            <th>Case</th>
            <th>Kind</th>
            <th>Payload</th>
          </tr>
        </thead>
        <tbody>
          {events.map((e) => (
            <tr key={e.id}>
              <td>{new Date(e.created_at).toLocaleString()}</td>
              <td>
                <Link to={`/cases/${e.case_id}`}>
                  <code>{e.case_id.slice(0, 8)}</code>
                </Link>
              </td>
              <td>
                <code>{e.kind}</code>
              </td>
              <td>
                <code style={{ fontSize: "0.75rem", whiteSpace: "pre-wrap" }}>
                  {JSON.stringify(e.payload)}
                </code>
              </td>
            </tr>
          ))}
          {!events.length && !error ? (
            <tr>
              <td colSpan={4}>No events yet.</td>
            </tr>
          ) : null}
        </tbody>
      </table>
    </section>
  );
}
