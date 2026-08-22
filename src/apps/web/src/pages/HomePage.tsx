import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getHealth, getMetrics, seedSynthetic, type MetricsSummary } from "../api";

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
        Expected-value recovery controller. Skeleton wires the empty paths — decide / execute / eval
        land next.
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
        <Link className="btn-link" to="/cases">
          View cases
        </Link>
      </div>
      {msg ? <p className="note">{msg}</p> : null}
    </section>
  );
}
