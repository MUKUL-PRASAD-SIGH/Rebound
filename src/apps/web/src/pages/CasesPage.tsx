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
  const [statusFilter, setStatusFilter] = useState("all");
  const [failureFilter, setFailureFilter] = useState("all");

  useEffect(() => {
    listCases()
      .then(setCases)
      .catch((requestError: unknown) => setError(String(requestError)));
  }, []);

  const visibleCases = useMemo(() => {
    const needle = query.trim().toLowerCase();
    return cases.filter((caseRow) => {
      const matchesSearch = !needle || [caseRow.case_key, caseRow.failure_class, caseRow.status, caseRow.latest_decision_action]
        .filter(Boolean)
        .some((value) => value?.toLowerCase().includes(needle));
      const matchesStatus = statusFilter === "all" || caseRow.status === statusFilter;
      const matchesFailure = failureFilter === "all" || caseRow.failure_class === failureFilter;
      return matchesSearch && matchesStatus && matchesFailure;
    });
  }, [cases, failureFilter, query, statusFilter]);

  const openCases = cases.filter((caseRow) => caseRow.status === "open").length;
  const inProgressCases = cases.filter((caseRow) => caseRow.status === "acting").length;
  const escalatedCases = cases.filter((caseRow) => caseRow.status === "escalated").length;
  const stoppedCases = cases.filter((caseRow) => caseRow.status === "stopped").length;
  const failureClasses = [...new Set(cases.map((caseRow) => caseRow.failure_class).filter(Boolean))].sort();

  return (
    <section className="page-stack">
      <header className="page-header">
        <div>
          <span className="eyebrow"><Icon name="cases" size={14} /> Recovery</span>
          <h1>Recovery</h1>
          <p>Review failed payments and take the next best recovery action.</p>
        </div>
        <Link className="button button--ghost" to="/eval"><Icon name="chart" size={16} /> View insights</Link>
      </header>

      <div className="summary-strip">
        <div><span>Open</span><strong>{openCases}</strong></div>
        <div><span>In progress</span><strong>{inProgressCases}</strong></div>
        <div><span>Escalated</span><strong>{escalatedCases}</strong></div>
        <div><span>Stopped</span><strong>{stoppedCases}</strong></div>
      </div>

      {error ? (
        <div className="notice notice--error"><Icon name="warning" size={18} /><span>{error}</span></div>
      ) : null}

      <section className="card data-card">
        <div className="table-toolbar">
          <div>
            <span className="eyebrow eyebrow--muted">Recovery queue</span>
            <h2>Cases requiring attention</h2>
          </div>
          <div className="queue-filters">
            <label className="filter-select"><span className="sr-only">Filter by status</span><select aria-label="Filter recovery cases by status" onChange={(event) => setStatusFilter(event.target.value)} value={statusFilter}><option value="all">All statuses</option><option value="open">Open</option><option value="acting">In progress</option><option value="escalated">Escalated</option><option value="stopped">Stopped</option><option value="recovered">Recovered</option></select></label>
            <label className="filter-select"><span className="sr-only">Filter by failure reason</span><select aria-label="Filter recovery cases by failure reason" onChange={(event) => setFailureFilter(event.target.value)} value={failureFilter}><option value="all">All failure reasons</option>{failureClasses.map((failure) => <option key={failure} value={failure}>{titleCase(failure)}</option>)}</select></label>
            <label className="search-field">
              <Icon name="cases" size={16} />
              <input aria-label="Search recovery cases" onChange={(event) => setQuery(event.target.value)} placeholder="Search case" value={query} />
            </label>
          </div>
        </div>

        {cases.length === 0 && !error ? (
          <EmptyState detail="Start from Operations and load the 60-case demo portfolio to populate the recovery queue." title="Your queue is ready for its first batch" />
        ) : visibleCases.length === 0 ? (
          <EmptyState detail="Try another case, status, or failure-reason filter." icon="warning" title="No cases match these filters" />
        ) : (
          <div className="table-scroll">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Case</th>
                  <th>Amount</th>
                  <th>Failure reason</th>
                  <th>Recommended action</th>
                  <th>Status</th>
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
                    <td className="currency-cell">{formatCurrency(caseRow.amount_paise)}</td>
                    <td><span className="soft-tag">{titleCase(caseRow.failure_class)}</span></td>
                    <td><span className="recommended-action">{caseRow.latest_decision_action ? titleCase(caseRow.latest_decision_action) : "Review"}</span></td>
                    <td><StatusPill tone={statusTone(caseRow.status)}>{titleCase(caseRow.status)}</StatusPill></td>
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
