import { Controller, Post, Body, UnauthorizedException, Get, UseGuards, Request } from '@nestjs/common';
import { AuthService } from './auth.service.js';
import { Prisma } from '@prisma/client';
import { AuthGuard } from '@nestjs/passport';
import { ApiTags, ApiBearerAuth, ApiOperation } from '@nestjs/swagger';
import { NotificationsGateway } from '../notifications/notifications.gateway.js';

@ApiTags('auth')
@Controller('auth')
export class AuthController {
  constructor(
    private authService: AuthService,
    private notificationsGateway: NotificationsGateway
  ) {}

  @ApiOperation({ summary: 'Iniciar sesión' })
  @Post('login')
  async login(@Body() body: any) {
    const user = await this.authService.validateUser(body.email, body.password);
    if (!user) {
      throw new UnauthorizedException('Credenciales inválidas');
    }
    
    // Emitimos una alerta en tiempo real a todos los clientes conectados
    this.notificationsGateway.emitNotification(`El usuario ${user.email} ha iniciado sesión.`, 'info');
    
    return this.authService.login(user);
  }

  @ApiOperation({ summary: 'Registrar nuevo usuario' })
  @Post('register')
  async register(@Body() body: Prisma.UserCreateInput) {
    return this.authService.register(body);
  }

  @ApiBearerAuth()
  @UseGuards(AuthGuard('jwt'))
  @ApiOperation({ summary: 'Obtener perfil propio (Requiere Token)' })
  @Get('profile')
  getProfile(@Request() req: any) {
    return req.user;
  }
}
