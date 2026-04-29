"use client";

import React, { useState, useMemo, useEffect } from 'react';
import { motion, AnimatePresence, useScroll, useSpring } from 'framer-motion';
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
  ArrowUpRight,
  Eye,
  EyeOff,
  Settings,
  Microscope,
  Compass,
  Briefcase,
  User,
  Coffee,
  Globe,
  Dna,
  Hexagon,
  Sparkles
} from 'lucide-react';
import portfolioData from '@/data/portfolio.json';
import { cn } from '@/lib/utils';

interface Project {
  path: string;
  is_git: boolean;
  is_system?: boolean;
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
  arch_weight?: { dirs: number; files: number };
  uncommitted?: number;
  unpushed?: number;
}

const NoiseBackground = () => (
  <div className="fixed inset-0 pointer-events-none z-[100] opacity-[0.03] contrast-150 brightness-150" style={{ backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E")` }} />
);

const CustomCursor = () => {
  const [position, setPosition] = useState({ x: 0, y: 0 });
  const [isHovering, setIsHovering] = useState(false);

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      setPosition({ x: e.clientX, y: e.clientY });
    };
    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  return (
    <motion.div 
      className="fixed top-0 left-0 w-8 h-8 rounded-full border border-accent/30 pointer-events-none z-[999] mix-blend-difference hidden lg:block"
      animate={{ 
        x: position.x - 16, 
        y: position.y - 16,
        scale: isHovering ? 2.5 : 1,
        backgroundColor: isHovering ? 'rgba(var(--accent-rgb), 0.1)' : 'transparent'
      }}
      transition={{ type: 'spring', damping: 20, stiffness: 250, mass: 0.5 }}
    />
  );
};

const ViewSwitcher = ({ mode, setMode }: { mode: string; setMode: (m: string) => void }) => (
  <div className="flex bg-white/5 p-1 rounded-full border border-white/10 backdrop-blur-3xl ring-1 ring-white/5">
    {[
      { id: 'grid', icon: Layout, label: 'Grid' },
      { id: 'table', icon: TableIcon, label: 'Technical' },
      { id: 'board', icon: Columns, label: 'Status' },
      { id: 'gallery', icon: Monitor, label: 'Showcase' }
    ].map((item) => (
      <button
        key={item.id}
        onClick={() => setMode(item.id)}
        className={cn(
          "px-4 py-2 rounded-full transition-all duration-500 flex items-center gap-2",
          mode === item.id ? "bg-white text-black scale-105 shadow-[0_0_20px_rgba(255,255,255,0.2)]" : "text-white/20 hover:text-white"
        )}
      >
        <item.icon size={12} />
        <span className="text-[10px] font-black uppercase tracking-widest">{item.label}</span>
      </button>
    ))}
  </div>
);

const ProjectCard = ({ project, index, view }: { project: Project; index: number; view: string }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const relPath = project.path.split('/').pop() || 'Untitled';
  const primaryLang = Object.entries(project.loc_breakdown || {}).sort((a,b) => b[1] - a[1])[0]?.[0] || 'Unknown';
  const roi = (project.recent_commits * 100) / (project.total_loc / 1000 + 1);
  
  if (view === 'gallery') {
    return (
      <motion.div 
        layout
        onClick={() => setIsExpanded(!isExpanded)}
        className="group relative aspect-[16/10] bg-[#080808] border border-white/5 overflow-hidden transition-all duration-700 hover:border-white/20 hover:shadow-[0_40px_100px_-20px_rgba(0,0,0,0.8)] cursor-pointer"
      >
        {project.preview_image ? (
           <img src={`/previews/${project.preview_image}`} alt={relPath} className="absolute inset-0 w-full h-full object-cover opacity-40 group-hover:opacity-90 transition-all duration-1000 group-hover:scale-105 group-hover:rotate-1" />
        ) : (
           <div className="absolute inset-0 flex items-center justify-center bg-[radial-gradient(#ffffff05_1px,transparent_1px)] [background-size:40px_40px]">
              <Code2 size={80} className="text-white/5 group-hover:text-accent/10 transition-all duration-1000 group-hover:scale-110" strokeWidth={0.3} />
           </div>
        )}
        <div className="absolute inset-0 bg-gradient-to-t from-black via-black/20 to-transparent opacity-80 group-hover:opacity-40 transition-opacity" />
        <div className="absolute inset-0 flex flex-col justify-end p-12 translate-y-4 group-hover:translate-y-0 transition-transform duration-700">
           <div className="flex justify-between items-end">
              <div className="space-y-3">
                 <p className="text-[10px] font-black uppercase tracking-[0.6em] text-accent/80 mb-2 flex items-center gap-3">
                    <Hexagon size={12} fill="currentColor" className="opacity-40" /> {primaryLang}
                 </p>
                 <h4 className="text-4xl font-black italic tracking-tighter uppercase leading-none group-hover:text-accent transition-colors drop-shadow-2xl">{relPath}</h4>
              </div>
              <div className="text-right">
                 <p className="text-[10px] font-black italic text-white/20 group-hover:text-white transition-colors">#{index.toString().padStart(2, '0')}</p>
              </div>
           </div>
        </div>
      </motion.div>
    );
  }

  if (view === 'table') {
     return (
        <div 
           onClick={() => setIsExpanded(!isExpanded)}
           className={cn(
              "group grid grid-cols-12 gap-8 items-center p-8 border-b border-white/5 hover:bg-white/[0.01] transition-all cursor-pointer relative overflow-hidden",
              project.is_system && "opacity-30"
           )}
        >
           <div className="col-span-4 flex items-center gap-6">
              <span className="text-[10px] font-mono text-white/10">{(index + 1).toString().padStart(3, '0')}</span>
              <h4 className="text-lg font-black italic tracking-tighter uppercase group-hover:text-accent transition-colors">{relPath}</h4>
           </div>
           <div className="col-span-2 text-[10px] font-black uppercase text-white/20 tracking-[0.4em]">{project.proj_type}</div>
           <div className="col-span-2 text-[10px] font-mono text-white/20">{(project.total_loc / 1000).toFixed(1)}K LOC</div>
           <div className="col-span-2 flex items-center gap-4">
              <div className="flex-1 h-[1px] bg-white/5 relative">
                 <div className="absolute top-0 left-0 h-full bg-accent" style={{ width: `${project.health}%` }} />
              </div>
              <span className="text-[10px] font-black italic text-white/30">{project.health}%</span>
           </div>
           <div className="col-span-2 flex justify-end">
              <ArrowUpRight size={16} className="text-white/10 group-hover:text-accent group-hover:translate-x-1 group-hover:-translate-y-1 transition-all" />
           </div>
        </div>
     );
  }

  return (
    <motion.div
      layout
      onClick={() => setIsExpanded(!isExpanded)}
      className={cn(
        "relative p-12 border border-white/5 bg-[#050505] group overflow-hidden transition-all duration-1000",
        isExpanded ? "md:col-span-2 border-accent/20 shadow-[0_60px_120px_rgba(0,0,0,0.9)]" : "hover:border-white/20 hover:bg-[#080808]",
        project.is_system && !isExpanded && "opacity-40 grayscale"
      )}
    >
      <div className="absolute inset-0 opacity-[0.02] pointer-events-none bg-[radial-gradient(#ffffff_1px,transparent_1px)] [background-size:30px_30px]" />
      
      <div className="relative flex justify-between items-start mb-24">
        <div className="space-y-4">
          <div className="flex items-center gap-8">
             <span className="text-[10px] font-black tracking-[0.6em] text-accent uppercase flex items-center gap-3">
                <Dna size={14} className="opacity-40" /> {primaryLang}
             </span>
             {project.is_system && <span className="text-[10px] font-black text-white/10 uppercase tracking-[0.4em] border border-white/5 px-3 py-1 rounded-full">SYSTEM</span>}
          </div>
          <h4 className="text-7xl font-black italic tracking-tighter leading-none uppercase translate-x-[-4px] group-hover:translate-x-0 transition-transform duration-1000">{relPath}</h4>
        </div>
        <div className="text-right">
           <p className="text-[10px] font-black uppercase text-white/10 tracking-[0.8em] mb-4">Diagnostics</p>
           <p className="text-5xl font-black italic tracking-tighter text-white/60 group-hover:text-accent transition-colors duration-700">{project.health}%</p>
        </div>
      </div>

      <div className="relative space-y-16">
        <div className="flex gap-2 h-[2px]">
          {project.activity_7d?.map((count, i) => (
            <div 
              key={i} 
              className={cn("flex-1 transition-all duration-1000", count > 0 ? "bg-accent/60 shadow-[0_0_10px_rgba(var(--accent-rgb),0.3)]" : "bg-white/5")}
              style={{ opacity: count > 0 ? 0.3 + (count/10) : 0.05 }}
            />
          ))}
        </div>

        <div className="flex flex-wrap gap-x-16 gap-y-8">
           <div className="flex items-center gap-5 text-[11px] font-black uppercase text-white/20 tracking-[0.5em] group-hover:text-white transition-colors duration-700">
              <Microscope size={16} className="text-accent/60" strokeWidth={1} /> {project.proj_type}
           </div>
           <div className="flex items-center gap-5 text-[11px] font-black uppercase text-white/20 tracking-[0.5em] group-hover:text-white transition-colors duration-700">
              <History size={16} className="text-accent/60" strokeWidth={1} /> {new Date(project.last_modified * 1000).toLocaleDateString()}
           </div>
           <div className="flex items-center gap-5 text-[11px] font-black uppercase text-white/20 tracking-[0.5em] group-hover:text-white transition-colors duration-700">
              <Target size={16} className="text-accent/60" strokeWidth={1} /> {Math.round(roi)} Velocity
           </div>
           {project.arch_weight && (
             <div className="flex items-center gap-5 text-[11px] font-black uppercase text-white/20 tracking-[0.5em] group-hover:text-white transition-colors duration-700">
                <Box size={16} className="text-accent/60" strokeWidth={1} /> {project.arch_weight.dirs}D / {project.arch_weight.files}F
             </div>
           )}
        </div>

        <AnimatePresence>
          {isExpanded && (
            <motion.div 
              initial={{ opacity: 0, height: 0, y: 20 }}
              animate={{ opacity: 1, height: 'auto', y: 0 }}
              exit={{ opacity: 0, height: 0, y: 10 }}
              className="pt-24 mt-24 border-t border-white/10 grid grid-cols-1 lg:grid-cols-2 gap-24 overflow-hidden"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="space-y-16">
                <div className="space-y-6">
                  <p className="text-[11px] font-black uppercase text-accent/40 tracking-[0.8em] flex items-center gap-4">
                     <FileCode size={14} /> System Narrative
                  </p>
                  <p className="text-xl font-serif text-white/50 leading-relaxed italic pr-16 bg-gradient-to-r from-white/10 to-transparent p-8 border-l-2 border-accent/20">
                    "{project.narrative}"
                  </p>
                </div>
                <div className="space-y-8">
                   <p className="text-[11px] font-black uppercase text-white/20 tracking-[0.8em]">Heavyweight Anatomy</p>
                   <div className="grid gap-3">
                      {project.largest_files?.map(file => (
                        <div key={file.name} className="group/file flex justify-between items-center text-[11px] font-mono p-5 bg-white/[0.03] border border-white/5 hover:border-accent/40 hover:bg-accent/[0.02] transition-all duration-500">
                           <span className="text-white/30 group-hover/file:text-white transition-colors truncate max-w-[350px]">{file.name}</span>
                           <span className="text-accent/40 font-black tracking-widest group-hover/file:text-accent transition-colors">{(file.size / 1024).toFixed(0)} KB</span>
                        </div>
                      ))}
                   </div>
                </div>
              </div>

              <div className="space-y-16">
                 <div className="grid grid-cols-2 gap-8">
                    <div className="p-10 bg-white/[0.02] border border-white/10 rounded-2xl group/stat transition-all hover:bg-white/[0.05] hover:border-accent/20">
                       <p className="text-[10px] font-black uppercase text-white/10 tracking-[0.5em] mb-6 group-hover/stat:text-accent transition-colors">Recursive Depth</p>
                       <p className="text-5xl font-black italic text-white/90 tracking-tighter">{project.deepest_dir?.split('/').length || 0} Layers</p>
                       <div className="h-[2px] w-12 bg-accent/20 mt-4 group-hover/stat:w-full transition-all duration-700" />
                       <p className="text-[10px] font-mono text-white/10 mt-6 truncate">{project.deepest_dir || '/root'}</p>
                    </div>
                    <div className="p-10 bg-white/[0.02] border border-white/10 rounded-2xl group/stat transition-all hover:bg-white/[0.05] hover:border-accent/20">
                       <p className="text-[10px] font-black uppercase text-white/10 tracking-[0.5em] mb-6 group-hover/stat:text-accent transition-colors">Total Saturation</p>
                       <p className="text-5xl font-black italic text-white/90 tracking-tighter">{(project.total_loc/1000).toFixed(1)}K</p>
                       <div className="h-[2px] w-12 bg-accent/20 mt-4 group-hover/stat:w-full transition-all duration-700" />
                       <p className="text-[10px] font-mono text-white/10 mt-6 uppercase tracking-widest">Lines of Code</p>
                    </div>
                 </div>
                 
                 <div className="space-y-6">
                    <p className="text-[11px] font-black uppercase text-white/20 tracking-[0.8em]">Core Dependencies</p>
                    <div className="flex flex-wrap gap-3">
                       {project.dependencies?.slice(0, 12).map(dep => (
                         <span key={dep} className="text-[10px] font-black uppercase tracking-[0.2em] px-4 py-2 bg-white/5 border border-white/5 hover:border-accent/30 hover:text-accent transition-all duration-500 rounded-md cursor-default">{dep}</span>
                       ))}
                       {project.dependencies?.length > 12 && <span className="text-[10px] font-black text-white/20 px-4 py-2">+{project.dependencies.length - 12} Artifacts</span>}
                    </div>
                 </div>

                 <div className="flex gap-6 pt-6">
                    <button className="group/btn flex-1 text-[11px] font-black uppercase py-8 border border-white/10 hover:border-accent/40 hover:text-accent transition-all duration-700 tracking-[0.6em] overflow-hidden relative rounded-xl">
                       <span className="relative z-10">Audit Source</span>
                       <div className="absolute inset-0 bg-accent/5 translate-y-full group-hover/btn:translate-y-0 transition-transform duration-700" />
                    </button>
                    <button className="flex-1 text-[11px] font-black uppercase py-8 bg-white text-black hover:bg-accent hover:text-white transition-all duration-1000 tracking-[0.6em] shadow-[0_20px_40px_rgba(255,255,255,0.05)] rounded-xl relative overflow-hidden group/nexus">
                       <span className="relative z-10">Nexus Deploy</span>
                       <div className="absolute inset-0 bg-white opacity-20 scale-x-0 group-hover/nexus:scale-x-100 transition-transform origin-left duration-1000" />
                    </button>
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
  const [viewMode, setViewMode] = useState('gallery');
  const [diagnosticMode, setDiagnosticMode] = useState(false);
  
  const projects = useMemo(() => (portfolioData.projects || []) as unknown as Project[], []);

  const stats = useMemo(() => {
    const totalLoc = projects.reduce((acc, p) => acc + p.total_loc, 0);
    const count = projects.length;
    const systemCount = projects.filter(p => p.is_system).length;
    const peakVelocity = projects.filter(p => ((p.recent_commits * 100) / (p.total_loc / 1000 + 1)) > 50).length;
    const avgHealth = Math.round(projects.reduce((acc, p) => acc + p.health, 0) / count);
    return { totalLoc, count, systemCount, peakVelocity, avgHealth };
  }, [projects]);

  const filteredProjects = projects
    .filter(p => {
      const matchesSearch = p.path.toLowerCase().includes(searchTerm.toLowerCase());
      const isVisible = diagnosticMode ? true : !p.is_system;
      return matchesSearch && isVisible;
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

  const featuredProjects = useMemo(() => {
    return filteredProjects.filter(p => p.preview_image || p.health > 90).slice(0, 6);
  }, [filteredProjects]);

  const boardData = useMemo(() => {
    const sections = {
      "ACTIVE ORBITS": [] as Project[],
      "STALE / ARCHIVED": [] as Project[],
      "DIAGNOSTIC WARNING": [] as Project[]
    };

    filteredProjects.forEach(p => {
      const threeMonthsAgo = Date.now() / 1000 - (90 * 24 * 60 * 60);
      if (p.health < 50 || p.env_exposed) sections["DIAGNOSTIC WARNING"].push(p);
      else if (p.last_modified < threeMonthsAgo) sections["STALE / ARCHIVED"].push(p);
      else sections["ACTIVE ORBITS"].push(p);
    });

    return sections;
  }, [filteredProjects]);

  const { scrollYProgress } = useScroll();
  const scaleX = useSpring(scrollYProgress, {
    stiffness: 100,
    damping: 30,
    restDelta: 0.001
  });

  return (
    <main className="min-h-screen bg-[#020202] text-white font-sans selection:bg-accent selection:text-black overflow-x-hidden">
      <NoiseBackground />
      <CustomCursor />
      
      {/* Progress Bar */}
      <motion.div className="fixed top-0 left-0 right-0 h-1 bg-accent z-[1000] origin-left" style={{ scaleX }} />

      {/* Precision Grid Overlay */}
      <div className="fixed inset-0 pointer-events-none z-0 opacity-[0.05] bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:60px_60px]" />

      <div className="max-w-[2400px] mx-auto p-8 lg:p-24 relative z-10">
        
        {/* NAV BAR */}
        <nav className="flex justify-between items-center mb-40 border-b border-white/10 pb-12 backdrop-blur-md sticky top-0 z-[100]">
           <div className="flex items-center gap-16">
              <div className="flex items-center gap-4">
                 <div className="w-4 h-4 bg-accent rotate-45" />
                 <div className="text-[11px] font-black uppercase tracking-[1em] text-white/40">PARANJAY // DESIGN ENGINEER</div>
              </div>
              <div className="hidden xl:flex gap-12">
                 {['Orbits', 'Analytics', 'Lab', 'Contact'].map(item => (
                   <a key={item} href="#" className="text-[10px] font-black uppercase tracking-[0.5em] text-white/10 hover:text-accent transition-all duration-500 hover:tracking-[0.8em]">{item}</a>
                 ))}
              </div>
           </div>
           <div className="flex items-center gap-10">
              <div className="text-[10px] font-mono text-white/20 uppercase tracking-widest hidden md:block">System Status: <span className="text-green-500">Nominal</span></div>
              <div className="w-12 h-[1px] bg-white/10" />
              <button className="p-3 bg-white/5 border border-white/10 rounded-full hover:bg-accent hover:text-black transition-all duration-700">
                 <Settings size={14} />
              </button>
           </div>
        </nav>

        {/* HERO SECTION: THE PORTFOLIO VISION */}
        <div className="grid grid-cols-1 xl:grid-cols-12 gap-24 mb-80 items-end">
          <div className="xl:col-span-9 space-y-20">
            <div className="flex items-center gap-10">
               <motion.div initial={{ width: 0 }} animate={{ width: 100 }} transition={{ duration: 1.5 }} className="h-[2px] bg-accent shadow-[0_0_40px_rgba(var(--accent-rgb),0.8)]" />
               <div className="flex items-center gap-6">
                  <span className="text-[12px] font-black uppercase tracking-[1.2em] text-accent/80">Recursive Workspace Intelligence</span>
                  <div className="flex gap-2">
                     {[1,2,3].map(i => <div key={i} className="w-1.5 h-1.5 bg-accent/20 rounded-full" />)}
                  </div>
               </div>
            </div>
            <h1 className="text-[12vw] font-black italic tracking-tighter uppercase leading-[0.75] translate-x-[-15px] mix-blend-difference drop-shadow-[0_20px_50px_rgba(0,0,0,0.5)]">
              Digital<br/>Product<br/><span className="text-accent italic underline decoration-white/5 decoration-1 underline-offset-[20px]">Ecosystem</span>
            </h1>
          </div>
          
          <div className="xl:col-span-3 space-y-16 text-right pb-10">
             <div className="space-y-6">
                <p className="text-lg font-serif text-white/30 leading-relaxed italic max-w-sm ml-auto">
                  "Building high-fidelity interfaces that orchestrate complex technical orbits. A Design Engineer's journey through 2M+ lines of saturation."
                </p>
                <div className="flex justify-end gap-6 pt-4">
                   <div className="px-5 py-2 border border-white/5 rounded-full text-[9px] font-black tracking-widest uppercase hover:bg-white hover:text-black transition-all duration-700 cursor-pointer">Follow Depth</div>
                   <div className="px-5 py-2 bg-accent text-black rounded-full text-[9px] font-black tracking-widest uppercase hover:bg-white transition-all duration-700 cursor-pointer">Initialize Nexus</div>
                </div>
             </div>
             <div className="grid grid-cols-2 gap-16 pt-12 border-t border-white/10">
                <div className="space-y-3">
                   <p className="text-[10px] font-black uppercase tracking-[0.6em] text-white/10">Total Orbits</p>
                   <p className="text-6xl font-black italic tracking-tighter">{stats.count}</p>
                </div>
                <div className="space-y-3">
                   <p className="text-[10px] font-black uppercase tracking-[0.6em] text-white/10">Avg Health</p>
                   <p className="text-6xl font-black italic tracking-tighter">{stats.avgHealth}%</p>
                </div>
             </div>
          </div>
        </div>

        {/* FEATURED / SHOWCASE SECTION */}
        <div className="mb-80 relative">
           <div className="absolute -left-24 top-0 bottom-0 w-1 bg-gradient-to-b from-accent to-transparent" />
           <div className="flex justify-between items-end mb-24">
              <div className="space-y-4">
                 <div className="flex items-center gap-4 text-accent">
                    <Sparkles size={20} />
                    <span className="text-[11px] font-black uppercase tracking-[1em]">Showcase Artifacts</span>
                 </div>
                 <h2 className="text-6xl font-black italic uppercase tracking-tighter">Selected Case Studies</h2>
              </div>
              <div className="text-right">
                 <p className="text-[10px] font-black uppercase tracking-[0.8em] text-white/10 mb-2 italic">Gallery View Enabled</p>
                 <div className="h-[2px] w-32 bg-white/10 ml-auto" />
              </div>
           </div>
           <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-1px bg-white/10 border border-white/10 shadow-[0_50px_100px_-20px_rgba(0,0,0,1)]">
              {featuredProjects.map((p, i) => <ProjectCard key={p.path} project={p} index={i} view="gallery" />)}
           </div>
        </div>

        {/* ANALYTICS SECTION: CHANH DAI STYLE PRECISION */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-32 mb-80">
           <div className="lg:col-span-5 space-y-24">
              <div className="space-y-8">
                 <div className="flex items-center gap-6">
                    <div className="w-16 h-16 border border-white/10 rounded-2xl flex items-center justify-center bg-[#050505] shadow-2xl">
                       <Dna size={32} className="text-accent" />
                    </div>
                    <div className="space-y-1">
                       <h3 className="text-4xl font-black italic uppercase tracking-tighter">Technical DNA</h3>
                       <p className="text-[10px] font-black uppercase tracking-[0.6em] text-white/20">Skillset Saturation Matrix</p>
                    </div>
                 </div>
                 <p className="text-base font-serif text-white/30 italic leading-relaxed max-w-md border-l-2 border-white/5 pl-8 mt-8">
                    "A quantified breakdown of technical proficiency across the global discovery radius. Measured by volume, complexity, and recursive depth."
                 </p>
              </div>
              
              <div className="space-y-12 pr-12">
                 {Object.entries(portfolioData.skills_matrix || {}).slice(0, 8).map(([lang, percent]) => (
                   <div key={lang} className="group relative">
                      <div className="flex justify-between items-end mb-5">
                         <div className="flex items-center gap-4">
                            <span className="text-2xl font-black italic uppercase tracking-tighter group-hover:text-accent transition-all duration-700">{lang}</span>
                            <div className="w-2 h-2 bg-white/5 rounded-full group-hover:bg-accent/40 transition-colors" />
                         </div>
                         <span className="text-[10px] font-mono text-white/20 tracking-[0.2em]">{Math.round(percent as number)}% PROFICIENCY</span>
                      </div>
                      <div className="h-[2px] bg-white/5 w-full relative overflow-hidden rounded-full">
                         <motion.div 
                           initial={{ width: 0 }}
                           whileInView={{ width: `${percent}%` }}
                           viewport={{ once: true }}
                           transition={{ duration: 1.5, ease: "circOut" }}
                           className="absolute top-0 left-0 h-full bg-gradient-to-r from-white to-accent group-hover:shadow-[0_0_30px_rgba(var(--accent-rgb),0.4)] transition-all duration-1000" 
                         />
                      </div>
                   </div>
                 ))}
              </div>
           </div>

           <div className="lg:col-span-7 grid grid-cols-1 md:grid-cols-2 gap-1px bg-white/10 border border-white/10 h-fit rounded-3xl overflow-hidden shadow-2xl">
              <div className="p-24 bg-[#030303] group relative overflow-hidden min-h-[450px] flex flex-col justify-between">
                 <div className="absolute -top-32 -right-32 opacity-[0.03] group-hover:opacity-10 transition-opacity duration-1000 rotate-12 scale-150">
                    <Zap size={400} strokeWidth={0.1} />
                 </div>
                 <div>
                    <p className="text-[11px] font-black uppercase tracking-[1em] text-white/10 mb-24">Velocity Gradient</p>
                    <h4 className="text-[12rem] font-black italic tracking-tighter text-white/95 leading-[0.8] mb-12 group-hover:text-accent transition-colors duration-1000">{stats.peakVelocity}</h4>
                 </div>
                 <div className="space-y-4">
                    <p className="text-white/30 text-lg leading-relaxed max-w-xs font-serif italic border-t border-white/5 pt-8">
                       High-velocity orbits actively maintained and optimized for peak system performance.
                    </p>
                    <button className="text-[10px] font-black uppercase tracking-[0.5em] text-accent flex items-center gap-4 group-hover:gap-8 transition-all">Audit Velocity <ChevronRight size={14} /></button>
                 </div>
              </div>
              <div className="p-24 bg-[#030303] group relative overflow-hidden min-h-[450px] flex flex-col justify-between">
                 <div className="absolute -bottom-32 -left-32 opacity-[0.03] group-hover:opacity-10 transition-opacity duration-1000 -rotate-12 scale-150">
                    <Compass size={400} strokeWidth={0.1} />
                 </div>
                 <div className="text-right">
                    <p className="text-[11px] font-black uppercase tracking-[1em] text-white/10 mb-24">Ecosystem Radius</p>
                    <h4 className="text-[12rem] font-black italic tracking-tighter text-white/95 leading-[0.8] mb-12 group-hover:text-accent transition-colors duration-1000">53</h4>
                 </div>
                 <div className="space-y-4 text-right">
                    <p className="text-white/30 text-lg leading-relaxed max-w-xs font-serif italic border-t border-white/5 pt-8 ml-auto">
                       Independent technical artifacts discovered across the global recursive mac-os radius.
                    </p>
                    <button className="text-[10px] font-black uppercase tracking-[0.5em] text-accent flex items-center gap-4 justify-end group-hover:gap-8 transition-all">Explore Discovery <ChevronRight size={14} /></button>
                 </div>
              </div>
           </div>
        </div>

        {/* CONTROL HUB: THE FLOATING INTERFACE */}
        <div className="sticky top-24 z-50 flex flex-col xl:flex-row justify-between items-center gap-16 px-16 py-10 bg-[#050505]/40 backdrop-blur-[60px] border border-white/10 rounded-3xl mb-48 ring-1 ring-white/5 shadow-[0_80px_150px_rgba(0,0,0,0.8)] group/hub transition-all hover:bg-[#080808]/60">
           <div className="relative flex-1 w-full max-w-2xl group/input">
              <div className="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-8 bg-accent/20 group-focus-within/input:bg-accent transition-all duration-700" />
              <Search className="absolute left-10 top-1/2 -translate-y-1/2 text-white/10 group-focus-within/input:text-accent transition-colors" size={20} />
              <input 
                type="text"
                placeholder="DISCOVER TECHNICAL ARTIFACTS..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full bg-transparent py-6 pl-24 pr-12 focus:outline-none text-sm font-black uppercase tracking-[0.6em] placeholder:text-white/5"
              />
           </div>
           
           <div className="flex flex-wrap items-center justify-center gap-16">
              <div className="flex items-center gap-12 border-r border-white/10 pr-16 group/diag">
                 <div className="text-right">
                    <p className="text-[8px] font-black uppercase text-white/10 tracking-[0.6em]">Telemetry</p>
                    <p className="text-[11px] font-black uppercase tracking-[0.2em] group-hover/diag:text-accent transition-colors">{diagnosticMode ? 'Deep Scan Active' : 'Standard Feed'}</p>
                 </div>
                 <button 
                   onClick={() => setDiagnosticMode(!diagnosticMode)}
                   className={cn(
                     "w-16 h-8 rounded-full border border-white/10 flex items-center p-2 transition-all duration-1000 relative overflow-hidden",
                     diagnosticMode ? "bg-accent shadow-[0_0_30px_rgba(var(--accent-rgb),0.4)]" : "bg-white/5"
                   )}
                 >
                   <motion.div 
                     animate={{ x: diagnosticMode ? 32 : 0 }}
                     className={cn("w-4 h-4 rounded-full shadow-2xl relative z-10", diagnosticMode ? "bg-black" : "bg-white/40")} 
                   />
                   {diagnosticMode && <div className="absolute inset-0 bg-white/20 animate-pulse" />}
                 </button>
              </div>

              <div className="flex items-center gap-16">
                 <div className="flex items-center gap-8 group/sort">
                    <div className="p-3 bg-white/5 rounded-xl group-hover/sort:bg-accent transition-colors">
                       <ArrowUpDown size={16} className="text-white/20 group-hover/sort:text-black transition-colors" />
                    </div>
                    <select value={sortBy} onChange={(e) => setSortBy(e.target.value)} className="bg-transparent text-[12px] font-black uppercase tracking-[0.4em] outline-none cursor-pointer hover:text-accent transition-all duration-700">
                      <option value="modified">Recency</option>
                      <option value="loc">Volume</option>
                      <option value="roi">Velocity</option>
                    </select>
                 </div>
                 <ViewSwitcher mode={viewMode} setMode={setViewMode} />
              </div>
           </div>
        </div>

        {/* MAIN FEED: THE SYSTEM LOG */}
        <div className="space-y-80 min-h-[120vh] pb-80">
          {viewMode === 'board' ? (
             <div className="flex gap-24 overflow-x-auto pb-64 scrollbar-hide snap-x">
                {Object.entries(boardData).map(([status, boardProjects]) => (
                   <div key={status} className="min-w-[750px] snap-start space-y-24 group/board">
                      <div className="flex justify-between items-center border-b-2 border-white/5 pb-10 group-hover/board:border-accent/40 transition-colors duration-1000">
                         <div className="flex items-center gap-10">
                            <div className={cn("w-5 h-5 rounded-sm rotate-45", status.includes('WARNING') ? 'bg-red-500' : status.includes('STALE') ? 'bg-white/10' : 'bg-accent')} />
                            <h3 className="text-4xl font-black italic uppercase tracking-tighter group-hover/board:text-accent transition-colors">{status}</h3>
                         </div>
                         <div className="text-right">
                            <span className="text-[11px] font-black tracking-[0.4em] text-white/10">{boardProjects.length} Independent Orbits</span>
                         </div>
                      </div>
                      <div className="space-y-24">
                         {boardProjects.map((p, i) => <ProjectCard key={p.path} project={p} index={i} view="grid" />)}
                      </div>
                   </div>
                ))}
             </div>
          ) : viewMode === 'gallery' ? (
            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4 gap-1px bg-white/10 border border-white/10 shadow-2xl">
                {filteredProjects.map((p, i) => <ProjectCard key={p.path} project={p} index={i} view="gallery" />)}
            </div>
          ) : viewMode === 'table' ? (
            <div className="border border-white/10 bg-[#050505] rounded-3xl overflow-hidden shadow-[0_100px_200px_rgba(0,0,0,1)]">
               <div className="grid grid-cols-12 gap-8 p-12 bg-white/[0.04] border-b border-white/10 text-[11px] font-black uppercase tracking-[1em] text-white/20">
                  <div className="col-span-4 flex items-center gap-4"><Terminal size={14} /> Artifact Identifier</div>
                  <div className="col-span-2">System Type</div>
                  <div className="col-span-2">Digital Mass</div>
                  <div className="col-span-2">Integrity</div>
                  <div className="col-span-2 text-right">Audit</div>
               </div>
               <div className="divide-y divide-white/5">
                  {filteredProjects.map((p, i) => <ProjectCard key={p.path} project={p} index={i} view="table" />)}
               </div>
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

        {/* FOOTER: THE DESIGNER'S SIGNATURE */}
        <footer className="mt-80 pt-64 border-t-2 border-white/10 flex flex-col xl:flex-row justify-between items-start gap-48 pb-80 relative group/footer">
           <motion.div 
             initial={{ width: 0 }} 
             whileInView={{ width: 300 }} 
             viewport={{ once: true }}
             className="absolute top-[-2px] left-0 h-[2px] bg-accent" 
           />
           
           <div className="max-w-3xl space-y-24">
              <div className="flex items-center gap-12 group/brand">
                 <div className="w-24 h-24 bg-white flex items-center justify-center rounded-2xl group-hover/brand:bg-accent transition-all duration-1000 rotate-0 group-hover/brand:rotate-12 group-hover/brand:scale-110">
                    <User size={48} className="text-black" />
                 </div>
                 <div className="space-y-2">
                    <h2 className="text-9xl font-black italic uppercase tracking-tighter leading-none translate-x-[-5px]">Paranjay<br/><span className="text-white/20 group-hover/brand:text-white transition-colors">Khachar</span></h2>
                    <p className="text-[12px] font-black uppercase tracking-[1em] text-accent/60">Digital Design Engineer // Systems Architect</p>
                 </div>
              </div>
              <p className="text-2xl font-serif text-white/30 leading-relaxed italic pr-24 border-l-4 border-white/5 pl-12 py-4">
                "Orchestrating the intersection of technical saturation and elite aesthetic quality. This portfolio is a living organism, recursively monitoring its own existence within the Ideaverse."
              </p>
           </div>
           
           <div className="grid grid-cols-2 md:grid-cols-3 gap-32 w-full xl:w-auto pt-10">
              <div className="space-y-8">
                 <p className="text-[11px] font-black uppercase tracking-[1em] text-white/10">Architecture</p>
                 <p className="text-3xl font-black italic uppercase tracking-tighter">OS v5.2<br/><span className="text-accent">Saturated</span></p>
                 <div className="flex gap-4 opacity-20">
                    <Globe size={18} />
                    <Network size={18} />
                    <Cpu size={18} />
                 </div>
              </div>
              <div className="space-y-8">
                 <p className="text-[11px] font-black uppercase tracking-[1em] text-white/10">Identity</p>
                 <p className="text-3xl font-black italic uppercase tracking-tighter text-white/80">Est. 2024<br/>Full Stack</p>
                 <div className="flex gap-4">
                    <button className="text-[10px] font-black uppercase tracking-widest border border-white/10 px-4 py-2 hover:bg-white hover:text-black transition-all">Resume</button>
                 </div>
              </div>
              <div className="space-y-8 text-right">
                 <p className="text-[11px] font-black uppercase tracking-[1em] text-white/10">Connected</p>
                 <div className="flex flex-col items-end gap-6 pt-4">
                    <div className="flex gap-6">
                       <Coffee size={24} className="text-white/10 hover:text-accent transition-colors cursor-pointer" />
                       <Terminal size={24} className="text-white/10 hover:text-accent transition-colors cursor-pointer" />
                       <Heart size={24} className="text-white/10 fill-accent/5 hover:fill-accent transition-all cursor-pointer" />
                    </div>
                    <p className="text-[11px] font-mono text-white/20 tracking-tighter uppercase">Local Time: {new Date().toLocaleTimeString()}</p>
                 </div>
              </div>
           </div>
        </footer>

      </div>
    </main>
  );
}

function Heart({ size, className }: { size: number, className?: string }) {
  return (
    <svg 
      xmlns="http://www.w3.org/2000/svg" 
      width={size} 
      height={size} 
      viewBox="0 0 24 24" 
      fill="none" 
      stroke="currentColor" 
      strokeWidth="2" 
      strokeLinecap="round" 
      strokeLinejoin="round" 
      className={className}
    >
      <path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z" />
    </svg>
  );
}
