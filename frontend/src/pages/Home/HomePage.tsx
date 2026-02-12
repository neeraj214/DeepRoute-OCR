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
          <div className="inline-flex items-center justify-center p-1 rounded-full bg-gradient-to-r from-action-primary/20 via-ai-highlight1/20 to-action-primary/20 p-[1px] mb-8 group hover:scale-105 transition-transform duration-300">
            <div className="bg-primary-base rounded-full px-6 py-2 flex items-center gap-3">
              <Scan className="w-5 h-5 text-action-primary animate-pulse" />
              <span className="text-sm font-medium text-text-neutral/80 tracking-wider uppercase">Next-Gen OCR Engine</span>
            </div>
          </div>
          
          <h1 
            className="text-6xl md:text-8xl font-black text-text-neutral tracking-tight leading-[1.1] transition-transform duration-300 ease-out"
            style={{ transform: `translate(${mousePos.x * -0.2}px, ${mousePos.y * -0.2}px)` }}
          >
            Unlock the Power of <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-action-primary via-ai-highlight1 to-action-primary bg-[length:200%_auto] animate-gradient">
              Your Documents
            </span>
          </h1>
          
          <p className="max-w-3xl mx-auto text-xl md:text-2xl text-text-secondary leading-relaxed font-light">
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
        </section>

        {/* Stats / Proof Section */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8 max-w-4xl mx-auto py-12 border-y border-white/5 relative group">
          <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-1000 ease-in-out pointer-events-none" />
          <StatItem label="Accuracy" value="99.9%" />
          <StatItem label="Processing" value="< 2s" />
          <StatItem label="Formats" value="50+" />
          <StatItem label="Secure" value="SOC2" />
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
