import { ExtractJwt, Strategy } from 'passport-jwt';
import { PassportStrategy } from '@nestjs/passport';
import { Injectable, UnauthorizedException } from '@nestjs/common';
import { UsersService } from '../users/users.service';

@Injectable()
export class JwtStrategy extends PassportStrategy(Strategy) {
  constructor(private usersService: UsersService) {
    super({
      jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
      ignoreExpiration: false,
      secretOrKey: process.env.JWT_SECRET || 'fallback_secret_for_dev',
    });
  }

  async validate(payload: any) {
    const user = await this.usersService.findById(payload.sub);
    // Si el usuario no existe o fue bloqueado (isActive === false)
    if (!user || !user.isActive) {
      throw new UnauthorizedException('Tu cuenta ha sido suspendida o no existe.');
    }
    return user;
  }
}
