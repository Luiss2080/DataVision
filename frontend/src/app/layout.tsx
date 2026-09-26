import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "DataVision | Plataforma de Analítica Avanzada",
  description: "Sistema web premium para la gestión y visualización de datos en tiempo real.",
};

import { ThemeProvider } from "@/components/theme-provider";
import { SocketProvider } from "@/components/socket-provider";
import { Toaster } from "sonner";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es" suppressHydrationWarning>
      <body className={`${inter.variable} antialiased selection:bg-blue-500/30`}>
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem disableTransitionOnChange>
          <SocketProvider>
            {children}
            <Toaster richColors position="top-right" />
          </SocketProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}
