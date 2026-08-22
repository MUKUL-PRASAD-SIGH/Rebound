import { Link, Navigate, Route, Routes } from "react-router-dom";
import AuditPage from "./pages/AuditPage";
import CaseDetailPage from "./pages/CaseDetailPage";
import CasesPage from "./pages/CasesPage";
import EvalPage from "./pages/EvalPage";
import HomePage from "./pages/HomePage";

export default function App() {
  return (
    <div className="shell">
      <header className="top">
        <Link to="/" className="brand">
          Rebound
        </Link>
        <nav>
          <Link to="/cases">Cases</Link>
          <Link to="/eval">Eval</Link>
          <Link to="/audit">Audit</Link>
        </nav>
        <span className="badge">Day 03 skeleton</span>
      </header>
      <main>
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
  );
}
