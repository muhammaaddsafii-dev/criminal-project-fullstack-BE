from django.contrib import admin
from .models import (
    JenisKejahatan, NamaKejahatan, Kecamatan, Desa, Status,
    LaporanKejahatan, FotoLaporanKejahatan, PosKeamanan, FotoPosKeamanan,
    CCTV, FotoCCTV, KejadianLainnya, FotoKejadianLainnya, User
)

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin



@admin.register(JenisKejahatan)
class JenisKejahatanAdmin(admin.ModelAdmin):
    list_display = ('id', 'nama_jenis_kejahatan', 'created_at', 'updated_at')
    search_fields = ('nama_jenis_kejahatan', 'deskripsi')
    list_filter = ('created_at',)


@admin.register(NamaKejahatan)
class NamaKejahatanAdmin(admin.ModelAdmin):
    list_display = ('id', 'nama', 'jenis_kejahatan', 'created_at')
    search_fields = ('nama', 'deskripsi')
    list_filter = ('jenis_kejahatan', 'created_at')
    autocomplete_fields = ('jenis_kejahatan',)


@admin.register(Kecamatan)
class KecamatanAdmin(admin.ModelAdmin):
    list_display = ('id', 'nama', 'created_at', 'updated_at')
    search_fields = ('nama', 'deskripsi')


@admin.register(Desa)
class DesaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nama', 'kecamatan', 'created_at')
    search_fields = ('nama', 'deskripsi')
    list_filter = ('kecamatan', 'created_at')
    autocomplete_fields = ('kecamatan',)


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'nama', 'created_at')
    search_fields = ('nama',)


class FotoLaporanKejahatanInline(admin.TabularInline):
    model = FotoLaporanKejahatan
    extra = 1


@admin.register(LaporanKejahatan)
class LaporanKejahatanAdmin(admin.ModelAdmin):
    list_display = ('id', 'nama_pelapor', 'jenis_kejahatan', 'nama_kejahatan', 
                    'tanggal_kejadian', 'status', 'is_approval', 'created_at')
    search_fields = ('nama_pelapor', 'alamat', 'deskripsi')
    list_filter = ('jenis_kejahatan', 'status', 'is_approval', 'tanggal_kejadian', 'created_at')
    date_hierarchy = 'tanggal_kejadian'
    inlines = [FotoLaporanKejahatanInline]
    autocomplete_fields = ('jenis_kejahatan', 'nama_kejahatan', 'kecamatan', 'desa', 'status')


@admin.register(FotoLaporanKejahatan)
class FotoLaporanKejahatanAdmin(admin.ModelAdmin):
    list_display = ('id', 'laporan_kejahatan', 'file_name', 'created_at')
    search_fields = ('file_name',)
    list_filter = ('created_at',)


class FotoPosKeamananInline(admin.TabularInline):
    model = FotoPosKeamanan
    extra = 1


@admin.register(PosKeamanan)
class PosKeamananAdmin(admin.ModelAdmin):
    list_display = ('id', 'nama', 'desa', 'created_at')
    search_fields = ('nama', 'alamat', 'keterangan')
    list_filter = ('desa', 'created_at')
    inlines = [FotoPosKeamananInline]
    autocomplete_fields = ('desa',)


@admin.register(FotoPosKeamanan)
class FotoPosKeamananAdmin(admin.ModelAdmin):
    list_display = ('id', 'pos_keamanan', 'file_name', 'created_at')
    search_fields = ('file_name',)
    list_filter = ('created_at',)


class FotoCCTVInline(admin.TabularInline):
    model = FotoCCTV
    extra = 1


@admin.register(CCTV)
class CCTVAdmin(admin.ModelAdmin):
    list_display = ('id', 'nama_lokasi', 'kecamatan', 'desa', 'created_at')
    search_fields = ('nama_lokasi', 'deskripsi')
    list_filter = ('kecamatan', 'desa', 'created_at')
    inlines = [FotoCCTVInline]
    autocomplete_fields = ('kecamatan', 'desa')


@admin.register(FotoCCTV)
class FotoCCTVAdmin(admin.ModelAdmin):
    list_display = ('id', 'cctv', 'file_name', 'created_at')
    search_fields = ('file_name',)
    list_filter = ('created_at',)


class FotoKejadianLainnyaInline(admin.TabularInline):
    model = FotoKejadianLainnya
    extra = 1


@admin.register(KejadianLainnya)
class KejadianLainnyaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nama_pelapor', 'nama_kejadian', 'tanggal_kejadian', 
                    'status', 'is_approval', 'created_at')
    search_fields = ('nama_pelapor', 'nama_kejadian', 'deskripsi_kejadian')
    list_filter = ('status', 'is_approval', 'tanggal_kejadian', 'created_at')
    date_hierarchy = 'tanggal_kejadian'
    inlines = [FotoKejadianLainnyaInline]
    autocomplete_fields = ('kecamatan', 'desa', 'status')


@admin.register(FotoKejadianLainnya)
class FotoKejadianLainnyaAdmin(admin.ModelAdmin):
    list_display = ('id', 'kejadian_lainnya', 'file_name', 'created_at')
    search_fields = ('file_name',)
    list_filter = ('created_at',)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'name', 'jabatan', 'is_active', 'is_staff', 'created_at')
    list_filter = ('jabatan', 'is_active', 'is_staff', 'created_at')
    search_fields = ('username', 'email', 'name')
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informasi Personal', {'fields': ('name', 'email', 'jabatan')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Tanggal Penting', {'fields': ('created_at', 'updated_at')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'name', 'jabatan', 'password1', 'password2', 'is_active', 'is_staff'),
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')