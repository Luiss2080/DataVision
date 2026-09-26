import { Module } from '@nestjs/common';
import { NotificationsGateway } from './notifications.gateway.js';

@Module({
  providers: [NotificationsGateway],
  exports: [NotificationsGateway],
})
export class NotificationsModule {}
