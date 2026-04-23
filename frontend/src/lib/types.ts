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

export interface ReportSection {
  overview: string;
  coreConcepts: string[];
  detailedContent: string;
  lectureTips: string;
  references: string[];
}

export interface AnalysisReport {
  videoId: string;
  title: string;
  sourceUrl: string;
  publishedAt: string;
  generatedAt: string;
  llmProvider: string;
  sections: ReportSection;
  markdown: string;
  savedPath: string;
}
