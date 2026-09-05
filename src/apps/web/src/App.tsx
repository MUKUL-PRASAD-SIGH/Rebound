import { FormEvent, useState } from "react";
import { Link, Navigate, NavLink, Route, Routes } from "react-router-dom";
import AuditPage from "./pages/AuditPage";
import CaseDetailPage from "./pages/CaseDetailPage";
import CasesPage from "./pages/CasesPage";
import EvalPage from "./pages/EvalPage";
import HomePage from "./pages/HomePage";
import { clearOperatorToken, getMetrics, getOperatorToken, setOperatorToken } from "./api";
import { Icon, type IconName } from "./ui";

const navigation: { label: string; to: string; icon: IconName }[] = [
  { label: "Operations", to: "/", icon: "dashboard" },
  { label: "Recovery", to: "/cases", icon: "cases" },
  { label: "Insights", to: "/eval", icon: "chart" },
  { label: "Activity", to: "/audit", icon: "audit" },
];

export default function App() {
  const [authorised, setAuthorised] = useState(Boolean(getOperatorToken()));
  const [token, setToken] = useState("");
  const [accessError, setAccessError] = useState("");
  const [checkingAccess, setCheckingAccess] = useState(false);

  async function unlock(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const candidate = token.trim();
    if (!candidate) return;
    setCheckingAccess(true);
    setAccessError("");
    setOperatorToken(candidate);
    try {
      await getMetrics();
      setAuthorised(true);
      setToken("");
    } catch {
      clearOperatorToken();
      setAccessError("Access could not be verified. Check REBOUND_API_TOKEN and try again.");
    } finally {
      setCheckingAccess(false);
    }
  }

  if (!authorised) {
    return (
      <main className="access-gate">
        <section className="access-gate__panel">
          <div className="access-gate__brand"><span className="brand__mark"><Icon name="spark" size={21} /></span><strong>Rebound</strong></div>
          <span className="eyebrow"><Icon name="shield" size={14} /> Private operator workspace</span>
          <h1>Make every payment failure a comeback.</h1>
          <p>Enter the local operator token to access recovery decisions, audit evidence, and connected payment controls.</p>
          <form onSubmit={(event) => void unlock(event)}>
            <label htmlFor="operator-token">Operator access token</label>
            <input autoComplete="current-password" id="operator-token" onChange={(event) => setToken(event.target.value)} placeholder="Stored in your local .env" type="password" value={token} />
            {accessError ? <p className="access-gate__error">{accessError}</p> : null}
            <button className="button button--primary" disabled={checkingAccess || !token.trim()} type="submit"><Icon name={checkingAccess ? "refresh" : "shield"} className={checkingAccess ? "spin" : undefined} size={16} />{checkingAccess ? "Verifying…" : "Unlock workspace"}</button>
          </form>
          <small>Your token stays in this browser session and is never displayed by Rebound.</small>
        </section>
      </main>
    );
  }

  return (
    <div className="app-frame">
      <aside className="sidebar">
        <Link aria-label="Rebound overview" className="brand" to="/">
          <span className="brand__mark"><Icon name="spark" size={19} /></span>
          <span>
            <strong>Rebound</strong>
            <small>Make every failure a comeback</small>
          </span>
        </Link>

        <nav aria-label="Primary navigation" className="nav-list">
          {navigation.map((item) => (
            <NavLink
              className={({ isActive }) => `nav-link${isActive ? " nav-link--active" : ""}`}
              key={item.to}
              to={item.to}
            >
              <Icon name={item.icon} size={18} />
              <span>{item.label}</span>
            </NavLink>
          ))}
        </nav>

        <div className="sidebar__footer">
          <div className="system-card">
            <div className="system-card__line"><span className="live-dot" /> System operational</div>
            <p>Policy-controlled · Audit enabled</p>
          </div>
        </div>
      </aside>

      <div className="app-body">
        <header className="topbar">
          <div className="topbar__context">
            <span className="topbar__eyebrow">Recovery operations</span>
            <span className="topbar__divider" />
            <span>Policy mvp-v1</span>
          </div>
          <button className="topbar__lock" onClick={() => { clearOperatorToken(); setAuthorised(false); }} type="button"><Icon name="shield" size={14} /> Lock workspace</button>
        </header>
        <main className="content">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/cases" element={<CasesPage />} />
            <Route path="/cases/:id" element={<CaseDetailPage />} />
            <Route path="/eval" element={<EvalPage />} />
            <Route path="/audit" element={<AuditPage />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
      </div>
    </div>
  );
}
