import React, { useState } from "react";
import AppLayout from "./components/layout/AppLayout";
import HomePage from "./pages/Home/HomePage";
import UploadPage from "./pages/Upload/UploadPage";

type Page = "home" | "upload";

const App: React.FC = () => {
  const [page, setPage] = useState<Page>("home");

  return (
    <AppLayout>
      <div className="mb-8 flex justify-end">
        <nav className="flex gap-1 bg-white/5 p-1 rounded-lg border border-white/10 backdrop-blur-sm">
          <button
            className={`px-4 py-1.5 rounded-md text-sm font-medium transition-all ${
              page === "home"
                ? "bg-action-primary text-white shadow-lg shadow-action-primary/20"
                : "text-text-secondary hover:text-text-neutral hover:bg-white/5"
            }`}
            onClick={() => setPage("home")}
          >
            Home
          </button>
          <button
            className={`px-4 py-1.5 rounded-md text-sm font-medium transition-all ${
              page === "upload"
                ? "bg-action-primary text-white shadow-lg shadow-action-primary/20"
                : "text-text-secondary hover:text-text-neutral hover:bg-white/5"
            }`}
            onClick={() => setPage("upload")}
          >
            Upload
          </button>
        </nav>
      </div>

      {page === "home" && <HomePage onNavigate={(p) => setPage(p)} />}
      {page === "upload" && <UploadPage />}
    </AppLayout>
  );
};

export default App;
