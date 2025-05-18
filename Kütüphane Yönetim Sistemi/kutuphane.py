import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from datetime import datetime, timedelta

# Dosya adları
KITAPLAR_DOSYA = "kitaplar.json"
UYELER_DOSYA = "uyeler.json"
KULLANICILAR_DOSYA = "kullanicilar.json"
ODUNC_DOSYA = "odunc.json"

# Veri saklama
kitaplar = []
uyeler = []
kullanicilar = []
odunc_kayitlari = []

# --- Sınıflar ---

class Kitap:
    def __init__(self, kitap_id, ad, yazar, aciklama="", kapak_yolu="", odunc_alindi_mi=False):
        self.kitap_id = kitap_id
        self.ad = ad
        self.yazar = yazar
        self.aciklama = aciklama
        self.kapak_yolu = kapak_yolu
        self.odunc_alindi_mi = odunc_alindi_mi

    def to_dict(self):
        return {
            "kitap_id": self.kitap_id,
            "ad": self.ad,
            "yazar": self.yazar,
            "aciklama": self.aciklama,
            "kapak_yolu": self.kapak_yolu,
            "odunc_alindi_mi": self.odunc_alindi_mi
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            d["kitap_id"],
            d["ad"],
            d["yazar"],
            d.get("aciklama", ""),
            d.get("kapak_yolu", ""),
            d.get("odunc_alindi_mi", False)
        )

class Uye:
    def __init__(self, uye_id, ad):
        self.uye_id = uye_id
        self.ad = ad

    def to_dict(self):
        return {"uye_id": self.uye_id, "ad": self.ad}

    @classmethod
    def from_dict(cls, d):
        return cls(d["uye_id"], d["ad"])

class Kullanici:
    def __init__(self, kullanici_adi, sifre, yetki):
        self.kullanici_adi = kullanici_adi
        self.sifre = sifre
        self.yetki = yetki  # "admin" veya "kullanici"

    def to_dict(self):
        return {"kullanici_adi": self.kullanici_adi, "sifre": self.sifre, "yetki": self.yetki}

    @classmethod
    def from_dict(cls, d):
        return cls(d["kullanici_adi"], d["sifre"], d["yetki"])

class Odunc:
    def __init__(self, uye_id, kitap_id, odunc_tarihi, iade_tarihi=None):
        self.uye_id = uye_id
        self.kitap_id = kitap_id
        self.odunc_tarihi = odunc_tarihi  # string format "YYYY-MM-DD"
        self.iade_tarihi = iade_tarihi    # string format "YYYY-MM-DD" ya da None

    def to_dict(self):
        return {
            "uye_id": self.uye_id,
            "kitap_id": self.kitap_id,
            "odunc_tarihi": self.odunc_tarihi,
            "iade_tarihi": self.iade_tarihi
        }

    @classmethod
    def from_dict(cls, d):
        return cls(d["uye_id"], d["kitap_id"], d["odunc_tarihi"], d.get("iade_tarihi"))

# --- Veri Yükleme ve Kaydetme Fonksiyonları ---

def dosya_yukle(dosya_adi):
    if os.path.exists(dosya_adi):
        with open(dosya_adi, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def dosya_kaydet(dosya_adi, veri):
    with open(dosya_adi, "w", encoding="utf-8") as f:
        json.dump(veri, f, indent=4, ensure_ascii=False)

def verileri_yukle():
    global kitaplar, uyeler, kullanicilar, odunc_kayitlari
    kitaplar = [Kitap.from_dict(d) for d in dosya_yukle(KITAPLAR_DOSYA)]
    uyeler = [Uye.from_dict(d) for d in dosya_yukle(UYELER_DOSYA)]
    kullanicilar = [Kullanici.from_dict(d) for d in dosya_yukle(KULLANICILAR_DOSYA)]
    odunc_kayitlari = [Odunc.from_dict(d) for d in dosya_yukle(ODUNC_DOSYA)]

def verileri_kaydet():
    dosya_kaydet(KITAPLAR_DOSYA, [k.to_dict() for k in kitaplar])
    dosya_kaydet(UYELER_DOSYA, [u.to_dict() for u in uyeler])
    dosya_kaydet(KULLANICILAR_DOSYA, [k.to_dict() for k in kullanicilar])
    dosya_kaydet(ODUNC_DOSYA, [o.to_dict() for o in odunc_kayitlari])

# --- Başlangıç için default admin ---

def admin_kontrol():
    if not kullanicilar:
        admin = Kullanici("admin", "admin123", "admin")
        kullanicilar.append(admin)
        verileri_kaydet()

# --- Tkinter Arayüz ---

pencere = tk.Tk()
pencere.title("Kütüphane Yönetim Sistemi")
pencere.geometry("900x650")
pencere.configure(bg="#2d3e50")

# Ortak stil
label_opts = {'font': ("Arial", 12, "bold"), 'bg': "#2d3e50", 'fg': "#ffffff"}
entry_opts = {'width': 40, 'font': ("Arial", 12), 'borderwidth': 2, 'relief': "solid"}
button_opts = {'font': ("Arial", 12, "bold"), 'bg': "#4CAF50", 'fg': "white",
               'padx': 15, 'pady': 8, 'bd': 0, 'activebackground': "#45a049",
               'relief': "flat", 'highlightthickness': 0}
button_error_opts = {'font': ("Arial", 12, "bold"), 'bg': "#f44336", 'fg': "white",
                     'padx': 15, 'pady': 8, 'bd': 0, 'activebackground': "#d32f2f",
                     'relief': "flat", 'highlightthickness': 0}
button_clear_opts = {'font': ("Arial", 12, "bold"), 'bg': "#2196F3", 'fg': "white",
                     'padx': 15, 'pady': 8, 'bd': 0, 'activebackground': "#1976d2",
                     'relief': "flat", 'highlightthickness': 0}

# --- Kullanıcı Giriş Ekranı ---

frame_giris = tk.Frame(pencere, bg="#2d3e50")
frame_giris.pack(expand=True)

tk.Label(frame_giris, text="Kullanıcı Adı:", **label_opts).pack(pady=10)
entry_kullanici_adi = tk.Entry(frame_giris, **entry_opts)
entry_kullanici_adi.pack(pady=5)

tk.Label(frame_giris, text="Şifre:", **label_opts).pack(pady=10)
entry_sifre = tk.Entry(frame_giris, show="*", **entry_opts)
entry_sifre.pack(pady=5)

def giris_yap():
    kullanici_adi = entry_kullanici_adi.get().strip()
    sifre = entry_sifre.get().strip()
    kullanici = next((k for k in kullanicilar if k.kullanici_adi == kullanici_adi and k.sifre == sifre), None)
    if kullanici:
        messagebox.showinfo("Başarılı", f"Hoşgeldiniz, {kullanici.kullanici_adi}!")
        frame_giris.pack_forget()
        acilir_menuler(kullanici)
    else:
        messagebox.showerror("Hata", "Kullanıcı adı veya şifre yanlış!")

tk.Button(frame_giris, text="Giriş Yap", command=giris_yap, **button_opts).pack(pady=20)

# --- Ana Menü ve Sekmeler ---

def acilir_menuler(kullanici):

    tablo = ttk.Notebook(pencere)
    tablo.pack(expand=1, fill="both")

    # -- Kitap Ekleme / Listeleme Sekmesi --
    kitap_frame = tk.Frame(tablo, bg="#34495e")

    # Form alanları
    tk.Label(kitap_frame, text="Kitap ID:", **label_opts).pack(pady=5)
    entry_kitap_id = tk.Entry(kitap_frame, **entry_opts)
    entry_kitap_id.pack(pady=2)

    tk.Label(kitap_frame, text="Kitap Adı:", **label_opts).pack(pady=5)
    entry_kitap_ad = tk.Entry(kitap_frame, **entry_opts)
    entry_kitap_ad.pack(pady=2)

    tk.Label(kitap_frame, text="Yazar:", **label_opts).pack(pady=5)
    entry_kitap_yazar = tk.Entry(kitap_frame, **entry_opts)
    entry_kitap_yazar.pack(pady=2)

    tk.Label(kitap_frame, text="Açıklama:", **label_opts).pack(pady=5)
    entry_kitap_aciklama = tk.Text(kitap_frame, width=30, height=4, font=("Arial", 11))
    entry_kitap_aciklama.pack(pady=2)


    def kitap_ekle():
        kitap_id = entry_kitap_id.get().strip()
        ad = entry_kitap_ad.get().strip()
        yazar = entry_kitap_yazar.get().strip()
        aciklama = entry_kitap_aciklama.get("1.0", tk.END).strip()

        if not kitap_id or not ad or not yazar:
            messagebox.showerror("Hata", "Kitap ID, Ad ve Yazar boş bırakılamaz!")
            return
        if any(k.kitap_id == kitap_id for k in kitaplar):
            messagebox.showerror("Hata", "Bu Kitap ID zaten mevcut!")
            return

        yeni_kitap = Kitap(kitap_id, ad, yazar, aciklama)
        kitaplar.append(yeni_kitap)
        verileri_kaydet()
        messagebox.showinfo("Başarılı", "Kitap başarıyla eklendi!")
        kitaplari_goster()

    tk.Button(kitap_frame, text="Kitap Ekle", command=kitap_ekle, **button_opts).pack(pady=10)

    # Treeview ile kitap listesi
    kitap_tree = ttk.Treeview(kitap_frame, columns=("ID", "Ad", "Yazar", "Durum"), show="headings", height=10)
    kitap_tree.pack(pady=10, fill="x")
    for col in ("ID", "Ad", "Yazar", "Durum"):
        kitap_tree.heading(col, text=col)
        kitap_tree.column(col, anchor="center")

    def kitaplari_goster():
        kitap_tree.delete(*kitap_tree.get_children())
        for k in kitaplar:
            durum = "Ödünçte" if k.odunc_alindi_mi else "Rafta"
            kitap_tree.insert("", tk.END, values=(k.kitap_id, k.ad, k.yazar, durum))

    kitaplari_goster()

    # -- Üye Ekleme / Listeleme Sekmesi --
    uye_frame = tk.Frame(tablo, bg="#34495e")

    tk.Label(uye_frame, text="Üye ID:", **label_opts).pack(pady=5)
    entry_uye_id = tk.Entry(uye_frame, **entry_opts)
    entry_uye_id.pack(pady=2)

    tk.Label(uye_frame, text="Üye Adı:", **label_opts).pack(pady=5)
    entry_uye_ad = tk.Entry(uye_frame, **entry_opts)
    entry_uye_ad.pack(pady=2)

    def uye_ekle():
        uye_id = entry_uye_id.get().strip()
        ad = entry_uye_ad.get().strip()

        if not uye_id or not ad:
            messagebox.showerror("Hata", "Üye ID ve Ad boş bırakılamaz!")
            return
        if any(u.uye_id == uye_id for u in uyeler):
            messagebox.showerror("Hata", "Bu Üye ID zaten mevcut!")
            return

        yeni_uye = Uye(uye_id, ad)
        uyeler.append(yeni_uye)
        verileri_kaydet()
        messagebox.showinfo("Başarılı", "Üye başarıyla eklendi!")
        uyeleri_goster()

    tk.Button(uye_frame, text="Üye Ekle", command=uye_ekle, **button_opts).pack(pady=10)

    uye_tree = ttk.Treeview(uye_frame, columns=("ID", "Ad"), show="headings", height=10)
    uye_tree.pack(pady=10, fill="x")
    for col in ("ID", "Ad"):
        uye_tree.heading(col, text=col)
        uye_tree.column(col, anchor="center")

    def uyeleri_goster():
        uye_tree.delete(*uye_tree.get_children())
        for u in uyeler:
            uye_tree.insert("", tk.END, values=(u.uye_id, u.ad))

    uyeleri_goster()

    # -- Ödünç Alma / İade Sekmesi --

    odunc_frame = tk.Frame(tablo, bg="#34495e")

    tk.Label(odunc_frame, text="Üye ID:", **label_opts).pack(pady=5)
    entry_odunc_uye_id = tk.Entry(odunc_frame, **entry_opts)
    entry_odunc_uye_id.pack(pady=2)

    tk.Label(odunc_frame, text="Kitap ID:", **label_opts).pack(pady=5)
    entry_odunc_kitap_id = tk.Entry(odunc_frame, **entry_opts)
    entry_odunc_kitap_id.pack(pady=2)

    def odunc_al():
        uye_id = entry_odunc_uye_id.get().strip()
        kitap_id = entry_odunc_kitap_id.get().strip()

        uye = next((u for u in uyeler if u.uye_id == uye_id), None)
        kitap = next((k for k in kitaplar if k.kitap_id == kitap_id), None)

        if not uye:
            messagebox.showerror("Hata", "Üye bulunamadı!")
            return
        if not kitap:
            messagebox.showerror("Hata", "Kitap bulunamadı!")
            return
        if kitap.odunc_alindi_mi:
            messagebox.showerror("Hata", "Kitap zaten ödünç verilmiş!")
            return

        # Ödünç alındı işaretle
        kitap.odunc_alindi_mi = True
        odunc_tarihi = datetime.now().strftime("%Y-%m-%d")
        iade_tarihi = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")  # 14 gün ödünç süresi
        yeni_odunc = Odunc(uye_id, kitap_id, odunc_tarihi, iade_tarihi)
        odunc_kayitlari.append(yeni_odunc)

        verileri_kaydet()
        messagebox.showinfo("Başarılı", f"Kitap ödünç alındı.\nİade Tarihi: {iade_tarihi}")
        kitaplari_goster()
        odunclari_goster()

    def odunc_ia():
        uye_id = entry_odunc_uye_id.get().strip()
        kitap_id = entry_odunc_kitap_id.get().strip()

        odunc = next((o for o in odunc_kayitlari if o.uye_id == uye_id and o.kitap_id == kitap_id), None)
        kitap = next((k for k in kitaplar if k.kitap_id == kitap_id), None)

        if not odunc:
            messagebox.showerror("Hata", "Bu ödünç kaydı bulunamadı!")
            return
        if not kitap:
            messagebox.showerror("Hata", "Kitap bulunamadı!")
            return

        # Kitap iade edildi olarak işaretle
        kitap.odunc_alindi_mi = False
        odunc_kayitlari.remove(odunc)

        verileri_kaydet()
        messagebox.showinfo("Başarılı", "Kitap iade edildi.")
        kitaplari_goster()
        odunclari_goster()

    tk.Button(odunc_frame, text="Ödünç Al", command=odunc_al, **button_opts).pack(pady=5)
    tk.Button(odunc_frame, text="İade Et", command=odunc_ia, **button_error_opts).pack(pady=5)

    odunc_tree = ttk.Treeview(odunc_frame, columns=("Üye ID", "Kitap ID", "Ödünç Tarihi", "İade Tarihi"), show="headings", height=10)
    odunc_tree.pack(pady=10, fill="x")
    for col in ("Üye ID", "Kitap ID", "Ödünç Tarihi", "İade Tarihi"):
        odunc_tree.heading(col, text=col)
        odunc_tree.column(col, anchor="center")

    def odunclari_goster():
        odunc_tree.delete(*odunc_tree.get_children())
        for o in odunc_kayitlari:
            odunc_tree.insert("", tk.END, values=(o.uye_id, o.kitap_id, o.odunc_tarihi, o.iade_tarihi))

    odunclari_goster()

    # -- Raporlar Sekmesi --

    rapor_frame = tk.Frame(tablo, bg="#34495e")

    rapor_text = tk.Text(rapor_frame, height=20, font=("Arial", 12))
    rapor_text.pack(pady=10, fill="both", expand=True)

    def raporlari_goster():
        rapor_text.delete("1.0", tk.END)

        # 1. Ödünç verilen kitaplar (henüz iade edilmemiş)
        rapor_text.insert(tk.END, "Ödünç Verilen Kitaplar:\n")
        odunc_kitaplar = [o for o in odunc_kayitlari]
        if odunc_kitaplar:
            for o in odunc_kitaplar:
                kitap = next((k for k in kitaplar if k.kitap_id == o.kitap_id), None)
                uye = next((u for u in uyeler if u.uye_id == o.uye_id), None)
                rapor_text.insert(tk.END, f"- {kitap.ad if kitap else 'Bilinmeyen Kitap'} ödünç alan: {uye.ad if uye else 'Bilinmeyen Üye'} - İade Tarihi: {o.iade_tarihi}\n")
        else:
            rapor_text.insert(tk.END, "Hiç ödünç kitap yok.\n")

        rapor_text.insert(tk.END, "\n")

        # 2. En çok ödünç alınan kitaplar (basit sayım)
        rapor_text.insert(tk.END, "En Çok Ödünç Alınan Kitaplar:\n")
        kitap_sayac = {}
        for o in odunc_kayitlari:
            kitap_sayac[o.kitap_id] = kitap_sayac.get(o.kitap_id, 0) + 1

        sirali_kitaplar = sorted(kitap_sayac.items(), key=lambda x: x[1], reverse=True)
        if sirali_kitaplar:
            for kitap_id, adet in sirali_kitaplar:
                kitap = next((k for k in kitaplar if k.kitap_id == kitap_id), None)
                rapor_text.insert(tk.END, f"- {kitap.ad if kitap else kitap_id}: {adet} kez ödünç alındı\n")
        else:
            rapor_text.insert(tk.END, "Veri yok.\n")

        rapor_text.insert(tk.END, "\n")

        # 3. Gecikme yapan üyeler (iade tarihi geçmiş)
        rapor_text.insert(tk.END, "Gecikme Yapan Üyeler:\n")
        simdi = datetime.now()
        gecikmeli = []
        for o in odunc_kayitlari:
            if o.iade_tarihi:
                iade_tarihi = datetime.strptime(o.iade_tarihi, "%Y-%m-%d")
                if iade_tarihi < simdi:
                    uye = next((u for u in uyeler if u.uye_id == o.uye_id), None)
                    kitap = next((k for k in kitaplar if k.kitap_id == o.kitap_id), None)
                    gecikmeli.append((uye.ad if uye else "Bilinmeyen Üye", kitap.ad if kitap else "Bilinmeyen Kitap", o.iade_tarihi))

        if gecikmeli:
            for u_ad, k_ad, iade in gecikmeli:
                rapor_text.insert(tk.END, f"- {u_ad} adlı üye, {k_ad} adlı kitabı {iade} tarihinde iade etmeliydi.\n")
        else:
            rapor_text.insert(tk.END, "Gecikme yapan üye yok.\n")

    tk.Button(rapor_frame, text="Raporları Güncelle", command=raporlari_goster, **button_opts).pack(pady=10)
    raporlari_goster()

    # --- Sekmeleri ekle ---
    tablo.add(kitap_frame, text="Kitaplar")
    tablo.add(uye_frame, text="Üyeler")
    tablo.add(odunc_frame, text="Ödünç İşlemleri")
    tablo.add(rapor_frame, text="Raporlar")

# --- Program Başlangıcı ---

verileri_yukle()
admin_kontrol()
pencere.mainloop()