import React from "react";
import { BookOpen, GitBranch, MessageSquare, ExternalLink } from "lucide-react";

export function SourceBadge({ source, sourceId, url }) {
  if (source === "arxiv") {
    return (
      <a
        href={url}
        target="_blank"
        rel="noopener noreferrer"
        className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-mono font-medium bg-rose-500/10 text-rose-400 border border-rose-500/20 hover:bg-rose-500/20 transition-colors"
        title={`View arXiv paper: ${sourceId}`}
      >
        <BookOpen className="w-3 h-3" />
        <span>arXiv:{sourceId}</span>
        <ExternalLink className="w-2.5 h-2.5 opacity-60" />
      </a>
    );
  }

  if (source === "github") {
    return (
      <a
        href={url}
        target="_blank"
        rel="noopener noreferrer"
        className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-mono font-medium bg-slate-500/10 text-slate-300 border border-slate-500/20 hover:bg-slate-500/20 transition-colors"
        title={`View GitHub Repository: ${sourceId}`}
      >
        <GitBranch className="w-3 h-3" />
        <span>{sourceId}</span>
        <ExternalLink className="w-2.5 h-2.5 opacity-60" />
      </a>
    );
  }

  return (
    <a
      href={url}
      target="_blank"
      rel="noopener noreferrer"
      className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-mono font-medium bg-amber-500/10 text-amber-400 border border-amber-500/20 hover:bg-amber-500/20 transition-colors"
      title={`Hacker News ID: ${sourceId}`}
    >
      <MessageSquare className="w-3 h-3" />
      <span>HN #{sourceId}</span>
      <ExternalLink className="w-2.5 h-2.5 opacity-60" />
    </a>
  );
}
