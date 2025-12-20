from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    JenisKejahatanViewSet, NamaKejahatanViewSet, KecamatanViewSet,
    DesaViewSet, StatusViewSet, LaporanKejahatanViewSet,
    FotoLaporanKejahatanViewSet, PosKeamananViewSet, FotoPosKeamananViewSet,
    CCTVViewSet, FotoCCTVViewSet, KejadianLainnyaViewSet,
    FotoKejadianLainnyaViewSet
)

router = DefaultRouter()
router.register(r'jenis-kejahatan', JenisKejahatanViewSet, basename='jenis-kejahatan')
router.register(r'nama-kejahatan', NamaKejahatanViewSet, basename='nama-kejahatan')
router.register(r'kecamatan', KecamatanViewSet, basename='kecamatan')
router.register(r'desa', DesaViewSet, basename='desa')
router.register(r'status', StatusViewSet, basename='status')
router.register(r'laporan-kejahatan', LaporanKejahatanViewSet, basename='laporan-kejahatan')
router.register(r'foto-laporan-kejahatan', FotoLaporanKejahatanViewSet, basename='foto-laporan-kejahatan')
router.register(r'pos-keamanan', PosKeamananViewSet, basename='pos-keamanan')
router.register(r'foto-pos-keamanan', FotoPosKeamananViewSet, basename='foto-pos-keamanan')
router.register(r'cctv', CCTVViewSet, basename='cctv')
router.register(r'foto-cctv', FotoCCTVViewSet, basename='foto-cctv')
router.register(r'kejadian-lainnya', KejadianLainnyaViewSet, basename='kejadian-lainnya')
router.register(r'foto-kejadian-lainnya', FotoKejadianLainnyaViewSet, basename='foto-kejadian-lainnya')

urlpatterns = [
    path('api/', include(router.urls)),
]