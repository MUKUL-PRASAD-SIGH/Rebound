import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { listCases, type CaseRow } from "../api";
import { EmptyState, formatCurrency, Icon, StatusPill, titleCase } from "../ui";

function statusTone(status: string): "good" | "neutral" | "warn" {
  if (status === "recovered") return "good";
  if (status === "stopped") return "neutral";
  return "warn";
}

export default function CasesPage() {
  const [cases, setCases] = useState<CaseRow[]>([]);
  const [error, setError] = useState("");
  const [query, setQuery] = useState("");

  useEffect(() => {
    listCases()
      .then(setCases)
      .catch((requestError: unknown) => setError(String(requestError)));
  }, []);

  const visibleCases = useMemo(() => {
    const needle = query.trim().toLowerCase();
    if (!needle) return cases;
    return cases.filter((caseRow) =>
      [caseRow.case_key, caseRow.failure_class, caseRow.status]
        .filter(Boolean)
        .some((value) => value?.toLowerCase().includes(needle)),
    );
  }, [cases, query]);

  const openCases = cases.filter((caseRow) => caseRow.status === "open").length;
  const escalatedCases = cases.filter((caseRow) => caseRow.status === "escalated").length;

  return (
    <section className="page-stack">
      <header className="page-header">
        <div>
          <span className="eyebrow"><Icon name="cases" size={14} /> Recovery portfolio</span>
          <h1>Recovery queue</h1>
          <p>Review every at-risk payment, its current policy state, and the route to a decision.</p>
        </div>
        <Link className="button button--ghost" to="/eval"><Icon name="chart" size={16} /> Evaluate portfolio</Link>
      </header>

      <div className="summary-strip">
        <div><span>Total cases</span><strong>{cases.length}</strong></div>
        <div><span>Awaiting action</span><strong>{openCases}</strong></div>
        <div><span>Escalated</span><strong>{escalatedCases}</strong></div>
        <div><span>Showing</span><strong>{visibleCases.length}</strong></div>
      </div>

      {error ? (
        <div className="notice notice--error"><Icon name="warning" size={18} /><span>{error}</span></div>
      ) : null}

      <section className="card data-card">
        <div className="table-toolbar">
          <div>
            <span className="eyebrow eyebrow--muted">Live queue</span>
            <h2>Cases requiring attention</h2>
          </div>
          <label className="search-field">
            <Icon name="cases" size={16} />
            <input aria-label="Filter recovery cases" onChange={(event) => setQuery(event.target.value)} placeholder="Search cases" value={query} />
          </label>
        </div>

        {cases.length === 0 && !error ? (
          <EmptyState detail="Start from Overview and seed the 60-case sample batch to populate the recovery portfolio." title="Your queue is ready for its first batch" />
        ) : visibleCases.length === 0 ? (
          <EmptyState detail="Try another case key, failure class, or status." icon="warning" title="No cases match that search" />
        ) : (
          <div className="table-scroll">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Case</th>
                  <th>Status</th>
                  <th>At risk</th>
                  <th>Failure signal</th>
                  <th>Method</th>
                  <th><span className="sr-only">Open case</span></th>
                </tr>
              </thead>
              <tbody>
                {visibleCases.map((caseRow) => (
                  <tr key={caseRow.id}>
                    <td>
                      <div className="case-cell">
                        <code>{caseRow.case_key}</code>
                        <span>Protected account</span>
                      </div>
                    </td>
                    <td><StatusPill tone={statusTone(caseRow.status)}>{titleCase(caseRow.status)}</StatusPill></td>
                    <td className="currency-cell">{formatCurrency(caseRow.amount_paise)}</td>
                    <td><span className="soft-tag">{titleCase(caseRow.failure_class)}</span></td>
                    <td><span className="method-cell">{titleCase(caseRow.method)}</span></td>
                    <td className="table-action"><Link aria-label={`Open ${caseRow.case_key}`} to={`/cases/${caseRow.id}`}><Icon name="chevron-right" size={18} /></Link></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </section>
  );
}
