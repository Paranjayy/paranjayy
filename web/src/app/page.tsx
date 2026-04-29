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
  Info
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

const FloatingDock = ({ mode, setMode }: { mode: string; setMode: (m: string) => void }) => (
  <div className="fixed bottom-10 left-1/2 -translate-x-1/2 z-50">
    <motion.div 
      initial={{ y: 100, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      className="flex bg-black/60 backdrop-blur-2xl p-2 rounded-3xl border border-white/10 shadow-[0_20px_50px_rgba(0,0,0,0.5)] ring-1 ring-white/5"
    >
      {[
        { id: 'grid', icon: Layout, label: 'Grid', color: 'text-accent' },
        { id: 'table', icon: TableIcon, label: 'Notion', color: 'text-blue-400' },
        { id: 'board', icon: Columns, label: 'Kanban', color: 'text-green-400' }
      ].map((item) => (
        <button
          key={item.id}
          onClick={() => setMode(item.id)}
          className={cn(
            "relative flex flex-col items-center gap-1 px-6 py-3 rounded-2xl transition-all duration-300",
            mode === item.id ? "bg-white/10 scale-110 shadow-inner" : "text-white/40 hover:text-white hover:bg-white/5"
          )}
        >
          {mode === item.id && (
            <motion.div 
              layoutId="dock-bg"
              className="absolute inset-0 bg-white/5 rounded-2xl"
              transition={{ type: 'spring', bounce: 0.2, duration: 0.6 }}
            />
          )}
          <item.icon size={20} className={cn("transition-colors", mode === item.id ? item.color : "text-current")} />
          <span className="text-[9px] font-black uppercase tracking-[0.2em]">{item.label}</span>
        </button>
      ))}
    </motion.div>
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
        className="group flex items-center gap-6 p-3 rounded-xl hover:bg-white/5 transition-all cursor-pointer border border-transparent hover:border-white/10"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <div className="w-10 h-10 rounded-xl bg-white/5 flex items-center justify-center text-white/20 group-hover:text-accent group-hover:bg-accent/10 transition-all">
          <Code size={18} />
        </div>
        <div className="flex-1 min-w-0">
          <h4 className="text-sm font-bold text-white/90 truncate">{relPath}</h4>
          <div className="flex items-center gap-2 mt-0.5">
            <span className="text-[9px] font-black uppercase text-accent/60 italic">{project.proj_type}</span>
            <span className="text-[10px] text-white/20 font-mono truncate">{project.path}</span>
          </div>
        </div>
        <div className="hidden xl:flex items-center gap-12 text-xs font-mono text-white/40">
           <div className="w-24 text-right">{project.total_loc.toLocaleString()} <span className="text-[8px] opacity-50 uppercase">LOC</span></div>
           <div className="w-20 text-center">
             <div className={cn(
               "px-2 py-0.5 rounded-full text-[9px] font-bold uppercase",
               project.health > 85 ? "bg-green-500/10 text-green-400 border border-green-500/20" : "bg-red-500/10 text-red-400 border border-red-500/20"
             )}>
               {project.health}%
             </div>
           </div>
           <div className="w-24 flex items-center gap-2">
             {project.unpushed && <ArrowUpDown size={12} className="text-accent-secondary" />}
             {project.uncommitted && <AlertCircle size={12} className="text-yellow-400" />}
             <span className="text-[10px]">{new Date(project.last_modified * 1000).toLocaleDateString()}</span>
           </div>
        </div>
      </motion.div>
    );
  }

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.01 }}
      onClick={() => setIsExpanded(!isExpanded)}
      className={cn(
        "glass-card group relative overflow-hidden cursor-pointer p-6 transition-all duration-500",
        isExpanded ? "md:col-span-2 bg-white/10 ring-2 ring-accent/20" : "hover:bg-white/5",
        isGhost && !isExpanded && "opacity-60 grayscale-[0.5] hover:grayscale-0 hover:opacity-100"
      )}
    >
      <div className="flex justify-between items-start mb-6">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-2">
            <span className="text-[10px] uppercase font-black tracking-widest text-accent bg-accent/10 px-2 py-0.5 rounded-md">
              {primaryLang}
            </span>
            {project.uncommitted && project.uncommitted > 0 && (
              <span className="text-[9px] font-black text-yellow-400 bg-yellow-400/10 px-2 py-0.5 rounded-md">
                MODIFIED
              </span>
            )}
          </div>
          <h4 className="text-xl font-black truncate tracking-tight">{relPath}</h4>
        </div>
        <div className="flex flex-col items-end gap-1">
          <div className={cn(
            "text-2xl font-black italic tracking-tighter leading-none",
            project.health > 85 ? "text-green-400" : project.health > 60 ? "text-yellow-400" : "text-red-400"
          )}>
            {project.health}%
          </div>
          <span className="text-[9px] font-black text-white/20 uppercase tracking-widest">Health Score</span>
        </div>
      </div>

      <div className="space-y-4">
        <div className="grid grid-cols-2 gap-4 text-xs font-mono">
           <div className="bg-white/5 p-2 rounded-lg border border-white/5">
             <p className="text-[9px] text-white/30 uppercase mb-1">Volume</p>
             <p className="font-black text-white/80">{project.total_loc.toLocaleString()} LOC</p>
           </div>
           <div className="bg-white/5 p-2 rounded-lg border border-white/5">
             <p className="text-[9px] text-white/30 uppercase mb-1">Activity</p>
             <p className="font-black text-white/80">{project.recent_commits} Commits</p>
           </div>
        </div>

        <div className="flex gap-1 h-1.5 rounded-full overflow-hidden bg-white/5">
          {project.activity_7d?.map((count, i) => (
            <div 
              key={i} 
              className={cn(
                "flex-1 transition-all",
                count > 0 ? "bg-accent" : "bg-white/5"
              )}
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
              className="pt-6 border-t border-white/10 mt-6 space-y-6"
              onClick={(e) => e.stopPropagation()}
            >
              {project.preview_image && (
                <div className="relative aspect-video rounded-2xl overflow-hidden border border-white/10 shadow-2xl">
                  <img src={`/previews/${project.preview_image}`} alt="" className="w-full h-full object-cover" />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent" />
                </div>
              )}

              <div className="bg-accent/5 rounded-2xl p-4 border border-accent/10">
                <p className="text-[10px] text-accent font-black uppercase mb-2 flex items-center gap-2">
                  <Fingerprint size={12} /> Workspace Intelligence Narrative
                </p>
                <p className="text-sm text-white/70 italic leading-relaxed font-serif">
                  "{project.narrative || "System scanning... Node analysis pending manual audit."}"
                </p>
              </div>

              <div className="flex flex-wrap gap-2">
                <button className="flex-1 flex items-center justify-center gap-2 bg-white/5 hover:bg-accent hover:text-black py-3 rounded-xl text-[10px] font-black uppercase transition-all ring-1 ring-white/10">
                  <FileText size={14} /> AI README
                </button>
                <button className="flex-1 flex items-center justify-center gap-2 bg-white/5 hover:bg-green-500 hover:text-black py-3 rounded-xl text-[10px] font-black uppercase transition-all ring-1 ring-white/10">
                  <Shield size={14} /> Harden
                </button>
                <button className="flex-1 flex items-center justify-center gap-2 bg-white/5 hover:bg-red-500 hover:text-black py-3 rounded-xl text-[10px] font-black uppercase transition-all ring-1 ring-white/10">
                  <Trash2 size={14} /> Archive
                </button>
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
    const totalTechDebt = projects.reduce((acc, p) => acc + p.tech_debt_count, 0);
    const criticalRepos = projects.filter(p => p.env_exposed).length;
    const pendingRepos = projects.filter(p => (p.uncommitted || 0) > 0 || (p.unpushed || 0) > 0).length;
    
    const totalCamel = projects.reduce((acc, p) => acc + (p.naming?.camel || 0), 0);
    const totalSnake = projects.reduce((acc, p) => acc + (p.naming?.snake || 0), 0);
    const personality = totalCamel > totalSnake ? "Modern Architect" : "Legacy Explorer";

    return { 
      totalLoc, 
      totalTechDebt, 
      criticalRepos, 
      pendingRepos,
      count: projects.length, 
      personality
    };
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
      if (sortBy === 'health') return b.health - a.health;
      if (sortBy === 'debt') return b.tech_debt_count - a.tech_debt_count;
      return 0;
    });

  const clusteredProjects = useMemo(() => {
    const clusters: Record<string, Project[]> = {};
    filteredProjects.forEach(p => {
      const parts = p.path.split('/');
      const clusterName = parts[parts.length - 2] || 'Root';
      if (!clusters[clusterName]) clusters[clusterName] = [];
      clusters[clusterName].push(p);
    });
    return clusters;
  }, [filteredProjects]);

  return (
    <main className="min-h-screen gradient-bg p-6 lg:p-16 pb-32">
      <FloatingDock mode={viewMode} setMode={setViewMode} />

      <div className="max-w-[1600px] mx-auto">
        {/* Header Section */}
        <div className="flex flex-col lg:flex-row justify-between items-start gap-12 mb-16">
          <div className="flex-1">
            <motion.div 
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              className="flex items-center gap-6 mb-6"
            >
              <div className="w-16 h-16 rounded-[2rem] bg-accent flex items-center justify-center shadow-[0_0_50px_rgba(168,85,247,0.4)] rotate-6 border-4 border-white/10">
                <Zap className="text-white fill-white" size={32} />
              </div>
              <div>
                <h1 className="text-7xl font-black tracking-tighter uppercase italic leading-none">
                  Ideaverse Hub
                </h1>
                <p className="text-white/40 mt-2 text-xl italic font-serif">
                  Recursive Workspace Intelligence Orchestrator.
                </p>
              </div>
            </motion.div>
          </div>

          <motion.div 
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="glass-card p-6 border-accent/20 bg-accent/5 flex items-center gap-6 min-w-[350px]"
          >
            <div className="w-16 h-16 rounded-full border-2 border-accent/30 flex items-center justify-center bg-black/40">
              <Fingerprint className="text-accent" size={32} />
            </div>
            <div>
              <p className="text-[10px] uppercase tracking-widest text-accent font-black mb-1">Coding Persona</p>
              <h2 className="text-2xl font-black italic uppercase tracking-tighter">{stats.personality}</h2>
              <p className="text-xs text-white/30">Vibe analysis complete.</p>
            </div>
          </motion.div>
        </div>

        {/* Controls Section */}
        <div className="flex flex-col xl:flex-row gap-6 mb-16 items-center">
          <div className="relative flex-1 w-full group">
            <Search className="absolute left-6 top-1/2 -translate-y-1/2 text-white/20 group-focus-within:text-accent transition-colors" size={24} />
            <input 
              type="text"
              placeholder="Query the Ideaverse (Path, Keywords, Language)..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full bg-white/5 border border-white/10 rounded-[2.5rem] py-7 pl-16 pr-8 focus:outline-none focus:ring-4 focus:ring-accent/20 transition-all backdrop-blur-3xl text-2xl font-mono shadow-2xl"
            />
          </div>
          
          <div className="flex gap-4 w-full xl:w-auto">
             <div className="flex-1 xl:flex-none flex items-center gap-3 bg-white/5 border border-white/10 rounded-[2rem] px-8 py-5 hover:bg-white/10 transition-all cursor-pointer group">
               <ArrowUpDown size={20} className="text-accent transition-transform group-hover:rotate-180" />
               <select value={sortBy} onChange={(e) => setSortBy(e.target.value)} className="bg-transparent text-xs font-black uppercase tracking-widest focus:outline-none cursor-pointer">
                 <option value="modified">Recency</option>
                 <option value="loc">Volume</option>
                 <option value="health">Health</option>
               </select>
             </div>
             <div className="flex-1 xl:flex-none flex items-center gap-3 bg-white/5 border border-white/10 rounded-[2rem] px-8 py-5 hover:bg-white/10 transition-all cursor-pointer group">
               <Filter size={20} className="text-accent transition-transform group-hover:scale-125" />
               <select value={filterType} onChange={(e) => setFilterType(e.target.value)} className="bg-transparent text-xs font-black uppercase tracking-widest focus:outline-none cursor-pointer">
                 <option value="all">Clusters</option>
                 <option value="web app">Apps</option>
                 <option value="extension">Exts</option>
               </select>
             </div>
          </div>
        </div>

        {/* Top Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-8 mb-20">
          {[
            { label: 'Orbiters', value: stats.count, color: 'text-accent', bg: 'bg-accent/5' },
            { label: 'Ecosystem LOC', value: `${(stats.totalLoc / 1000000).toFixed(1)}M`, color: 'text-blue-400', bg: 'bg-blue-400/5' },
            { label: 'Pending Backlog', value: stats.pendingRepos, color: 'text-yellow-400', bg: 'bg-yellow-400/5' },
            { label: 'Security Risks', value: stats.criticalRepos, color: 'text-red-400', bg: 'bg-red-400/5' }
          ].map((stat, i) => (
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
              key={stat.label} 
              className={cn("glass-card p-8 border-white/5 relative group", stat.bg)}
            >
              <div className="absolute top-0 right-0 p-4 opacity-5 group-hover:opacity-20 transition-opacity">
                <Activity size={80} />
              </div>
              <p className="text-[11px] font-black uppercase tracking-[0.3em] opacity-40 mb-3">{stat.label}</p>
              <div className={cn("text-5xl font-black italic tracking-tighter", stat.color)}>{stat.value}</div>
            </motion.div>
          ))}
        </div>

        {/* Main Content Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12">
          {/* Feed Column */}
          <div className="lg:col-span-8 space-y-12">
            <div className="flex items-center justify-between border-b border-white/10 pb-8">
              <h2 className="text-4xl font-black italic uppercase tracking-tighter flex items-center gap-4">
                <Activity size={40} className="text-accent" />
                Intelligence Feed
              </h2>
              <div className="flex items-center gap-4">
                <span className="text-xs font-black text-white/30 uppercase tracking-[0.2em]">{stats.count} ACTIVE SIGNALS</span>
                <div className="flex gap-1.5">
                  <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse shadow-[0_0_10px_rgba(34,197,94,0.5)]" />
                  <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse [animation-delay:200ms]" />
                </div>
              </div>
            </div>

            {viewMode === 'board' ? (
              <div className="flex gap-8 overflow-x-auto pb-12 snap-x scrollbar-hide">
                {Object.entries(clusteredProjects).map(([cluster, clusterProjects]) => (
                  <div key={cluster} className="min-w-[420px] snap-start space-y-8">
                    <div className="flex items-center justify-between px-6 py-4 bg-white/5 rounded-3xl border border-white/10 backdrop-blur-xl">
                      <h3 className="text-sm font-black uppercase tracking-widest text-white flex items-center gap-4">
                        <Layers size={20} className="text-accent" />
                        {cluster}
                      </h3>
                      <span className="text-xs font-black text-accent bg-accent/20 px-3 py-1 rounded-xl ring-1 ring-accent/30">{clusterProjects.length}</span>
                    </div>
                    <div className="space-y-8">
                      {clusterProjects.map((project, i) => (
                        <ProjectCard key={project.path} project={project} index={i} view="grid" />
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className={cn(
                "grid gap-8",
                viewMode === 'grid' ? "grid-cols-1 md:grid-cols-2" : "grid-cols-1"
              )}>
                <AnimatePresence mode="popLayout">
                  {filteredProjects.map((project, i) => (
                    <ProjectCard key={project.path} project={project} index={i} view={viewMode} />
                  ))}
                </AnimatePresence>
              </div>
            )}
          </div>

          {/* Sidebar Column (Action Deck) */}
          <div className="lg:col-span-4 space-y-12">
            <div className="glass-card p-8 border-accent/20 bg-accent/5 sticky top-10">
              <h3 className="text-xl font-black uppercase italic tracking-tighter flex items-center gap-3 mb-8">
                <Zap size={24} className="text-accent" />
                Action Deck
              </h3>
              
              <div className="space-y-6">
                 {[
                   { id: 1, type: 'ALERT', msg: 'Missing LICENSE in Workout buddy', icon: ShieldAlert, color: 'text-red-400', bg: 'bg-red-400/10' },
                   { id: 2, type: 'WARN', msg: 'High tech debt in Learning OS', icon: AlertTriangle, color: 'text-yellow-400', bg: 'bg-yellow-400/10' },
                   { id: 3, type: 'TASK', msg: 'Sync social hub with local repo', icon: Info, color: 'text-blue-400', bg: 'bg-blue-400/10' }
                 ].map(item => (
                   <div key={item.id} className="flex gap-4 p-4 rounded-2xl bg-white/5 border border-white/5 hover:border-white/10 transition-all cursor-pointer group">
                     <div className={cn("w-10 h-10 rounded-xl flex items-center justify-center shrink-0", item.bg, item.color)}>
                       <item.icon size={20} />
                     </div>
                     <div>
                       <p className={cn("text-[9px] font-black uppercase tracking-widest mb-1", item.color)}>{item.type}</p>
                       <p className="text-xs text-white/70 font-medium group-hover:text-white transition-colors">{item.msg}</p>
                     </div>
                   </div>
                 ))}
              </div>

              <div className="mt-12 pt-8 border-t border-white/10">
                <h4 className="text-[11px] font-black uppercase tracking-widest text-white/30 mb-6">System Status</h4>
                <div className="space-y-4">
                  <div className="flex justify-between items-center text-xs">
                    <span className="text-white/50">Intelligence Core</span>
                    <span className="text-green-400 font-bold flex items-center gap-2">
                      <div className="w-1.5 h-1.5 bg-green-400 rounded-full animate-pulse" />
                      OPERATIONAL
                    </span>
                  </div>
                  <div className="flex justify-between items-center text-xs">
                    <span className="text-white/50">Vercel Pipeline</span>
                    <span className="text-blue-400 font-bold">STABLE</span>
                  </div>
                  <div className="flex justify-between items-center text-xs">
                    <span className="text-white/50">Sync Engine</span>
                    <span className="text-accent font-bold">IDLE</span>
                  </div>
                </div>
              </div>

              <button className="w-full mt-12 bg-white text-black py-4 rounded-2xl font-black uppercase text-xs tracking-[0.2em] hover:bg-accent hover:text-white transition-all shadow-[0_10px_30px_rgba(255,255,255,0.1)]">
                Initialize System Audit
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
