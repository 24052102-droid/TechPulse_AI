import { create } from "zustand";
import { api } from "../api/client";

export const useFeedStore = create((set, get) => ({
  // Navigation & View State
  activeRoute: "/",
  selectedItemId: null,
  isAssistantOpen: false,

  // Feed State
  items: [],
  total: 0,
  page: 1,
  pages: 1,
  hasNext: false,
  isLoading: false,
  feedError: null,

  // Filter & Sort State
  selectedDomains: [],
  selectedSource: "all",
  sortBy: "impact_score",
  searchQuery: "",

  // Metadata Cache
  domainsData: [],
  healthData: null,

  // Actions
  setActiveRoute: (route, itemId = null) => set({ activeRoute: route, selectedItemId: itemId }),
  toggleAssistant: () => set((state) => ({ isAssistantOpen: !state.isAssistantOpen })),

  setSelectedSource: (source) => {
    set({ selectedSource: source, page: 1 });
    get().loadFeed();
  },

  setSortBy: (sort) => {
    set({ sortBy: sort, page: 1 });
    get().loadFeed();
  },

  setPage: (page) => {
    set({ page });
    get().loadFeed();
  },

  toggleDomain: (domain) => {
    const current = get().selectedDomains;
    const next = current.includes(domain)
      ? current.filter((d) => d !== domain)
      : [...current, domain];
    set({ selectedDomains: next, page: 1 });
    get().loadFeed();
  },

  clearDomains: () => {
    set({ selectedDomains: [], page: 1 });
    get().loadFeed();
  },

  setSearchQuery: (query) => {
    set({ searchQuery: query });
  },

  loadDomains: async () => {
    try {
      const data = await api.getDomains();
      set({ domainsData: data });
    } catch (err) {
      console.error("Failed to load domains:", err);
    }
  },

  loadHealth: async () => {
    try {
      const data = await api.getHealth();
      set({ healthData: data });
    } catch (err) {
      console.error("Failed to load health:", err);
    }
  },

  loadFeed: async () => {
    const { selectedDomains, selectedSource, sortBy, page, searchQuery } = get();
    set({ isLoading: true, feedError: null });
    try {
      if (searchQuery.trim().length > 1) {
        const res = await api.search({
          q: searchQuery.trim(),
          domain: selectedDomains.length === 1 ? selectedDomains[0] : null,
          sort: sortBy,
          page,
        });
        set({
          items: res.results || [],
          total: res.total || 0,
          pages: Math.max(1, Math.ceil((res.total || 0) / 20)),
          hasNext: false,
          isLoading: false,
          feedError: null,
        });
      } else {
        const res = await api.getFeed({
          domains: selectedDomains,
          source: selectedSource,
          sort: sortBy,
          page,
          limit: 20,
        });
        set({
          items: res.items || [],
          total: res.total || 0,
          page: res.page || 1,
          pages: res.pages || 1,
          hasNext: res.has_next || false,
          isLoading: false,
          feedError: null,
        });
      }
    } catch (err) {
      console.error("Failed to load feed:", err);
      set({ isLoading: false, feedError: err.message || "Failed to load feed from backend" });
    }
  },
}));
