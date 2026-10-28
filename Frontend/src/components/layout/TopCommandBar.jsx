import React, { useState } from "react";
import { useFeedStore } from "../../store/useFeedStore";

export function TopCommandBar() {
  const {
    searchQuery,
    setSearchQuery,
    loadFeed,
    toggleAssistant,
    activeRoute,
    setActiveRoute,
  } = useFeedStore();

  const [inputVal, setInputVal] = useState(searchQuery);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    setSearchQuery(inputVal);
    setActiveRoute("/");
    loadFeed();
  };

  const navItems = [
    { id: "/", label: "Feed" },
    { id: "/trends", label: "Trends" },
    { id: "/methodology", label: "Methodology" },
    { id: "/evaluation", label: "Evaluation" },
  ];

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-surface-container-lowest border-b border-surface-variant">
      <div className="h-14 max-w-[1440px] mx-auto px-margin flex items-center justify-between gap-space-lg">
        {/* Brand Identity */}
        <div
          onClick={() => setActiveRoute("/")}
          className="flex items-center gap-space-md shrink-0 cursor-pointer select-none"
        >
          <div className="w-7 h-7 bg-primary rounded-DEFAULT flex items-center justify-center">
            <span className="font-code-sm text-code-sm text-on-primary font-semibold">AT</span>
          </div>
          <span className="font-headline-sm text-headline-sm font-semibold tracking-tight text-on-surface">
            ATIP
          </span>
          <div className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full bg-surface-container-low border border-surface-variant">
            <span className="w-1.5 h-1.5 rounded-full bg-[#10B981]"></span>
            <span className="font-code-sm text-code-sm text-on-surface-variant">v1.0 · Live</span>
          </div>
        </div>

        {/* Search bar with ⌘K */}
        <div className="flex-1 max-w-[420px] mx-space-md hidden md:block">
          <form onSubmit={handleSearchSubmit} className="relative flex items-center w-full">
            <span className="material-symbols-outlined absolute left-space-sm text-[16px] text-outline pointer-events-none">
              search
            </span>
            <input
              type="text"
              value={inputVal}
              onChange={(e) => setInputVal(e.target.value)}
              placeholder="Search papers, repos, methods..."
              className="w-full h-8 pl-8 pr-12 bg-surface text-on-surface placeholder:text-outline border border-surface-variant rounded-lg font-body-sm text-body-sm focus:outline-none focus:border-primary transition-colors"
            />
            <kbd className="absolute right-space-sm px-1.5 py-0.5 bg-surface-container text-on-surface-variant border border-surface-variant rounded font-code-sm text-code-sm">
              ⌘K
            </kbd>
          </form>
        </div>

        {/* Right Nav & Utilities */}
        <div className="flex items-center gap-space-lg shrink-0">
          <nav className="hidden lg:flex items-center gap-space-xs p-0.5 bg-surface-container-low rounded-xl border border-surface-variant">
            {navItems.map((item) => {
              const isActive =
                activeRoute === item.id || (item.id === "/" && activeRoute.startsWith("/item/"));
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveRoute(item.id)}
                  type="button"
                  className={`px-space-md py-1 transition-colors ${
                    isActive
                      ? "bg-primary-container text-on-primary font-medium rounded-lg"
                      : "font-body-sm text-body-sm text-on-surface-variant hover:text-on-surface"
                  }`}
                >
                  {item.label}
                </button>
              );
            })}
          </nav>

          {/* Synced status */}
          <div
            onClick={() => setActiveRoute("/evaluation")}
            className="hidden sm:flex items-center gap-1.5 px-2 py-1 rounded-DEFAULT bg-surface-container-low border border-surface-variant cursor-pointer hover:border-outline-variant transition-colors"
            title="Telemetry synced with models"
          >
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-[#10B981] opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-[#10B981]"></span>
            </span>
            <span className="font-code-sm text-code-sm text-on-surface-variant">Synced 2h ago</span>
          </div>

          {/* Ask AI button */}
          <button
            onClick={toggleAssistant}
            type="button"
            className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-primary text-on-primary rounded-lg font-body-sm text-body-sm hover:bg-surface-tint transition-colors"
          >
            <span className="font-code-sm text-code-sm">✦</span>
            <span>Ask AI</span>
          </button>

          {/* Profile Avatar */}
          <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center shrink-0">
            <span className="material-symbols-outlined text-on-primary text-[18px]">person</span>
          </div>
        </div>
      </div>
    </header>
  );
}
