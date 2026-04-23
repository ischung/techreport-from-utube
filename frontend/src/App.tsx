export default function App() {
  return (
    <main className="min-h-screen bg-bg text-fg font-sans flex items-center justify-center">
      <div className="max-w-xl text-center px-6">
        <h1 className="text-3xl font-semibold mb-3">TechReport from YouTube</h1>
        <p className="text-fg-muted mb-6">
          Monorepo scaffolding complete. The dashboard UI (CI-7 Walking Skeleton) will render here
          once{" "}
          <code className="font-mono text-sm bg-bg-card px-1.5 py-0.5 rounded">/api/health</code> is
          implemented.
        </p>
        <p className="text-xs font-mono text-fg-subtle">
          feature/issue-1-monorepo-scaffolding · v0.1.0-pre
        </p>
      </div>
    </main>
  );
}
