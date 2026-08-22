import { useParams } from "react-router-dom";

export default function CaseDetailPage() {
  const { id } = useParams();
  return (
    <section className="panel">
      <h1>Case detail</h1>
      <p className="lede">
        Placeholder for explainability (proposal → gate → action). Case id: <code>{id}</code>
      </p>
      <p className="note">Wire decide/execute UI on Day 04–05.</p>
    </section>
  );
}
