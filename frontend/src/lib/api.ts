import axios from "axios";

export interface HealthData {
  status: "up" | "degraded" | "down";
  llmProvider: string;
  version: string;
}

export interface HealthResponse {
  ok: boolean;
  data: HealthData;
}

const client = axios.create({
  baseURL: "/api",
  timeout: 3000,
});

export async function fetchHealth(): Promise<HealthData> {
  const response = await client.get<HealthResponse>("/health");
  return response.data.data;
}
