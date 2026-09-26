"use client";

import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { useState } from "react";
import { api } from "@/lib/axios";
import { useAuthStore } from "@/store/useAuthStore";
import { useRouter } from "next/navigation";
import { Lock, Mail, Activity } from "lucide-react";
import Link from "next/link";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  
  const setAuth = useAuthStore((state) => state.setAuth);
  const router = useRouter();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const response = await api.post("/auth/login", { email, password });
      setAuth(response.data.access_token, response.data.user);
      router.push("/dashboard");
    } catch (err: any) {
      setError(err.response?.data?.message || "Error al iniciar sesión");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-background p-4 relative overflow-hidden">
      <div className="absolute top-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-blue-600/10 blur-[120px]" />
      
      <motion.div 
        className="glass w-full max-w-md p-8 rounded-3xl relative z-10"
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.3 }}
      >
        <div className="flex justify-center mb-6">
          <div className="w-12 h-12 rounded-xl bg-blue-600 flex items-center justify-center shadow-lg shadow-blue-500/20">
            <Activity className="w-7 h-7 text-white" />
          </div>
        </div>
        
        <h2 className="text-3xl font-bold text-center mb-2">Bienvenido de vuelta</h2>
        <p className="text-zinc-500 dark:text-zinc-400 text-center mb-8">Ingresa tus credenciales para acceder a tu panel.</p>
        
        {error && <div className="p-3 rounded-lg bg-red-500/10 border border-red-500/20 text-red-500 text-sm mb-6 text-center">{error}</div>}

        <form onSubmit={handleLogin} className="flex flex-col gap-4">
          <div className="relative">
            <Mail className="absolute left-3 top-3 w-5 h-5 text-zinc-400" />
            <input 
              type="email" 
              placeholder="tu@email.com" 
              className="w-full h-12 bg-black/5 dark:bg-white/5 border border-zinc-200 dark:border-zinc-800 rounded-xl pl-11 pr-4 focus:ring-2 focus:ring-blue-500 outline-none transition-all"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="relative">
            <Lock className="absolute left-3 top-3 w-5 h-5 text-zinc-400" />
            <input 
              type="password" 
              placeholder="Contraseña" 
              className="w-full h-12 bg-black/5 dark:bg-white/5 border border-zinc-200 dark:border-zinc-800 rounded-xl pl-11 pr-4 focus:ring-2 focus:ring-blue-500 outline-none transition-all"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <Button type="submit" size="lg" className="w-full mt-4" disabled={loading}>
            {loading ? "Autenticando..." : "Ingresar"}
          </Button>
        </form>

        <p className="text-center mt-6 text-zinc-500 text-sm">
          ¿No tienes cuenta? <Link href="/register" className="text-blue-500 hover:underline">Regístrate</Link>
        </p>
      </motion.div>
    </div>
  );
}
