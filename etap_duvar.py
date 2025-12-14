#!/usr/bin/env python3
import gi
import os
import subprocess
import sys
import shutil
import json

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf

# Ayar dosyasının yolu
CONFIG_FILE = os.path.expanduser("~/.etap_duvar_config.json")

class WallpaperManager(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="ETAP Yönetici v8 (SMB 3.0)")
        self.set_border_width(15)
        self.set_default_size(500, 650)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_resizable(False)

        # Ana Kutu
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(main_box)

        # --- BÖLÜM 1: Bağlantı Ayarları ---
        frame_server = Gtk.Frame(label=" 1. Bağlantı Ayarları ")
        main_box.pack_start(frame_server, False, False, 0)
        
        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_row_spacing(10)
        grid.set_margin_top(10)
        grid.set_margin_bottom(10)
        grid.set_margin_start(10)
        grid.set_margin_end(10)
        frame_server.add(grid)

        # Giriş Alanları
        self.entry_ip = Gtk.Entry(placeholder_text="192.168.1.xxx")
        self.entry_share = Gtk.Entry(placeholder_text="Klasör Adı")
        self.entry_user = Gtk.Entry(placeholder_text="Kullanıcı")
        self.entry_pass = Gtk.Entry()
        self.entry_pass.set_visibility(False)
        
        # Domain (Çalışma Grubu) - Önemli!
        self.entry_domain = Gtk.Entry(placeholder_text="Genelde: WORKGROUP")
        self.entry_domain.set_text("WORKGROUP")

        grid.attach(Gtk.Label(label="Sunucu IP:", xalign=1), 0, 0, 1, 1)
        grid.attach(self.entry_ip, 1, 0, 1, 1)
        
        grid.attach(Gtk.Label(label="Paylaşım Adı:", xalign=1), 0, 1, 1, 1)
        grid.attach(self.entry_share, 1, 1, 1, 1)

        grid.attach(Gtk.Label(label="Kullanıcı:", xalign=1), 0, 2, 1, 1)
        grid.attach(self.entry_user, 1, 2, 1, 1)

        grid.attach(Gtk.Label(label="Şifre:", xalign=1), 0, 3, 1, 1)
        grid.attach(self.entry_pass, 1, 3, 1, 1)

        grid.attach(Gtk.Label(label="Domain/Grup:", xalign=1), 0, 4, 1, 1)
        grid.attach(self.entry_domain, 1, 4, 1, 1)

        # Yapılandır Butonu
        btn_config = Gtk.Button(label="Sistemi Yapılandır (Kilit & Servis)")
        btn_config.connect("clicked", self.on_config_clicked)
        grid.attach(btn_config, 1, 5, 1, 1)

        # --- BÖLÜM 2: Resim Önizleme ve Yükleme ---
        frame_img = Gtk.Frame(label=" 2. Resim Seçimi ve Önizleme ")
        main_box.pack_start(frame_img, True, True, 0)

        vbox_img = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox_img.set_margin_top(10)
        vbox_img.set_margin_bottom(10)
        vbox_img.set_margin_start(10)
        vbox_img.set_margin_end(10)
        frame_img.add(vbox_img)

        self.file_chooser = Gtk.FileChooserButton(title="Resim Seçiniz")
        filter_img = Gtk.FileFilter()
        filter_img.set_name("Resim Dosyaları")
        filter_img.add_mime_type("image/jpeg")
        filter_img.add_mime_type("image/png")
        self.file_chooser.add_filter(filter_img)
        self.file_chooser.connect("file-set", self.on_file_selected)
        vbox_img.pack_start(self.file_chooser, False, False, 0)

        self.img_preview = Gtk.Image()
        self.img_preview.set_from_icon_name("image-x-generic", Gtk.IconSize.DIALOG)
        self.img_preview.set_pixel_size(150)
        vbox_img.pack_start(self.img_preview, True, True, 0)

        self.lbl_preview_info = Gtk.Label(label="<i>Henüz resim seçilmedi.</i>")
        self.lbl_preview_info.set_use_markup(True)
        vbox_img.pack_start(self.lbl_preview_info, False, False, 0)

        btn_upload = Gtk.Button(label="SEÇİLEN RESMİ YAYINLA")
        btn_upload.get_style_context().add_class("suggested-action")
        btn_upload.set_size_request(-1, 40)
        btn_upload.connect("clicked", self.on_upload_clicked)
        main_box.pack_start(btn_upload, False, False, 0)

        # --- BÖLÜM 3: Temizlik ---
        box_reset = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        main_box.pack_start(box_reset, False, False, 5)
        
        btn_reset = Gtk.Button(label="SİSTEMİ ESKİ HALİNE DÖNDÜR")
        btn_reset.get_style_context().add_class("destructive-action")
        btn_reset.connect("clicked", self.on_uninstall_clicked)
        box_reset.pack_start(btn_reset, True, True, 0)

        self.lbl_status = Gtk.Label(label="Hazır.")
        main_box.pack_end(self.lbl_status, False, False, 0)

        self.load_config()

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    data = json.load(f)
                    self.entry_ip.set_text(data.get("ip", ""))
                    self.entry_share.set_text(data.get("share", ""))
                    self.entry_user.set_text(data.get("user", ""))
                    self.entry_pass.set_text(data.get("pass", ""))
                    self.entry_domain.set_text(data.get("domain", "WORKGROUP"))
            except:
                pass

    def save_config(self):
        data = {
            "ip": self.entry_ip.get_text().strip(),
            "share": self.entry_share.get_text().strip(),
            "user": self.entry_user.get_text().strip(),
            "pass": self.entry_pass.get_text().strip(),
            "domain": self.entry_domain.get_text().strip()
        }
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Ayar hatası: {e}")

    def on_file_selected(self, widget):
        filename = widget.get_filename()
        if filename:
            try:
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                    filename, width=400, height=250, preserve_aspect_ratio=True
                )
                self.img_preview.set_from_pixbuf(pixbuf)
                self.lbl_preview_info.set_text(f"Dosya: {os.path.basename(filename)}")
            except:
                self.lbl_status.set_text("Önizleme hatası!")

    def run_command_list(self, cmd_list):
        try:
            subprocess.run(cmd_list, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Komut Hatası: {e}")
            return False
    
    def run_command_shell(self, cmd_str):
        try:
            subprocess.run(cmd_str, shell=True, check=True)
            return True
        except:
            return False

    def get_mount_params(self):
        ip = self.entry_ip.get_text().strip()
        share = self.entry_share.get_text().strip()
        user = self.entry_user.get_text().strip()
        password = self.entry_pass.get_text().strip()
        domain = self.entry_domain.get_text().strip()
        
        if not ip or not share: return None, None

        source = f"//{ip}/{share}"
        # SMB 3.0 Sabitlendi
        options = f"username={user},password={password},domain={domain},iocharset=utf8,vers=3.0,noperm"
        
        return source, options

    def ensure_mount(self):
        if not os.path.exists("/media/sunucu_resim"):
            os.makedirs("/media/sunucu_resim")
        
        if os.path.ismount("/media/sunucu_resim"):
            return True
            
        source, options = self.get_mount_params()
        
        if not source:
            self.lbl_status.set_text("Hata: Bilgiler eksik!")
            return False
            
        cmd = ["mount", "-t", "cifs", source, "/media/sunucu_resim", "-o", options]
        
        if self.run_command_list(cmd):
            return True
        else:
            self.lbl_status.set_text("Hata: Bağlantı reddedildi! Domain kısmını kontrol edin.")
            return False

    def on_config_clicked(self, widget):
        self.save_config()
        source, options = self.get_mount_params()
        ip_addr = self.entry_ip.get_text().strip()
        
        if not source:
            self.lbl_status.set_text("Hata: Eksik bilgi!")
            return

        if shutil.which("dconf") is None:
            self.lbl_status.set_text("HATA: 'dconf-cli' yüklü değil!")
            return

        self.lbl_status.set_text("Ayarlanıyor...")
        self.run_command_shell("mkdir -p /media/sunucu_resim")
        
        # Script
        script_content = f"""#!/bin/bash
LOG="/var/log/etap_duvar.log"
echo "$(date) - Servis basladi." > $LOG
TARGET="{ip_addr}"
MAX_RETRIES=30
COUNT=0
while ! ping -c 1 -W 1 $TARGET &> /dev/null; do
    echo "Bekleniyor... ($COUNT)" >> $LOG
    sleep 2
    ((COUNT++))
    if [ $COUNT -ge $MAX_RETRIES ]; then
        echo "Zaman asimi!" >> $LOG
        exit 1
    fi
done
umount /media/sunucu_resim 2>/dev/null
# Mount komutu (vers=3.0)
mount -t cifs {source} /media/sunucu_resim -o {options} >> $LOG 2>&1

if [ -f "/media/sunucu_resim/guncel_duvar.jpg" ]; then
    cp "/media/sunucu_resim/guncel_duvar.jpg" "/usr/share/backgrounds/kurumsal_arkaplan.jpg"
    chmod 644 "/usr/share/backgrounds/kurumsal_arkaplan.jpg"
    echo "Guncellendi." >> $LOG
fi
"""
        with open("/usr/local/bin/duvarkagidi_guncelle.sh", "w") as f:
            f.write(script_content)
        self.run_command_shell("chmod +x /usr/local/bin/duvarkagidi_guncelle.sh")
        
        os.system('echo "@reboot /usr/local/bin/duvarkagidi_guncelle.sh" | crontab -')

        os.makedirs("/etc/dconf/profile", exist_ok=True)
        with open("/etc/dconf/profile/user", "w") as f:
            f.write("user-db:user\nsystem-db:local\n")
        
        os.makedirs("/etc/dconf/db/local.d/locks", exist_ok=True)
        with open("/etc/dconf/db/local.d/00-wallpaper", "w") as f:
            f.write("[org/cinnamon/desktop/background]\npicture-uri='file:///usr/share/backgrounds/kurumsal_arkaplan.jpg'\npicture-options='zoom'\n[org/gnome/desktop/background]\npicture-uri='file:///usr/share/backgrounds/kurumsal_arkaplan.jpg'\npicture-options='zoom'\n")
        with open("/etc/dconf/db/local.d/locks/wallpaper", "w") as f:
            f.write("/org/cinnamon/desktop/background/picture-uri\n/org/cinnamon/desktop/background/picture-options\n")

        if self.run_command_shell("dconf update"):
            self.lbl_status.set_text("Başarılı! (SMB 3.0)")
        else:
            self.lbl_status.set_text("Hata: dconf çalışmadı.")

    def on_upload_clicked(self, widget):
        self.save_config()
        local_file = self.file_chooser.get_filename()
        if not local_file:
            self.lbl_status.set_text("Lütfen resim seçin!")
            return
        self.lbl_status.set_text("Yükleniyor...")
        if not self.ensure_mount(): return
        try:
            shutil.copy2(local_file, "/media/sunucu_resim/guncel_duvar.jpg")
            shutil.copy2(local_file, "/usr/share/backgrounds/kurumsal_arkaplan.jpg")
            self.lbl_status.set_text("BAŞARILI! Resim yayına alındı.")
        except Exception as e:
            self.lbl_status.set_text(f"Hata: {str(e)}")

    def on_uninstall_clicked(self, widget):
        dialog = Gtk.MessageDialog(
            transient_for=self, flags=0, message_type=Gtk.MessageType.WARNING,
            buttons=Gtk.ButtonsType.YES_NO, text="Sistemi Sıfırla"
        )
        dialog.format_secondary_text("Her şey silinecek. Emin misiniz?")
        response = dialog.run()
        dialog.destroy()

        if response == Gtk.ResponseType.YES:
            self.lbl_status.set_text("Temizleniyor...")
            try:
                os.system("crontab -r") 
                files = [
                    "/usr/local/bin/duvarkagidi_guncelle.sh",
                    "/etc/dconf/profile/user",
                    "/etc/dconf/db/local.d/00-wallpaper",
                    "/etc/dconf/db/local.d/locks/wallpaper",
                    "/usr/share/backgrounds/kurumsal_arkaplan.jpg"
                ]
                for f in files:
                    if os.path.exists(f): os.remove(f)

                self.run_command_shell("umount /media/sunucu_resim || true")
                if os.path.exists("/media/sunucu_resim"): os.rmdir("/media/sunucu_resim")
                
                self.run_command_shell("dconf update")
                self.lbl_status.set_text("Sistem sıfırlandı.")
            except Exception as e:
                self.lbl_status.set_text(f"Hata: {e}")

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("Root yetkisi gerekli (sudo).")
        sys.exit(1)
        
    if shutil.which("dconf") is None:
        print("UYARI: dconf-cli yüklü değil.")

    win = WallpaperManager()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
