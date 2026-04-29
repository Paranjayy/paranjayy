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
  MoreVertical
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
  branch?: string;
  uncommitted?: number;
  unpushed?: number;
}

const ViewSwitcher = ({ mode, setMode }: { mode: string; setMode: (m: string) => void }) => (
  <div className="flex bg-white/5 p-1 rounded-2xl border border-white/10 backdrop-blur-xl ring-1 ring-white/5">
    {[
      { id: 'grid', icon: Layout, label: 'Grid' },
      { id: 'table', icon: TableIcon, label: 'Notion' },
      { id: 'board', icon: Columns, label: 'Board' }
    ].map((item) => (
      <button
        key={item.id}
        onClick={() => setMode(item.id)}
        className={cn(
          "flex items-center gap-2 px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all",
          mode === item.id ? "bg-accent text-white shadow-lg shadow-accent/20" : "text-white/30 hover:text-white"
        )}
      >
        <item.icon size={14} />
        <span className="hidden sm:inline">{item.label}</span>
      </button>
    ))}
  </div>
);

const ProjectCard = ({ project, index, view }: { project: Project; index: number; view: string }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const relPath = project.path.split('/').pop() || 'Untitled';
  const lastModDate = new Date(project.last_modified * 1000);
  const isGhost = (Date.now() - lastModDate.getTime()) > (30 * 24 * 60 * 60 * 1000);
  const primaryLang = Object.entries(project.loc_breakdown || {}).sort((a,b) => b[1] - a[1])[0]?.[0] || 'Unknown';
  
  if (view === 'table') {
    return (
      <motion.div 
        layout
        className="group flex items-center gap-6 p-4 rounded-xl hover:bg-white/5 transition-all cursor-pointer border border-transparent hover:border-white/10"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <div className="w-10 h-10 rounded-xl bg-white/5 flex items-center justify-center text-white/20 group-hover:text-accent group-hover:bg-accent/10 transition-all">
          <Code size={18} />
        </div>
        <div className="flex-1 min-w-0">
          <h4 className="text-sm font-bold text-white/90 truncate">{relPath}</h4>
          <p className="text-[10px] text-white/20 font-mono truncate">{project.path}</p>
        </div>
        <div className="hidden lg:flex items-center gap-8 text-[11px] font-mono text-white/40">
           <div className="w-20 text-right">{project.total_loc.toLocaleString()}</div>
           <div className="w-24 text-center">
             <div className={cn(
               "px-2 py-0.5 rounded text-[9px] font-black uppercase",
               project.health > 85 ? "text-green-400 bg-green-500/10" : "text-red-400 bg-red-500/10"
             )}>
               {project.health}%
             </div>
           </div>
           <div className="w-32 flex items-center gap-4">
             <span className="opacity-40">{new Date(project.last_modified * 1000).toLocaleDateString()}</span>
             {project.unpushed && <ArrowUpDown size={12} className="text-accent" />}
           </div>
        </div>
      </motion.div>
    );
  }

  return (
    <motion.div
      layout
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ delay: index * 0.01 }}
      onClick={() => setIsExpanded(!isExpanded)}
      className={cn(
        "glass-card group relative overflow-hidden cursor-pointer p-6 transition-all duration-500",
        isExpanded ? "md:col-span-2 bg-white/10 ring-2 ring-accent/20" : "hover:bg-white/5",
        isGhost && !isExpanded && "opacity-60 grayscale-[0.5]"
      )}
    >
      <div className="flex justify-between items-start mb-6">
        <div>
          <span className="text-[9px] uppercase font-black tracking-widest text-accent mb-2 block">{primaryLang} // {project.proj_type}</span>
          <h4 className="text-xl font-black truncate">{relPath}</h4>
        </div>
        <div className={cn(
          "text-2xl font-black italic",
          project.health > 85 ? "text-green-400" : project.health > 60 ? "text-yellow-400" : "text-red-400"
        )}>
          {project.health}%
        </div>
      </div>

      <div className="space-y-4">
        <div className="flex gap-1 h-1.5 rounded-full overflow-hidden bg-white/5">
          {project.activity_7d?.map((count, i) => (
            <div 
              key={i} 
              className={cn("flex-1", count > 0 ? "bg-accent" : "bg-white/5")}
              style={{ opacity: count > 0 ? Math.min(0.2 + (count/5), 1) : 0.05 }}
            />
          ))}
        </div>

        <AnimatePresence>
          {isExpanded && (
            <motion.div 
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 'auto', opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              className="pt-6 border-t border-white/10 mt-6 space-y-4"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="bg-white/5 rounded-xl p-4 border border-white/5">
                <p className="text-sm text-white/70 italic font-serif">"{project.narrative}"</p>
              </div>
              <div className="flex flex-wrap gap-2">
                <button className="flex-1 bg-white/5 hover:bg-accent hover:text-black py-3 rounded-xl text-[10px] font-black uppercase transition-all">AI README</button>
                <button className="flex-1 bg-white/5 hover:bg-green-500 hover:text-black py-3 rounded-xl text-[10px] font-black uppercase transition-all">Harden</button>
                <button className="flex-1 bg-white/5 hover:bg-red-500 hover:text-black py-3 rounded-xl text-[10px] font-black uppercase transition-all">Archive</button>
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
  const [filterType, setFilterType] = useState('all');
  const [viewMode, setViewMode] = useState('grid');
  
  const projects = portfolioData.projects as unknown as Project[];

  const stats = useMemo(() => {
    const totalLoc = projects.reduce((acc, p) => acc + p.total_loc, 0);
    const criticalRepos = projects.filter(p => p.env_exposed).length;
    const pendingRepos = projects.filter(p => (p.uncommitted || 0) > 0 || (p.unpushed || 0) > 0).length;
    return { totalLoc, criticalRepos, pendingRepos, count: projects.length };
  }, [projects]);

  const filteredProjects = projects
    .filter(p => {
      const matchesSearch = p.path.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesType = filterType === 'all' || p.proj_type.toLowerCase().includes(filterType.toLowerCase());
      return matchesSearch && matchesType;
    })
    .sort((a, b) => {
      if (sortBy === 'modified') return b.last_modified - a.last_modified;
      if (sortBy === 'loc') return b.total_loc - a.total_loc;
      return 0;
    });

  const clusteredProjects = useMemo(() => {
    const clusters: Record<string, Project[]> = {};
    filteredProjects.forEach(p => {
      const clusterName = p.path.split('/')[p.path.split('/').length - 2] || 'Root';
      if (!clusters[clusterName]) clusters[clusterName] = [];
      clusters[clusterName].push(p);
    });
    return clusters;
  }, [filteredProjects]);

  return (
    <main className="min-h-screen gradient-bg p-6 lg:p-12">
      <div className="max-w-[1600px] mx-auto">
        
        {/* TOP BAR: Title & Alerts */}
        <div className="flex flex-col xl:flex-row justify-between items-center gap-8 mb-16">
          <div className="flex items-center gap-6">
            <div className="w-14 h-14 rounded-2xl bg-accent flex items-center justify-center shadow-2xl shadow-accent/40 rotate-6 border border-white/20">
              <Zap className="text-white fill-white" size={28} />
            </div>
            <div>
              <h1 className="text-5xl font-black tracking-tighter uppercase italic">Ideaverse Hub</h1>
              <p className="text-white/30 text-xs font-black uppercase tracking-[0.3em]">{stats.count} ACTIVE ORBITERS</p>
            </div>
          </div>

          <div className="flex flex-wrap justify-center gap-4">
             <div className="flex items-center gap-3 bg-red-500/10 border border-red-500/20 px-6 py-4 rounded-2xl">
               <ShieldAlert className="text-red-400" size={20} />
               <div>
                 <p className="text-[10px] font-black uppercase text-red-400">Security Risks</p>
                 <p className="text-xl font-black text-white leading-none">{stats.criticalRepos}</p>
               </div>
             </div>
             <div className="flex items-center gap-3 bg-yellow-500/10 border border-yellow-500/20 px-6 py-4 rounded-2xl">
               <AlertTriangle className="text-yellow-400" size={20} />
               <div>
                 <p className="text-[10px] font-black uppercase text-yellow-400">Pending Backlog</p>
                 <p className="text-xl font-black text-white leading-none">{stats.pendingRepos}</p>
               </div>
             </div>
             <div className="flex items-center gap-3 bg-blue-500/10 border border-blue-500/20 px-6 py-4 rounded-2xl">
               <Activity className="text-blue-400" size={20} />
               <div>
                 <p className="text-[10px] font-black uppercase text-blue-400">System Status</p>
                 <p className="text-xs font-black text-white uppercase flex items-center gap-2">
                   <div className="w-1.5 h-1.5 bg-green-400 rounded-full animate-pulse" />
                   STABLE
                 </p>
               </div>
             </div>
          </div>
        </div>

        {/* SEARCH & VIEW SWITCHER (CRITICAL FIX) */}
        <div className="glass-card p-4 rounded-[2rem] border-white/10 bg-white/[0.02] mb-16 flex flex-col md:flex-row gap-4 items-center">
          <div className="relative flex-1 w-full">
            <Search className="absolute left-6 top-1/2 -translate-y-1/2 text-white/20" size={20} />
            <input 
              type="text"
              placeholder="Query the Workspace..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full bg-transparent py-4 pl-14 pr-8 focus:outline-none text-xl font-mono"
            />
          </div>
          <div className="h-10 w-[1px] bg-white/10 hidden md:block" />
          <div className="flex items-center gap-4 w-full md:w-auto overflow-x-auto pb-2 md:pb-0">
             <select value={sortBy} onChange={(e) => setSortBy(e.target.value)} className="bg-white/5 border border-white/10 rounded-xl px-4 py-2 text-[10px] font-black uppercase focus:outline-none">
               <option value="modified">Recency</option>
               <option value="loc">Volume</option>
             </select>
             <select value={filterType} onChange={(e) => setFilterType(e.target.value)} className="bg-white/5 border border-white/10 rounded-xl px-4 py-2 text-[10px] font-black uppercase focus:outline-none">
               <option value="all">All Clusters</option>
               <option value="web app">Apps</option>
             </select>
             <ViewSwitcher mode={viewMode} setMode={setViewMode} />
          </div>
        </div>

        {/* MAIN FEED (FULL WIDTH) */}
        <div className="space-y-12">
          <div className="flex items-center gap-4">
             <h2 className="text-2xl font-black italic uppercase tracking-tighter">Intelligence Feed</h2>
             <div className="h-[1px] flex-1 bg-white/5" />
          </div>

          {viewMode === 'board' ? (
            <div className="flex gap-8 overflow-x-auto pb-12 snap-x scrollbar-hide">
              {Object.entries(clusteredProjects).map(([cluster, clusterProjects]) => (
                <div key={cluster} className="min-w-[400px] snap-start space-y-6">
                  <div className="flex items-center justify-between px-6 py-3 bg-white/5 rounded-2xl border border-white/10">
                    <h3 className="text-xs font-black uppercase tracking-[0.2em]">{cluster}</h3>
                    <span className="text-[10px] font-black text-accent">{clusterProjects.length}</span>
                  </div>
                  <div className="space-y-6">
                    {clusterProjects.map((p, i) => <ProjectCard key={p.path} project={p} index={i} view="grid" />)}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className={cn(
              "grid gap-8",
              viewMode === 'grid' ? "grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4" : "grid-cols-1"
            )}>
              <AnimatePresence mode="popLayout">
                {filteredProjects.map((p, i) => <ProjectCard key={p.path} project={p} index={i} view={viewMode} />)}
              </AnimatePresence>
            </div>
          )}
        </div>

        {/* Dependency Nebula (Horizontal Footer) */}
        <div className="mt-24 pt-12 border-t border-white/5">
           <h3 className="text-[10px] font-black uppercase tracking-[0.4em] text-white/20 mb-8">Nexus: Internal Dependency Nebula</h3>
           <div className="flex flex-wrap gap-4">
              {projects.filter(p => p.internal_deps?.length > 0).map(p => (
                <div key={p.path} className="bg-white/5 px-4 py-3 rounded-xl border border-white/5 flex items-center gap-3">
                  <Box size={14} className="text-accent" />
                  <span className="text-[10px] font-black uppercase">{p.path.split('/').pop()}</span>
                  <ChevronRight size={10} className="text-white/20" />
                  <div className="flex gap-2">
                    {p.internal_deps.map(d => <span key={d} className="text-[9px] text-accent/60 font-bold">{d}</span>)}
                  </div>
                </div>
              ))}
           </div>
        </div>

      </div>
    </main>
  );
}
