import { Controller, Get, UseGuards } from '@nestjs/common';
import { DashboardService } from './dashboard.service.js';
import { AuthGuard } from '@nestjs/passport';
import { ApiBearerAuth, ApiTags, ApiOperation } from '@nestjs/swagger';

@ApiTags('dashboard')
@Controller('dashboard')
export class DashboardController {
  constructor(private readonly dashboardService: DashboardService) {}

  @ApiBearerAuth()
  @UseGuards(AuthGuard('jwt'))
  @ApiOperation({ summary: 'Obtener métricas reales para los gráficos del frontend' })
  @Get('metrics')
  getMetrics() {
    return this.dashboardService.getMetrics();
  }
}
