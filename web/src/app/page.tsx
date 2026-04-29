"use client";

import React from 'react';
import { motion } from 'framer-motion';
import { 
  Zap, 
  Monitor, 
  FlaskConical, 
  Activity, 
  Box,
  ChevronRight,
  Shield,
  Fingerprint
} from 'lucide-react';
import Link from 'next/link';

export default function IdeaverseLanding() {
  return (
    <main className="min-h-screen gradient-bg flex items-center justify-center p-6 lg:p-12">
      <div className="max-w-4xl w-full">
        <motion.div 
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-20"
        >
          <div className="w-24 h-24 rounded-[2.5rem] bg-accent mx-auto flex items-center justify-center shadow-[0_0_80px_rgba(168,85,247,0.5)] rotate-12 border-4 border-white/20 mb-10">
            <Zap className="text-white fill-white" size={48} />
          </div>
          <h1 className="text-8xl font-black italic uppercase tracking-tighter mb-6 leading-none">
            Ideaverse <br/> <span className="text-accent">OS</span>
          </h1>
          <p className="text-white/30 text-xl font-serif max-w-xl mx-auto">
            Recursive Workspace Intelligence. Monitoring sixty-seven projects across your ecosystem with deep-scan telemetry.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <Link href="/hub">
            <motion.div 
              whileHover={{ scale: 1.02, y: -5 }}
              className="glass-card p-10 border-white/10 bg-white/[0.03] group hover:border-accent/50 transition-all cursor-pointer relative overflow-hidden"
            >
              <div className="absolute top-0 right-0 p-8 opacity-5 group-hover:opacity-10 transition-opacity">
                <Monitor size={120} />
              </div>
              <div className="flex items-center gap-4 mb-6">
                <div className="w-12 h-12 rounded-xl bg-accent/20 flex items-center justify-center text-accent">
                  <Monitor size={24} />
                </div>
                <h2 className="text-2xl font-black uppercase italic tracking-tighter">Command Hub</h2>
              </div>
              <p className="text-white/40 text-sm leading-relaxed mb-8">
                Access the primary intelligence feed, project grid, and real-time activity metrics.
              </p>
              <div className="flex items-center gap-2 text-accent font-black uppercase text-xs tracking-widest">
                Initialize <ChevronRight size={14} />
              </div>
            </motion.div>
          </Link>

          <Link href="/lab">
            <motion.div 
              whileHover={{ scale: 1.02, y: -5 }}
              className="glass-card p-10 border-white/10 bg-white/[0.03] group hover:border-blue-500/50 transition-all cursor-pointer relative overflow-hidden"
            >
              <div className="absolute top-0 right-0 p-8 opacity-5 group-hover:opacity-10 transition-opacity">
                <FlaskConical size={120} />
              </div>
              <div className="flex items-center gap-4 mb-6">
                <div className="w-12 h-12 rounded-xl bg-blue-500/20 flex items-center justify-center text-blue-400">
                  <FlaskConical size={24} />
                </div>
                <h2 className="text-2xl font-black uppercase italic tracking-tighter">Research Lab</h2>
              </div>
              <p className="text-white/40 text-sm leading-relaxed mb-8">
                Experimental telemetry including Nexus dependency mapping and AI Narrative generation.
              </p>
              <div className="flex items-center gap-2 text-blue-400 font-black uppercase text-xs tracking-widest">
                Enter Lab <ChevronRight size={14} />
              </div>
            </motion.div>
          </Link>
        </div>

        <div className="mt-20 flex justify-center gap-12 grayscale opacity-20">
           <div className="flex items-center gap-2 text-xs font-black uppercase tracking-widest"><Shield size={16}/> Hardened</div>
           <div className="flex items-center gap-2 text-xs font-black uppercase tracking-widest"><Fingerprint size={16}/> Verified</div>
           <div className="flex items-center gap-2 text-xs font-black uppercase tracking-widest"><Activity size={16}/> Real-time</div>
        </div>
      </div>
    </main>
  );
}
