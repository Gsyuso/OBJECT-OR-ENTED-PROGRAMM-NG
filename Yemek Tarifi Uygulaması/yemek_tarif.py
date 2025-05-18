import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

root = tk.Tk()

root.title("🍽️ Yemek Tarifi Uygulaması")
root.geometry("1100x700")
root.configure(bg="#f0f2f5")

# Stil ayarları
style = ttk.Style()
style.theme_use('clam')

style.configure('TNotebook.Tab', font=('Segoe UI', 12, 'bold'), padding=[10, 8])
style.configure('TButton', font=('Segoe UI', 11, 'bold'), padding=6)
style.configure('TLabel', font=('Segoe UI', 11))
style.configure('TEntry', padding=5)
style.configure('TListbox', font=('Segoe UI', 10))

# Veri Yapıları
tarifler = []
favoriler = []

class Malzeme:
    def __init__(self, ad, miktar):
        self.ad = ad.strip()
        self.miktar = miktar.strip()

    def to_dict(self):
        return {'ad': self.ad, 'miktar': self.miktar}

    @staticmethod
    def from_dict(data):
        return Malzeme(data['ad'], data['miktar'])

class Tarif:
    def __init__(self, ad, malzemeler, icerik):
        self.ad = ad.strip()
        self.malzemeler = malzemeler
        self.icerik = icerik.strip()
        self.puanlar = []

    def ortalama_puan(self):
        if not self.puanlar:
            return 0
        return round(sum(self.puanlar) / len(self.puanlar), 2)

    def puan_ekle(self, puan):
        self.puanlar.append(puan)

    def to_dict(self):
        return {
            'ad': self.ad,
            'malzemeler': [m.to_dict() for m in self.malzemeler],
            'icerik': self.icerik,
            'puanlar': self.puanlar
        }

    @staticmethod
    def from_dict(data):
        malzemeler = [Malzeme.from_dict(m) for m in data['malzemeler']]
        tarif = Tarif(data['ad'], malzemeler, data['icerik'])
        tarif.puanlar = data.get('puanlar', [])
        return tarif

DATA_FILE = "tarifler.json"

def verileri_kaydet():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "tarifler": [t.to_dict() for t in tarifler],
            "favoriler": [t.ad for t in favoriler]
        }, f, ensure_ascii=False, indent=4)

def verileri_yukle():
    global tarifler, favoriler
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            veri = json.load(f)
            if isinstance(veri, dict):
                tarifler = [Tarif.from_dict(t) for t in veri.get('tarifler', [])]
                favori_listesi = []
                for fav_ad in veri.get('favoriler', []):
                    for t in tarifler:
                        if t.ad == fav_ad:
                            favori_listesi.append(t)
                            break
                favoriler = favori_listesi
            elif isinstance(veri, list):
                tarifler = [Tarif.from_dict(t) for t in veri]
                favoriler = []
            else:
                tarifler = []
                favoriler = []
    else:
        tarifler = []
        favoriler = []

# --- Arayüz ---
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=10, pady=10)

# Frame'ler
tarif_ekle_frame = ttk.Frame(notebook, padding=15)
tarifler_frame = ttk.Frame(notebook, padding=15)
favori_frame = ttk.Frame(notebook, padding=15)
filtre_frame = ttk.Frame(notebook, padding=15)
puanli_frame = ttk.Frame(notebook, padding=15)
degerlendirme_frame = ttk.Frame(notebook, padding=15)

notebook.add(tarif_ekle_frame, text="📝 Tarif Ekle")
notebook.add(tarifler_frame, text="📜 Tüm Tarifler")
notebook.add(favori_frame, text="⭐ Favoriler")
notebook.add(filtre_frame, text="🔍 Malzemeye Göre Filtrele")
notebook.add(puanli_frame, text="🏆 En Yüksek Puanlılar")
notebook.add(degerlendirme_frame, text="📝 Tarif Değerlendir")

# --- Tarif Ekle ---
ttk.Label(tarif_ekle_frame, text="Tarif Adı").pack(anchor='w')
tarif_adi_entry = ttk.Entry(tarif_ekle_frame, width=60)
tarif_adi_entry.pack(pady=4)

ttk.Label(tarif_ekle_frame, text="Malzemeler (örnek: Soğan, 1 adet)").pack(anchor='w')
malzeme_text = tk.Text(tarif_ekle_frame, width=60, height=5, relief='solid', bd=1)
malzeme_text.insert(tk.END, "Soğan, 1 adet\nTuz, 1 çay kaşığı")
malzeme_text.pack(pady=4)

ttk.Label(tarif_ekle_frame, text="Tarif İçeriği").pack(anchor='w')
tarif_icerik_text = tk.Text(tarif_ekle_frame, width=60, height=10, relief='solid', bd=1)
tarif_icerik_text.pack(pady=4)

ttk.Button(tarif_ekle_frame, text="Tarifi Ekle", command=lambda:[tarif_ekle(), tarif_adi_entry.focus_set()]).pack(pady=8)

# --- Tüm Tarifler ---
tarif_listebox = tk.Listbox(tarifler_frame, width=70, height=15, font=('Segoe UI', 11))
tarif_listebox.pack(pady=5)

tarif_detay_text = tk.Text(tarifler_frame, width=85, height=15, relief='solid', bd=1, font=('Segoe UI', 11))
tarif_detay_text.pack(pady=5)

btn_frame = ttk.Frame(tarifler_frame)
btn_frame.pack(pady=8)

ttk.Button(btn_frame, text="Sil", command=lambda:[tarif_sil(), tarif_adi_entry.focus_set()]).grid(row=0, column=0, padx=5)
ttk.Button(btn_frame, text="Favorilere Ekle", command=lambda:[favori_ekle(), tarif_adi_entry.focus_set()]).grid(row=0, column=1, padx=5)

# --- Favoriler ---
favori_listbox = tk.Listbox(favori_frame, width=70, height=25, font=('Segoe UI', 11))
favori_listbox.pack(pady=5)

# --- Filtreleme ---
ttk.Label(filtre_frame, text="Malzeme Adı").pack(anchor='w')
malzeme_entry = ttk.Entry(filtre_frame, width=50)
malzeme_entry.pack(pady=5)

filtre_sonuc = tk.Listbox(filtre_frame, width=70, height=15, font=('Segoe UI', 11))
filtre_sonuc.pack(pady=5)

btn_filtrele = ttk.Button(filtre_frame, text="Filtrele", command=lambda:[filtrele(), malzeme_entry.focus_set()])
btn_filtrele.pack()

# --- En Yüksek Puanlılar ---
puanli_listbox = tk.Listbox(puanli_frame, width=70, height=25, font=('Segoe UI', 11))
puanli_listbox.pack(pady=5)

# --- Tarif Değerlendir ---
ttk.Label(degerlendirme_frame, text="Bir tarif seçin ve puan verin:").pack(anchor='w')
degerlendirme_listbox = tk.Listbox(degerlendirme_frame, width=60, height=15, font=('Segoe UI', 11))
degerlendirme_listbox.pack(pady=5)

puan_kutusu_frame = ttk.Frame(degerlendirme_frame)
puan_kutusu_frame.pack(pady=5)
ttk.Label(puan_kutusu_frame, text="Puan (1-5):").grid(row=0, column=0, padx=5)
degerlendirme_spinbox = ttk.Spinbox(puan_kutusu_frame, from_=1, to=5, width=5)
degerlendirme_spinbox.grid(row=0, column=1, padx=5)
ttk.Button(puan_kutusu_frame, text="Puan Ver", command=lambda:[puan_ver_degerlendirme(), degerlendirme_spinbox.focus_set()]).grid(row=0, column=2, padx=5)

# --- Fonksiyonlar ---

def tarif_ekle():
    ad = tarif_adi_entry.get().strip()
    icerik = tarif_icerik_text.get("1.0", tk.END).strip()
    malzeme_raw = malzeme_text.get("1.0", tk.END).strip()

    if not ad or not malzeme_raw or not icerik:
        messagebox.showerror("Hata", "Tüm alanlar doldurmalı.")
        return

    malzeme_list = []
    for satir in malzeme_raw.split("\n"):
        if "," in satir:
            ad_malz, miktar = satir.split(",", 1)
            malzeme_list.append(Malzeme(ad_malz.strip(), miktar.strip()))
        else:
            messagebox.showerror("Hata", f"Malzeme formatı hatalı: '{satir}'")
            return

    # Aynı isimde tarif varsa uyar
    for t in tarifler:
        if t.ad.lower() == ad.lower():
            messagebox.showerror("Hata", "Bu isimde başka bir tarif zaten var.")
            return

    yeni_tarif = Tarif(ad, malzeme_list, icerik)
    tarifler.append(yeni_tarif)
    verileri_kaydet()
    tarif_adi_entry.delete(0, tk.END)
    malzeme_text.delete("1.0", tk.END)
    tarif_icerik_text.delete("1.0", tk.END)
    liste_guncelle()
    favori_liste_guncelle()
    filtre_sonuc.delete(0, tk.END)
    puanli_liste_guncelle()
    degerlendirme_liste_guncelle()
    messagebox.showinfo("Başarılı", "Tarif eklendi.")

def liste_guncelle():
    tarif_listebox.delete(0, tk.END)
    for t in tarifler:
        puan_str = f" - Ortalama Puan: {t.ortalama_puan()}"
        tarif_listebox.insert(tk.END, t.ad + puan_str)

def tarif_sil():
    secili = tarif_listebox.curselection()
    if not secili:
        messagebox.showwarning("Uyarı", "Silmek için bir tarif seçiniz.")
        return
    idx = secili[0]
    tarif_adi = tarif_listebox.get(idx).split(" - ")[0]
    for t in tarifler:
        if t.ad == tarif_adi:
            tarifler.remove(t)
            if t in favoriler:
                favoriler.remove(t)
            break
    verileri_kaydet()
    liste_guncelle()
    favori_liste_guncelle()
    filtre_sonuc.delete(0, tk.END)
    puanli_liste_guncelle()
    degerlendirme_liste_guncelle()
    tarif_detay_text.delete("1.0", tk.END)
    messagebox.showinfo("Başarılı", "Tarif silindi.")

def favori_ekle():
    secili = tarif_listebox.curselection()
    if not secili:
        messagebox.showwarning("Uyarı", "Favorilere eklemek için bir tarif seçiniz.")
        return
    idx = secili[0]
    tarif_adi = tarif_listebox.get(idx).split(" - ")[0]
    for t in tarifler:
        if t.ad == tarif_adi:
            if t in favoriler:
                messagebox.showinfo("Bilgi", "Bu tarif zaten favorilerde.")
                return
            favoriler.append(t)
            verileri_kaydet()
            favori_liste_guncelle()
            messagebox.showinfo("Başarılı", "Tarif favorilere eklendi.")
            break

def favori_liste_guncelle():
    favori_listbox.delete(0, tk.END)
    for t in favoriler:
        puan_str = f" - Ortalama Puan: {t.ortalama_puan()}"
        favori_listbox.insert(tk.END, t.ad + puan_str)

def filtrele():
    malzeme_adi = malzeme_entry.get().strip().lower()
    filtre_sonuc.delete(0, tk.END)
    if not malzeme_adi:
        messagebox.showwarning("Uyarı", "Lütfen malzeme adı giriniz.")
        return
    bulunanlar = []
    for t in tarifler:
        for m in t.malzemeler:
            if malzeme_adi in m.ad.lower():
                bulunanlar.append(t)
                break
    if not bulunanlar:
        filtre_sonuc.insert(tk.END, "Bu malzemeye uygun tarif bulunamadı.")
    else:
        for t in bulunanlar:
            puan_str = f" - Ortalama Puan: {t.ortalama_puan()}"
            filtre_sonuc.insert(tk.END, t.ad + puan_str)

def puanli_liste_guncelle():
    puanli_listbox.delete(0, tk.END)
    sirali = sorted(tarifler, key=lambda x: x.ortalama_puan(), reverse=True)
    for t in sirali:
        puanli_listbox.insert(tk.END, f"{t.ad} - Ortalama Puan: {t.ortalama_puan()}")

def degerlendirme_liste_guncelle():
    degerlendirme_listbox.delete(0, tk.END)
    for t in tarifler:
        degerlendirme_listbox.insert(tk.END, t.ad)

def puan_ver_degerlendirme():
    secili = degerlendirme_listbox.curselection()
    if not secili:
        messagebox.showwarning("Uyarı", "Lütfen bir tarif seçiniz.")
        return
    idx = secili[0]
    tarif_adi = degerlendirme_listbox.get(idx)
    try:
        puan = int(degerlendirme_spinbox.get())
        if puan < 1 or puan > 5:
            raise ValueError
    except ValueError:
        messagebox.showerror("Hata", "Lütfen 1 ile 5 arasında bir puan giriniz.")
        return
    for t in tarifler:
        if t.ad == tarif_adi:
            t.puan_ekle(puan)
            break
    verileri_kaydet()
    puanli_liste_guncelle()
    liste_guncelle()
    favori_liste_guncelle()
    messagebox.showinfo("Başarılı", f"{tarif_adi} tarifine {puan} puan verildi.")

def tarif_detay_goster(event):
    secili = tarif_listebox.curselection()
    if not secili:
        return
    idx = secili[0]
    tarif_adi = tarif_listebox.get(idx).split(" - ")[0]
    for t in tarifler:
        if t.ad == tarif_adi:
            detay = f"Tarif Adı: {t.ad}\n\nMalzemeler:\n"
            for m in t.malzemeler:
                detay += f"- {m.ad}, {m.miktar}\n"
            detay += f"\nTarif:\n{t.icerik}\n\nOrtalama Puan: {t.ortalama_puan()}"
            tarif_detay_text.delete("1.0", tk.END)
            tarif_detay_text.insert(tk.END, detay)
            break

tarif_listebox.bind("<<ListboxSelect>>", tarif_detay_goster)

# --- Uygulama başlatılırken veri yükleme ---
verileri_yukle()
liste_guncelle()
favori_liste_guncelle()
puanli_liste_guncelle()
degerlendirme_liste_guncelle()

root.mainloop()