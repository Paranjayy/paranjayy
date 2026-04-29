"use client";

import React from 'react';
import { motion } from 'framer-motion';
import { 
  FlaskConical, 
  Network, 
  Cpu, 
  Terminal, 
  ChevronRight,
  Box,
  Activity,
  ArrowLeft
} from 'lucide-react';
import portfolioData from '@/data/portfolio.json';
import Link from 'next/link';

export default function ExperimentalLab() {
  const projects = portfolioData.projects;
  
  return (
    <main className="min-h-screen gradient-bg p-8 lg:p-16">
      <div className="max-w-7xl mx-auto">
        <Link href="/hub" className="flex items-center gap-2 text-white/40 hover:text-accent transition-colors mb-12 text-sm font-black uppercase tracking-widest">
          <ArrowLeft size={16} /> Back to Hub
        </Link>

        <div className="flex items-center gap-6 mb-16">
          <div className="w-16 h-16 rounded-2xl bg-accent/20 flex items-center justify-center border border-accent/40 shadow-[0_0_50px_rgba(168,85,247,0.2)]">
            <FlaskConical className="text-accent" size={32} />
          </div>
          <div>
            <h1 className="text-6xl font-black italic uppercase tracking-tighter">Research Lab</h1>
            <p className="text-white/40 mt-2 text-lg font-serif">Experimental workspace telemetry & mapping.</p>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          {/* Dependency Nebula */}
          <div className="glass-card p-10 border-accent/20 bg-accent/5">
            <h3 className="text-sm font-black uppercase tracking-[0.4em] text-accent mb-10 flex items-center gap-4">
              <Network size={20} />
              Nexus: Dependency Nebula
            </h3>
            <div className="space-y-6">
              {projects.filter(p => p.internal_deps?.length > 0).map(p => (
                <div key={p.path} className="bg-black/40 p-6 rounded-2xl border border-white/5 group hover:border-accent/50 transition-all">
                  <p className="text-xs font-black text-white uppercase tracking-widest mb-3">{p.path.split('/').pop()}</p>
                  <div className="flex flex-wrap gap-2">
                    {p.internal_deps.map(dep => (
                      <span key={dep} className="px-3 py-1 rounded-full bg-accent/10 text-[10px] text-accent font-bold flex items-center gap-2 border border-accent/20">
                        <ChevronRight size={12} /> {dep}
                      </span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* AI Narrative Engine */}
          <div className="glass-card p-10 border-blue-500/20 bg-blue-500/5">
            <h3 className="text-sm font-black uppercase tracking-[0.4em] text-blue-400 mb-10 flex items-center gap-4">
              <Cpu size={20} />
              AI Narrative Archive
            </h3>
            <div className="space-y-6">
              {projects.slice(0, 5).map(p => (
                <div key={p.path} className="bg-black/40 p-6 rounded-2xl border border-white/5">
                  <div className="flex justify-between items-center mb-3">
                    <p className="text-xs font-black text-white/60 uppercase">{p.path.split('/').pop()}</p>
                    <span className="text-[10px] font-black text-blue-400">STABLE</span>
                  </div>
                  <p className="text-sm text-white/80 italic font-serif leading-relaxed">
                    "{p.narrative || "Scanning project dna..."}"
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
