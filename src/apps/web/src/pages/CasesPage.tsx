import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { listCases, type CaseRow } from "../api";

export default function CasesPage() {
  const [cases, setCases] = useState<CaseRow[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    listCases()
      .then(setCases)
      .catch((e) => setError(String(e)));
  }, []);

  return (
    <section className="panel">
      <h1>Cases</h1>
      {error ? <p className="note">{error}</p> : null}
      <table>
        <thead>
          <tr>
            <th>Key</th>
            <th>Status</th>
            <th>Amount</th>
            <th>Failure</th>
            <th>Method</th>
            <th />
          </tr>
        </thead>
        <tbody>
          {cases.map((c) => (
            <tr key={c.id}>
              <td>
                <code>{c.case_key}</code>
              </td>
              <td>{c.status}</td>
              <td>₹{(c.amount_paise / 100).toFixed(2)}</td>
              <td>{c.failure_class}</td>
              <td>{c.method}</td>
              <td>
                <Link to={`/cases/${c.id}`}>Open</Link>
              </td>
            </tr>
          ))}
          {!cases.length && !error ? (
            <tr>
              <td colSpan={6}>No cases yet — seed from Home.</td>
            </tr>
          ) : null}
        </tbody>
      </table>
    </section>
  );
}
