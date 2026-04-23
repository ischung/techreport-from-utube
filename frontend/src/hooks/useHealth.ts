import { type HealthData, fetchHealth } from "@/lib/api";
import { useEffect, useState } from "react";

export type HealthStatus = "up" | "degraded" | "down" | "loading" | "error";

export interface UseHealthResult {
  status: HealthStatus;
  data: HealthData | null;
  error: string | null;
}

export function useHealth(): UseHealthResult {
  const [status, setStatus] = useState<HealthStatus>("loading");
  const [data, setData] = useState<HealthData | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    fetchHealth()
      .then((payload) => {
        if (cancelled) return;
        setData(payload);
        setStatus(payload.status);
        setError(null);
      })
      .catch((err: unknown) => {
        if (cancelled) return;
        setStatus("error");
        setError(err instanceof Error ? err.message : "unknown error");
      });

    return () => {
      cancelled = true;
    };
  }, []);

  return { status, data, error };
}
