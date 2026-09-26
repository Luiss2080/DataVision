"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/axios";
import { motion } from "framer-motion";
import { ShieldAlert, User, Trash2, Ban, CheckCircle } from "lucide-react";
import { toast } from "sonner";
import { useAuthStore } from "@/store/useAuthStore";
import { useRouter } from "next/navigation";

interface UserData {
  id: string;
  email: string;
  role: string;
  isActive: boolean;
  createdAt: string;
}

export default function AdminPanel() {
  const [users, setUsers] = useState<UserData[]>([]);
  const [loading, setLoading] = useState(true);
  const currentUser = useAuthStore(state => state.user);
  const router = useRouter();

  const fetchUsers = async () => {
    try {
      const { data } = await api.get('/users/all');
      setUsers(data);
    } catch (error) {
      toast.error("Error al cargar usuarios. Probablemente no tengas permisos.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (currentUser && currentUser.role !== 'ADMIN') {
      toast.error("Acceso denegado. No eres administrador.");
      router.push("/dashboard");
      return;
    }
    fetchUsers();
  }, [currentUser, router]);

  const handleToggleBlock = async (id: string, currentStatus: boolean) => {
    try {
      await api.patch(`/users/${id}/block`);
      toast.success(currentStatus ? "Usuario bloqueado exitosamente" : "Usuario desbloqueado exitosamente");
      fetchUsers(); // Recargar la tabla
    } catch (error: any) {
      toast.error(error.response?.data?.message || "No se pudo cambiar el estado del usuario");
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm("¿Estás seguro de que deseas eliminar este usuario permanentemente? Esta acción es irreversible.")) return;
    
    try {
      await api.delete(`/users/${id}`);
      toast.success("Usuario eliminado de la base de datos");
      fetchUsers(); // Recargar la tabla
    } catch (error: any) {
      toast.error(error.response?.data?.message || "Error al eliminar usuario");
    }
  };

  if (loading) return <div className="text-zinc-500">Cargando datos clasificados...</div>;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="flex items-center gap-3 mb-8">
        <div className="w-10 h-10 rounded-lg bg-amber-500/10 flex items-center justify-center border border-amber-500/20">
          <ShieldAlert className="w-5 h-5 text-amber-500" />
        </div>
        <h1 className="text-3xl font-bold tracking-tight">Panel de Administración</h1>
      </div>

      <div className="bg-white dark:bg-[#18181b] border border-zinc-200 dark:border-zinc-800 rounded-2xl shadow-sm overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-zinc-50 dark:bg-zinc-900 border-b border-zinc-200 dark:border-zinc-800">
            <tr>
              <th className="px-6 py-4 font-semibold text-zinc-600 dark:text-zinc-300">Usuario</th>
              <th className="px-6 py-4 font-semibold text-zinc-600 dark:text-zinc-300">Rol</th>
              <th className="px-6 py-4 font-semibold text-zinc-600 dark:text-zinc-300">Estado</th>
              <th className="px-6 py-4 font-semibold text-zinc-600 dark:text-zinc-300">Registro</th>
              <th className="px-6 py-4 font-semibold text-zinc-600 dark:text-zinc-300 text-right">Acciones</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-zinc-200 dark:divide-zinc-800">
            {users.map((u, i) => (
              <motion.tr 
                key={u.id}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: i * 0.05 }}
                className="hover:bg-zinc-50 dark:hover:bg-zinc-900/50 transition-colors"
              >
                <td className="px-6 py-4">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-full bg-zinc-200 dark:bg-zinc-800 flex items-center justify-center">
                      <User className="w-4 h-4" />
                    </div>
                    <span className="font-medium">{u.email}</span>
                  </div>
                </td>
                <td className="px-6 py-4">
                  <span className={`px-2 py-1 rounded text-xs font-bold ${u.role === 'ADMIN' ? 'bg-amber-500/10 text-amber-500' : 'bg-blue-500/10 text-blue-500'}`}>
                    {u.role}
                  </span>
                </td>
                <td className="px-6 py-4">
                  <span className={`px-2 py-1 rounded text-xs font-bold ${u.isActive ? 'bg-green-500/10 text-green-500' : 'bg-red-500/10 text-red-500'}`}>
                    {u.isActive ? 'Activo' : 'Bloqueado'}
                  </span>
                </td>
                <td className="px-6 py-4 text-zinc-500 dark:text-zinc-400">
                  {new Date(u.createdAt).toLocaleDateString()}
                </td>
                <td className="px-6 py-4 text-right">
                  <button 
                    onClick={() => handleToggleBlock(u.id, u.isActive)}
                    className={`p-2 transition-colors ml-2 ${u.isActive ? 'text-zinc-400 hover:text-amber-500' : 'text-amber-500 hover:text-green-500'}`} 
                    title={u.isActive ? "Bloquear Usuario" : "Desbloquear Usuario"}
                  >
                    {u.isActive ? <Ban className="w-4 h-4" /> : <CheckCircle className="w-4 h-4" />}
                  </button>
                  <button 
                    onClick={() => handleDelete(u.id)}
                    className="p-2 text-zinc-400 hover:text-red-500 transition-colors ml-2" 
                    title="Eliminar Usuario Permanentemente"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </td>
              </motion.tr>
            ))}
            {users.length === 0 && (
              <tr>
                <td colSpan={5} className="px-6 py-8 text-center text-zinc-500">No hay usuarios registrados.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </motion.div>
  );
}
