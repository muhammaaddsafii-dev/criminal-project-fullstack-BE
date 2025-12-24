from rest_framework import serializers
from .models import (
    JenisKejahatan, NamaKejahatan, Kecamatan, Desa, Status,
    LaporanKejahatan, FotoLaporanKejahatan, PosKeamanan, FotoPosKeamanan,
    CCTV, FotoCCTV, KejadianLainnya, FotoKejadianLainnya, Area
)

from django.contrib.gis.geos import GEOSGeometry
import json


class JenisKejahatanSerializer(serializers.ModelSerializer):
    class Meta:
        model = JenisKejahatan
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class NamaKejahatanSerializer(serializers.ModelSerializer):
    jenis_kejahatan_nama = serializers.CharField(
        source='jenis_kejahatan.nama_jenis_kejahatan', 
        read_only=True
    )

    class Meta:
        model = NamaKejahatan
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class KecamatanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kecamatan
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class DesaSerializer(serializers.ModelSerializer):
    kecamatan_nama = serializers.CharField(
        source='kecamatan.nama', 
        read_only=True
    )

    class Meta:
        model = Desa
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class FotoLaporanKejahatanSerializer(serializers.ModelSerializer):
    class Meta:
        model = FotoLaporanKejahatan
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class LaporanKejahatanSerializer(serializers.ModelSerializer):
    jenis_kejahatan_nama = serializers.CharField(
        source='jenis_kejahatan.nama_jenis_kejahatan', 
        read_only=True
    )
    nama_kejahatan_nama = serializers.CharField(
        source='nama_kejahatan.nama', 
        read_only=True
    )
    kecamatan_nama = serializers.CharField(
        source='kecamatan.nama', 
        read_only=True
    )
    desa_nama = serializers.CharField(
        source='desa.nama', 
        read_only=True
    )
    status_nama = serializers.CharField(
        source='status.nama', 
        read_only=True
    )
    foto = FotoLaporanKejahatanSerializer(many=True, read_only=True)
    
    # Untuk input lokasi dalam format [longitude, latitude]
    longitude = serializers.FloatField(write_only=True, required=False)
    latitude = serializers.FloatField(write_only=True, required=False)

    class Meta:
        model = LaporanKejahatan
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def create(self, validated_data):
        longitude = validated_data.pop('longitude', None)
        latitude = validated_data.pop('latitude', None)
        
        if longitude and latitude:
            from django.contrib.gis.geos import Point
            validated_data['lokasi'] = Point(longitude, latitude, srid=4326)
        
        return super().create(validated_data)

    def update(self, instance, validated_data):
        longitude = validated_data.pop('longitude', None)
        latitude = validated_data.pop('latitude', None)
        
        if longitude and latitude:
            from django.contrib.gis.geos import Point
            validated_data['lokasi'] = Point(longitude, latitude, srid=4326)
        
        return super().update(instance, validated_data)


class FotoPosKeamananSerializer(serializers.ModelSerializer):
    class Meta:
        model = FotoPosKeamanan
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class PosKeamananSerializer(serializers.ModelSerializer):
    desa_nama = serializers.CharField(
        source='desa.nama', 
        read_only=True
    )
    kecamatan_nama = serializers.CharField(
        source='desa.kecamatan.nama', 
        read_only=True
    )
    foto = FotoPosKeamananSerializer(many=True, read_only=True)
    
    longitude = serializers.FloatField(write_only=True, required=False)
    latitude = serializers.FloatField(write_only=True, required=False)

    class Meta:
        model = PosKeamanan
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def create(self, validated_data):
        longitude = validated_data.pop('longitude', None)
        latitude = validated_data.pop('latitude', None)
        
        if longitude and latitude:
            from django.contrib.gis.geos import Point
            validated_data['lokasi'] = Point(longitude, latitude, srid=4326)
        
        return super().create(validated_data)

    def update(self, instance, validated_data):
        longitude = validated_data.pop('longitude', None)
        latitude = validated_data.pop('latitude', None)
        
        if longitude and latitude:
            from django.contrib.gis.geos import Point
            validated_data['lokasi'] = Point(longitude, latitude, srid=4326)
        
        return super().update(instance, validated_data)


class FotoCCTVSerializer(serializers.ModelSerializer):
    class Meta:
        model = FotoCCTV
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class CCTVSerializer(serializers.ModelSerializer):
    kecamatan_nama = serializers.CharField(
        source='kecamatan.nama', 
        read_only=True
    )
    desa_nama = serializers.CharField(
        source='desa.nama', 
        read_only=True
    )
    foto = FotoCCTVSerializer(many=True, read_only=True)
    
    longitude = serializers.FloatField(write_only=True, required=False)
    latitude = serializers.FloatField(write_only=True, required=False)

    class Meta:
        model = CCTV
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def create(self, validated_data):
        longitude = validated_data.pop('longitude', None)
        latitude = validated_data.pop('latitude', None)
        
        if longitude and latitude:
            from django.contrib.gis.geos import Point
            validated_data['lokasi'] = Point(longitude, latitude, srid=4326)
        
        return super().create(validated_data)

    def update(self, instance, validated_data):
        longitude = validated_data.pop('longitude', None)
        latitude = validated_data.pop('latitude', None)
        
        if longitude and latitude:
            from django.contrib.gis.geos import Point
            validated_data['lokasi'] = Point(longitude, latitude, srid=4326)
        
        return super().update(instance, validated_data)


class FotoKejadianLainnyaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FotoKejadianLainnya
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class KejadianLainnyaSerializer(serializers.ModelSerializer):
    kecamatan_nama = serializers.CharField(
        source='kecamatan.nama', 
        read_only=True
    )
    desa_nama = serializers.CharField(
        source='desa.nama', 
        read_only=True
    )
    status_nama = serializers.CharField(
        source='status.nama', 
        read_only=True
    )
    foto = FotoKejadianLainnyaSerializer(many=True, read_only=True)
    
    longitude = serializers.FloatField(write_only=True, required=False)
    latitude = serializers.FloatField(write_only=True, required=False)

    class Meta:
        model = KejadianLainnya
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def create(self, validated_data):
        longitude = validated_data.pop('longitude', None)
        latitude = validated_data.pop('latitude', None)
        
        if longitude and latitude:
            from django.contrib.gis.geos import Point
            validated_data['lokasi'] = Point(longitude, latitude, srid=4326)
        
        return super().create(validated_data)

    def update(self, instance, validated_data):
        longitude = validated_data.pop('longitude', None)
        latitude = validated_data.pop('latitude', None)
        
        if longitude and latitude:
            from django.contrib.gis.geos import Point
            validated_data['lokasi'] = Point(longitude, latitude, srid=4326)
        
        return super().update(instance, validated_data)
    

from rest_framework import serializers
from django.contrib.gis.geos import GEOSGeometry
import json


class AreaSerializer(serializers.ModelSerializer):
    """Serializer untuk Area dengan geometry dalam format GeoJSON"""
    kecamatan_nama = serializers.CharField(source='kecamatan.nama', read_only=True)
    desa_nama = serializers.CharField(source='desa.nama', read_only=True)
    geometry = serializers.SerializerMethodField()
    
    class Meta:
        model = Area
        fields = [
            'id', 'external_id', 'wadmkc', 'wadmkd', 'wadmkk', 
            'wadmpr', 'luas', 'kecamatan', 'kecamatan_nama', 
            'desa', 'desa_nama', 'geometry', 'created_at', 'updated_at'
        ]
    
    def get_geometry(self, obj):
        """Konversi geometry ke GeoJSON format"""
        if obj.geom:
            return json.loads(obj.geom.geojson)
        return None


class MapLocationSerializer(serializers.Serializer):
    """Serializer untuk data lokasi di peta"""
    id = serializers.IntegerField()
    type = serializers.CharField()  # 'crime', 'security_post', 'cctv'
    name = serializers.CharField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    description = serializers.CharField(required=False, allow_blank=True)
    status = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    date = serializers.DateField(required=False, allow_null=True)
    time = serializers.TimeField(required=False, allow_null=True)
    kecamatan = serializers.CharField(required=False, allow_blank=True)
    desa = serializers.CharField(required=False, allow_blank=True)
    photos = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        allow_empty=True
    )


class LaporanKejahatanMapSerializer(serializers.ModelSerializer):
    """Serializer khusus untuk Laporan Kejahatan di peta"""
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()
    jenis_kejahatan_nama = serializers.CharField(source='jenis_kejahatan.nama_jenis_kejahatan', read_only=True)
    nama_kejahatan_nama = serializers.CharField(source='nama_kejahatan.nama', read_only=True)
    kecamatan_nama = serializers.CharField(source='kecamatan.nama', read_only=True)
    desa_nama = serializers.CharField(source='desa.nama', read_only=True)
    status_nama = serializers.CharField(source='status.nama', read_only=True)
    foto_urls = serializers.SerializerMethodField()
    
    class Meta:
        model = LaporanKejahatan
        fields = [
            'id', 'nama_pelapor', 'jenis_kejahatan_nama', 'nama_kejahatan_nama',
            'tanggal_kejadian', 'waktu_kejadian', 'kecamatan_nama', 'desa_nama',
            'alamat', 'deskripsi', 'status_nama', 'latitude', 'longitude', 
            'foto_urls', 'is_approval', 'created_at'
        ]
    
    def get_latitude(self, obj):
        if obj.lokasi:
            return obj.lokasi.y
        return None
    
    def get_longitude(self, obj):
        if obj.lokasi:
            return obj.lokasi.x
        return None
    
    def get_foto_urls(self, obj):
        try:
            return [foto.file_path.url for foto in obj.foto.all()]
        except:
            return []


class PosKeamananMapSerializer(serializers.ModelSerializer):
    """Serializer khusus untuk Pos Keamanan di peta"""
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()
    kecamatan_nama = serializers.CharField(source='desa.kecamatan.nama', read_only=True)
    desa_nama = serializers.CharField(source='desa.nama', read_only=True)
    foto_urls = serializers.SerializerMethodField()
    
    class Meta:
        model = PosKeamanan
        fields = [
            'id', 'nama', 'kecamatan_nama', 'desa_nama', 'alamat',
            'keterangan', 'latitude', 'longitude', 'foto_urls', 'created_at'
        ]
    
    def get_latitude(self, obj):
        if obj.lokasi:
            return obj.lokasi.y
        return None
    
    def get_longitude(self, obj):
        if obj.lokasi:
            return obj.lokasi.x
        return None
    
    def get_foto_urls(self, obj):
        try:
            return [foto.file_path.url for foto in obj.foto.all()]
        except:
            return []


class CCTVMapSerializer(serializers.ModelSerializer):
    """Serializer khusus untuk CCTV di peta"""
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()
    kecamatan_nama = serializers.CharField(source='kecamatan.nama', read_only=True)
    desa_nama = serializers.CharField(source='desa.nama', read_only=True)
    foto_urls = serializers.SerializerMethodField()
    
    class Meta:
        model = CCTV
        fields = [
            'id', 'nama_lokasi', 'kecamatan_nama', 'desa_nama', 
            'deskripsi', 'url_cctv', 'latitude', 'longitude', 
            'foto_urls', 'created_at'
        ]
    
    def get_latitude(self, obj):
        if obj.lokasi:
            return obj.lokasi.y
        return None
    
    def get_longitude(self, obj):
        if obj.lokasi:
            return obj.lokasi.x
        return None
    
    def get_foto_urls(self, obj):
        try:
            return [foto.file_path.url for foto in obj.foto.all()]
        except:
            return []