from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q, Count
from .models import (
    JenisKejahatan, NamaKejahatan, Kecamatan, Desa, Status,
    LaporanKejahatan, FotoLaporanKejahatan, PosKeamanan, FotoPosKeamanan,
    CCTV, FotoCCTV, KejadianLainnya, FotoKejadianLainnya, User
)
from .serializers import (
    JenisKejahatanSerializer, NamaKejahatanSerializer, KecamatanSerializer,
    DesaSerializer, StatusSerializer, LaporanKejahatanSerializer,
    FotoLaporanKejahatanSerializer, PosKeamananSerializer, FotoPosKeamananSerializer,
    CCTVSerializer, FotoCCTVSerializer, KejadianLainnyaSerializer,
    FotoKejadianLainnyaSerializer, UserSerializer, UserCreateSerializer, UserUpdateSerializer,
    LoginSerializer, ChangePasswordSerializer
)

from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db.models.functions import AsGeoJSON
import json
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_exempt
from django.db import models
from rest_framework import permissions 




class JenisKejahatanViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    """
    ViewSet untuk CRUD Jenis Kejahatan
    """
    queryset = JenisKejahatan.objects.all()
    serializer_class = JenisKejahatanSerializer

    def get_queryset(self):
        queryset = JenisKejahatan.objects.all()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(nama_jenis_kejahatan__icontains=search) |
                Q(deskripsi__icontains=search)
            )
        return queryset


class NamaKejahatanViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    """
    ViewSet untuk CRUD Nama Kejahatan
    """
    queryset = NamaKejahatan.objects.select_related('jenis_kejahatan').all()
    serializer_class = NamaKejahatanSerializer

    def get_queryset(self):
        queryset = NamaKejahatan.objects.select_related('jenis_kejahatan').all()
        jenis_kejahatan_id = self.request.query_params.get('jenis_kejahatan_id', None)
        search = self.request.query_params.get('search', None)
        
        if jenis_kejahatan_id:
            queryset = queryset.filter(jenis_kejahatan_id=jenis_kejahatan_id)
        
        if search:
            queryset = queryset.filter(
                Q(nama__icontains=search) |
                Q(deskripsi__icontains=search)
            )
        return queryset


class KecamatanViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    """
    ViewSet untuk CRUD Kecamatan
    """
    queryset = Kecamatan.objects.all()
    serializer_class = KecamatanSerializer

    def get_queryset(self):
        queryset = Kecamatan.objects.all()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(nama__icontains=search) |
                Q(deskripsi__icontains=search)
            )
        return queryset


class DesaViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    """
    ViewSet untuk CRUD Desa
    """
    queryset = Desa.objects.select_related('kecamatan').all()
    serializer_class = DesaSerializer

    def get_queryset(self):
        queryset = Desa.objects.select_related('kecamatan').all()
        kecamatan_id = self.request.query_params.get('kecamatan_id', None)
        search = self.request.query_params.get('search', None)
        
        if kecamatan_id:
            queryset = queryset.filter(kecamatan_id=kecamatan_id)
        
        if search:
            queryset = queryset.filter(
                Q(nama__icontains=search) |
                Q(deskripsi__icontains=search)
            )
        return queryset


class StatusViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    """
    ViewSet untuk CRUD Status
    """
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class LaporanKejahatanViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    """
    ViewSet untuk CRUD Laporan Kejahatan
    """
    queryset = LaporanKejahatan.objects.select_related(
        'jenis_kejahatan', 'nama_kejahatan', 'kecamatan', 'desa', 'status'
    ).prefetch_related('foto').all()
    serializer_class = LaporanKejahatanSerializer

    def get_queryset(self):
        queryset = LaporanKejahatan.objects.select_related(
            'jenis_kejahatan', 'nama_kejahatan', 'kecamatan', 'desa', 'status'
        ).prefetch_related('foto').all()
        
        # Filter parameters
        jenis_kejahatan_id = self.request.query_params.get('jenis_kejahatan_id', None)
        nama_kejahatan_id = self.request.query_params.get('nama_kejahatan_id', None)
        kecamatan_id = self.request.query_params.get('kecamatan_id', None)
        desa_id = self.request.query_params.get('desa_id', None)
        status_id = self.request.query_params.get('status_id', None)
        is_approval = self.request.query_params.get('is_approval', None)
        search = self.request.query_params.get('search', None)
        
        if jenis_kejahatan_id:
            queryset = queryset.filter(jenis_kejahatan_id=jenis_kejahatan_id)
        if nama_kejahatan_id:
            queryset = queryset.filter(nama_kejahatan_id=nama_kejahatan_id)
        if kecamatan_id:
            queryset = queryset.filter(kecamatan_id=kecamatan_id)
        if desa_id:
            queryset = queryset.filter(desa_id=desa_id)
        if status_id:
            queryset = queryset.filter(status_id=status_id)
        if is_approval is not None:
            queryset = queryset.filter(is_approval=is_approval.lower() == 'true')
        if search:
            queryset = queryset.filter(
                Q(nama_pelapor__icontains=search) |
                Q(alamat__icontains=search) |
                Q(deskripsi__icontains=search)
            )
        
        return queryset

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Endpoint untuk approve laporan"""
        laporan = self.get_object()
        laporan.is_approval = True
        laporan.save()
        serializer = self.get_serializer(laporan)
        return Response(serializer.data)


class FotoLaporanKejahatanViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    """
    ViewSet untuk CRUD Foto Laporan Kejahatan
    """
    queryset = FotoLaporanKejahatan.objects.all()
    serializer_class = FotoLaporanKejahatanSerializer

    def get_queryset(self):
        queryset = FotoLaporanKejahatan.objects.all()
        laporan_kejahatan_id = self.request.query_params.get('laporan_kejahatan_id', None)
        
        if laporan_kejahatan_id:
            queryset = queryset.filter(laporan_kejahatan_id=laporan_kejahatan_id)
        
        return queryset


class PosKeamananViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    """
    ViewSet untuk CRUD Pos Keamanan
    """
    queryset = PosKeamanan.objects.select_related('desa__kecamatan').prefetch_related('foto').all()
    serializer_class = PosKeamananSerializer

    def get_queryset(self):
        queryset = PosKeamanan.objects.select_related('desa__kecamatan').prefetch_related('foto').all()
        
        desa_id = self.request.query_params.get('desa_id', None)
        search = self.request.query_params.get('search', None)
        
        if desa_id:
            queryset = queryset.filter(desa_id=desa_id)
        if search:
            queryset = queryset.filter(
                Q(nama__icontains=search) |
                Q(alamat__icontains=search) |
                Q(keterangan__icontains=search)
            )
        
        return queryset


class FotoPosKeamananViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    """
    ViewSet untuk CRUD Foto Pos Keamanan
    """
    queryset = FotoPosKeamanan.objects.all()
    serializer_class = FotoPosKeamananSerializer

    def get_queryset(self):
        queryset = FotoPosKeamanan.objects.all()
        pos_keamanan_id = self.request.query_params.get('pos_keamanan_id', None)
        
        if pos_keamanan_id:
            queryset = queryset.filter(pos_keamanan_id=pos_keamanan_id)
        
        return queryset


class CCTVViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    """
    ViewSet untuk CRUD CCTV
    """
    queryset = CCTV.objects.select_related('kecamatan', 'desa').prefetch_related('foto').all()
    serializer_class = CCTVSerializer

    def get_queryset(self):
        queryset = CCTV.objects.select_related('kecamatan', 'desa').prefetch_related('foto').all()
        
        kecamatan_id = self.request.query_params.get('kecamatan_id', None)
        desa_id = self.request.query_params.get('desa_id', None)
        search = self.request.query_params.get('search', None)
        
        if kecamatan_id:
            queryset = queryset.filter(kecamatan_id=kecamatan_id)
        if desa_id:
            queryset = queryset.filter(desa_id=desa_id)
        if search:
            queryset = queryset.filter(
                Q(nama_lokasi__icontains=search) |
                Q(deskripsi__icontains=search)
            )
        
        return queryset


class FotoCCTVViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    """
    ViewSet untuk CRUD Foto CCTV
    """
    queryset = FotoCCTV.objects.all()
    serializer_class = FotoCCTVSerializer

    def get_queryset(self):
        queryset = FotoCCTV.objects.all()
        cctv_id = self.request.query_params.get('cctv_id', None)
        
        if cctv_id:
            queryset = queryset.filter(cctv_id=cctv_id)
        
        return queryset


class KejadianLainnyaViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    """
    ViewSet untuk CRUD Kejadian Lainnya
    """
    queryset = KejadianLainnya.objects.select_related(
        'kecamatan', 'desa', 'status'
    ).prefetch_related('foto').all()
    serializer_class = KejadianLainnyaSerializer

    def get_queryset(self):
        queryset = KejadianLainnya.objects.select_related(
            'kecamatan', 'desa', 'status'
        ).prefetch_related('foto').all()
        
        kecamatan_id = self.request.query_params.get('kecamatan_id', None)
        desa_id = self.request.query_params.get('desa_id', None)
        status_id = self.request.query_params.get('status_id', None)
        is_approval = self.request.query_params.get('is_approval', None)
        search = self.request.query_params.get('search', None)
        
        if kecamatan_id:
            queryset = queryset.filter(kecamatan_id=kecamatan_id)
        if desa_id:
            queryset = queryset.filter(desa_id=desa_id)
        if status_id:
            queryset = queryset.filter(status_id=status_id)
        if is_approval is not None:
            queryset = queryset.filter(is_approval=is_approval.lower() == 'true')
        if search:
            queryset = queryset.filter(
                Q(nama_pelapor__icontains=search) |
                Q(nama_kejadian__icontains=search) |
                Q(deskripsi_kejadian__icontains=search)
            )
        
        return queryset

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Endpoint untuk approve kejadian"""
        kejadian = self.get_object()
        kejadian.is_approval = True
        kejadian.save()
        serializer = self.get_serializer(kejadian)
        return Response(serializer.data)


class FotoKejadianLainnyaViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    """
    ViewSet untuk CRUD Foto Kejadian Lainnya
    """
    queryset = FotoKejadianLainnya.objects.all()
    serializer_class = FotoKejadianLainnyaSerializer

    def get_queryset(self):
        queryset = FotoKejadianLainnya.objects.all()
        kejadian_lainnya_id = self.request.query_params.get('kejadian_lainnya_id', None)
        
        if kejadian_lainnya_id:
            queryset = queryset.filter(kejadian_lainnya_id=kejadian_lainnya_id)
        
        return queryset


@api_view(['GET'])
def statistik_dashboard(request):
    """
    API endpoint untuk mendapatkan statistik dashboard:
    - Jumlah Laporan Kejahatan yang sudah diapprove (is_approval = True)
    - Jumlah Desa
    - Jumlah Pos Keamanan
    - Jumlah CCTV
    """
    try:
        # 1. Jumlah Laporan Kejahatan yang diapprove
        jumlah_laporan_kejahatan_approved = LaporanKejahatan.objects.filter(
            is_approval=True
        ).count()
        
        # 2. Jumlah Desa
        jumlah_desa = Desa.objects.count()
        
        # 3. Jumlah Pos Keamanan
        jumlah_pos_keamanan = PosKeamanan.objects.count()
        
        # 4. Jumlah CCTV
        jumlah_cctv = CCTV.objects.count()
        
        # Menyusun response data
        data = {
            'success': True,
            'message': 'Statistik berhasil diambil',
            'data': {
                'jumlah_laporan_kejahatan_approved': jumlah_laporan_kejahatan_approved,
                'jumlah_desa': jumlah_desa,
                'jumlah_pos_keamanan': jumlah_pos_keamanan,
                'jumlah_cctv': jumlah_cctv
            }
        }
        
        return Response(data, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Terjadi kesalahan: {str(e)}',
            'data': None
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


@api_view(['GET'])
def map_data(request):
    """
    API endpoint untuk mendapatkan semua data peta:
    - Areas (polygon dengan warna berbeda)
    - Laporan Kejahatan (markers)
    - Pos Keamanan (markers)
    - CCTV (markers)
    """
    try:
        # 1. Ambil data Areas dengan geometry
        from .models import Area
        areas = Area.objects.select_related('kecamatan', 'desa').all()
        
        # Generate warna untuk setiap area
        colors = [
            '#ef4444',  # red
            '#f59e0b',  # amber
            '#10b981',  # emerald
            '#3b82f6',  # blue
            '#8b5cf6',  # violet
            '#ec4899',  # pink
            '#14b8a6',  # teal
            '#f97316',  # orange
        ]
        
        # Konversi areas ke GeoJSON
        area_features = []
        for idx, area in enumerate(areas):
            if area.geom:
                feature = {
                    'type': 'Feature',
                    'id': area.id,
                    'properties': {
                        'id': area.id,
                        'name': area.wadmkd or area.desa.nama,
                        'kecamatan': area.kecamatan.nama,
                        'desa': area.desa.nama,
                        'luas': float(area.luas) if area.luas else 0,
                        'color': colors[idx % len(colors)],
                    },
                    'geometry': json.loads(area.geom.geojson)
                }
                area_features.append(feature)
        
        areas_geojson = {
            'type': 'FeatureCollection',
            'features': area_features
        }
        
        # 2. Ambil Laporan Kejahatan yang sudah di-approve
        from .models import LaporanKejahatan
        laporan_kejahatan = LaporanKejahatan.objects.filter(
            is_approval=True,
            lokasi__isnull=False
        ).select_related(
            'jenis_kejahatan', 'nama_kejahatan', 'kecamatan', 'desa', 'status'
        ).prefetch_related('foto')
        
        crime_markers = []
        for laporan in laporan_kejahatan:
            if laporan.lokasi:
                crime_markers.append({
                    'id': laporan.id,
                    'type': 'crime',
                    'name': laporan.nama_kejahatan.nama,
                    'jenis': laporan.jenis_kejahatan.nama_jenis_kejahatan,
                    'latitude': laporan.lokasi.y,
                    'longitude': laporan.lokasi.x,
                    'address': laporan.alamat,
                    'description': laporan.deskripsi,
                    'date': str(laporan.tanggal_kejadian),
                    'time': str(laporan.waktu_kejadian),
                    'status': laporan.status.nama,
                    'kecamatan': laporan.kecamatan.nama,
                    'desa': laporan.desa.nama,
                    'pelapor': laporan.nama_pelapor,
                    'photos': [foto.file_path.url for foto in laporan.foto.all()]
                })
        
        # 3. Ambil Pos Keamanan
        from .models import PosKeamanan
        pos_keamanan = PosKeamanan.objects.filter(
            lokasi__isnull=False
        ).select_related('desa__kecamatan').prefetch_related('foto')
        
        security_markers = []
        for pos in pos_keamanan:
            if pos.lokasi:
                security_markers.append({
                    'id': pos.id,
                    'type': 'security_post',
                    'name': pos.nama,
                    'latitude': pos.lokasi.y,
                    'longitude': pos.lokasi.x,
                    'address': pos.alamat,
                    'description': pos.keterangan or '',
                    'kecamatan': pos.desa.kecamatan.nama,
                    'desa': pos.desa.nama,
                    'photos': [foto.file_path.url for foto in pos.foto.all()]
                })
        
        # 4. Ambil CCTV
        from .models import CCTV
        cctv_list = CCTV.objects.filter(
            lokasi__isnull=False
        ).select_related('kecamatan', 'desa').prefetch_related('foto')
        
        cctv_markers = []
        for cctv in cctv_list:
            if cctv.lokasi:
                cctv_markers.append({
                    'id': cctv.id,
                    'type': 'cctv',
                    'name': cctv.nama_lokasi,
                    'latitude': cctv.lokasi.y,
                    'longitude': cctv.lokasi.x,
                    'description': cctv.deskripsi or '',
                    'url_cctv': cctv.url_cctv or '',
                    'kecamatan': cctv.kecamatan.nama,
                    'desa': cctv.desa.nama,
                    'photos': [foto.file_path.url for foto in cctv.foto.all()]
                })
        
        # Response data
        data = {
            'success': True,
            'message': 'Data peta berhasil diambil',
            'data': {
                'areas': areas_geojson,
                'crime_reports': crime_markers,
                'security_posts': security_markers,
                'cctvs': cctv_markers,
                'summary': {
                    'total_areas': len(area_features),
                    'total_crime_reports': len(crime_markers),
                    'total_security_posts': len(security_markers),
                    'total_cctvs': len(cctv_markers),
                }
            }
        }
        
        return Response(data, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Terjadi kesalahan: {str(e)}',
            'data': None
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def area_statistics(request, area_id=None):
    """
    API endpoint untuk mendapatkan statistik area tertentu
    """
    try:
        from .models import Area, LaporanKejahatan, PosKeamanan, CCTV
        from django.contrib.gis.geos import GEOSGeometry
        
        if area_id:
            # Statistik untuk area spesifik
            area = Area.objects.get(id=area_id)
            
            # Hitung laporan kejahatan dalam area
            # Menggunakan spatial query untuk cek point dalam polygon
            crime_in_area = LaporanKejahatan.objects.filter(
                is_approval=True,
                lokasi__isnull=False,
                lokasi__within=area.geom
            ).select_related('jenis_kejahatan', 'nama_kejahatan', 'status')
            
            # Hitung pos keamanan dalam area
            security_in_area = PosKeamanan.objects.filter(
                lokasi__isnull=False,
                lokasi__within=area.geom
            )
            
            # Hitung CCTV dalam area
            cctv_in_area = CCTV.objects.filter(
                lokasi__isnull=False,
                lokasi__within=area.geom
            )
            
            # Statistik berdasarkan jenis kejahatan
            crime_by_type = crime_in_area.values(
                'jenis_kejahatan__nama_jenis_kejahatan'
            ).annotate(
                count=Count('id')
            ).order_by('-count')
            
            # Statistik berdasarkan status
            crime_by_status = crime_in_area.values(
                'status__nama'
            ).annotate(
                count=Count('id')
            )
            
            # Format data untuk chart
            by_type = [
                {
                    'name': item['jenis_kejahatan__nama_jenis_kejahatan'],
                    'value': item['count']
                }
                for item in crime_by_type
            ]
            
            solved = crime_by_status.filter(status__nama='Selesai').first()
            pending = crime_by_status.exclude(status__nama='Selesai').aggregate(
                total=Count('id')
            )
            
            # Recent cases
            recent_cases = []
            for crime in crime_in_area.order_by('-created_at')[:10]:
                recent_cases.append({
                    'id': crime.id,
                    'type': crime.nama_kejahatan.nama,
                    'location': crime.alamat,
                    'date': str(crime.tanggal_kejadian),
                    'status': crime.status.nama
                })
            
            # Monthly trend (simulasi - sesuaikan dengan kebutuhan)
            from django.db.models.functions import TruncMonth
            monthly_data = crime_in_area.annotate(
                month=TruncMonth('tanggal_kejadian')
            ).values('month').annotate(
                cases=Count('id')
            ).order_by('month')
            
            monthly_trend = [
                {
                    'month': item['month'].strftime('%b'),
                    'cases': item['cases']
                }
                for item in monthly_data
            ]
            
            statistics = {
                'area_info': {
                    'id': area.id,
                    'name': area.wadmkd or area.desa.nama,
                    'kecamatan': area.kecamatan.nama,
                    'desa': area.desa.nama,
                    'luas': float(area.luas) if area.luas else 0,
                },
                'crime_stats': {
                    'totalCases': crime_in_area.count(),
                    'solved': solved['count'] if solved else 0,
                    'pending': pending['total'] or 0,
                    'byType': by_type,
                    'recentCases': recent_cases,
                    'monthlyTrend': monthly_trend
                },
                'infrastructure': {
                    'security_posts': security_in_area.count(),
                    'cctvs': cctv_in_area.count()
                }
            }
            
            return Response({
                'success': True,
                'message': 'Statistik area berhasil diambil',
                'data': statistics
            }, status=status.HTTP_200_OK)
        
        else:
            # Statistik semua area
            areas = Area.objects.all()
            area_stats = []
            
            for area in areas:
                crime_count = LaporanKejahatan.objects.filter(
                    is_approval=True,
                    lokasi__isnull=False,
                    lokasi__within=area.geom
                ).count()
                
                area_stats.append({
                    'id': area.id,
                    'name': area.wadmkd or area.desa.nama,
                    'crime_count': crime_count,
                })
            
            return Response({
                'success': True,
                'message': 'Statistik semua area berhasil diambil',
                'data': area_stats
            }, status=status.HTTP_200_OK)
    
    except Area.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Area tidak ditemukan',
            'data': None
        }, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Terjadi kesalahan: {str(e)}',
            'data': None
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AreaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet untuk CRUD Area (Read-only karena managed=False)
    """
    from .models import Area
    from .serializers import AreaSerializer
    
    queryset = Area.objects.select_related('kecamatan', 'desa').all()
    serializer_class = AreaSerializer
    
    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """Endpoint untuk mendapatkan statistik area"""
        return area_statistics(request, area_id=pk)
    



class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permission kustom: Admin bisa semua, user lain hanya read
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_authenticated and request.user.jabatan == 'admin'


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet untuk CRUD User
    """
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer
    
    def get_queryset(self):
        queryset = User.objects.all()
        
        # Filter berdasarkan status
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        # Filter berdasarkan jabatan
        jabatan = self.request.query_params.get('jabatan', None)
        if jabatan:
            queryset = queryset.filter(jabatan=jabatan)
        
        # Search
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                models.Q(username__icontains=search) |
                models.Q(name__icontains=search) |
                models.Q(email__icontains=search)
            )
        
        return queryset.order_by('-created_at')
    
    @action(detail=True, methods=['post'])
    def change_password(self, request, pk=None):
        """Endpoint untuk ganti password user tertentu (admin only)"""
        user = self.get_object()
        
        if request.user.jabatan != 'admin' and request.user.id != user.id:
            return Response(
                {'error': 'Anda tidak memiliki akses'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Password berhasil diubah'})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def toggle_status(self, request, pk=None):
        """Toggle status aktif/nonaktif user"""
        user = self.get_object()
        user.is_active = not user.is_active
        user.save()
        
        return Response({
            'message': f"User {'diaktifkan' if user.is_active else 'dinonaktifkan'}",
            'is_active': user.is_active
        })


@csrf_exempt  # ← TAMBAHKAN INI untuk bypass CSRF check pada login
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    """
    Login endpoint
    POST /api/auth/login/
    Body: { "username": "admin", "password": "admin123" }
    
    Returns:
    {
        "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
        "user": {
            "id": 1,
            "username": "admin",
            "email": "admin@kriminalitas.com",
            "name": "Administrator",
            "jabatan": "admin"
        },
        "message": "Login berhasil"
    }
    """
    try:
        # Log request untuk debugging
        print(f"Login attempt - Username: {request.data.get('username')}")
        
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Hapus token lama jika ada
            Token.objects.filter(user=user).delete()
            
            # Buat token baru
            token = Token.objects.create(user=user)
            
            # OPTIONAL: Login user untuk session (tidak diperlukan untuk token auth)
            # login(request, user)
            
            print(f"Login successful - User: {user.username}")
            
            return Response({
                'token': token.key,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'name': user.name,
                    'jabatan': user.jabatan,
                },
                'message': 'Login berhasil'
            }, status=status.HTTP_200_OK)
        
        # Invalid credentials
        print(f"Login failed - Errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        # Catch any unexpected errors
        print(f"Login error: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return Response({
            'error': 'Terjadi kesalahan server',
            'detail': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt  # ← TAMBAHKAN INI juga untuk logout
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """
    Logout endpoint
    POST /api/auth/logout/
    Headers: Authorization: Token <token>
    """
    try:
        # Hapus token
        request.user.auth_token.delete()
        logout(request)
        return Response({'message': 'Logout berhasil'})
    except Exception as e:
        print(f"Logout error: {str(e)}")
        return Response(
            {'error': 'Logout gagal', 'detail': str(e)}, 
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def current_user(request):
    """
    Get current logged in user
    GET /api/auth/me/
    Headers: Authorization: Token <token>
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_profile(request):
    """
    Update current user profile
    PUT /api/auth/profile/
    Headers: Authorization: Token <token>
    """
    serializer = UserUpdateSerializer(
        request.user, 
        data=request.data, 
        partial=True
    )
    
    if serializer.is_valid():
        serializer.save()
        return Response({
            'user': UserSerializer(request.user).data,
            'message': 'Profile berhasil diupdate'
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def change_password_view(request):
    """
    Change password for current user
    POST /api/auth/change-password/
    Headers: Authorization: Token <token>
    Body: {
        "old_password": "old",
        "new_password": "new",
        "new_password_confirm": "new"
    }
    """
    serializer = ChangePasswordSerializer(
        data=request.data,
        context={'request': request}
    )
    
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Password berhasil diubah'})
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
