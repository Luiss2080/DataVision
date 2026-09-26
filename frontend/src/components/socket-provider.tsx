"use client";

import { useEffect, useState } from "react";
import { io, Socket } from "socket.io-client";
import { toast } from "sonner";
import { useAuthStore } from "@/store/useAuthStore";

export function SocketProvider({ children }: { children: React.ReactNode }) {
  const [socket, setSocket] = useState<Socket | null>(null);
  const token = useAuthStore((state) => state.token);

  useEffect(() => {
    // Solo conectarse a WebSockets si el usuario está autenticado
    if (!token) return;

    const socketInstance = io(process.env.NEXT_PUBLIC_API_URL?.replace('/api', '') || 'http://localhost:3000', {
      transports: ["websocket"],
    });

    socketInstance.on("connect", () => {
      console.log("WebSocket Conectado");
    });

    socketInstance.on("onNotification", (data: { message: string, type: 'success'|'info'|'warning'|'error' }) => {
      switch (data.type) {
        case "success": toast.success(data.message); break;
        case "error": toast.error(data.message); break;
        case "warning": toast.warning(data.message); break;
        default: toast.info(data.message);
      }
    });

    setSocket(socketInstance);

    return () => {
      socketInstance.disconnect();
    };
  }, [token]);

  return <>{children}</>;
}
