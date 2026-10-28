import React from "react";
import { TopCommandBar } from "./TopCommandBar";
import { SidebarDomainFilter } from "./SidebarDomainFilter";
import { AssistantDrawer } from "./AssistantDrawer";

export function AppShell({ children }) {
  return (
    <div className="bg-background font-body-md text-body-md text-on-surface antialiased min-h-screen flex flex-col justify-between">
      <div>
        <TopCommandBar />

        <main className="w-full pt-14 bg-background min-h-[calc(100vh-56px)]">
          <div className="max-w-[1440px] mx-auto px-margin py-space-lg">
            <div className="flex flex-col w-full">
              {/* Top Viewport Sub-header / System Status Strip */}
              <div className="w-full bg-surface-container-lowest border-b border-outline-variant/40 px-gutter-desktop py-space-sm flex items-center justify-between">
                <div className="flex items-center gap-space-md">
                  <span className="font-label-caps text-label-caps uppercase text-on-surface-variant tracking-wider flex items-center gap-1.5">
                    <span className="w-1.5 h-1.5 rounded-full bg-[#10B981]"></span>
                    Telemetry Pipeline: Active
                  </span>
                  <span className="font-code-sm text-code-sm text-outline-variant">/</span>
                  <span className="font-code-sm text-code-sm text-on-surface-variant">
                    Stream:{" "}
                    <span className="font-code-sm text-code-sm text-primary font-medium">
                      realtime.arxiv.gh.hn
                    </span>
                  </span>
                </div>
                <div className="hidden sm:flex items-center gap-space-lg font-code-sm text-code-sm text-secondary">
                  <span>
                    Buffer Latency: <span className="text-on-surface font-medium">18ms</span>
                  </span>
                  <span className="text-outline-variant">·</span>
                  <span>
                    Confidence Cutoff: <span className="text-on-surface font-medium">≥0.85</span>
                  </span>
                </div>
              </div>

              {/* 2-Column Desktop Grid Workspace */}
              <div className="w-full flex items-start">
                <SidebarDomainFilter />
                {children}
              </div>
            </div>
          </div>
        </main>
      </div>

      {/* Footer */}
      <footer className="w-full bg-surface-container-lowest border-t border-surface-variant py-space-md">
        <div className="max-w-[1440px] mx-auto px-margin flex flex-col sm:flex-row items-center justify-between gap-space-sm">
          <div className="flex items-center gap-space-md">
            <span className="font-label-caps text-label-caps uppercase text-outline tracking-wider">
              ATIP Autonomous Intelligence Core
            </span>
            <span className="font-code-sm text-code-sm text-outline">·</span>
            <span className="font-code-sm text-code-sm text-outline">1440px Grid Baseline</span>
          </div>
          <div className="font-code-sm text-code-sm text-on-surface-variant">
            © 2025 ATIP Systems. Precision Engineering.
          </div>
        </div>
      </footer>

      {/* Assistant Drawer */}
      <AssistantDrawer />
    </div>
  );
}
