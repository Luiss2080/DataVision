import { Module } from '@nestjs/common';
import { AppController } from './app.controller.js';
import { AppService } from './app.service.js';
import { AuthModule } from './auth/auth.module.js';
import { UsersModule } from './users/users.module.js';
import { PrismaModule } from './prisma/prisma.module.js';
import { NotificationsModule } from './notifications/notifications.module.js';

@Module({
  imports: [AuthModule, UsersModule, PrismaModule, NotificationsModule],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
