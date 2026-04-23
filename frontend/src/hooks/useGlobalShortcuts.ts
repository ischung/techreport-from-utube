import { useEffect } from "react";

/**
 * Global "/" shortcut — focus the keyword input from anywhere.
 * Ignores the keystroke when the user is already typing in a form field
 * so it doesn't hijack in-progress edits.
 */
export function useGlobalShortcuts() {
  useEffect(() => {
    function onKeydown(event: KeyboardEvent) {
      if (event.key !== "/") return;

      const target = event.target as HTMLElement | null;
      if (target) {
        const tag = target.tagName;
        if (tag === "INPUT" || tag === "TEXTAREA" || target.isContentEditable) {
          return;
        }
      }

      const input = document.querySelector<HTMLInputElement>('[data-testid="keyword-input"]');
      if (input) {
        event.preventDefault();
        input.focus();
        input.select();
      }
    }

    window.addEventListener("keydown", onKeydown);
    return () => window.removeEventListener("keydown", onKeydown);
  }, []);
}
