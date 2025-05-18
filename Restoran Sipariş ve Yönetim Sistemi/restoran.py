import tkinter as tk
from tkinter import ttk, messagebox
import json

# Yazı Tipi Tanımları
FONT = ("Helvetica", 10)
HEADER_FONT = ("Helvetica", 14, "bold")

# Ana Pencereyi Başlat
root = tk.Tk()
root.title("Restoran Sipariş ve Yönetim Sistemi")
root.geometry("1000x720")
root.configure(bg="#e0e6f0")  # Modern bir görünüm için açık mavi-gri arka plan

# Özel Stil Yapılandırması
style = ttk.Style()
style.theme_use('clam')  # Daha iyi stil kontrolü için 'clam' teması

# Treeview Yapılandırması
style.configure("Treeview", 
                font=FONT, 
                rowheight=30, 
                background="#ffffff", 
                foreground="#333333", 
                fieldbackground="#ffffff")
style.configure("Treeview.Heading", 
                font=("Helvetica", 10, "bold"), 
                background="#4a90e2",  # Mavi başlık
                foreground="#ffffff")
style.map("Treeview", 
          background=[('selected', '#a3c1e6')])  # Seçim için açık mavi

# Notebook Yapılandırması
style.configure("TNotebook", 
                background="#e0e6f0")
style.configure("TNotebook.Tab", 
                font=FONT, 
                padding=[10, 5], 
                background="#4a90e2", 
                foreground="#ffffff")
style.map("TNotebook.Tab", 
          background=[('selected', '#ffffff'), ('active', '#a3c1e6')],
          foreground=[('selected', '#333333'), ('active', '#333333')])

# Button Stili
style.configure("TButton", 
                font=FONT, 
                padding=8, 
                background="#4a90e2", 
                foreground="#ffffff")
style.map("TButton", 
          background=[('active', '#357abd')],
          foreground=[('active', '#ffffff')])

# Entry Stili
style.configure("TEntry", 
                font=FONT, 
                padding=5)

# Combobox Stili
style.configure("TCombobox", 
                font=FONT, 
                padding=5)

# Veri Sınıfları
class Urun:
    def __init__(self, urun_id, ad, fiyat, stok, kategori="Genel"):
        self.urun_id = urun_id
        self.ad = ad
        self.fiyat = fiyat
        self.stok = stok
        self.kategori = kategori

class Musteri:
    def __init__(self, musteri_id, ad, adres, telefon="", email=""):
        self.musteri_id = musteri_id
        self.ad = ad
        self.adres = adres
        self.telefon = telefon
        self.email = email

class Siparis:
    def __init__(self, siparis_no, musteri, urunler_adet, durum="Hazırlanıyor"):
        self.siparis_no = siparis_no
        self.musteri = musteri
        self.urunler_adet = urunler_adet  # Liste [(Urun, adet), ...]
        self.durum = durum

urunler = {}
musteriler = {}
siparisler = []
siparis_sayaci = 1

def veri_kaydet():
    data = {
        "urunler": [
            {"urun_id": u.urun_id, "ad": u.ad, "fiyat": u.fiyat, "stok": u.stok, "kategori": u.kategori}
            for u in urunler.values()
        ],
        "musteriler": [
            {"musteri_id": m.musteri_id, "ad": m.ad, "adres": m.adres, "telefon": m.telefon, "email": m.email}
            for m in musteriler.values()
        ],
        "siparisler": [
            {
                "siparis_no": s.siparis_no,
                "musteri_id": s.musteri.musteri_id,
                "urunler_adet": [{"urun_id": ua[0].urun_id, "adet": ua[1]} for ua in s.urunler_adet],
                "durum": s.durum
            }
            for s in siparisler
        ],
        "siparis_sayaci": siparis_sayaci
    }
    with open("veriler.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def veri_yukle():
    global siparis_sayaci
    try:
        with open("veriler.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        urunler.clear()
        for u in data.get("urunler", []):
            urun = Urun(u["urun_id"], u["ad"], u["fiyat"], u["stok"], u.get("kategori", "Genel"))
            urunler[urun.urun_id] = urun
        musteriler.clear()
        for m in data.get("musteriler", []):
            musteri = Musteri(m["musteri_id"], m["ad"], m["adres"], m.get("telefon", ""), m.get("email", ""))
            musteriler[musteri.musteri_id] = musteri
        siparisler.clear()
        for s in data.get("siparisler", []):
            musteri = musteriler.get(s["musteri_id"])
            urunler_adet = []
            for ua in s.get("urunler_adet", []):
                urun = urunler.get(ua["urun_id"])
                if urun:
                    urunler_adet.append((urun, ua["adet"]))
            siparis = Siparis(s["siparis_no"], musteri, urunler_adet, s.get("durum", "Hazırlanıyor"))
            siparisler.append(siparis)
        siparis_sayaci = data.get("siparis_sayaci", 1)
        guncelle_urun_tablosu()
        guncelle_urun_combobox()
        guncelle_siparis_tablosu()
    except FileNotFoundError:
        pass

# Sekmeler
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=10, pady=10)

# --- Ürün Yönetimi ---
urun_frame = ttk.Frame(notebook, padding=20)
notebook.add(urun_frame, text="Ürün Yönetimi")

# Başlık
ttk.Label(urun_frame, text="Ürün Ekle", font=HEADER_FONT, background="#e0e6f0", foreground="#333333").grid(row=0, column=0, columnspan=3, pady=(0, 20))

labels = ["Ürün ID", "Ürün Adı", "Fiyat", "Stok", "Kategori"]
entries = []

# Giriş Alanları
for i, text in enumerate(labels):
    ttk.Label(urun_frame, text=text, font=FONT, background="#e0e6f0", foreground="#333333").grid(row=i+1, column=0, sticky="e", padx=10, pady=8)
    entry = ttk.Entry(urun_frame, font=FONT, width=35)
    entry.grid(row=i+1, column=1, sticky="w", padx=10, pady=8)
    entries.append(entry)

urun_id_entry, urun_ad_entry, urun_fiyat_entry, urun_stok_entry, urun_kategori_entry = entries
urun_kategori_entry.insert(0, "Genel")

def guncelle_urun_tablosu():
    for i in urun_tablosu.get_children():
        urun_tablosu.delete(i)
    for urun in urunler.values():
        urun_tablosu.insert("", "end", values=(urun.urun_id, urun.ad, f"{urun.fiyat:.2f}", urun.stok, urun.kategori))

def guncelle_urun_combobox():
    liste = [urun.ad for urun in urunler.values()]
    urun_sec_combobox['values'] = liste

def urun_ekle():
    uid = urun_id_entry.get().strip()
    ad = urun_ad_entry.get().strip()
    kategori = urun_kategori_entry.get().strip()
    try:
        fiyat = float(urun_fiyat_entry.get())
        stok = int(urun_stok_entry.get())
    except:
        messagebox.showerror("Hata", "Geçerli sayı giriniz.")
        return
    if uid in urunler:
        messagebox.showerror("Hata", "Bu ID zaten var.")
        return
    if not uid or not ad:
        messagebox.showerror("Hata", "ID ve Ad boş olamaz.")
        return
    urunler[uid] = Urun(uid, ad, fiyat, stok, kategori)
    guncelle_urun_tablosu()
    guncelle_urun_combobox()
    for e in entries: e.delete(0, tk.END)
    urun_kategori_entry.insert(0, "Genel")
    veri_kaydet()

# Ürün Ekle Düğmesi
ttk.Button(urun_frame, text="Ürün Ekle", command=urun_ekle).grid(row=6, column=0, columnspan=2, pady=20)

# Ürün Tablosu
urun_tablosu = ttk.Treeview(urun_frame, columns=("ID", "Ad", "Fiyat", "Stok", "Kategori"), show="headings")
for col in ("ID", "Ad", "Fiyat", "Stok", "Kategori"):
    urun_tablosu.heading(col, text=col)
    urun_tablosu.column(col, width=120)
urun_tablosu.grid(row=7, column=0, columnspan=3, pady=10, sticky="nsew")

# --- Sipariş Al ---
siparis_frame = ttk.Frame(notebook, padding=20)
notebook.add(siparis_frame, text="Sipariş Al")

# Başlık
ttk.Label(siparis_frame, text="Sipariş Ver", font=HEADER_FONT, background="#e0e6f0", foreground="#333333").grid(row=0, column=0, columnspan=3, pady=(0, 20), sticky="w")

# Müşteri Giriş Alanları
labels = ["Müşteri ID", "Müşteri Adı", "Adres", "Telefon", "E-posta"]
siparis_entries = []

for i, text in enumerate(labels):
    ttk.Label(siparis_frame, text=text, font=FONT, background="#e0e6f0", foreground="#333333").grid(row=i+1, column=0, sticky="e", padx=10, pady=8)
    entry = ttk.Entry(siparis_frame, font=FONT, width=35)
    entry.grid(row=i+1, column=1, sticky="w", padx=10, pady=8)
    siparis_entries.append(entry)

musteri_id_entry, musteri_ad_entry, musteri_adres_entry, musteri_telefon_entry, musteri_email_entry = siparis_entries

# Ürün Seçimi
ttk.Label(siparis_frame, text="Ürün Seç", font=FONT, background="#e0e6f0", foreground="#333333").grid(row=6, column=0, sticky="e", padx=10, pady=8)
urun_sec_combobox = ttk.Combobox(siparis_frame, font=FONT, width=33, state="readonly")
urun_sec_combobox.grid(row=6, column=1, sticky="w", padx=10, pady=8)

# Adet Girişi
ttk.Label(siparis_frame, text="Adet", font=FONT, background="#e0e6f0", foreground="#333333").grid(row=7, column=0, sticky="e", padx=10, pady=8)
adet_entry = ttk.Entry(siparis_frame, font=FONT, width=35)
adet_entry.grid(row=7, column=1, sticky="w", padx=10, pady=8)

# Sepet Tablosu Başlığı
ttk.Label(siparis_frame, text="Sipariş Sepeti", font=HEADER_FONT, background="#e0e6f0", foreground="#333333").grid(row=8, column=0, columnspan=3, pady=(20, 10), sticky="w")

# Sepet Tablosu
sepet_tablosu = ttk.Treeview(siparis_frame, columns=("Ürün", "Adet", "Birim Fiyat", "Toplam"), show="headings", height=5)
for col in ("Ürün", "Adet", "Birim Fiyat", "Toplam"):
    sepet_tablosu.heading(col, text=col)
    sepet_tablosu.column(col, width=120)
sepet_tablosu.grid(row=9, column=0, columnspan=3, pady=10, sticky="nsew")

# Toplam Tutar Etiketi
toplam_label = ttk.Label(siparis_frame, text="Toplam Tutar: 0.00 ₺", font=FONT, background="#e0e6f0", foreground="#333333")
toplam_label.grid(row=10, column=0, columnspan=2, pady=10, sticky="w")

sepet = []

# Sepete Ekle Fonksiyonu
def sepete_ekle():
    urun_ad = urun_sec_combobox.get()
    if not urun_ad:
        messagebox.showerror("Hata", "Lütfen ürün seçin.")
        return
    try:
        adet = int(adet_entry.get())
        if adet <= 0:
            raise ValueError
    except:
        messagebox.showerror("Hata", "Adet pozitif tam sayı olmalı.")
        return
    # Ürün nesnesi bul
    urun = next((u for u in urunler.values() if u.ad == urun_ad), None)
    if not urun:
        messagebox.showerror("Hata", "Seçilen ürün bulunamadı.")
        return
    if adet > urun.stok:
        messagebox.showerror("Hata", f"Yeterli stok yok! Stok: {urun.stok}")
        return
    # Sepete ekle veya adet artır
    for i, (u, a) in enumerate(sepet):
        if u.urun_id == urun.urun_id:
            sepet[i] = (u, a + adet)
            break
    else:
        sepet.append((urun, adet))
    guncelle_sepet_tablosu()
    adet_entry.delete(0, tk.END)

# Sepet Tablosu Güncelleme
def guncelle_sepet_tablosu():
    for i in sepet_tablosu.get_children():
        sepet_tablosu.delete(i)
    toplam_tutar = 0
    for urun, adet in sepet:
        toplam = urun.fiyat * adet
        toplam_tutar += toplam
        sepet_tablosu.insert("", "end", values=(urun.ad, adet, f"{urun.fiyat:.2f}", f"{toplam:.2f}"))
    toplam_label.config(text=f"Toplam Tutar: {toplam_tutar:.2f} ₺")

# Sipariş Ver Fonksiyonu
def siparis_ver():
    global siparis_sayaci
    musteri_id = musteri_id_entry.get().strip()
    musteri_ad = musteri_ad_entry.get().strip()
    musteri_adres = musteri_adres_entry.get().strip()
    musteri_tel = musteri_telefon_entry.get().strip()
    musteri_email = musteri_email_entry.get().strip()
    if not musteri_id or not musteri_ad or not musteri_adres:
        messagebox.showerror("Hata", "Müşteri ID, Adı ve Adres zorunlu.")
        return
    if len(sepet) == 0:
        messagebox.showerror("Hata", "Sipariş sepeti boş.")
        return
    # Müşteri var mı kontrol et
    if musteri_id in musteriler:
        musteri = musteriler[musteri_id]
        # Gerekirse bilgileri güncelle
        musteri.ad = musteri_ad
        musteri.adres = musteri_adres
        musteri.telefon = musteri_tel
        musteri.email = musteri_email
    else:
        musteri = Musteri(musteri_id, musteri_ad, musteri_adres, musteri_tel, musteri_email)
        musteriler[musteri_id] = musteri
    # Stok kontrol tekrar, stok güncelle
    for urun, adet in sepet:
        if urun.stok < adet:
            messagebox.showerror("Hata", f"{urun.ad} stok yetersiz!")
            return
    for urun, adet in sepet:
        urun.stok -= adet
    # Siparişi oluştur
    siparis = Siparis(siparis_sayaci, musteri, sepet.copy())
    siparisler.append(siparis)
    siparis_sayaci += 1
    # Sepeti temizle
    sepet.clear()
    guncelle_sepet_tablosu()
    guncelle_urun_tablosu()
    guncelle_siparis_tablosu()
    # Form temizle
    for e in siparis_entries:
        e.delete(0, tk.END)
    veri_kaydet()
    messagebox.showinfo("Başarılı", f"Sipariş oluşturuldu! Sipariş No: {siparis.siparis_no}")

# Sepete Ekle ve Siparişi Ver Düğmeleri
ttk.Button(siparis_frame, text="Sepete Ekle", command=sepete_ekle).grid(row=7, column=2, padx=10, pady=8, sticky="w")
ttk.Button(siparis_frame, text="Siparişi Ver", command=siparis_ver).grid(row=10, column=2, pady=10, padx=10, sticky="e")

# --- Sipariş Takip ---
siparis_takip_frame = ttk.Frame(notebook, padding=20)
notebook.add(siparis_takip_frame, text="Sipariş Takip")

# Sipariş Tablosu
siparis_tablosu = ttk.Treeview(siparis_takip_frame, columns=("No", "Müşteri", "Ürünler", "Durum", "Toplam"), show="headings", height=15)
siparis_tablosu.heading("No", text="Sipariş No")
siparis_tablosu.heading("Müşteri", text="Müşteri")
siparis_tablosu.heading("Ürünler", text="Ürünler (Adet)")
siparis_tablosu.heading("Durum", text="Durum")
siparis_tablosu.heading("Toplam", text="Toplam Tutar (₺)")

for col in ("No", "Müşteri", "Ürünler", "Durum", "Toplam"):
    siparis_tablosu.column(col, width=150)
siparis_tablosu.grid(row=0, column=0, columnspan=3, sticky="nsew", pady=10)

# Durum Seçimi
durumlar = ["Hazırlanıyor", "Hazırlandı", "Teslim Edildi", "İptal Edildi"]
durum_combobox = ttk.Combobox(siparis_takip_frame, values=durumlar, state="readonly", font=FONT, width=20)
durum_combobox.grid(row=1, column=1, pady=10)

def guncelle_siparis_tablosu():
    for i in siparis_tablosu.get_children():
        siparis_tablosu.delete(i)
    for s in siparisler:
        urunler_str = ", ".join(f"{u.ad} ({a})" for u, a in s.urunler_adet)
        toplam = sum(u.fiyat * a for u, a in s.urunler_adet)
        siparis_tablosu.insert("", "end", values=(s.siparis_no, s.musteri.ad, urunler_str, s.durum, f"{toplam:.2f}"))

def durum_guncelle():
    secim = siparis_tablosu.selection()
    if not secim:
        messagebox.showerror("Hata", "Lütfen bir sipariş seçin.")
        return
    yeni_durum = durum_combobox.get()
    if not yeni_durum:
        messagebox.showerror("Hata", "Lütfen yeni durumu seçin.")
        return
    siparis_no = siparis_tablosu.item(secim)["values"][0]
    for s in siparisler:
        if s.siparis_no == siparis_no:
            s.durum = yeni_durum
            break
    guncelle_siparis_tablosu()
    veri_kaydet()
    messagebox.showinfo("Başarılı", f"Sipariş durumu '{yeni_durum}' olarak güncellendi.")

# Durum Güncelle Düğmesi
ttk.Button(siparis_takip_frame, text="Durumu Güncelle", command=durum_guncelle).grid(row=1, column=2, padx=10, pady=10)

# Pencere kapanırken veri kaydet
def on_closing():
    veri_kaydet()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

veri_yukle()
root.mainloop()