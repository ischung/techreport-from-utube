interface DashboardHeaderProps {
  title: string;
  subtitle?: string;
}

export function DashboardHeader({ title, subtitle }: DashboardHeaderProps) {
  return (
    <header className="flex items-baseline justify-between border-b border-border bg-bg-subtle px-8 py-5">
      <div>
        <h1 className="text-xl font-semibold tracking-tight">{title}</h1>
        {subtitle ? <p className="mt-1 text-sm text-fg-muted">{subtitle}</p> : null}
      </div>
      <span className="font-mono text-[11px] text-fg-subtle">
        {new Date().toISOString().slice(0, 10)}
      </span>
    </header>
  );
}
