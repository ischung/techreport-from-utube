import { Youtube } from "lucide-react";

export function BrandMark() {
  return (
    <div className="flex items-center gap-2 px-4 py-4 border-b border-border">
      <span className="grid h-8 w-8 place-items-center rounded-md bg-error/10 text-error">
        <Youtube size={18} strokeWidth={2.25} aria-hidden="true" />
      </span>
      <div className="flex flex-col leading-tight">
        <span className="font-semibold text-sm text-fg">TechReport</span>
        <span className="font-mono text-[10px] text-fg-subtle">from YouTube</span>
      </div>
    </div>
  );
}
