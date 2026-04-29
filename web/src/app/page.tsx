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
  HardDrive
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

const ViewToggle = ({ mode, setMode }: { mode: string; setMode: (m: string) => void }) => (
  <div className="flex bg-white/5 p-1 rounded-xl border border-white/10 backdrop-blur-md">
    {[
      { id: 'grid', icon: Layout, label: 'Grid' },
      { id: 'table', icon: TableIcon, label: 'Table' },
      { id: 'board', icon: Columns, label: 'Board' }
    ].map((item) => (
      <button
        key={item.id}
        onClick={() => setMode(item.id)}
        className={cn(
          "flex items-center gap-2 px-4 py-2 rounded-lg text-[10px] font-black uppercase tracking-widest transition-all",
          mode === item.id ? "bg-accent text-black shadow-lg shadow-accent/20" : "text-white/40 hover:text-white"
        )}
      >
        <item.icon size={14} />
        {item.label}
      </button>
    ))}
  </div>
);

const ProjectCard = ({ project, index, view }: { project: Project; index: number; view: string }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const relPath = project.path.split('/').pop() || 'Untitled';
  const lastModDate = new Date(project.last_modified * 1000);
  const lastMod = lastModDate.toLocaleDateString();
  const isGhost = (Date.now() - lastModDate.getTime()) > (30 * 24 * 60 * 60 * 1000);
  const primaryLang = Object.entries(project.loc_breakdown || {}).sort((a,b) => b[1] - a[1])[0]?.[0] || 'Unknown';
  
  if (view === 'table') {
    return (
      <motion.div 
        layout
        initial={{ opacity: 0, x: -10 }}
        animate={{ opacity: 1, x: 0 }}
        className="flex items-center gap-4 p-4 border-b border-white/5 hover:bg-white/[0.03] group transition-colors cursor-pointer"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <div className="w-8 h-8 rounded-lg bg-white/5 flex items-center justify-center text-accent">
          <Code size={16} />
        </div>
        <div className="flex-1 min-w-0">
          <h4 className="text-sm font-bold truncate">{relPath}</h4>
          <p className="text-[10px] text-white/30 truncate">{project.path}</p>
        </div>
        <div className="hidden md:flex gap-4 items-center">
          <span className="text-[10px] font-mono text-white/40 w-24">LOC: {project.total_loc.toLocaleString()}</span>
          <div className={cn(
            "w-24 px-2 py-0.5 rounded text-[10px] font-bold text-center",
            project.health > 85 ? "bg-green-500/10 text-green-400" : "bg-red-500/10 text-red-400"
          )}>
            {project.health}%
          </div>
          <div className="flex gap-2 w-20">
            {project.unpushed && project.unpushed > 0 && <ArrowUpDown size={12} className="text-accent-secondary" />}
            {project.uncommitted && project.uncommitted > 0 && <AlertCircle size={12} className="text-yellow-400" />}
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
      transition={{ delay: index * 0.02 }}
      onClick={() => setIsExpanded(!isExpanded)}
      className={cn(
        "glass-card group relative overflow-hidden cursor-pointer p-5 transition-all duration-500",
        isExpanded ? "col-span-1 md:col-span-2 bg-white/10 ring-1 ring-accent/30" : "hover:bg-white/5",
        isGhost && !isExpanded && "opacity-60 grayscale-[0.5] hover:grayscale-0 hover:opacity-100"
      )}
    >
      <div className="absolute top-0 right-0 p-3 opacity-10 group-hover:opacity-20 transition-opacity">
        <Code2 size={isExpanded ? 120 : 40} />
      </div>

      <div className="flex justify-between items-start mb-4">
        <div className="flex flex-col">
          <div className="flex items-center gap-2 mb-1">
            <span className="text-[10px] uppercase tracking-widest text-accent font-black italic">
              {project.proj_type} // {primaryLang}
            </span>
            {isGhost && (
              <span className="text-[8px] bg-white/10 text-white/40 px-1.5 py-0.5 rounded flex items-center gap-1 font-bold">
                <Box size={8} /> GHOST
              </span>
            )}
          </div>
          <h4 className="text-lg font-bold truncate max-w-[200px]">{relPath}</h4>
        </div>
        <div className={cn(
          "px-2 py-1 rounded text-[10px] font-bold border flex items-center gap-1",
          project.health > 85 ? "bg-green-500/10 text-green-400 border-green-500/20" : 
          project.health > 60 ? "bg-yellow-500/10 text-yellow-400 border-yellow-500/20" : 
          "bg-red-500/10 text-red-400 border-red-500/20"
        )}>
          {project.health}%
          <TrendingUp size={10} />
        </div>
      </div>

      <div className="space-y-3">
        <div className="flex justify-between items-center text-xs text-white/60">
          <div className="flex gap-4">
            <span className="font-mono flex items-center gap-1"><Terminal size={10} /> {project.total_loc.toLocaleString()}</span>
            <span className="font-mono flex items-center gap-1"><Activity size={10} /> {project.tech_debt_count}</span>
          </div>
          <div className="flex gap-2">
            {project.uncommitted && project.uncommitted > 0 && (
              <span className="text-[9px] text-yellow-400 font-bold flex items-center gap-1">
                <AlertCircle size={10} /> {project.uncommitted} dirty
              </span>
            )}
            {project.unpushed && project.unpushed > 0 && (
              <span className="text-[9px] text-accent-secondary font-bold flex items-center gap-1">
                <ArrowUpDown size={10} /> {project.unpushed} unpushed
              </span>
            )}
          </div>
        </div>
        
        <div className="flex gap-1 h-2 rounded-full overflow-hidden bg-white/5">
          {project.activity_7d?.map((count, i) => (
            <div 
              key={i} 
              className={cn(
                "flex-1 transition-all",
                count > 0 ? "bg-accent" : "bg-white/5"
              )}
              style={{ opacity: count > 0 ? Math.min(0.3 + (count/5), 1) : 0.1 }}
            />
          ))}
        </div>

        <AnimatePresence>
          {isExpanded && (
            <motion.div 
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 'auto', opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              className="pt-4 border-t border-white/10 mt-4 space-y-4"
            >
              {project.preview_image && (
                <div className="relative aspect-video rounded-xl overflow-hidden border border-white/10 mb-4 group/img">
                  <img 
                    src={`/previews/${project.preview_image}`} 
                    alt="Project Preview" 
                    className="w-full h-full object-cover grayscale-[0.2] group-hover/img:grayscale-0 transition-all duration-700"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
                </div>
              )}

              <div className="bg-white/5 rounded-xl p-3 border border-white/5">
                <p className="text-[10px] text-accent font-bold uppercase mb-1 flex items-center gap-2">
                  <Fingerprint size={12} /> Narrative
                </p>
                <p className="text-sm text-white/80 italic leading-relaxed">
                  "{project.narrative || "No narrative generated for this node."}"
                </p>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <p className="text-[10px] text-white/40 uppercase">Naming Vibe</p>
                  <p className="text-xs font-mono">
                    {project.naming?.camel > project.naming?.snake ? "Pascal/CamelCase" : "Snake_Case_Loyalist"}
                  </p>
                </div>
                <div className="space-y-2">
                  <p className="text-[10px] text-white/40 uppercase">Intelligence Deck</p>
                  <div className="flex items-center gap-2 text-xs text-accent-secondary font-bold">
                    <Monitor size={12} />
                    {project.suggested_tool || "General Audit"}
                  </div>
                </div>
              </div>
              
              <div className="space-y-2">
                <p className="text-[10px] text-white/40 uppercase">Ecosystem Path</p>
                <p className="text-[10px] font-mono break-all opacity-60">{project.path}</p>
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
    const dirtyRepos = projects.filter(p => (p.uncommitted || 0) > 0 || (p.unpushed || 0) > 0).length;
    
    const totalCamel = projects.reduce((acc, p) => acc + (p.naming?.camel || 0), 0);
    const totalSnake = projects.reduce((acc, p) => acc + (p.naming?.snake || 0), 0);
    const personality = totalCamel > totalSnake ? "Modern Architect" : "Legacy Explorer";

    const globalKeywords: Record<string, number> = {};
    projects.forEach(p => {
      Object.entries(p.keywords || {}).forEach(([word, count]) => {
        globalKeywords[word] = (globalKeywords[word] || 0) + (count as number);
      });
    });
    const sortedKeywords = Object.entries(globalKeywords).sort((a, b) => b[1] - a[1]);

    return { 
      totalLoc, 
      totalTechDebt, 
      criticalRepos, 
      dirtyRepos,
      count: projects.length, 
      personality,
      globalKeywords: Object.fromEntries(sortedKeywords)
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
    <main className="min-h-screen gradient-bg p-8 lg:p-16">
      <div className="max-w-7xl mx-auto mb-16 flex flex-col lg:flex-row justify-between items-center gap-12">
        <div className="flex-1">
          <motion.div 
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="flex items-center gap-4 mb-4"
          >
            <div className="w-14 h-14 rounded-3xl bg-accent flex items-center justify-center shadow-2xl shadow-accent/40 rotate-12">
              <Zap className="text-white" size={32} />
            </div>
            <h1 className="text-6xl font-black tracking-tighter neon-text uppercase italic">
              Ideaverse Hub
            </h1>
          </motion.div>
          <p className="text-white/50 max-w-lg text-lg leading-relaxed italic">
            Automated workspace intelligence. Monitoring {stats.count} projects with recursive AI auditing.
          </p>
        </div>

        <motion.div 
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="glass-card p-6 border-accent/20 bg-accent/5 flex items-center gap-6"
        >
          <div className="w-16 h-16 rounded-full border-2 border-accent/30 flex items-center justify-center bg-black/40">
            <Fingerprint className="text-accent" size={32} />
          </div>
          <div>
            <p className="text-[10px] uppercase tracking-widest text-accent font-bold mb-1">Coding Persona</p>
            <h2 className="text-xl font-black italic uppercase tracking-tighter">{stats.personality}</h2>
            <p className="text-xs text-white/40">Based on naming patterns & LOC volume</p>
          </div>
        </motion.div>
      </div>

      <div className="max-w-7xl mx-auto mb-12 flex flex-col md:flex-row gap-6 items-end justify-between">
        <div className="flex-1 space-y-4">
          <div className="relative group">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-white/30 group-focus-within:text-accent transition-colors" size={18} />
            <input 
              type="text"
              placeholder="Search the Ideaverse..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full bg-white/5 border border-white/10 rounded-2xl py-4 pl-12 pr-4 focus:outline-none focus:ring-2 focus:ring-accent/50 transition-all backdrop-blur-xl text-lg font-mono"
            />
          </div>
          <div className="flex flex-wrap gap-4">
             <div className="flex items-center gap-2 bg-white/5 border border-white/10 rounded-xl px-4 py-2">
               <ArrowUpDown size={14} className="text-white/40" />
               <select value={sortBy} onChange={(e) => setSortBy(e.target.value)} className="bg-transparent text-[10px] font-black uppercase focus:outline-none">
                 <option value="modified">Recency</option>
                 <option value="loc">LOC</option>
                 <option value="health">Health</option>
                 <option value="debt">Debt</option>
               </select>
             </div>
             <div className="flex items-center gap-2 bg-white/5 border border-white/10 rounded-xl px-4 py-2">
               <Filter size={14} className="text-white/40" />
               <select value={filterType} onChange={(e) => setFilterType(e.target.value)} className="bg-transparent text-[10px] font-black uppercase focus:outline-none">
                 <option value="all">All Clusters</option>
                 <option value="web app">Web Apps</option>
                 <option value="extension">Extensions</option>
               </select>
             </div>
          </div>
        </div>
        <ViewToggle mode={viewMode} setMode={setViewMode} />
      </div>

      <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-6 mb-16">
        <div className="glass-card p-6 border-accent/20 bg-accent/5">
          <p className="text-[10px] text-accent font-black uppercase mb-1">Orbiters</p>
          <div className="text-3xl font-black italic">{stats.count}</div>
        </div>
        <div className="glass-card p-6 border-white/5">
          <p className="text-[10px] text-white/40 font-black uppercase mb-1">Ecosystem LOC</p>
          <div className="text-3xl font-black italic">{Math.round(stats.totalLoc/1000)}k</div>
        </div>
        <div className={cn("glass-card p-6 border-yellow-500/20", stats.dirtyRepos > 0 && "bg-yellow-500/5")}>
          <p className="text-[10px] text-yellow-500 font-black uppercase mb-1">Dirty Repos</p>
          <div className="text-3xl font-black italic">{stats.dirtyRepos}</div>
        </div>
        <div className={cn("glass-card p-6 border-red-500/20", stats.criticalRepos > 0 && "bg-red-500/5")}>
          <p className="text-[10px] text-red-500 font-black uppercase mb-1">Risks</p>
          <div className="text-3xl font-black italic">{stats.criticalRepos}</div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <h2 className="text-2xl font-black uppercase tracking-tighter italic flex items-center gap-3">
            <Activity size={28} className="text-accent" />
            Intelligence Feed
          </h2>
        </div>

        {viewMode === 'board' ? (
          <div className="flex gap-6 overflow-x-auto pb-8 snap-x">
            {Object.entries(clusteredProjects).map(([cluster, clusterProjects]) => (
              <div key={cluster} className="min-w-[350px] snap-start space-y-4">
                <div className="flex items-center justify-between px-2">
                  <h3 className="text-xs font-black uppercase tracking-widest text-white/60 flex items-center gap-2">
                    <Layers size={14} className="text-accent" />
                    {cluster}
                  </h3>
                  <span className="text-[10px] font-bold text-white/20">{clusterProjects.length}</span>
                </div>
                <div className="space-y-4">
                  {clusterProjects.map((project, i) => (
                    <ProjectCard key={project.path} project={project} index={i} view="grid" />
                  ))}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className={cn(
            "grid gap-6",
            viewMode === 'grid' ? "grid-cols-1 md:grid-cols-2 lg:grid-cols-3" : "grid-cols-1"
          )}>
            <AnimatePresence mode="popLayout">
              {filteredProjects.map((project, i) => (
                <ProjectCard key={project.path} project={project} index={i} view={viewMode} />
              ))}
            </AnimatePresence>
          </div>
        )}
      </div>
    </main>
  );
}
