import type { AnalysisReport, ApiError, VideoSearchResult } from "@/lib/types";
import axios, { type AxiosError } from "axios";

export interface HealthData {
  status: "up" | "degraded" | "down";
  llmProvider: string;
  version: string;
  tokensInput?: number;
  tokensOutput?: number;
  tokensCacheRead?: number;
  estimatedCostUsd?: number;
}

interface Envelope<T> {
  ok: boolean;
  data: T;
}

interface ErrorEnvelope {
  detail: ApiError;
}

const client = axios.create({
  baseURL: "/api",
  timeout: 10_000,
});

export async function fetchHealth(): Promise<HealthData> {
  const response = await client.get<Envelope<HealthData>>("/health");
  return response.data.data;
}

export async function searchVideos(keyword: string): Promise<VideoSearchResult[]> {
  try {
    const response = await client.post<Envelope<{ videos: VideoSearchResult[] }>>("/search", {
      keyword,
    });
    return response.data.data.videos;
  } catch (err) {
    const axiosErr = err as AxiosError<ErrorEnvelope>;
    if (axiosErr.response?.data?.detail) {
      const { code, message, retryable } = axiosErr.response.data.detail;
      throw Object.assign(new Error(message), { code, retryable });
    }
    throw err;
  }
}

export async function analyzeVideo(selection: {
  videoId: string;
  title: string;
  url: string;
  publishedAt?: string;
}): Promise<AnalysisReport> {
  const analyzeClient = axios.create({ baseURL: "/api", timeout: 180_000 });
  try {
    const response = await analyzeClient.post<Envelope<AnalysisReport>>("/analyze", selection);
    return response.data.data;
  } catch (err) {
    const axiosErr = err as AxiosError<ErrorEnvelope>;
    if (axiosErr.response?.data?.detail) {
      const { code, message, retryable } = axiosErr.response.data.detail;
      throw Object.assign(new Error(message), { code, retryable });
    }
    throw err;
  }
}
