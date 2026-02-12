import React, { useState, useEffect } from "react";
import { Button } from "../../components/ui/Button";
import { Card } from "../../components/ui/Card";
import { Scan, FileText, Zap, Shield } from "lucide-react";

interface HomePageProps {
  onNavigate: (page: "upload") => void;
}

const HomePage: React.FC<HomePageProps> = ({ onNavigate }) => {
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      setMousePos({
        x: (e.clientX / window.innerWidth - 0.5) * 20,
        y: (e.clientY / window.innerHeight - 0.5) * 20,
      });
    };
    window.addEventListener("mousemove", handleMouseMove);
    return () => window.removeEventListener("mousemove", handleMouseMove);
  }, []);

  return (
    <div className="relative min-h-screen overflow-hidden bg-primary-base">
      {/* Mesh Background Pattern */}
      <div className="absolute inset-0 -z-30 opacity-30">
        <div className="absolute inset-0 bg-[radial-gradient(at_top_right,rgba(99,102,241,0.15),transparent_50%),radial-gradient(at_bottom_left,rgba(216,180,254,0.1),transparent_50%)]" />
      </div>

      {/* Interactive Background Layer */}
      <div 
        className="absolute inset-0 -z-20 transition-transform duration-75 ease-out pointer-events-none"
        style={{ 
          transform: `translate(${mousePos.x}px, ${mousePos.y}px)` 
        }}
      >
        {/* Animated Gradient Orbs */}
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-action-primary/20 blur-[120px] rounded-full animate-pulse-slow" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[50%] h-[50%] bg-ai-highlight1/15 blur-[150px] rounded-full animate-float" />
        <div className="absolute top-[20%] right-[10%] w-[30%] h-[30%] bg-ai-highlight2/10 blur-[100px] rounded-full animate-pulse-slow [animation-delay:2s]" />
        
        {/* Moving Light Beam */}
        <div 
          className="absolute top-0 left-0 w-full h-full opacity-30 mix-blend-soft-light"
          style={{
            background: `radial-gradient(circle at ${50 + mousePos.x}% ${50 + mousePos.y}%, rgba(99, 102, 241, 0.15) 0%, transparent 50%)`
          }}
        />
      </div>

      {/* Grid & Noise Overlays */}
      <div className="absolute inset-0 -z-10 pointer-events-none">
        <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20 mix-blend-overlay" />
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:40px_40px] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_0%,#000_70%,transparent_100%)]" />
      </div>

      <div className="space-y-24 py-12 relative z-10 animate-fade-in">
        {/* Hero Section */}
        <section className="text-center space-y-10 py-20 relative max-w-5xl mx-auto px-4">
          <div className="inline-flex items-center justify-center p-1 rounded-full bg-white/5 backdrop-blur-md border border-white/10 p-[1px] mb-8 group hover:scale-105 transition-all duration-300 shadow-xl shadow-black/20">
            <div className="bg-primary-base/40 rounded-full px-6 py-2 flex items-center gap-3">
              <Scan className="w-5 h-5 text-action-primary animate-pulse" />
              <span className="text-sm font-bold text-text-neutral/80 tracking-wider uppercase">Next-Gen OCR Engine</span>
            </div>
          </div>
          
          <h1 
            className="text-6xl md:text-8xl tracking-tight leading-[1.15] transition-transform duration-300 ease-out"
            style={{ transform: `translate(${mousePos.x * -0.2}px, ${mousePos.y * -0.2}px)` }}
          >
            <span className="font-light text-text-neutral/90">Unlock the Power of</span> <br />
            <span className="font-black text-transparent bg-clip-text bg-gradient-to-r from-action-primary via-ai-highlight1 to-action-primary bg-[length:200%_auto] animate-gradient">
              Your Documents
            </span>
          </h1>
          
          <p className="max-w-[65ch] mx-auto text-xl md:text-2xl text-text-secondary leading-relaxed font-light">
            DocVision AI uses enterprise-grade transformers to extract structured data 
            from invoices, forms, and handwritten notes with human-level accuracy.
          </p>
          
          <div className="flex flex-col sm:flex-row justify-center items-center gap-6 pt-10">
            <Button size="lg" onClick={() => onNavigate("upload")} className="text-xl px-10 py-6 h-auto rounded-2xl shadow-2xl shadow-action-primary/30 hover:shadow-action-primary/50 transition-all duration-500 group relative overflow-hidden">
              <span className="relative z-10 flex items-center">
                Start Free Extraction
                <Zap className="ml-2 w-5 h-5 group-hover:fill-current group-hover:scale-125 transition-transform duration-300" />
              </span>
              <div className="absolute inset-0 bg-gradient-to-r from-action-primary via-ai-highlight1 to-action-primary opacity-0 group-hover:opacity-100 transition-opacity duration-500 blur-xl -z-10" />
            </Button>
            <Button variant="secondary" size="lg" className="text-xl px-10 py-6 h-auto rounded-2xl border-white/10 hover:bg-white/5 backdrop-blur-sm transition-all duration-300">
              Enterprise Demo
            </Button>
          </div>

          {/* Product Preview / Before-After Section */}
          <div className="mt-20 relative max-w-5xl mx-auto px-4">
            <div className="relative rounded-3xl overflow-hidden border border-white/10 bg-white/5 backdrop-blur-xl shadow-2xl animate-slide-up">
              <div className="flex flex-col lg:flex-row items-stretch">
                {/* Before: Messy Invoice */}
                <div className="flex-1 p-8 border-b lg:border-b-0 lg:border-r border-white/10 bg-white/[0.02]">
                  <div className="flex items-center gap-2 mb-6 text-text-secondary/60 text-sm font-medium uppercase tracking-wider">
                    <FileText className="w-4 h-4" />
                    Input: Raw Document
                  </div>
                  <div className="relative aspect-[4/5] bg-white/5 rounded-xl border border-white/5 overflow-hidden group">
                    <div className="absolute inset-0 p-6 space-y-4 opacity-40 group-hover:opacity-60 transition-opacity duration-500">
                      <div className="h-4 w-1/3 bg-white/20 rounded" />
                      <div className="space-y-2">
                        <div className="h-2 w-full bg-white/10 rounded" />
                        <div className="h-2 w-5/6 bg-white/10 rounded" />
                      </div>
                      <div className="pt-8 space-y-3">
                        <div className="h-8 w-full border border-white/10 rounded" />
                        <div className="h-8 w-full border border-white/10 rounded" />
                        <div className="h-8 w-full border border-white/10 rounded" />
                      </div>
                    </div>
                    {/* Scanning Animation */}
                    <div className="absolute inset-0 bg-gradient-to-b from-transparent via-action-primary/20 to-transparent h-1/2 w-full animate-[scan_3s_ease-in-out_infinite] pointer-events-none" />
                  </div>
                </div>

                {/* Transformation Arrow */}
                <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 z-20 hidden lg:block">
                  <div className="w-12 h-12 rounded-full bg-action-primary flex items-center justify-center shadow-lg shadow-action-primary/50 animate-pulse">
                    <Zap className="w-6 h-6 text-white" />
                  </div>
                </div>

                {/* After: Clean JSON */}
                <div className="flex-1 p-8 bg-black/40">
                  <div className="flex items-center justify-between mb-6">
                    <div className="flex items-center gap-2 text-ai-highlight1 text-sm font-medium uppercase tracking-wider">
                      <Zap className="w-4 h-4" />
                      Output: Structured Data
                    </div>
                    <div className="px-2 py-1 rounded bg-ai-highlight1/10 text-ai-highlight1 text-[10px] font-bold border border-ai-highlight1/20">
                      JSON
                    </div>
                  </div>
                  <div className="relative aspect-[4/5] font-mono text-sm overflow-hidden">
                    <div className="text-ai-highlight1/90 space-y-1">
                      <div className="text-text-secondary/50">{"{"}</div>
                      <div className="pl-4"><span className="text-ai-highlight2">"invoice_id"</span>: <span className="text-action-primary">"INV-2024-001"</span>,</div>
                      <div className="pl-4"><span className="text-ai-highlight2">"date"</span>: <span className="text-action-primary">"2024-02-12"</span>,</div>
                      <div className="pl-4"><span className="text-ai-highlight2">"vendor"</span>: <span className="text-action-primary">"TechCorp Systems"</span>,</div>
                      <div className="pl-4"><span className="text-ai-highlight2">"items"</span>: [</div>
                      <div className="pl-8">{"{"}</div>
                      <div className="pl-12"><span className="text-ai-highlight2">"desc"</span>: <span className="text-action-primary">"Cloud API Usage"</span>,</div>
                      <div className="pl-12"><span className="text-ai-highlight2">"total"</span>: <span className="text-action-primary">1240.50</span></div>
                      <div className="pl-8">{"}"}</div>
                      <div className="pl-4">],</div>
                      <div className="pl-4"><span className="text-ai-highlight2">"confidence"</span>: <span className="text-green-400">0.998</span></div>
                      <div className="text-text-secondary/50">{"}"}</div>
                    </div>
                    {/* Floating Glow */}
                    <div className="absolute -bottom-10 -right-10 w-40 h-40 bg-action-primary/20 blur-[60px] rounded-full" />
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Logo Cloud Section */}
          <div className="mt-32 max-w-7xl mx-auto px-4">
            <p className="text-center text-sm font-semibold text-text-secondary/50 uppercase tracking-[0.2em] mb-12">
              Trusted by industry leaders worldwide
            </p>
            <div className="flex flex-wrap justify-center items-center gap-12 md:gap-24 opacity-40 grayscale hover:grayscale-0 transition-all duration-700">
              <LogoItem name="GlobateCorp" />
              <LogoItem name="DataPrime" />
              <LogoItem name="NexusTech" />
              <LogoItem name="FutureSolutions" />
            </div>
          </div>
        </section>

        {/* Stats / Proof Section */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8 max-w-4xl mx-auto py-12 border-y border-white/5 relative group">
          <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-1000 ease-in-out pointer-events-none" />
          <StatItem label="Accuracy" value="99.9%" />
          <StatItem label="Processing" value="< 2s" />
          <StatItem label="Formats" value="50+" />
          <StatItem label="Secure" value="SOC2" />
        </div>

        {/* Security Trust Badges */}
        <div className="flex justify-center gap-8 py-8 opacity-60">
          <div className="flex items-center gap-2 text-xs font-bold text-text-secondary border border-white/10 rounded-lg px-4 py-2 backdrop-blur-sm">
            <Shield className="w-4 h-4 text-ai-highlight2" />
            SOC2 COMPLIANT
          </div>
          <div className="flex items-center gap-2 text-xs font-bold text-text-secondary border border-white/10 rounded-lg px-4 py-2 backdrop-blur-sm">
            <Zap className="w-4 h-4 text-action-primary" />
            AES-256 ENCRYPTED
          </div>
        </div>

        {/* Features Grid */}
        <section className="grid md:grid-cols-3 gap-8 px-4 max-w-7xl mx-auto">
          <FeatureCard
            icon={<Zap className="w-8 h-8 text-ai-highlight2" />}
            title="Transformer OCR"
            description="Leverage TrOCR and Vision Transformers for unmatched character recognition even in low-quality scans."
          />
          <FeatureCard
            icon={<FileText className="w-8 h-8 text-action-primary" />}
            title="Intelligent Routing"
            description="Our AI classifier automatically routes documents to the specialized engine for the best possible results."
          />
          <FeatureCard
            icon={<Shield className="w-8 h-8 text-ai-highlight1" />}
            title="Data Governance"
            description="Enterprise-grade encryption and PII masking ensure your sensitive financial data remains private."
          />
        </section>
      </div>
    </div>
  );
};

const LogoItem: React.FC<{ name: string }> = ({ name }) => (
  <div className="flex items-center gap-2 group/logo">
    <div className="w-8 h-8 rounded bg-white/10 flex items-center justify-center font-black text-xs group-hover/logo:bg-action-primary/20 group-hover/logo:text-action-primary transition-colors">
      {name[0]}
    </div>
    <span className="font-bold tracking-tight text-lg group-hover/logo:text-white transition-colors">{name}</span>
  </div>
);

const StatItem: React.FC<{ label: string; value: string }> = ({ label, value }) => (
  <div className="text-center">
    <div className="text-2xl font-bold text-text-neutral">{value}</div>
    <div className="text-sm text-text-secondary uppercase tracking-widest">{label}</div>
  </div>
);

const FeatureCard: React.FC<{
  icon: React.ReactNode;
  title: string;
  description: string;
}> = ({ icon, title, description }) => (
  <Card className="p-8 hover:bg-white/10 transition-colors group border-white/5">
    <div className="mb-6 p-3 bg-white/5 w-fit rounded-lg group-hover:scale-110 transition-transform duration-300 ring-1 ring-white/10">
      {icon}
    </div>
    <h3 className="text-xl font-bold text-text-neutral mb-3">{title}</h3>
    <p className="text-text-secondary leading-relaxed">{description}</p>
  </Card>
);

export default HomePage;
