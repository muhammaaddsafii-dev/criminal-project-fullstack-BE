from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    JenisKejahatanViewSet, NamaKejahatanViewSet, KecamatanViewSet,
    DesaViewSet, StatusViewSet, LaporanKejahatanViewSet,
    FotoLaporanKejahatanViewSet, PosKeamananViewSet, FotoPosKeamananViewSet,
    CCTVViewSet, FotoCCTVViewSet, KejadianLainnyaViewSet,
    FotoKejadianLainnyaViewSet, statistik_dashboard,
    # Import view baru untuk map
    AreaViewSet, map_data, area_statistics,

     # Authentication views
    UserViewSet, login_view, logout_view, current_user,
    update_profile, change_password_view
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
router.register(r'areas', AreaViewSet, basename='areas')

# Authentication routes
router.register(r'users', UserViewSet, basename='users')

# urlpatterns = [
#     path('api/', include(router.urls)),
#     path('api/statistik/', statistik_dashboard, name='statistik-dashboard'),
#     # Endpoint baru untuk map
#     path('api/map/data/', map_data, name='map-data'),
#     path('api/map/area-statistics/', area_statistics, name='area-statistics-all'),
#     path('api/map/area-statistics/<int:area_id>/', area_statistics, name='area-statistics-detail'),

#     # Authentication endpoints
#     path('api/auth/login/', login_view, name='login'),
#     path('api/auth/logout/', logout_view, name='logout'),
#     path('api/auth/me/', current_user, name='current-user'),
#     path('api/auth/profile/', update_profile, name='update-profile'),
#     path('api/auth/change-password/', change_password_view, name='change-password'),
# ]

urlpatterns = [
    path('', include(router.urls)),
    path('statistik/', statistik_dashboard, name='statistik-dashboard'),
    # Endpoint baru untuk map
    path('map/data/', map_data, name='map-data'),
    path('map/area-statistics/', area_statistics, name='area-statistics-all'),
    path('map/area-statistics/<int:area_id>/', area_statistics, name='area-statistics-detail'),

    # Authentication endpoints
    path('auth/login/', login_view, name='login'),
    path('auth/logout/', logout_view, name='logout'),
    path('auth/me/', current_user, name='current-user'),
    path('auth/profile/', update_profile, name='update-profile'),
    path('auth/change-password/', change_password_view, name='change-password'),
]

