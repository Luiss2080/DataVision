"use client";

import { motion } from "framer-motion";
import { Camera, Save, User as UserIcon, Lock, CheckCircle2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useAuthStore } from "@/store/useAuthStore";
import { useState, useRef } from "react";
import { toast } from "sonner";
import { api } from "@/lib/axios";

export default function SettingsPage() {
  const { user, setAuth, token } = useAuthStore();
  const [loading, setLoading] = useState(false);
  const [password, setPassword] = useState("");
  const [preview, setPreview] = useState<string | null>(null);
  const [file, setFile] = useState<File | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      setFile(selectedFile);
      setPreview(URL.createObjectURL(selectedFile));
    }
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const formData = new FormData();
      if (password) formData.append('password', password);
      if (file) formData.append('avatar', file);

      // Si no hay archivo ni password, no hacemos nada
      if (!password && !file) {
        toast.info("No hay cambios para guardar");
        setLoading(false);
        return;
      }

      const { data } = await api.post('/users/profile', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      // Actualizar Zustand con la nueva data del usuario (que ahora incluye profile.avatarUrl)
      if (token) setAuth(token, data);

      toast.success("Perfil actualizado correctamente en la base de datos");
      setPassword("");
    } catch (error: any) {
      toast.error(error.response?.data?.message || "Ocurrió un error al guardar");
    } finally {
      setLoading(false);
    }
  };

  const currentAvatarUrl = user?.profile?.avatarUrl 
    ? `${process.env.NEXT_PUBLIC_API_URL?.replace('/api', '') || 'http://localhost:3000'}${user.profile.avatarUrl}` 
    : null;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="max-w-2xl mx-auto"
    >
      <h1 className="text-3xl font-bold tracking-tight mb-8">Configuración de Perfil</h1>
      
      <div className="bg-white dark:bg-[#18181b] border border-zinc-200 dark:border-zinc-800 rounded-2xl shadow-sm overflow-hidden p-8">
        
        {/* Avatar Upload Section */}
        <div className="flex items-center gap-6 mb-10 pb-10 border-b border-zinc-200 dark:border-zinc-800">
          <div 
            className="relative group cursor-pointer"
            onClick={() => fileInputRef.current?.click()}
          >
            <div className="w-24 h-24 rounded-full bg-zinc-200 dark:bg-zinc-800 flex items-center justify-center overflow-hidden border-2 border-transparent group-hover:border-blue-500 transition-colors">
              {(preview || currentAvatarUrl) ? (
                <img src={preview || currentAvatarUrl} alt="Avatar" className="w-full h-full object-cover" />
              ) : (
                <UserIcon className="w-10 h-10 text-zinc-400" />
              )}
            </div>
            <div className="absolute inset-0 bg-black/50 rounded-full opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
              <Camera className="w-6 h-6 text-white" />
            </div>
            <input 
              type="file" 
              className="hidden" 
              accept="image/*" 
              ref={fileInputRef}
              onChange={handleImageChange}
            />
          </div>
          <div>
            <h3 className="text-lg font-semibold mb-1">Foto de Perfil</h3>
            <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-3">Sube una imagen cuadrada (JPG, PNG). Se guardará localmente.</p>
            {file && <span className="text-xs text-green-500 font-medium flex items-center gap-1"><CheckCircle2 className="w-3 h-3"/> Imagen lista para guardar</span>}
          </div>
        </div>

        {/* Update Form */}
        <form onSubmit={handleSave} className="flex flex-col gap-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="flex flex-col gap-2">
              <label className="text-sm font-medium text-zinc-700 dark:text-zinc-300">Correo Electrónico</label>
              <div className="relative">
                <input 
                  type="email" 
                  disabled
                  defaultValue={user?.email || ""}
                  className="w-full h-11 bg-zinc-100 dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-xl px-4 text-zinc-500 cursor-not-allowed"
                />
              </div>
            </div>
            
            <div className="flex flex-col gap-2">
              <label className="text-sm font-medium text-zinc-700 dark:text-zinc-300">Nueva Contraseña</label>
              <div className="relative">
                <Lock className="absolute left-3 top-3 w-5 h-5 text-zinc-400" />
                <input 
                  type="password" 
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Dejar en blanco para no cambiar"
                  className="w-full h-11 bg-black/5 dark:bg-white/5 border border-zinc-200 dark:border-zinc-800 rounded-xl pl-10 pr-4 focus:ring-2 focus:ring-blue-500 outline-none transition-all"
                />
              </div>
            </div>
          </div>

          <div className="flex justify-end pt-4">
            <Button type="submit" className="gap-2" disabled={loading || (!password && !file)}>
              <Save className="w-4 h-4" />
              {loading ? "Guardando..." : "Guardar Cambios"}
            </Button>
          </div>
        </form>
      </div>
    </motion.div>
  );
}
