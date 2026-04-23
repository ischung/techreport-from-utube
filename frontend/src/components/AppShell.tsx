import { DashboardHeader } from "@/components/DashboardHeader";
import { Sidebar } from "@/components/Sidebar";

interface AppShellProps {
  children?: React.ReactNode;
}

export function AppShell({ children }: AppShellProps) {
  return (
    <div className="flex min-h-screen bg-bg text-fg">
      <Sidebar />
      <main className="flex flex-1 flex-col" aria-label="Main content">
        <DashboardHeader
          title="TechReport from YouTube"
          subtitle="Walking Skeleton — /api/health 가 녹색이어야 기능 슬라이스가 시작됩니다."
        />
        <div className="flex-1 overflow-auto px-8 py-8">{children}</div>
      </main>
    </div>
  );
}
