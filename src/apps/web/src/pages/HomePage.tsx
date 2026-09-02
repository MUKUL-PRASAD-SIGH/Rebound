import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { batchDecide, getHealth, getMetrics, seedSynthetic, type MetricsSummary } from "../api";
import { Icon, StatusPill } from "../ui";

export default function HomePage() {
  const [health, setHealth] = useState<string>("Checking API…");
  const [metrics, setMetrics] = useState<MetricsSummary | null>(null);
  const [message, setMessage] = useState<string>("");
  const [busy, setBusy] = useState<"batch" | "seed" | null>(null);

  const apiReady = health.startsWith("ok");

  async function refresh() {
    try {
      const [apiHealth, summary] = await Promise.all([getHealth(), getMetrics()]);
      setHealth(`${apiHealth.status} · v${apiHealth.version}`);
      setMetrics(summary);
    } catch {
      setHealth("Offline — start API on :8000");
      setMetrics(null);
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

  return (
    <section className="page-stack">
      <header className="hero">
        <div className="hero__copy">
          <span className="eyebrow"><span className="eyebrow__dot" /> Recovery command center</span>
          <h1>Make every recovery<br /><em>decision count.</em></h1>
          <p>
            Rebound evaluates each failed payment for expected value, applies deterministic policy
            gates, and makes the outcome auditable from one quiet operations console.
          </p>
          <div className="hero__actions">
            <Link className="button button--primary" to="/cases">
              Open recovery queue <Icon name="arrow-right" size={17} />
            </Link>
            <Link className="button button--ghost" to="/eval">
              <Icon name="chart" size={17} /> View evaluation
            </Link>
          </div>
        </div>
        <div className="hero__signal">
          <div className="hero__signal-head">
            <span>CONTROL STATUS</span>
            <StatusPill tone={apiReady ? "good" : "warn"}>{apiReady ? "LIVE" : "OFFLINE"}</StatusPill>
          </div>
          <div className="hero__signal-value">{apiReady ? "Ready" : "Waiting"}</div>
          <p>{health}</p>
          <div className="hero__signal-line"><span style={{ width: apiReady ? "76%" : "22%" }} /></div>
          <small>Policy gate · audit log · safe execution</small>
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
          <span className="metric-card__label">Recovery queue</span>
          <strong>{metrics?.cases_open ?? "—"}</strong>
          <p>cases awaiting a decision</p>
        </article>
        <article className="metric-card">
          <span className="metric-card__icon"><Icon name="activity" size={19} /></span>
          <span className="metric-card__label">Recovered</span>
          <strong>{metrics?.cases_recovered ?? "—"}</strong>
          <p>outcomes recorded to date</p>
        </article>
        <article className="metric-card">
          <span className="metric-card__icon"><Icon name="shield" size={19} /></span>
          <span className="metric-card__label">Stopped safely</span>
          <strong>{metrics?.cases_stopped ?? "—"}</strong>
          <p>cases protected by policy</p>
        </article>
        <article className="metric-card">
          <span className="metric-card__icon"><Icon name="chart" size={19} /></span>
          <span className="metric-card__label">Eval runs</span>
          <strong>{metrics?.eval_runs ?? "—"}</strong>
          <p>simulated baseline comparisons</p>
        </article>
      </div>

      <div className="overview-grid">
        <section className="card card--operations">
          <div className="section-heading">
            <div>
              <span className="eyebrow eyebrow--muted">Operations</span>
              <h2>Run the recovery loop</h2>
            </div>
            <span className="section-heading__number">01 / 02</span>
          </div>
          <p className="section-copy">Start with a clean synthetic batch, then let the policy-gated controller process only open cases.</p>
          <div className="operation-list">
            <div className="operation-row">
              <span className="operation-row__step">01</span>
              <div>
                <strong>Load a sample portfolio</strong>
                <p>Seed the 60-case scenario set for a repeatable demo.</p>
              </div>
              <button className="button button--subtle" disabled={busy !== null} onClick={() => void handleSeed()} type="button">
                {busy === "seed" ? <Icon className="spin" name="refresh" size={16} /> : <Icon name="play" size={16} />}
                {busy === "seed" ? "Seeding…" : "Seed batch"}
              </button>
            </div>
            <div className="operation-row">
              <span className="operation-row__step">02</span>
              <div>
                <strong>Decide and execute open cases</strong>
                <p>Evaluate value, apply guardrails, and log every safe action.</p>
              </div>
              <button className="button button--primary" disabled={busy !== null} onClick={() => void handleBatch()} type="button">
                {busy === "batch" ? <Icon className="spin" name="refresh" size={16} /> : <Icon name="arrow-right" size={16} />}
                {busy === "batch" ? "Processing…" : "Run queue"}
              </button>
            </div>
          </div>
        </section>

        <aside className="card workflow-card">
          <div className="section-heading">
            <div>
              <span className="eyebrow eyebrow--muted">Guardrailed by design</span>
              <h2>Decision path</h2>
            </div>
          </div>
          <div className="workflow-list">
            <div><span className="workflow-list__icon"><Icon name="activity" size={16} /></span><span>Score recovery probability <small>Expected value</small></span></div>
            <div><span className="workflow-list__icon"><Icon name="spark" size={16} /></span><span>Propose a bounded action <small>Rules + model</small></span></div>
            <div><span className="workflow-list__icon"><Icon name="shield" size={16} /></span><span>Enforce policy limits <small>Stop / escalate / allow</small></span></div>
            <div><span className="workflow-list__icon"><Icon name="audit" size={16} /></span><span>Record every outcome <small>Append-only audit</small></span></div>
          </div>
          <Link className="text-link" to="/audit">Inspect the audit trail <Icon name="arrow-right" size={15} /></Link>
        </aside>
      </div>
    </section>
  );
}
