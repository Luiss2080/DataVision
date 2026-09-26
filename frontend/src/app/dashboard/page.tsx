"use client";

import { motion } from "framer-motion";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Area, AreaChart } from 'recharts';

const data = [
  { name: 'Lun', usuarios: 400, ingresos: 2400 },
  { name: 'Mar', usuarios: 300, ingresos: 1398 },
  { name: 'Mié', usuarios: 200, ingresos: 9800 },
  { name: 'Jue', usuarios: 278, ingresos: 3908 },
  { name: 'Vie', usuarios: 189, ingresos: 4800 },
  { name: 'Sáb', usuarios: 239, ingresos: 3800 },
  { name: 'Dom', usuarios: 349, ingresos: 4300 },
];

export default function DashboardPage() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <h1 className="text-3xl font-bold tracking-tight mb-8">Resumen Analítico</h1>
      
      {/* Tarjetas Superiores */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        {[
          { title: "Usuarios Activos", value: "1,248", change: "+12%" },
          { title: "Ingresos Brutos", value: "$42,390", change: "+8.4%" },
          { title: "Peticiones API", value: "849k", change: "-2.1%" }
        ].map((stat, i) => (
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
              <span className={`text-sm font-medium px-2 py-1 rounded-full ${stat.change.startsWith('+') ? 'bg-green-500/10 text-green-500' : 'bg-red-500/10 text-red-500'}`}>
                {stat.change}
              </span>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Gráfico Principal */}
      <div className="bg-white dark:bg-[#18181b] border border-zinc-200 dark:border-zinc-800 p-6 rounded-2xl shadow-sm">
        <h3 className="text-lg font-semibold mb-6">Tráfico e Ingresos (Últimos 7 días)</h3>
        <div className="h-[400px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
              <defs>
                <linearGradient id="colorIngresos" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
                  <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#3f3f46" opacity={0.2} />
              <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{fill: '#71717a'}} dy={10} />
              <YAxis axisLine={false} tickLine={false} tick={{fill: '#71717a'}} dx={-10} />
              <Tooltip 
                contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '12px', color: '#fff' }}
                itemStyle={{ color: '#fff' }}
              />
              <Area type="monotone" dataKey="ingresos" stroke="#3b82f6" strokeWidth={3} fillOpacity={1} fill="url(#colorIngresos)" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>
    </motion.div>
  );
}
