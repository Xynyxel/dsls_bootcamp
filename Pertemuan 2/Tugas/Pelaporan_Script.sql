select * from pelaporan;

select Count(*) from pelaporan;
2670 Row

variabel
Bulan 
Tahun 
Kota_Kabupaten
Kecamatan
Keluarahan
Jenis Kelamin
Jumlah

1. Berdasarkan kota/kabupaten, urutkanlah jumlah kedatangan
pendatang baru dari yang paling banyak

select kota_kabupaten,sum(jumlah) as "Jumlah_Kedatangan"
from pelaporan p
group by kota_kabupaten
order by Jumlah_Kedatangan DESC; 


2. Tentukanlah 10 kecamatan dengan jumlah kedatangan pendatang
baru terbanyak dan tersedikit

select kecamatan ,sum(jumlah) as "Jumlah_Kedatangan_terbanyak"
from pelaporan p
group by kecamatan
order by Jumlah_Kedatangan_terbanyak desc
limit 10; 

select kecamatan ,sum(jumlah) as "Jumlah_Kedatangan_tersedikit"
from pelaporan p
group by kecamatan
order by Jumlah_Kedatangan_tersedikit asc
limit 10; 

3. Manakah pendatang baru yang lebih banyak: laki-laki atau
perempuan?

select jenis_kelamin, sum(jumlah) as "Pendatang_baru"
from pelaporan p 
group by jenis_kelamin;

4. Untuk setiap kota/kabupaten administrasi, berapa jumlah
kecamatan dan kelurahan dan jumlah pendatang baru?

select kota_kabupaten, count(distinct(kecamatan)) as "jumlah_kecamatan", 
count(distinct(kelurahan)) as "jumlah_kelurahan" ,sum(jumlah) as "Pendatang_baru"
from pelaporan p 
group by kota_kabupaten;