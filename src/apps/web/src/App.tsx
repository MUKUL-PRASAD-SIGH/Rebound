import { Link, Navigate, NavLink, Route, Routes } from "react-router-dom";
import AuditPage from "./pages/AuditPage";
import CaseDetailPage from "./pages/CaseDetailPage";
import CasesPage from "./pages/CasesPage";
import EvalPage from "./pages/EvalPage";
import HomePage from "./pages/HomePage";
import { Icon, type IconName } from "./ui";

const navigation: { label: string; to: string; icon: IconName }[] = [
  { label: "Overview", to: "/", icon: "dashboard" },
  { label: "Recovery queue", to: "/cases", icon: "cases" },
  { label: "Evaluation", to: "/eval", icon: "chart" },
  { label: "Audit trail", to: "/audit", icon: "audit" },
];

export default function App() {
  return (
    <div className="app-frame">
      <aside className="sidebar">
        <Link aria-label="Rebound overview" className="brand" to="/">
          <span className="brand__mark"><Icon name="spark" size={19} /></span>
          <span>
            <strong>Rebound</strong>
            <small>Recovery operations</small>
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
            <div className="system-card__line"><span className="live-dot" /> System ready</div>
            <p>All decisions are policy-gated and test-mode safe.</p>
          </div>
          <span className="environment-label"><Icon name="shield" size={14} /> Test-mode workspace</span>
        </div>
      </aside>

      <div className="app-body">
        <header className="topbar">
          <div className="topbar__context">
            <span className="topbar__eyebrow">Revenue recovery controller</span>
            <span className="topbar__divider" />
            <span>Policy-first operations</span>
          </div>
          <div className="topbar__status"><span className="live-dot" /> API connected when running</div>
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
