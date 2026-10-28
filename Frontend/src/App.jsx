import React from "react";
import { AppShell } from "./components/layout/AppShell";
import { DashboardPage } from "./pages/DashboardPage";
import { TrendsPage } from "./pages/TrendsPage";
import { ItemDetailPage } from "./pages/ItemDetailPage";
import { EvaluationPage } from "./pages/EvaluationPage";
import { useFeedStore } from "./store/useFeedStore";

export default function App() {
  const { activeRoute, selectedItemId } = useFeedStore();

  const renderContent = () => {
    if (activeRoute === "/trends") {
      return <TrendsPage />;
    }
    if (activeRoute.startsWith("/item/")) {
      return <ItemDetailPage itemId={selectedItemId} />;
    }
    if (activeRoute === "/evaluation") {
      return <EvaluationPage />;
    }
    return <DashboardPage />;
  };

  return <AppShell>{renderContent()}</AppShell>;
}
