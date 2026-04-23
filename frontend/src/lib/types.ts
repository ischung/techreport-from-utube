export interface VideoSearchResult {
  videoId: string;
  title: string;
  url: string;
  publishedAt: string;
  channelTitle: string;
}

export type Phase = "input" | "list" | "analyzing" | "result";

export interface ApiError {
  code: string;
  message: string;
  retryable: boolean;
}
