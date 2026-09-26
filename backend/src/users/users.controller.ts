import { Controller, Get, Delete, Patch, Param, UseGuards, HttpException, HttpStatus, Post, UseInterceptors, UploadedFile, Body, Request } from '@nestjs/common';
import { FileInterceptor } from '@nestjs/platform-express';
import { diskStorage } from 'multer';
import { extname } from 'path';
import { UsersService } from './users.service.js';
import { AuthGuard } from '@nestjs/passport';
import { RolesGuard } from '../auth/roles.guard.js';
import { Roles } from '../auth/roles.decorator.js';
import { ApiBearerAuth, ApiTags, ApiOperation } from '@nestjs/swagger';

@ApiTags('users')
@Controller('users')
export class UsersController {
  constructor(private readonly usersService: UsersService) {}

  @ApiBearerAuth()
  @UseGuards(AuthGuard('jwt'), RolesGuard)
  @Roles('ADMIN')
  @ApiOperation({ summary: 'Listar todos los usuarios (Solo ADMIN)' })
  @Get('all')
  findAll() {
    return this.usersService.findAll();
  }

  @ApiBearerAuth()
  @UseGuards(AuthGuard('jwt'), RolesGuard)
  @Roles('ADMIN')
  @ApiOperation({ summary: 'Bloquear / Desbloquear un usuario' })
  @Patch(':id/block')
  async toggleBlock(@Param('id') id: string) {
    try {
      return await this.usersService.toggleBlock(id);
    } catch (error: any) {
      throw new HttpException(error.message, HttpStatus.BAD_REQUEST);
    }
  }

  @ApiBearerAuth()
  @UseGuards(AuthGuard('jwt'), RolesGuard)
  @Roles('ADMIN')
  @ApiOperation({ summary: 'Eliminar un usuario permanentemente' })
  @Delete(':id')
  async remove(@Param('id') id: string) {
    try {
      return await this.usersService.remove(id);
    } catch (error: any) {
      throw new HttpException(error.message, HttpStatus.BAD_REQUEST);
    }
  }

  @ApiBearerAuth()
  @UseGuards(AuthGuard('jwt'))
  @ApiOperation({ summary: 'Actualizar perfil (Avatar, Contraseña)' })
  @Post('profile')
  @UseInterceptors(FileInterceptor('avatar', {
    storage: diskStorage({
      destination: './uploads/avatars',
      filename: (req, file, cb) => {
        const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
        cb(null, `${uniqueSuffix}${extname(file.originalname)}`);
      }
    })
  }))
  async updateProfile(
    @Request() req: any, 
    @Body() body: { password?: string, firstName?: string, lastName?: string },
    @UploadedFile() file?: Express.Multer.File
  ) {
    const avatarUrl = file ? `/uploads/avatars/${file.filename}` : undefined;
    return this.usersService.updateProfile(req.user.id, { ...body, avatarUrl });
  }
}
