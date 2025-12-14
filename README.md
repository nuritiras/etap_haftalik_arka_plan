PARDUS ETAP 23 Her Hafta Otomatik Değişen Arka Plan Sistemi ve Kullanıcıların Arka Plan Değiştirmesini Engelleme

Windows üzerinde paylaşılan bir klasör içindeki resimleri,

ETAP 23 akıllı tahtalara haftanın numarasına göre otomatik olarak arka plan resmi yapmak,

Tüm öğretmen/öğrenci kullanıcılarında otomatik çalışmasını sağlamak,

Arka plan değiştirme yetkisini kapatmak.

Bu çözümde:

✔ Windows paylaşımları kullanılır

✔ CIFS/SMB protokolü ile ETAP’a erişilir

✔ Haftalık arka plan otomatik güncellenir

✔ Tüm kullanıcılar için autostart

✔ Dconf Lockdown ile arka plan değişim engellenir

## Pardus ETAP 23’te Gerekli Paketler
### sudo apt update
### sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0 samba cifs-utils -y
## Çalıştırma
### sudo chmod +x etap_duvar.py
### sudo python3 etap_duvar.py
<img width="511" height="913" alt="Ekran Görüntüsü - 2025-12-14 18-16-27" src="https://github.com/user-attachments/assets/9adc97f5-4357-42f0-8936-3ff0d72ca712" />
