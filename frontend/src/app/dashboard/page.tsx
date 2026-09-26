"use client";

import { motion } from "framer-motion";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Area, AreaChart } from 'recharts';
import { useEffect, useState } from "react";
import { api } from "@/lib/axios";

interface MetricStats {
  title: string;
  value: string;
  change: string;
}

interface ChartData {
  name: string;
  usuarios: number;
  ingresos: number;
}

interface DashboardData {
  stats: MetricStats[];
  chartData: ChartData[];
}

export default function DashboardPage() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const res = await api.get('/dashboard/metrics');
        setData(res.data);
      } catch (error) {
        console.error("Error cargando métricas", error);
      } finally {
        setLoading(false);
      }
    };
    fetchMetrics();
  }, []);

  if (loading || !data) return <div className="text-zinc-500 animate-pulse">Cargando métricas de la Base de Datos...</div>;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <h1 className="text-3xl font-bold tracking-tight mb-8">Resumen Analítico (En Vivo)</h1>
      
      {/* Tarjetas Superiores */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        {data.stats.map((stat, i) => (
          <motion.div 
            key={i} 
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: i * 0.1 }}
            className="bg-white dark:bg-[#18181b] border border-zinc-200 dark:border-zinc-800 p-6 rounded-2xl shadow-sm hover:shadow-md transition-shadow"
          >
            <h3 className="text-zinc-500 dark:text-zinc-400 text-sm font-medium mb-2">{stat.title}</h3>
            <div className="flex items-end justify-between">
              <span className="text-3xl font-bold">{stat.value}</span>
              <span className={`text-sm font-medium px-2 py-1 rounded-full ${stat.change.startsWith('+') ? 'bg-green-500/10 text-green-500' : stat.change === 'Estable' ? 'bg-zinc-500/10 text-zinc-500' : 'bg-red-500/10 text-red-500'}`}>
                {stat.change}
              </span>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Gráfico Principal */}
      <div className="bg-white dark:bg-[#18181b] border border-zinc-200 dark:border-zinc-800 p-6 rounded-2xl shadow-sm">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-semibold">Crecimiento de Usuarios vs Rendimiento (Últimos 7 días)</h3>
          <span className="text-xs px-2 py-1 bg-blue-500/10 text-blue-500 rounded-full font-medium">Datos Reales (DB)</span>
        </div>
        <div className="h-[400px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={data.chartData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
              <defs>
                <linearGradient id="colorUsuarios" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
                  <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                </linearGradient>
                <linearGradient id="colorIngresos" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#10b981" stopOpacity={0.3}/>
                  <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#3f3f46" opacity={0.2} />
              <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{fill: '#71717a'}} dy={10} />
              <YAxis yAxisId="left" axisLine={false} tickLine={false} tick={{fill: '#71717a'}} dx={-10} />
              <YAxis yAxisId="right" orientation="right" axisLine={false} tickLine={false} tick={{fill: '#71717a'}} dx={10} />
              <Tooltip 
                contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '12px', color: '#fff' }}
                itemStyle={{ color: '#fff' }}
              />
              <Area yAxisId="left" type="monotone" dataKey="ingresos" name="Rendimiento Base" stroke="#10b981" strokeWidth={3} fillOpacity={1} fill="url(#colorIngresos)" />
              <Area yAxisId="right" type="monotone" dataKey="usuarios" name="Usuarios BD" stroke="#3b82f6" strokeWidth={3} fillOpacity={1} fill="url(#colorUsuarios)" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>
    </motion.div>
  );
}
