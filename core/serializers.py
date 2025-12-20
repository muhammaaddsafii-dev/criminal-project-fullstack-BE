from rest_framework import serializers
from .models import (
    JenisKejahatan, NamaKejahatan, Kecamatan, Desa, Status,
    LaporanKejahatan, FotoLaporanKejahatan, PosKeamanan, FotoPosKeamanan,
    CCTV, FotoCCTV, KejadianLainnya, FotoKejadianLainnya
)


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