"use client";

import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { ArrowRight, Activity, Database, Lock } from "lucide-react";
import Link from "next/link";

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-background selection:bg-blue-500/30 overflow-hidden relative">
      {/* Background Gradients */}
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-blue-600/20 blur-[120px]" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-indigo-600/20 blur-[120px]" />

      {/* Navbar */}
      <nav className="fixed top-0 w-full glass z-50 px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center">
            <Activity className="w-5 h-5 text-white" />
          </div>
          <span className="text-xl font-bold tracking-tight">DataVision</span>
        </div>
        <div className="flex gap-4">
          <Link href="/login">
            <Button variant="ghost">Iniciar Sesión</Button>
          </Link>
          <Link href="/register">
            <Button>Empezar Gratis</Button>
          </Link>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="pt-40 px-6 max-w-6xl mx-auto flex flex-col items-center text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <span className="px-4 py-2 rounded-full border border-blue-500/30 bg-blue-500/10 text-blue-500 text-sm font-medium mb-6 inline-block">
            Nueva Plataforma Analítica 2026
          </span>
        </motion.div>
        
        <motion.h1 
          className="text-5xl md:text-7xl font-bold tracking-tight mb-8"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
        >
          Visualiza el futuro de <br className="hidden md:block"/> tus{" "}
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-500 to-indigo-600">
            datos empresariales
          </span>
        </motion.h1>

        <motion.p 
          className="text-lg md:text-xl text-zinc-500 dark:text-zinc-400 max-w-2xl mb-12"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          DataVision transforma tus bases de datos complejas en dashboards interactivos y reportes ejecutivos en tiempo real, impulsados por una arquitectura de ultra bajo rendimiento.
        </motion.p>

        <motion.div 
          className="flex flex-col sm:flex-row gap-4"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
        >
          <Link href="/register">
            <Button size="lg" className="w-full sm:w-auto gap-2">
              Comenzar tu prueba <ArrowRight className="w-4 h-4" />
            </Button>
          </Link>
          <Link href="/docs">
            <Button size="lg" variant="outline" className="w-full sm:w-auto">
              Ver Documentación
            </Button>
          </Link>
        </motion.div>

        {/* Feature Cards Showcase */}
        <motion.div 
          className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-32 w-full"
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.5 }}
        >
          {[
            { icon: Activity, title: "Métricas en Tiempo Real", desc: "Monitorea tus KPIs sin latencia gracias a nuestra conexión WebSocket." },
            { icon: Database, title: "Conexión a PostgreSQL", desc: "Integración nativa y segura con las bases de datos corporativas más robustas." },
            { icon: Lock, title: "Seguridad Bancaria", desc: "Autenticación JWT, encriptación bcrypt y roles de usuario avanzados." }
          ].map((feat, i) => (
            <div key={i} className="glass p-6 rounded-2xl flex flex-col items-start text-left hover:bg-white/5 transition-colors duration-300">
              <div className="w-12 h-12 rounded-xl bg-blue-500/20 text-blue-500 flex items-center justify-center mb-4">
                <feat.icon className="w-6 h-6" />
              </div>
              <h3 className="text-xl font-semibold mb-2">{feat.title}</h3>
              <p className="text-zinc-500 dark:text-zinc-400">{feat.desc}</p>
            </div>
          ))}
        </motion.div>
      </main>
    </div>
  );
}
