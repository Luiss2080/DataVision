import { Injectable } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service.js';

@Injectable()
export class DashboardService {
  constructor(private prisma: PrismaService) {}

  async getMetrics() {
    // 1. Consultas Reales a la Base de Datos
    const totalUsers = await this.prisma.user.count();
    const activeUsers = await this.prisma.user.count({ where: { isActive: true } });
    const adminUsers = await this.prisma.user.count({ where: { role: 'ADMIN' } });

    // 2. Generación de data para el Gráfico (Mezclando el conteo real con datos de simulación para Ingresos, ya que aún no tenemos tabla de Ventas)
    const baseVal = totalUsers * 10;
    const chartData = [
      { name: 'Lun', usuarios: totalUsers > 0 ? totalUsers - 1 : 0, ingresos: baseVal + 2400 },
      { name: 'Mar', usuarios: totalUsers, ingresos: baseVal + 1398 },
      { name: 'Mié', usuarios: totalUsers, ingresos: baseVal + 9800 },
      { name: 'Jue', usuarios: totalUsers + 1, ingresos: baseVal + 3908 },
      { name: 'Vie', usuarios: totalUsers + 2, ingresos: baseVal + 4800 },
      { name: 'Sáb', usuarios: totalUsers + 4, ingresos: baseVal + 3800 },
      { name: 'Dom', usuarios: totalUsers + 5, ingresos: baseVal + 4300 },
    ];

    return {
      stats: [
        { title: 'Usuarios Totales', value: totalUsers.toString(), change: '+100%' },
        { title: 'Cuentas Activas', value: activeUsers.toString(), change: '+100%' },
        { title: 'Administradores', value: adminUsers.toString(), change: 'Estable' }
      ],
      chartData
    };
  }
}
