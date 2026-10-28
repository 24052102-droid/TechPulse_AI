const RAW_URL = import.meta.env.VITE_API_BASE_URL || "/api";
const BASE_URL = RAW_URL.replace(/\/+$/, "");

async function request(endpoint, options = {}) {
  const url = `${BASE_URL}${endpoint}`;
  try {
    const res = await fetch(url, {
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
      ...options,
    });
    if (!res.ok) {
      const errText = await res.text();
      throw new Error(`API Error ${res.status}: ${errText}`);
    }
    return await res.json();
  } catch (err) {
    console.error(`Request to ${url} failed:`, err);
    throw err;
  }
}

export const api = {
  getFeed: ({ domains = [], source = "all", sort = "impact_score", page = 1, limit = 20 } = {}) => {
    const params = new URLSearchParams();
    if (domains && domains.length > 0) params.append("domain", domains.join(","));
    if (source && source !== "all") params.append("source", source);
    if (sort) params.append("sort", sort);
    params.append("page", page.toString());
    params.append("limit", limit.toString());
    return request(`/feed?${params.toString()}`);
  },

  getItem: (id) => request(`/item/${id}`),

  getInsights: (id) => request(`/item/${id}/insights`),

  getTrends: (window = "7d") => request(`/trends?window=${window}`),

  search: ({ q, domain = null, sort = "impact_score", page = 1 } = {}) => {
    const params = new URLSearchParams();
    params.append("q", q);
    if (domain) params.append("domain", domain);
    if (sort) params.append("sort", sort);
    params.append("page", page.toString());
    return request(`/search?${params.toString()}`);
  },

  getDomains: () => request("/domains"),

  getHealth: () => request("/health"),

  getEvaluation: () => request("/evaluation"),

  triggerRefresh: (maxResults = 10) =>
    request(`/admin/refresh?max_results=${maxResults}`, { method: "POST" }),
};
