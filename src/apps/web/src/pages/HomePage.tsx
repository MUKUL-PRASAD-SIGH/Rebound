import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { batchDecide, getHealth, getMetrics, listCases, seedSynthetic, type CaseRow, type MetricsSummary } from "../api";
import { formatCurrency, Icon, StatusPill, titleCase } from "../ui";

export default function HomePage() {
  const [health, setHealth] = useState<string>("Checking API…");
  const [metrics, setMetrics] = useState<MetricsSummary | null>(null);
  const [cases, setCases] = useState<CaseRow[]>([]);
  const [message, setMessage] = useState<string>("");
  const [busy, setBusy] = useState<"batch" | "seed" | null>(null);

  const apiReady = health.startsWith("ok");

  async function refresh() {
    try {
      const [apiHealth, summary, caseRows] = await Promise.all([getHealth(), getMetrics(), listCases()]);
      setHealth(`${apiHealth.status} · v${apiHealth.version}`);
      setMetrics(summary);
      setCases(caseRows);
    } catch {
      setHealth("Offline — start API on :8000");
      setMetrics(null);
      setCases([]);
    }
  }

  useEffect(() => {
    void refresh();
  }, []);

  async function handleSeed() {
    setBusy("seed");
    setMessage("");
    try {
      const result = await seedSynthetic();
      setMessage(`Sample batch ready — ${result.inserted} seeded, ${result.skipped} already present.`);
      await refresh();
    } catch (error) {
      setMessage(String(error));
    } finally {
      setBusy(null);
    }
  }

  async function handleBatch() {
    setBusy("batch");
    setMessage("");
    try {
      const result = await batchDecide(true);
      setMessage(`${result.count} open cases processed through the policy gate.`);
      await refresh();
    } catch (error) {
      setMessage(String(error));
    } finally {
      setBusy(null);
    }
  }

  const needsAttention = cases.filter((caseRow) => caseRow.status === "open").slice(0, 3);
  const inProgress = cases.filter((caseRow) => caseRow.status === "acting").length;

  return (
    <section className="page-stack">
      <header className="hero">
        <div className="hero__copy">
          <span className="eyebrow"><span className="eyebrow__dot" /> Recovery command center</span>
          <h1>Recovery operations,<br /><em>made deliberate.</em></h1>
          <p>
            Monitor failed payments and run policy-controlled recovery workflows from one focused
            operating view.
          </p>
          <div className="hero__actions">
            <Link className="button button--primary" to="/cases">
              View recovery queue <Icon name="arrow-right" size={17} />
            </Link>
            <Link className="button button--ghost" to="/eval">
              <Icon name="chart" size={17} /> View insights
            </Link>
          </div>
        </div>
        <div className="hero__signal">
          <div className="hero__signal-head">
            <span>SYSTEM STATUS</span>
            <StatusPill tone={apiReady ? "good" : "warn"}>{apiReady ? "OPERATIONAL" : "OFFLINE"}</StatusPill>
          </div>
          <div className="hero__signal-value">{apiReady ? "Ready" : "Waiting"}</div>
          <p>{health}</p>
          <div className="hero__signal-line"><span style={{ width: apiReady ? "76%" : "22%" }} /></div>
          <small>Policy: mvp-v1</small>
        </div>
      </header>

      {message ? (
        <div className={`notice${message.startsWith("Error") ? " notice--error" : ""}`} role="status">
          <Icon name={message.startsWith("Error") ? "warning" : "check"} size={18} />
          <span>{message}</span>
        </div>
      ) : null}

      <div className="metric-grid">
        <article className="metric-card metric-card--accent">
          <span className="metric-card__icon"><Icon name="cases" size={19} /></span>
          <span className="metric-card__label">Open recovery cases</span>
          <strong>{metrics?.cases_open ?? "—"}</strong>
          <p>cases ready for review</p>
        </article>
        <article className="metric-card">
          <span className="metric-card__icon"><Icon name="activity" size={19} /></span>
          <span className="metric-card__label">In progress</span>
          <strong>{metrics ? inProgress : "—"}</strong>
          <p>approved recovery workflows</p>
        </article>
        <article className="metric-card">
          <span className="metric-card__icon"><Icon name="shield" size={19} /></span>
          <span className="metric-card__label">Recovered</span>
          <strong>{metrics?.cases_recovered ?? "—"}</strong>
          <p>recorded outcomes</p>
        </article>
        <article className="metric-card">
          <span className="metric-card__icon"><Icon name="chart" size={19} /></span>
          <span className="metric-card__label">Stopped by policy</span>
          <strong>{metrics?.cases_stopped ?? "—"}</strong>
          <p>cases where no action was best</p>
        </article>
      </div>

      <div className="overview-grid">
        <section className="card card--operations">
          <div className="section-heading">
            <div>
              <span className="eyebrow eyebrow--muted">Recovery controls</span>
              <h2>Run the recovery workflow</h2>
            </div>
            <span className="section-heading__number">01 / 02</span>
          </div>
          <p className="section-copy">Load the repeatable demo portfolio, then score open cases and execute only approved actions.</p>
          <div className="operation-list">
            <div className="operation-row">
              <span className="operation-row__step">01</span>
              <div>
                <strong>Load demo portfolio</strong>
                <p>Load a repeatable synthetic dataset for demonstration.</p>
              </div>
              <button className="button button--subtle" disabled={busy !== null} onClick={() => void handleSeed()} type="button">
                {busy === "seed" ? <Icon className="spin" name="refresh" size={16} /> : <Icon name="play" size={16} />}
                {busy === "seed" ? "Loading…" : "Load portfolio"}
              </button>
            </div>
            <div className="operation-row">
              <span className="operation-row__step">02</span>
              <div>
                <strong>Process open cases</strong>
                <p>Score cases, apply policy, and execute approved actions.</p>
              </div>
              <button className="button button--primary" disabled={busy !== null} onClick={() => void handleBatch()} type="button">
                {busy === "batch" ? <Icon className="spin" name="refresh" size={16} /> : <Icon name="arrow-right" size={16} />}
                {busy === "batch" ? "Processing…" : "Run recovery"}
              </button>
            </div>
          </div>
        </section>

        <aside className="card attention-card">
          <div className="section-heading">
            <div>
              <span className="eyebrow eyebrow--muted">Needs attention</span>
              <h2>Open recovery cases</h2>
            </div>
          </div>
          {needsAttention.length ? <div className="attention-list">
            {needsAttention.map((caseRow) => (
              <Link className="attention-row" key={caseRow.id} to={`/cases/${caseRow.id}`}>
                <div><code>{caseRow.case_key}</code><small>{titleCase(caseRow.failure_class)}</small></div>
                <div><strong>{formatCurrency(caseRow.amount_paise)}</strong><span>{caseRow.latest_decision_action ? titleCase(caseRow.latest_decision_action) : "Review"}</span></div>
              </Link>
            ))}
          </div> : <p className="section-copy">No open recovery cases yet. Load the demo portfolio to begin.</p>}
          <Link className="text-link" to="/cases">View recovery queue <Icon name="arrow-right" size={15} /></Link>
        </aside>
      </div>

      <details className="workflow-disclosure">
        <summary>How decisions are processed</summary>
        <p>Score <Icon name="arrow-right" size={14} /> Propose <Icon name="arrow-right" size={14} /> Policy check <Icon name="arrow-right" size={14} /> Execute <Icon name="arrow-right" size={14} /> Record</p>
      </details>
    </section>
  );
}
