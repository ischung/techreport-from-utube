import { BrandMark } from "@/components/BrandMark";
import { StatusDot } from "@/components/StatusDot";
import { useHealth } from "@/hooks/useHealth";
import { FileText, Home, Settings } from "lucide-react";

interface NavItem {
  label: string;
  icon: React.ComponentType<{ size?: number; strokeWidth?: number; "aria-hidden"?: boolean }>;
  active: boolean;
  disabled?: boolean;
}

const NAV_ITEMS: NavItem[] = [
  { label: "Dashboard", icon: Home, active: true },
  { label: "History", icon: FileText, active: false, disabled: true },
  { label: "Settings", icon: Settings, active: false, disabled: true },
];

export function Sidebar() {
  const { status, data } = useHealth();

  return (
    <aside
      className="flex h-screen w-60 flex-col border-r border-border bg-bg-subtle"
      aria-label="Primary navigation"
    >
      <BrandMark />

      <nav className="flex-1 px-3 py-4">
        <ul className="space-y-1">
          {NAV_ITEMS.map((item) => (
            <li key={item.label}>
              <button
                type="button"
                disabled={item.disabled}
                aria-current={item.active ? "page" : undefined}
                className={
                  item.active
                    ? "flex w-full items-center gap-2 rounded-md bg-bg-card px-3 py-2 text-sm text-fg shadow-card"
                    : "flex w-full items-center gap-2 rounded-md px-3 py-2 text-sm text-fg-muted hover:bg-bg-card hover:text-fg disabled:cursor-not-allowed disabled:opacity-50"
                }
              >
                <item.icon size={16} strokeWidth={2} aria-hidden />
                <span>{item.label}</span>
                {item.disabled ? (
                  <span className="ml-auto font-mono text-[10px] text-fg-subtle">soon</span>
                ) : null}
              </button>
            </li>
          ))}
        </ul>
      </nav>

      <footer className="border-t border-border px-4 py-3 text-xs text-fg-muted">
        <div className="flex items-center justify-between">
          <StatusDot status={status} />
          <span className="font-mono text-fg-subtle">v{data?.version ?? "0.0.0"}</span>
        </div>
        {data ? (
          <p className="mt-1 font-mono text-[10px] text-fg-subtle">llm: {data.llmProvider}</p>
        ) : null}
      </footer>
    </aside>
  );
}
