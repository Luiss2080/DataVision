import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module.js';
import { SwaggerModule, DocumentBuilder } from '@nestjs/swagger';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  
  // Configuración de Swagger (Documentación interactiva de la API)
  const config = new DocumentBuilder()
    .setTitle('DataVision API')
    .setDescription('API Backend para Landing Page y Sistema Web')
    .setVersion('1.0')
    .addBearerAuth()
    .build();
  const document = SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('api/docs', app, document);

  // Habilitar CORS para conectar con Next.js después
  app.enableCors();

  await app.listen(process.env.PORT ?? 3000);
}
await bootstrap();
