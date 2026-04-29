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
  Target
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
  const roi = (project.recent_commits * 100) / (project.total_loc / 1000 + 1);
  
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
      {roi > 50 && (
         <div className="absolute top-0 right-0 p-2 bg-accent/20 text-accent text-[8px] font-black uppercase tracking-tighter rounded-bl-xl border-l border-b border-white/10">
            🔥 HIGH ROI
         </div>
      )}

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

        <div className="flex flex-wrap gap-2">
           {Object.keys(project.loc_breakdown).slice(0, 3).map(lang => (
             <span key={lang} className="text-[8px] font-black px-2 py-0.5 rounded bg-white/5 text-white/40 uppercase tracking-widest">
               {lang}
             </span>
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
              <div className="grid grid-cols-2 gap-4 text-[10px] font-mono text-white/40">
                 <div className="flex justify-between"><span>VOLUME</span> <span className="text-white">{project.total_loc.toLocaleString()}</span></div>
                 <div className="flex justify-between"><span>VELOCITY</span> <span className="text-white">{Math.round(roi)} ROI</span></div>
                 <div className="flex justify-between"><span>NAMING</span> <span className="text-white">{project.naming.camel > project.naming.snake ? 'Camel' : 'Snake'}</span></div>
                 <div className="flex justify-between"><span>STATUS</span> <span className="text-accent">{project.unpushed ? 'UNPUSHED' : 'SYNCED'}</span></div>
              </div>
              <div className="flex flex-wrap gap-2">
                <button className="flex-1 bg-white/5 hover:bg-accent hover:text-black py-3 rounded-xl text-[10px] font-black uppercase transition-all">AI README</button>
                <button className="flex-1 bg-white/5 hover:bg-green-500 hover:text-black py-3 rounded-xl text-[10px] font-black uppercase transition-all">Harden</button>
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
  
  const projects = (portfolioData.projects || []) as unknown as Project[];

  const stats = useMemo(() => {
    const totalLoc = projects.reduce((acc, p) => acc + p.total_loc, 0);
    const criticalRepos = projects.filter(p => p.env_exposed).length;
    const pendingRepos = projects.filter(p => (p.uncommitted || 0) > 0 || (p.unpushed || 0) > 0).length;
    const highRoiRepos = projects.filter(p => ((p.recent_commits * 100) / (p.total_loc / 1000 + 1)) > 50).length;
    return { totalLoc, criticalRepos, pendingRepos, count: projects.length, highRoiRepos };
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
      if (sortBy === 'roi') {
        const roiA = (a.recent_commits * 100) / (a.total_loc / 1000 + 1);
        const roiB = (b.recent_commits * 100) / (b.total_loc / 1000 + 1);
        return roiB - roiA;
      }
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
        
        {/* HEADER SECTION */}
        <div className="flex flex-col xl:flex-row justify-between items-center gap-8 mb-16">
          <div className="flex items-center gap-6">
            <div className="w-16 h-16 rounded-[2rem] bg-accent flex items-center justify-center shadow-2xl shadow-accent/40 rotate-12 border-2 border-white/20">
              <Zap className="text-white fill-white" size={32} />
            </div>
            <div>
              <h1 className="text-6xl font-black tracking-tighter uppercase italic leading-none">Ideaverse Hub</h1>
              <p className="text-white/30 text-sm font-black uppercase tracking-[0.4em] mt-2">Workspace Intelligence v4.0</p>
            </div>
          </div>

          <div className="flex gap-6">
             <div className="flex items-center gap-3 bg-white/5 border border-white/10 px-6 py-4 rounded-3xl">
                <div className="w-10 h-10 rounded-full bg-green-500/20 flex items-center justify-center text-green-400">
                   <Target size={20} />
                </div>
                <div>
                   <p className="text-[10px] font-black uppercase text-white/40">Efficiency</p>
                   <p className="text-xl font-black italic tracking-tighter">OPTIMIZED</p>
                </div>
             </div>
             <div className="flex items-center gap-3 bg-white/5 border border-white/10 px-6 py-4 rounded-3xl">
                <div className="w-10 h-10 rounded-full bg-blue-500/20 flex items-center justify-center text-blue-400">
                   <Activity size={20} />
                </div>
                <div>
                   <p className="text-[10px] font-black uppercase text-white/40">Status</p>
                   <p className="text-xl font-black italic tracking-tighter">STABLE</p>
                </div>
             </div>
          </div>
        </div>

        {/* INTELLIGENCE GRID */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
           <div className="glass-card p-8 border-accent/20 bg-accent/5 relative overflow-hidden group">
              <div className="flex justify-between items-start mb-6">
                 <div className="p-3 bg-accent/20 rounded-2xl text-accent"><Activity size={24}/></div>
                 <span className="text-[10px] font-black text-accent uppercase tracking-widest">Ecosystem</span>
              </div>
              <h3 className="text-4xl font-black italic uppercase tracking-tighter mb-2">{stats.count} Orbits</h3>
              <p className="text-white/40 text-[10px] font-black uppercase tracking-widest">Active Mac Discovery</p>
              <div className="absolute -bottom-6 -right-6 opacity-5 group-hover:opacity-10 transition-all"><Activity size={120}/></div>
           </div>

           <div className="glass-card p-8 border-blue-500/20 bg-blue-500/5 relative overflow-hidden group">
              <div className="flex justify-between items-start mb-6">
                 <div className="p-3 bg-blue-500/20 rounded-2xl text-blue-400"><Code2 size={24}/></div>
                 <span className="text-[10px] font-black text-blue-400 uppercase tracking-widest">Skill Matrix</span>
              </div>
              <div className="space-y-4">
                 {Object.entries(portfolioData.skills_matrix || {}).slice(0, 3).map(([lang, percent]) => (
                   <div key={lang} className="space-y-1">
                      <div className="flex justify-between text-[9px] font-black uppercase text-white/60">
                         <span>{lang}</span>
                         <span>{Math.round(percent as number)}%</span>
                      </div>
                      <div className="h-1.5 bg-white/5 rounded-full overflow-hidden">
                         <motion.div 
                           initial={{ width: 0 }}
                           animate={{ width: `${percent}%` }}
                           className="h-full bg-blue-500 shadow-[0_0_10px_rgba(59,130,246,0.5)]" 
                         />
                      </div>
                   </div>
                 ))}
              </div>
           </div>

           <div className="glass-card p-8 border-yellow-500/20 bg-yellow-500/5 relative overflow-hidden group">
              <div className="flex justify-between items-start mb-6">
                 <div className="p-3 bg-yellow-500/20 rounded-2xl text-yellow-500"><TrendingUp size={24}/></div>
                 <span className="text-[10px] font-black text-yellow-500 uppercase tracking-widest">Efficiency</span>
              </div>
              <h3 className="text-4xl font-black italic uppercase tracking-tighter mb-2">{stats.highRoiRepos} High ROI</h3>
              <p className="text-white/40 text-[10px] font-black uppercase tracking-widest">Velocity Grade: A+</p>
              <div className="absolute -bottom-6 -right-6 opacity-5 group-hover:opacity-10 transition-all"><TrendingUp size={120}/></div>
           </div>

           <div className="glass-card p-8 border-red-500/20 bg-red-500/5 relative overflow-hidden group">
              <div className="flex justify-between items-start mb-6">
                 <div className="p-3 bg-red-500/20 rounded-2xl text-red-400"><ShieldAlert size={24}/></div>
                 <span className="text-[10px] font-black text-red-400 uppercase tracking-widest">Security</span>
              </div>
              <h3 className="text-4xl font-black italic uppercase tracking-tighter mb-2">{stats.criticalRepos} Risks</h3>
              <p className="text-white/40 text-[10px] font-black uppercase tracking-widest">Environment Shield: ACTIVE</p>
              <div className="absolute -bottom-6 -right-6 opacity-5 group-hover:opacity-10 transition-all"><ShieldAlert size={120}/></div>
           </div>
        </div>

        {/* SEARCH & CONTROLS */}
        <div className="glass-card p-4 rounded-[2.5rem] border-white/10 bg-white/[0.03] mb-16 flex flex-col md:flex-row gap-4 items-center ring-1 ring-white/5 shadow-2xl">
          <div className="relative flex-1 w-full">
            <Search className="absolute left-6 top-1/2 -translate-y-1/2 text-white/20" size={20} />
            <input 
              type="text"
              placeholder="Query the Workspace..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full bg-transparent py-4 pl-14 pr-8 focus:outline-none text-2xl font-mono tracking-tighter"
            />
          </div>
          <div className="flex items-center gap-4 w-full md:w-auto">
             <select value={sortBy} onChange={(e) => setSortBy(e.target.value)} className="bg-white/5 border border-white/10 rounded-2xl px-6 py-3 text-[10px] font-black uppercase tracking-widest focus:ring-2 focus:ring-accent outline-none">
               <option value="modified">Recency</option>
               <option value="loc">Volume</option>
               <option value="roi">Velocity ROI</option>
             </select>
             <ViewSwitcher mode={viewMode} setMode={setViewMode} />
          </div>
        </div>

        {/* MAIN FEED */}
        <div className="space-y-12">
          <div className="flex items-center gap-4">
             <h2 className="text-3xl font-black italic uppercase tracking-tighter">Intelligence Feed</h2>
             <div className="h-[1px] flex-1 bg-gradient-to-r from-white/10 to-transparent" />
          </div>

          {viewMode === 'board' ? (
            <div className="flex gap-8 overflow-x-auto pb-12 snap-x scrollbar-hide">
              {Object.entries(clusteredProjects).map(([cluster, clusterProjects]) => (
                <div key={cluster} className="min-w-[450px] snap-start space-y-6">
                  <div className="flex items-center justify-between px-8 py-4 bg-white/5 rounded-3xl border border-white/10">
                    <h3 className="text-xs font-black uppercase tracking-[0.3em]">{cluster}</h3>
                    <span className="bg-accent/20 text-accent text-[10px] font-black px-3 py-1 rounded-full">{clusterProjects.length}</span>
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

        {/* DYNAMIC FOOTER: Ecosystem Stats */}
        <div className="mt-32 pt-16 border-t border-white/10 grid grid-cols-1 md:grid-cols-3 gap-12 pb-20 grayscale opacity-40 hover:grayscale-0 hover:opacity-100 transition-all duration-700">
           <div>
              <p className="text-[10px] font-black uppercase tracking-[0.4em] mb-6">Omniscient Diagnostics</p>
              <div className="space-y-4">
                 <div className="flex justify-between text-xs font-mono"><span>Total LOC</span> <span>{stats.totalLoc.toLocaleString()}</span></div>
                 <div className="flex justify-between text-xs font-mono"><span>Orbits Detected</span> <span>{stats.count}</span></div>
                 <div className="flex justify-between text-xs font-mono"><span>Efficiency Rating</span> <span className="text-accent">A+</span></div>
              </div>
           </div>
           <div>
              <p className="text-[10px] font-black uppercase tracking-[0.4em] mb-6">Nexus Nebula</p>
              <div className="flex flex-wrap gap-2">
                 {projects.filter(p => p.internal_deps?.length > 0).slice(0, 10).map(p => (
                   <span key={p.path} className="text-[8px] font-black px-2 py-1 rounded border border-white/10">{p.path.split('/').pop()}</span>
                 ))}
              </div>
           </div>
           <div className="text-right flex flex-col justify-end">
              <p className="text-[10px] font-black uppercase tracking-[0.4em]">Ideaverse OS v4.0</p>
              <p className="text-[9px] font-mono mt-2">© 2026 Paranjay Khachar. All Rights Reserved.</p>
           </div>
        </div>

      </div>
    </main>
  );
}
