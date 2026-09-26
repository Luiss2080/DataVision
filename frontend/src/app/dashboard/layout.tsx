"use client";

import { useAuthStore } from "@/store/useAuthStore";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";
import { Activity, User as UserIcon, LogOut, Settings, BarChart } from "lucide-react";
import { ThemeSwitcher } from "@/components/theme-switcher";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const { user, token, logout } = useAuthStore();
  const router = useRouter();

  useEffect(() => {
    // Si no hay token en el estado de Zustand, redireccionamos a Login
    if (!token) {
      router.push("/login");
    }
  }, [token, router]);

  if (!user) return null; // Evitar flash de contenido desprotegido

  return (
    <div className="min-h-screen bg-zinc-50 dark:bg-[#09090b] flex">
      {/* Sidebar Lateral */}
      <aside className="w-64 border-r border-zinc-200 dark:border-zinc-800 bg-white dark:bg-[#0f0f11] flex flex-col">
        <div className="h-16 flex items-center px-6 border-b border-zinc-200 dark:border-zinc-800 justify-between">
          <div className="flex items-center">
            <div className="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center mr-3">
              <Activity className="w-5 h-5 text-white" />
            </div>
            <span className="font-bold">DataVision</span>
          </div>
          <ThemeSwitcher />
        </div>
        
        <nav className="flex-1 p-4 space-y-2">
          <div className="px-4 py-2 rounded-lg bg-blue-50 dark:bg-blue-900/20 text-blue-600 flex items-center gap-3 font-medium">
            <BarChart className="w-5 h-5" /> Métricas
          </div>
          <div className="px-4 py-2 rounded-lg text-zinc-500 hover:bg-zinc-100 dark:hover:bg-zinc-800 flex items-center gap-3 font-medium cursor-pointer transition-colors">
            <Settings className="w-5 h-5" /> Ajustes
          </div>
        </nav>

        <div className="p-4 border-t border-zinc-200 dark:border-zinc-800">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 rounded-full bg-zinc-200 dark:bg-zinc-800 flex items-center justify-center">
              <UserIcon className="w-5 h-5" />
            </div>
            <div className="flex flex-col overflow-hidden">
              <span className="text-sm font-semibold truncate">{user.email}</span>
              <span className="text-xs text-zinc-500">{user.role}</span>
            </div>
          </div>
          <Button variant="outline" className="w-full text-red-500 hover:text-red-600 gap-2" onClick={logout}>
            <LogOut className="w-4 h-4" /> Cerrar Sesión
          </Button>
        </div>
      </aside>

      {/* Contenido Principal */}
      <main className="flex-1 p-8 relative overflow-hidden">
        {/* Decoración */}
        <div className="absolute top-0 right-0 w-96 h-96 bg-blue-500/5 rounded-full blur-[100px] pointer-events-none" />
        
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
          className="relative z-10"
        >
          {children}
        </motion.div>
      </main>
    </div>
  );
}
