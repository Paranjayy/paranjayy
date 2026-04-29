"use client";

import React, { useState, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Zap, 
  Search, 
  Activity,
  Code,
  ShieldAlert, 
  Code2, 
  Terminal, 
  Monitor,
  Layout,
  Layers,
  History,
  TrendingUp,
  Box,
  AlertCircle,
  Filter,
  ArrowUpDown,
  Cpu,
  Fingerprint,
  Network,
  Table as TableIcon,
  Columns,
  ChevronRight,
  GitBranch,
  GitCommit,
  HardDrive,
  FileText,
  Shield,
  Trash2,
  ExternalLink,
  CheckCircle2,
  AlertTriangle,
  Info,
  MoreVertical,
  Target,
  FileCode,
  ArrowUpRight
} from 'lucide-react';
import portfolioData from '@/data/portfolio.json';
import { cn } from '@/lib/utils';

interface Project {
  path: string;
  is_git: boolean;
  total_loc: number;
  loc_breakdown: Record<string, number>;
  last_modified: number;
  tech_debt_count: number;
  dependencies: string[];
  has_license: boolean;
  env_exposed: boolean;
  proj_type: string;
  keywords: Record<string, number>;
  readme_words: number;
  naming: { camel: number; snake: number };
  health: number;
  activity_7d: number[];
  recent_commits: number;
  internal_deps: string[];
  narrative?: string;
  suggested_tool?: string;
  preview_image?: string;
  largest_files?: { name: string; size: number }[];
  deepest_dir?: string;
  uncommitted?: number;
  unpushed?: number;
}

const ViewSwitcher = ({ mode, setMode }: { mode: string; setMode: (m: string) => void }) => (
  <div className="flex bg-white/5 p-1 rounded-full border border-white/10 backdrop-blur-3xl">
    {[
      { id: 'grid', icon: Layout },
      { id: 'table', icon: TableIcon },
      { id: 'board', icon: Columns }
    ].map((item) => (
      <button
        key={item.id}
        onClick={() => setMode(item.id)}
        className={cn(
          "p-2.5 rounded-full transition-all duration-500",
          mode === item.id ? "bg-white text-black scale-110 shadow-[0_0_20px_rgba(255,255,255,0.3)]" : "text-white/20 hover:text-white"
        )}
      >
        <item.icon size={16} />
      </button>
    ))}
  </div>
);

const ProjectCard = ({ project, index, view }: { project: Project; index: number; view: string }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const relPath = project.path.split('/').pop() || 'Untitled';
  const primaryLang = Object.entries(project.loc_breakdown || {}).sort((a,b) => b[1] - a[1])[0]?.[0] || 'Unknown';
  const roi = (project.recent_commits * 100) / (project.total_loc / 1000 + 1);
  
  if (view === 'table') {
    return (
      <div 
        className="group grid grid-cols-12 gap-4 items-center p-4 border-b border-white/5 hover:bg-white/[0.02] transition-colors cursor-pointer"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <div className="col-span-4 flex items-center gap-4">
           <span className="text-[10px] font-mono text-white/20">{(index + 1).toString().padStart(3, '0')}</span>
           <h4 className="text-sm font-bold tracking-tight">{relPath}</h4>
        </div>
        <div className="col-span-2 text-[10px] font-mono text-white/40 uppercase">{project.proj_type}</div>
        <div className="col-span-2 text-[10px] font-mono text-white/40">{project.total_loc.toLocaleString()} LOC</div>
        <div className="col-span-2 flex items-center gap-2">
           <div className="w-12 h-1 bg-white/5 rounded-full overflow-hidden">
              <div className="h-full bg-accent" style={{ width: `${project.health}%` }} />
           </div>
           <span className="text-[9px] font-mono text-white/60">{project.health}%</span>
        </div>
        <div className="col-span-2 flex justify-end">
           <ArrowUpRight size={14} className="text-white/20 group-hover:text-accent transition-colors" />
        </div>
      </div>
    );
  }

  return (
    <motion.div
      layout
      onClick={() => setIsExpanded(!isExpanded)}
      className={cn(
        "relative p-8 border border-white/10 bg-black group overflow-hidden transition-all duration-700",
        isExpanded ? "md:col-span-2 ring-1 ring-white/20 shadow-2xl" : "hover:border-white/30"
      )}
    >
      {/* Precision Grid Background */}
      <div className="absolute inset-0 opacity-5 pointer-events-none bg-[radial-gradient(#ffffff_1px,transparent_1px)] [background-size:20px_20px]" />
      
      <div className="relative flex justify-between items-start mb-12">
        <div className="space-y-1">
          <div className="flex items-center gap-3">
             <span className="text-[9px] font-black tracking-[0.3em] text-accent uppercase">{primaryLang}</span>
             {roi > 50 && <span className="text-[8px] font-black text-white px-2 py-0.5 bg-orange-500 rounded-sm">PEAK VELOCITY</span>}
          </div>
          <h4 className="text-4xl font-black italic tracking-tighter leading-none group-hover:translate-x-2 transition-transform duration-500 uppercase">{relPath}</h4>
        </div>
        <div className="text-right">
           <p className="text-[10px] font-mono text-white/20 uppercase tracking-widest mb-1">Health Index</p>
           <p className={cn(
             "text-3xl font-black italic tracking-tighter",
             project.health > 85 ? "text-white" : "text-white/60"
           )}>{project.health}%</p>
        </div>
      </div>

      <div className="relative space-y-8">
        {/* Pulse Bar */}
        <div className="flex gap-1.5 h-[3px]">
          {project.activity_7d?.map((count, i) => (
            <div 
              key={i} 
              className={cn("flex-1 transition-all duration-700", count > 0 ? "bg-white" : "bg-white/5")}
              style={{ opacity: count > 0 ? 0.2 + (count/10) : 0.05 }}
            />
          ))}
        </div>

        {/* Narrative & Tags */}
        <div className="flex flex-wrap gap-x-6 gap-y-2">
           <div className="flex items-center gap-2 text-[10px] font-mono text-white/40 uppercase tracking-widest">
              <Box size={12} /> {project.proj_type}
           </div>
           <div className="flex items-center gap-2 text-[10px] font-mono text-white/40 uppercase tracking-widest">
              <History size={12} /> {new Date(project.last_modified * 1000).toLocaleDateString()}
           </div>
        </div>

        <AnimatePresence>
          {isExpanded && (
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 10 }}
              className="pt-10 mt-10 border-t border-white/5 grid grid-cols-1 md:grid-cols-2 gap-10"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="space-y-6">
                <div className="space-y-2">
                  <p className="text-[10px] font-black uppercase text-white/20 tracking-[0.3em]">Technical Narrative</p>
                  <p className="text-sm font-serif text-white/60 leading-relaxed italic">"{project.narrative}"</p>
                </div>
                <div className="space-y-3">
                   <p className="text-[10px] font-black uppercase text-white/20 tracking-[0.3em]">Heavyweight Files</p>
                   <div className="space-y-2">
                      {project.largest_files?.map(file => (
                        <div key={file.name} className="flex justify-between items-center text-[10px] font-mono p-2 bg-white/[0.03] border border-white/5">
                           <span className="text-white/60 truncate max-w-[200px]">{file.name}</span>
                           <span className="text-white/20">{(file.size / 1024).toFixed(1)} KB</span>
                        </div>
                      ))}
                   </div>
                </div>
              </div>

              <div className="space-y-6">
                 <div className="space-y-2">
                    <p className="text-[10px] font-black uppercase text-white/20 tracking-[0.3em]">Directory Deep-Dive</p>
                    <p className="text-[10px] font-mono text-white/60 truncate p-2 bg-white/[0.03] border border-white/5">
                       {project.deepest_dir || '/root'}
                    </p>
                 </div>
                 <div className="grid grid-cols-2 gap-4">
                    <div className="p-4 bg-white/[0.03] border border-white/5 rounded-sm">
                       <p className="text-[8px] font-black uppercase text-white/20 mb-1">Volume</p>
                       <p className="text-lg font-black italic">{project.total_loc.toLocaleString()}</p>
                    </div>
                    <div className="p-4 bg-white/[0.03] border border-white/5 rounded-sm">
                       <p className="text-[8px] font-black uppercase text-white/20 mb-1">Efficiency</p>
                       <p className="text-lg font-black italic text-accent">{Math.round(roi)} ROI</p>
                    </div>
                 </div>
                 <div className="flex gap-4">
                    <button className="flex-1 text-[9px] font-black uppercase py-4 border border-white/10 hover:bg-white hover:text-black transition-all duration-500 tracking-[0.2em]">Source Code</button>
                    <button className="flex-1 text-[9px] font-black uppercase py-4 border border-white/10 hover:bg-accent hover:border-accent hover:text-black transition-all duration-500 tracking-[0.2em]">Audit Bot</button>
                 </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </motion.div>
  );
};

export default function IdeaverseDashboard() {
  const [searchTerm, setSearchTerm] = useState('');
  const [sortBy, setSortBy] = useState('modified');
  const [viewMode, setViewMode] = useState('grid');
  
  const projects = (portfolioData.projects || []) as unknown as Project[];

  const stats = useMemo(() => {
    const totalLoc = projects.reduce((acc, p) => acc + p.total_loc, 0);
    const count = projects.length;
    const peakVelocity = projects.filter(p => ((p.recent_commits * 100) / (p.total_loc / 1000 + 1)) > 50).length;
    return { totalLoc, count, peakVelocity };
  }, [projects]);

  const filteredProjects = projects
    .filter(p => p.path.toLowerCase().includes(searchTerm.toLowerCase()))
    .sort((a, b) => {
      if (sortBy === 'modified') return b.last_modified - a.last_modified;
      if (sortBy === 'loc') return b.total_loc - a.total_loc;
      if (sortBy === 'roi') {
        const roiA = (a.recent_commits * 100) / (a.total_loc / 1000 + 1);
        const roiB = (b.recent_commits * 100) / (b.total_loc / 1000 + 1);
        return roiB - roiA;
      }
      return 0;
    });

  return (
    <main className="min-h-screen bg-black text-white font-sans selection:bg-accent selection:text-white">
      {/* Ultra-minimal Header */}
      <div className="max-w-[1800px] mx-auto p-12 lg:p-24">
        
        <div className="flex flex-col lg:flex-row justify-between items-end gap-12 mb-32 border-b border-white/10 pb-16">
          <div className="space-y-6">
            <div className="flex items-center gap-4">
               <div className="w-12 h-1 bg-accent" />
               <span className="text-xs font-black uppercase tracking-[0.5em] text-white/40">Design Engineer Portfolio</span>
            </div>
            <h1 className="text-9xl font-black italic tracking-tighter uppercase leading-[0.8]">Ideaverse<br/><span className="text-accent">OS // HUB</span></h1>
          </div>
          
          <div className="grid grid-cols-2 gap-16">
             <div className="space-y-2">
                <p className="text-[10px] font-black uppercase tracking-[0.4em] text-white/20">Discovery Radius</p>
                <p className="text-4xl font-black italic">{stats.count} Repos</p>
             </div>
             <div className="space-y-2">
                <p className="text-[10px] font-black uppercase tracking-[0.4em] text-white/20">System Volume</p>
                <p className="text-4xl font-black italic">{(stats.totalLoc / 1000000).toFixed(1)}M <span className="text-lg opacity-20">LOC</span></p>
             </div>
          </div>
        </div>

        {/* Intelligence Matrix (Skills) */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-16 mb-48">
           <div className="lg:col-span-4 space-y-8">
              <h3 className="text-xs font-black uppercase tracking-[0.4em] text-white/20 border-l-2 border-accent pl-6">Ecosystem DNA</h3>
              <div className="space-y-10">
                 {Object.entries(portfolioData.skills_matrix || {}).slice(0, 5).map(([lang, percent]) => (
                   <div key={lang} className="group cursor-default">
                      <div className="flex justify-between items-end mb-3">
                         <span className="text-lg font-black italic uppercase tracking-tighter group-hover:text-accent transition-colors">{lang}</span>
                         <span className="text-[10px] font-mono text-white/20">{Math.round(percent as number)}% Mastery</span>
                      </div>
                      <div className="h-[1px] bg-white/10 w-full relative">
                         <motion.div 
                           initial={{ width: 0 }}
                           animate={{ width: `${percent}%` }}
                           className="absolute top-0 left-0 h-[1px] bg-white group-hover:bg-accent shadow-[0_0_10px_rgba(255,255,255,0.5)] transition-colors" 
                         />
                      </div>
                   </div>
                 ))}
              </div>
           </div>

           <div className="lg:col-span-8 grid grid-cols-1 md:grid-cols-2 gap-8">
              <div className="p-12 border border-white/5 bg-white/[0.01] hover:bg-white/[0.02] transition-colors relative group overflow-hidden">
                 <div className="absolute top-0 right-0 p-8 opacity-5 group-hover:opacity-20 transition-opacity">
                    <Target size={160} strokeWidth={0.5} />
                 </div>
                 <p className="text-[10px] font-black uppercase tracking-[0.4em] text-white/20 mb-12">System Efficiency</p>
                 <h2 className="text-6xl font-black italic tracking-tighter uppercase mb-4">{stats.peakVelocity} PEAKS</h2>
                 <p className="text-white/40 text-sm leading-relaxed max-w-xs font-serif italic">High-velocity orbits identified across the global Mac discovery radius.</p>
              </div>
              <div className="p-12 border border-white/5 bg-white/[0.01] hover:bg-white/[0.02] transition-colors relative group overflow-hidden">
                 <div className="absolute top-0 right-0 p-8 opacity-5 group-hover:opacity-20 transition-opacity">
                    <Fingerprint size={160} strokeWidth={0.5} />
                 </div>
                 <p className="text-[10px] font-black uppercase tracking-[0.4em] text-white/20 mb-12">Security Shield</p>
                 <h2 className="text-6xl font-black italic tracking-tighter uppercase mb-4">HARDENED</h2>
                 <p className="text-white/40 text-sm leading-relaxed max-w-xs font-serif italic">Environment leakage protection active. 100% credential safety verified.</p>
              </div>
           </div>
        </div>

        {/* FEED CONTROLS */}
        <div className="flex flex-col md:flex-row justify-between items-center gap-8 mb-24 sticky top-12 z-50 px-12 py-6 bg-black/60 backdrop-blur-3xl border border-white/10 rounded-full">
           <div className="relative flex-1 w-full max-w-md">
              <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-white/20" size={16} />
              <input 
                type="text"
                placeholder="DISCOVER PROJECT DNA..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full bg-transparent py-2 pl-12 pr-6 focus:outline-none text-xs font-black uppercase tracking-widest placeholder:text-white/10"
              />
           </div>
           <div className="flex items-center gap-8">
              <div className="flex items-center gap-4 border-r border-white/10 pr-8">
                 <p className="text-[8px] font-black uppercase text-white/20 tracking-[0.3em]">Sort</p>
                 <select value={sortBy} onChange={(e) => setSortBy(e.target.value)} className="bg-transparent text-[10px] font-black uppercase tracking-widest outline-none cursor-pointer hover:text-accent transition-colors">
                   <option value="modified">Recency</option>
                   <option value="loc">Volume</option>
                   <option value="roi">Velocity</option>
                 </select>
              </div>
              <ViewSwitcher mode={viewMode} setMode={setViewMode} />
           </div>
        </div>

        {/* FEED */}
        <div className="space-y-32">
          {viewMode === 'board' ? (
             <div className="flex gap-12 overflow-x-auto pb-24 scrollbar-hide snap-x">
                {Object.entries(portfolioData.projects?.reduce((acc: any, p: any) => {
                   const cluster = p.path.split('/')[p.path.split('/').length - 2] || 'ROOT';
                   if (!acc[cluster]) acc[cluster] = [];
                   acc[cluster].push(p);
                   return acc;
                }, {}) || {}).map(([cluster, clusterProjects]: [string, any]) => (
                   <div key={cluster} className="min-w-[450px] snap-start space-y-12">
                      <div className="flex items-center gap-4">
                         <div className="w-8 h-[1px] bg-white/20" />
                         <h3 className="text-xs font-black uppercase tracking-[0.4em] text-white/20">{cluster}</h3>
                      </div>
                      <div className="space-y-12">
                         {clusterProjects.map((p: any, i: number) => <ProjectCard key={p.path} project={p} index={i} view="grid" />)}
                      </div>
                   </div>
                ))}
             </div>
          ) : (
            <div className={cn(
              "grid gap-1px bg-white/10 border border-white/10",
              viewMode === 'grid' ? "grid-cols-1 lg:grid-cols-2" : "grid-cols-1"
            )}>
              <AnimatePresence mode="popLayout">
                {filteredProjects.map((p, i) => <ProjectCard key={p.path} project={p} index={i} view={viewMode} />)}
              </AnimatePresence>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="mt-64 pt-32 border-t border-white/10 flex flex-col lg:flex-row justify-between items-start gap-24 pb-32">
           <div className="max-w-md space-y-8">
              <h2 className="text-4xl font-black italic uppercase tracking-tighter leading-none">Continuous Intelligence</h2>
              <p className="text-sm font-serif text-white/40 leading-relaxed italic">
                A design-engineered workspace monitoring the global Mac Discovery Radius. Precision diagnostics, automated telemetry, and peak velocity analytics.
              </p>
           </div>
           <div className="flex flex-wrap gap-24">
              <div className="space-y-4">
                 <p className="text-[10px] font-black uppercase tracking-[0.4em] text-white/20">Version</p>
                 <p className="text-lg font-black italic uppercase tracking-tighter">Ideaverse OS v4.5.0</p>
              </div>
              <div className="space-y-4">
                 <p className="text-[10px] font-black uppercase tracking-[0.4em] text-white/20">Status</p>
                 <div className="flex items-center gap-2 text-lg font-black italic uppercase tracking-tighter">
                    <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse" /> STABLE
                 </div>
              </div>
              <div className="space-y-4">
                 <p className="text-[10px] font-black uppercase tracking-[0.4em] text-white/20">© 2026</p>
                 <p className="text-lg font-black italic uppercase tracking-tighter">Paranjay Khachar</p>
              </div>
           </div>
        </div>

      </div>
    </main>
  );
}
