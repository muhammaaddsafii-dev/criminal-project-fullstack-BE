from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django.db.models import Q, Count
from .models import (
    JenisKejahatan, NamaKejahatan, Kecamatan, Desa, Status,
    LaporanKejahatan, FotoLaporanKejahatan, PosKeamanan, FotoPosKeamanan,
    CCTV, FotoCCTV, KejadianLainnya, FotoKejadianLainnya
)
from .serializers import (
    JenisKejahatanSerializer, NamaKejahatanSerializer, KecamatanSerializer,
    DesaSerializer, StatusSerializer, LaporanKejahatanSerializer,
    FotoLaporanKejahatanSerializer, PosKeamananSerializer, FotoPosKeamananSerializer,
    CCTVSerializer, FotoCCTVSerializer, KejadianLainnyaSerializer,
    FotoKejadianLainnyaSerializer
)


class JenisKejahatanViewSet(viewsets.ModelViewSet):
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
    """
    ViewSet untuk CRUD Status
    """
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class LaporanKejahatanViewSet(viewsets.ModelViewSet):
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