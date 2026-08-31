import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { batchDecide, getHealth, getMetrics, seedSynthetic, type MetricsSummary } from "../api";

export default function HomePage() {
  const [health, setHealth] = useState<string>("checking…");
  const [metrics, setMetrics] = useState<MetricsSummary | null>(null);
  const [msg, setMsg] = useState<string>("");

  async function refresh() {
    try {
      const h = await getHealth();
      setHealth(`${h.status} · v${h.version}`);
      setMetrics(await getMetrics());
    } catch {
      setHealth("API offline — start uvicorn on :8000");
      setMetrics(null);
    }
  }

  useEffect(() => {
    void refresh();
  }, []);

  return (
    <section className="panel">
      <h1>Ops console</h1>
      <p className="lede">
        Expected-value recovery controller: seed a batch, decide open cases, then measure{" "}
        <code>lift_value</code> vs Baseline A.
      </p>
      <dl className="meta">
        <div>
          <dt>API</dt>
          <dd>{health}</dd>
        </div>
        <div>
          <dt>Cases</dt>
          <dd>{metrics ? metrics.cases_total : "—"}</dd>
        </div>
        <div>
          <dt>Open</dt>
          <dd>{metrics ? metrics.cases_open : "—"}</dd>
        </div>
        <div>
          <dt>Recovered</dt>
          <dd>{metrics ? metrics.cases_recovered : "—"}</dd>
        </div>
      </dl>
      <div className="row">
        <button
          type="button"
          onClick={async () => {
            try {
              const r = await seedSynthetic();
              setMsg(`Seeded ${r.inserted}, skipped ${r.skipped}`);
              await refresh();
            } catch (e) {
              setMsg(String(e));
            }
          }}
        >
          Seed sample batch
        </button>
        <button
          type="button"
          onClick={async () => {
            try {
              const data = await batchDecide(true);
              setMsg(`Batch decided ${data.count} open cases`);
              await refresh();
            } catch (e) {
              setMsg(String(e));
            }
          }}
        >
          Batch decide+execute open
        </button>
        <Link className="btn-link" to="/cases">
          View cases
        </Link>
        <Link className="btn-link" to="/eval">
          Eval
        </Link>
      </div>
      {msg ? <p className="note">{msg}</p> : null}
    </section>
  );
}
