import type { AnalysisReport, ApiError, Phase, VideoSearchResult } from "@/lib/types";
import { create } from "zustand";

interface AppState {
  phase: Phase;
  keyword: string;
  videos: VideoSearchResult[];
  selectedVideoId: string | null;
  report: AnalysisReport | null;
  isLoading: boolean;
  error: ApiError | null;

  setKeyword: (keyword: string) => void;
  setVideos: (videos: VideoSearchResult[]) => void;
  selectVideo: (videoId: string) => void;
  setReport: (report: AnalysisReport) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: ApiError | null) => void;
  goTo: (phase: Phase) => void;
  reset: () => void;
  backToList: () => void;
}

const INITIAL = {
  phase: "input" as Phase,
  keyword: "",
  videos: [],
  selectedVideoId: null,
  report: null,
  isLoading: false,
  error: null,
};

export const useAppStore = create<AppState>((set, get) => ({
  ...INITIAL,
  setKeyword: (keyword) => set({ keyword }),
  setVideos: (videos) => set({ videos, phase: "list" }),
  selectVideo: (videoId) => set({ selectedVideoId: videoId, phase: "analyzing" }),
  setReport: (report) => set({ report, phase: "result" }),
  setLoading: (isLoading) => set({ isLoading }),
  setError: (error) => set({ error }),
  goTo: (phase) => set({ phase }),
  reset: () => set(INITIAL),
  backToList: () =>
    set({ phase: get().videos.length > 0 ? "list" : "input", selectedVideoId: null, report: null }),
}));
