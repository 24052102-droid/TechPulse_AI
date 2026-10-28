import React, { useEffect } from "react";
import { TrendingBanner } from "../components/feed/TrendingBanner";
import { FeedList } from "../components/feed/FeedList";
import { useFeedStore } from "../store/useFeedStore";

export function DashboardPage() {
  const { items, loadFeed } = useFeedStore();

  useEffect(() => {
    loadFeed();
  }, [loadFeed]);

  return (
    <section className="flex-1 bg-surface-container-lowest px-8 py-6 min-h-screen">
      <div className="max-w-[960px] mx-auto">
        <TrendingBanner items={items} />
        <FeedList />
      </div>
    </section>
  );
}
