from django.contrib.gis.db import models as gis_models
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class JenisKejahatan(models.Model):
    """Model untuk jenis kejahatan"""
    nama_jenis_kejahatan = models.CharField(max_length=100, unique=True)
    deskripsi = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'jenis_kejahatan'
        verbose_name = 'Jenis Kejahatan'
        verbose_name_plural = 'Jenis Kejahatan'

    def __str__(self):
        return self.nama_jenis_kejahatan


class NamaKejahatan(models.Model):
    """Model untuk nama kejahatan berdasarkan jenis"""
    jenis_kejahatan = models.ForeignKey(
        JenisKejahatan, 
        on_delete=models.CASCADE,
        related_name='nama_kejahatan'
    )
    nama = models.CharField(max_length=200)
    deskripsi = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'nama_kejahatan'
        verbose_name = 'Nama Kejahatan'
        verbose_name_plural = 'Nama Kejahatan'

    def __str__(self):
        return f"{self.nama} ({self.jenis_kejahatan.nama_jenis_kejahatan})"


class Kecamatan(models.Model):
    """Model untuk kecamatan"""
    nama = models.CharField(max_length=100)
    deskripsi = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'kecamatan'
        verbose_name = 'Kecamatan'
        verbose_name_plural = 'Kecamatan'

    def __str__(self):
        return self.nama


class Desa(models.Model):
    """Model untuk desa/kelurahan"""
    nama = models.CharField(max_length=100)
    deskripsi = models.TextField(blank=True, null=True)
    kecamatan = models.ForeignKey(
        Kecamatan,
        on_delete=models.CASCADE,
        related_name='desa'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'desa'
        verbose_name = 'Desa'
        verbose_name_plural = 'Desa'

    def __str__(self):
        return f"{self.nama} - {self.kecamatan.nama}"


class Status(models.Model):
    """Model untuk status laporan"""
    nama = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'status'
        verbose_name = 'Status'
        verbose_name_plural = 'Status'

    def __str__(self):
        return self.nama


class LaporanKejahatan(models.Model):
    """Model untuk laporan kejahatan"""
    nama_pelapor = models.CharField(max_length=200)
    jenis_kejahatan = models.ForeignKey(
        JenisKejahatan,
        on_delete=models.PROTECT,
        related_name='laporan'
    )
    nama_kejahatan = models.ForeignKey(
        NamaKejahatan,
        on_delete=models.PROTECT,
        related_name='laporan'
    )
    tanggal_kejadian = models.DateField()
    waktu_kejadian = models.TimeField()
    kecamatan = models.ForeignKey(
        Kecamatan,
        on_delete=models.PROTECT,
        related_name='laporan_kejahatan'
    )
    desa = models.ForeignKey(
        Desa,
        on_delete=models.PROTECT,
        related_name='laporan_kejahatan'
    )
    alamat = models.TextField()
    deskripsi = models.TextField()
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name='laporan_kejahatan'
    )
    lokasi = gis_models.PointField(geography=True, null=True, blank=True)
    is_approval = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'laporan_kejahatan'
        verbose_name = 'Laporan Kejahatan'
        verbose_name_plural = 'Laporan Kejahatan'
        ordering = ['-created_at']

    def __str__(self):
        return f"Laporan {self.nama_kejahatan.nama} - {self.tanggal_kejadian}"


class FotoLaporanKejahatan(models.Model):
    """Model untuk foto laporan kejahatan"""
    laporan_kejahatan = models.ForeignKey(
        LaporanKejahatan,
        on_delete=models.CASCADE,
        related_name='foto'
    )
    file_path = models.ImageField(upload_to='laporan_kejahatan/')
    file_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'foto_laporan_kejahatan'
        verbose_name = 'Foto Laporan Kejahatan'
        verbose_name_plural = 'Foto Laporan Kejahatan'

    def __str__(self):
        return f"Foto {self.laporan_kejahatan.id} - {self.file_name}"


class PosKeamanan(models.Model):
    """Model untuk pos keamanan"""
    nama = models.CharField(max_length=200)
    desa = models.ForeignKey(
        Desa,
        on_delete=models.CASCADE,
        related_name='pos_keamanan'
    )
    alamat = models.TextField()
    lokasi = gis_models.PointField(geography=True, null=True, blank=True)
    keterangan = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pos_keamanan'
        verbose_name = 'Pos Keamanan'
        verbose_name_plural = 'Pos Keamanan'

    def __str__(self):
        return self.nama


class FotoPosKeamanan(models.Model):
    """Model untuk foto pos keamanan"""
    pos_keamanan = models.ForeignKey(
        PosKeamanan,
        on_delete=models.CASCADE,
        related_name='foto'
    )
    file_path = models.ImageField(upload_to='pos_keamanan/')
    file_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'foto_pos_keamanan'
        verbose_name = 'Foto Pos Keamanan'
        verbose_name_plural = 'Foto Pos Keamanan'

    def __str__(self):
        return f"Foto {self.pos_keamanan.nama} - {self.file_name}"


class CCTV(models.Model):
    """Model untuk CCTV"""
    nama_lokasi = models.CharField(max_length=200)
    kecamatan = models.ForeignKey(
        Kecamatan,
        on_delete=models.CASCADE,
        related_name='cctv'
    )
    desa = models.ForeignKey(
        Desa,
        on_delete=models.CASCADE,
        related_name='cctv'
    )
    deskripsi = models.TextField(blank=True, null=True)
    url_cctv = models.URLField(max_length=500, blank=True, null=True)
    lokasi = gis_models.PointField(geography=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cctv'
        verbose_name = 'CCTV'
        verbose_name_plural = 'CCTV'

    def __str__(self):
        return self.nama_lokasi


class FotoCCTV(models.Model):
    """Model untuk foto CCTV"""
    cctv = models.ForeignKey(
        CCTV,
        on_delete=models.CASCADE,
        related_name='foto'
    )
    file_path = models.ImageField(upload_to='cctv/')
    file_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'foto_cctv'
        verbose_name = 'Foto CCTV'
        verbose_name_plural = 'Foto CCTV'

    def __str__(self):
        return f"Foto {self.cctv.nama_lokasi} - {self.file_name}"


class KejadianLainnya(models.Model):
    """Model untuk kejadian lainnya"""
    nama_pelapor = models.CharField(max_length=200)
    nama_kejadian = models.CharField(max_length=200)
    deskripsi_kejadian = models.TextField()
    tanggal_kejadian = models.DateField()
    waktu_kejadian = models.TimeField()
    kecamatan = models.ForeignKey(
        Kecamatan,
        on_delete=models.PROTECT,
        related_name='kejadian_lainnya'
    )
    desa = models.ForeignKey(
        Desa,
        on_delete=models.PROTECT,
        related_name='kejadian_lainnya'
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name='kejadian_lainnya'
    )
    lokasi = gis_models.PointField(geography=True, null=True, blank=True)
    is_approval = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'kejadian_lainnya'
        verbose_name = 'Kejadian Lainnya'
        verbose_name_plural = 'Kejadian Lainnya'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.nama_kejadian} - {self.tanggal_kejadian}"


class FotoKejadianLainnya(models.Model):
    """Model untuk foto kejadian lainnya"""
    kejadian_lainnya = models.ForeignKey(
        KejadianLainnya,
        on_delete=models.CASCADE,
        related_name='foto'
    )
    file_path = models.ImageField(upload_to='kejadian_lainnya/')
    file_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'foto_kejadian_lainnya'
        verbose_name = 'Foto Kejadian Lainnya'
        verbose_name_plural = 'Foto Kejadian Lainnya'

    def __str__(self):
        return f"Foto {self.kejadian_lainnya.nama_kejadian} - {self.file_name}"
    

class Area(models.Model):
    """Model untuk area/wilayah dengan geometry polygon"""
    external_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    metadata = models.TextField(blank=True, null=True)
    srs_id = models.CharField(max_length=100, blank=True, null=True)
    wadmkc = models.CharField(max_length=255, blank=True, null=True)
    wadmkd = models.CharField(max_length=255, blank=True, null=True)
    wadmkk = models.CharField(max_length=255, blank=True, null=True)
    wadmpr = models.CharField(max_length=255, blank=True, null=True)
    uupp = models.CharField(max_length=255, blank=True, null=True)
    luas = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    kecamatan = models.ForeignKey(
        'Kecamatan',
        on_delete=models.RESTRICT,
        related_name='areas'
    )
    desa = models.ForeignKey(
        'Desa',
        on_delete=models.RESTRICT,
        related_name='areas'
    )
    geom = gis_models.GeometryField(srid=4326, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'areas'
        managed = False  # Karena tabel sudah dibuat manual
        verbose_name = 'Area'
        verbose_name_plural = 'Areas'

    def __str__(self):
        return f"{self.wadmkd or 'Area'} - {self.desa.nama if self.desa else ''}"
    

class CustomUserManager(BaseUserManager):
    """Manager untuk custom user model"""
    
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('Username harus diisi')
        if not email:
            raise ValueError('Email harus diisi')
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser harus memiliki is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser harus memiliki is_superuser=True')
        
        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom User Model"""
    
    JABATAN_CHOICES = [
        ('admin', 'Administrator'),
        ('operator', 'Operator'),
        ('viewer', 'Viewer'),
        ('petugas', 'Petugas Keamanan'),
    ]
    
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    jabatan = models.CharField(max_length=50, choices=JABATAN_CHOICES, default='viewer')
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # FIX: Tambahkan related_name untuk menghindari clash
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_user_set',  # ← PERBAIKAN DI SINI
        related_query_name='custom_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set',  # ← PERBAIKAN DI SINI
        related_query_name='custom_user',
    )
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'name']
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.username} - {self.name}"
    
    def get_full_name(self):
        return self.name
    
    def get_short_name(self):
        return self.username