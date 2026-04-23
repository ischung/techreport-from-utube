import type { AnalysisReport, ApiError, Phase, VideoSearchResult } from "@/lib/types";
import { create } from "zustand";

export interface StatusLogEntry {
  id: number;
  message: string;
  level: "info" | "success" | "error";
}

interface AppState {
  phase: Phase;
  keyword: string;
  videos: VideoSearchResult[];
  selectedVideoId: string | null;
  report: AnalysisReport | null;
  isLoading: boolean;
  error: ApiError | null;
  statusLog: StatusLogEntry[];

  setKeyword: (keyword: string) => void;
  setVideos: (videos: VideoSearchResult[]) => void;
  selectVideo: (videoId: string) => void;
  setReport: (report: AnalysisReport) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: ApiError | null) => void;
  goTo: (phase: Phase) => void;
  reset: () => void;
  backToList: () => void;
  pushLog: (message: string, level?: StatusLogEntry["level"]) => void;
  clearLog: () => void;
}

const INITIAL = {
  phase: "input" as Phase,
  keyword: "",
  videos: [],
  selectedVideoId: null,
  report: null,
  isLoading: false,
  error: null,
  statusLog: [] as StatusLogEntry[],
};

let logCounter = 0;

export const useAppStore = create<AppState>((set, get) => ({
  ...INITIAL,
  setKeyword: (keyword) => set({ keyword }),
  setVideos: (videos) => set({ videos, phase: "list" }),
  selectVideo: (videoId) => set({ selectedVideoId: videoId, phase: "analyzing", statusLog: [] }),
  setReport: (report) => set({ report, phase: "result" }),
  setLoading: (isLoading) => set({ isLoading }),
  setError: (error) => set({ error }),
  goTo: (phase) => set({ phase }),
  reset: () => set({ ...INITIAL, statusLog: [] }),
  backToList: () =>
    set({
      phase: get().videos.length > 0 ? "list" : "input",
      selectedVideoId: null,
      report: null,
    }),
  pushLog: (message, level = "info") =>
    set((state) => ({
      statusLog: [...state.statusLog, { id: ++logCounter, message, level }],
    })),
  clearLog: () => set({ statusLog: [] }),
}));
