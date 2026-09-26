import { Injectable, CanActivate, ExecutionContext } from '@nestjs/common';
import { Reflector } from '@nestjs/core';

@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const roles = this.reflector.get<string[]>('roles', context.getHandler());
    if (!roles) {
      return true; // Si no hay roles requeridos, dejar pasar
    }
    const request = context.switchToHttp().getRequest();
    const user = request.user;
    
    // Comparar rol del usuario (sacado del JWT) con los roles requeridos
    return user && roles.includes(user.role);
  }
}
