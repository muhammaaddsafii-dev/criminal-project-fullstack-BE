from django.core.management.base import BaseCommand
from core.models import JenisKejahatan, NamaKejahatan, Status


class Command(BaseCommand):
    help = 'Seed initial data untuk jenis kejahatan, nama kejahatan, dan status'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')
        
        # Seed Jenis Kejahatan
        jenis_kejahatan_data = [
            {'nama': 'Kejahatan Kekerasan', 'deskripsi': 'Kejahatan yang melibatkan kekerasan fisik'},
            {'nama': 'Kejahatan Properti', 'deskripsi': 'Kejahatan terkait harta benda'},
            {'nama': 'Kejahatan Ekonomi', 'deskripsi': 'Kejahatan di bidang ekonomi dan keuangan'},
            {'nama': 'Kejahatan Seksual', 'deskripsi': 'Kejahatan terkait seksual'},
            {'nama': 'Kejahatan Narkoba', 'deskripsi': 'Kejahatan terkait narkotika dan obat terlarang'},
            {'nama': 'Kejahatan Siber', 'deskripsi': 'Kejahatan menggunakan teknologi digital'},
            {'nama': 'Kejahatan Terorganisir', 'deskripsi': 'Kejahatan yang dilakukan secara terorganisir'},
            {'nama': 'Kejahatan Lainnya', 'deskripsi': 'Kejahatan yang tidak termasuk kategori lain'},
        ]
        
        jenis_objects = {}
        for data in jenis_kejahatan_data:
            obj, created = JenisKejahatan.objects.get_or_create(
                nama_jenis_kejahatan=data['nama'],
                defaults={'deskripsi': data['deskripsi']}
            )
            jenis_objects[data['nama']] = obj
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created: {data["nama"]}'))
        
        # Seed Nama Kejahatan
        nama_kejahatan_data = [
            # Kejahatan Kekerasan
            {'jenis': 'Kejahatan Kekerasan', 'nama': 'KDRT', 'deskripsi': 'Kekerasan Dalam Rumah Tangga'},
            {'jenis': 'Kejahatan Kekerasan', 'nama': 'Pembunuhan', 'deskripsi': 'Tindakan menghilangkan nyawa'},
            {'jenis': 'Kejahatan Kekerasan', 'nama': 'Penganiyayaan', 'deskripsi': 'Tindakan kekerasan fisik'},
            {'jenis': 'Kejahatan Kekerasan', 'nama': 'Pemerkosaan', 'deskripsi': 'Kekerasan seksual'},
            {'jenis': 'Kejahatan Kekerasan', 'nama': 'Penjambretan', 'deskripsi': 'Merampas barang dengan kekerasan'},
            {'jenis': 'Kejahatan Kekerasan', 'nama': 'Pemerasan', 'deskripsi': 'Memaksa memberikan sesuatu dengan ancaman'},
            
            # Kejahatan Properti
            {'jenis': 'Kejahatan Properti', 'nama': 'Pencurian Uang/Barang', 'deskripsi': 'Mengambil harta orang lain'},
            
            # Kejahatan Ekonomi
            {'jenis': 'Kejahatan Ekonomi', 'nama': 'Korupsi', 'deskripsi': 'Penyalahgunaan kewenangan untuk keuntungan pribadi'},
            {'jenis': 'Kejahatan Ekonomi', 'nama': 'Penipuan', 'deskripsi': 'Menipu untuk mendapatkan keuntungan'},
            {'jenis': 'Kejahatan Ekonomi', 'nama': 'Penggelapan', 'deskripsi': 'Menggelapkan barang/uang yang dipercayakan'},
            {'jenis': 'Kejahatan Ekonomi', 'nama': 'Uang Palsu', 'deskripsi': 'Membuat atau mengedarkan uang palsu'},
            {'jenis': 'Kejahatan Ekonomi', 'nama': 'Perjudian', 'deskripsi': 'Aktivitas judi ilegal'},
            
            # Kejahatan Seksual
            {'jenis': 'Kejahatan Seksual', 'nama': 'Tindak Asusila', 'deskripsi': 'Perbuatan asusila'},
            {'jenis': 'Kejahatan Seksual', 'nama': 'Pelecehan', 'deskripsi': 'Pelecehan seksual'},
            {'jenis': 'Kejahatan Seksual', 'nama': 'Pemerkosaan', 'deskripsi': 'Kekerasan seksual'},
            
            # Kejahatan Narkoba
            {'jenis': 'Kejahatan Narkoba', 'nama': 'Narkotika', 'deskripsi': 'Kepemilikan narkotika'},
            {'jenis': 'Kejahatan Narkoba', 'nama': 'Penyalahgunaan', 'deskripsi': 'Penyalahgunaan narkotika'},
            {'jenis': 'Kejahatan Narkoba', 'nama': 'Peredaran', 'deskripsi': 'Mengedarkan narkotika'},
            {'jenis': 'Kejahatan Narkoba', 'nama': 'Bandar', 'deskripsi': 'Bandar narkotika'},
            
            # Kejahatan Siber
            {'jenis': 'Kejahatan Siber', 'nama': 'Penipuan Online', 'deskripsi': 'Penipuan melalui media online'},
            {'jenis': 'Kejahatan Siber', 'nama': 'Peretasan', 'deskripsi': 'Meretas sistem komputer'},
            {'jenis': 'Kejahatan Siber', 'nama': 'Pencurian Data', 'deskripsi': 'Mencuri data digital'},
            {'jenis': 'Kejahatan Siber', 'nama': 'Pemalsuan Data', 'deskripsi': 'Memalsukan data digital'},
            
            # Kejahatan Terorganisir
            {'jenis': 'Kejahatan Terorganisir', 'nama': 'Perdagangan Manusia', 'deskripsi': 'Trafficking'},
            {'jenis': 'Kejahatan Terorganisir', 'nama': 'Penyelundupan', 'deskripsi': 'Penyelundupan barang ilegal'},
            {'jenis': 'Kejahatan Terorganisir', 'nama': 'Mafia', 'deskripsi': 'Kegiatan mafia'},
            {'jenis': 'Kejahatan Terorganisir', 'nama': 'Pencucian Uang Terorganisir', 'deskripsi': 'Money laundering'},
            
            # Kejahatan Lainnya
            {'jenis': 'Kejahatan Lainnya', 'nama': 'Bunuh Diri', 'deskripsi': 'Percobaan atau kasus bunuh diri'},
            {'jenis': 'Kejahatan Lainnya', 'nama': 'Konflik', 'deskripsi': 'Konflik antar warga'},
            {'jenis': 'Kejahatan Lainnya', 'nama': 'Miras', 'deskripsi': 'Minuman keras ilegal'},
        ]
        
        for data in nama_kejahatan_data:
            jenis_obj = jenis_objects.get(data['jenis'])
            if jenis_obj:
                obj, created = NamaKejahatan.objects.get_or_create(
                    jenis_kejahatan=jenis_obj,
                    nama=data['nama'],
                    defaults={'deskripsi': data['deskripsi']}
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created: {data["nama"]}'))
        
        # Seed Status
        status_data = ['Dilaporkan', 'Diproses', 'Selesai']
        for status_nama in status_data:
            obj, created = Status.objects.get_or_create(nama=status_nama)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created Status: {status_nama}'))
        
        self.stdout.write(self.style.SUCCESS('Data seeding completed!'))