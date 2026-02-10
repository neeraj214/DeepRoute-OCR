import React, { useState } from "react";
import { Button } from "./ui/Button";
import { Card } from "./ui/Card";
import { FileText, Code, File as FileIcon, Download, Copy, Check } from "lucide-react";

interface OCRResult {
  text: string;
  structured: any;
  confidence: number;
  language: string;
  pdf_url?: string;
  metadata?: {
    processing_time_ms: number;
  };
}

interface ResultsDisplayProps {
  result: OCRResult;
}

export const ResultsDisplay: React.FC<ResultsDisplayProps> = ({ result }) => {
  const [activeTab, setActiveTab] = useState<"text" | "json" | "pdf">("text");
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    const content = activeTab === "json" 
      ? JSON.stringify(result.structured, null, 2) 
      : result.text;
    navigator.clipboard.writeText(content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = (format: "txt" | "json") => {
    const content = format === "json" 
      ? JSON.stringify(result.structured, null, 2) 
      : result.text;
    const blob = new Blob([content], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `ocr-result.${format}`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-4">
      {result.routing_info && (
          <div className="flex gap-4 p-3 bg-white/5 rounded-lg border border-white/10 text-sm">
              <div className="flex items-center gap-2">
                  <span className="text-text-secondary">Document Type:</span>
                  <span className="font-semibold text-ai-highlight2">{result.routing_info.doc_type}</span>
              </div>
              <div className="flex items-center gap-2">
                  <span className="text-text-secondary">Engine:</span>
                  <span className="font-semibold text-ai-highlight">{result.routing_info.ocr_engine}</span>
              </div>
              {result.routing_info.fallback_used && (
                  <span className="text-yellow-500 text-xs px-2 py-0.5 bg-yellow-500/10 rounded">Fallback Used</span>
              )}
          </div>
      )}

      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div className="flex p-1 bg-white/5 rounded-lg border border-white/10">
          <TabButton 
            active={activeTab === "text"} 
            onClick={() => setActiveTab("text")} 
            icon={<FileText className="w-4 h-4" />}
            label="Text"
          />
          <TabButton 
            active={activeTab === "json"} 
            onClick={() => setActiveTab("json")} 
            icon={<Code className="w-4 h-4" />}
            label="JSON"
          />
          {result.pdf_url && (
            <TabButton 
              active={activeTab === "pdf"} 
              onClick={() => setActiveTab("pdf")} 
              icon={<FileIcon className="w-4 h-4" />}
              label="PDF"
            />
          )}
        </div>

        <div className="flex gap-2">
          <Button variant="secondary" size="sm" onClick={handleCopy}>
            {copied ? <Check className="w-4 h-4 mr-2 text-ai-highlight2" /> : <Copy className="w-4 h-4 mr-2" />}
            {copied ? "Copied" : "Copy"}
          </Button>
          <Button variant="outline" size="sm" onClick={() => handleDownload("txt")}>
            <Download className="w-4 h-4 mr-2" />
            TXT
          </Button>
          <Button variant="outline" size="sm" onClick={() => handleDownload("json")}>
            <Download className="w-4 h-4 mr-2" />
            JSON
          </Button>
        </div>
      </div>

      <Card className="overflow-hidden border-white/10">
        <div className="min-h-[400px] max-h-[600px] overflow-auto bg-black/20 p-6 font-mono text-sm text-text-neutral">
          {activeTab === "text" && (
            <pre className="whitespace-pre-wrap font-sans text-base leading-relaxed">
              {result.text}
            </pre>
          )}

          {activeTab === "json" && (
            <pre className="text-ai-highlight2">
              {JSON.stringify(result.structured, null, 2)}
            </pre>
          )}

          {activeTab === "pdf" && result.pdf_url && (
            <iframe 
              src={`http://localhost:8000${result.pdf_url}`} 
              className="w-full h-[600px] rounded-lg border border-white/10"
              title="PDF Preview"
            />
          )}
        </div>
        
        <div className="bg-white/5 border-t border-white/10 px-6 py-3 flex justify-between text-xs text-text-secondary">
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-ai-highlight2"></span>
            Confidence: {(result.confidence * 100).toFixed(1)}%
          </div>
          <div>Language: {result.language}</div>
          {result.metadata && <div>Processing Time: {result.metadata.processing_time_ms}ms</div>}
        </div>
      </Card>
    </div>
  );
};

const TabButton: React.FC<{ active: boolean; onClick: () => void; icon: React.ReactNode; label: string }> = ({ active, onClick, icon, label }) => (
  <button
    onClick={onClick}
    className={`flex items-center gap-2 px-3 py-1.5 rounded-md text-sm font-medium transition-all ${
      active 
        ? "bg-action-primary text-white shadow-lg shadow-action-primary/25" 
        : "text-text-secondary hover:text-text-neutral hover:bg-white/5"
    }`}
  >
    {icon}
    {label}
  </button>
);
