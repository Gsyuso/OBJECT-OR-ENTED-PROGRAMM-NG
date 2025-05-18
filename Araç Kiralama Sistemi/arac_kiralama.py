import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import json
import os

# --- Veri Dosyası ---
VERI_DOSYASI = "veri.json"

# --- Sınıflar ---
class Arac:
    def __init__(self, arac_id, model, ucret):
        self.arac_id = arac_id
        self.model = model
        self.ucret = ucret
        self.kiralama_durumu = False

    def arac_durumu_guncelle(self, durum):
        self.kiralama_durumu = durum

class Musteri:
    def __init__(self, musteri_id, ad):
        self.musteri_id = musteri_id
        self.ad = ad

class Kiralama:
    def __init__(self):
        self.kiralamalar = []

    def kiralama_yap(self, musteri, arac, baslangic, bitis):
        if arac.kiralama_durumu:
            return False
        arac.arac_durumu_guncelle(True)
        self.kiralamalar.append({
            "musteri_id": musteri.musteri_id,
            "musteri_ad": musteri.ad,
            "arac_id": arac.arac_id,
            "arac_model": arac.model,
            "ucret": arac.ucret,
            "baslangic": baslangic,
            "bitis": bitis
        })
        return True

    def kiralama_iptal_et(self, musteri_id, arac_id):
        for i, kiralama in enumerate(self.kiralamalar):
            if kiralama["musteri_id"] == musteri_id and kiralama["arac_id"] == arac_id:
                araclar[arac_id].arac_durumu_guncelle(False)
                del self.kiralamalar[i]
                return True
        return False

# --- Veri Yüklenmesi ve Kaydı ---
def verileri_yukle():
    global araclar, musteriler, kiralama_sistemi
    if not os.path.exists(VERI_DOSYASI):
        return
    with open(VERI_DOSYASI, "r") as f:
        veri = json.load(f)
    for aid, a in veri.get("araclar", {}).items():
        arac = Arac(aid, a["model"], a["ucret"])
        arac.arac_durumu_guncelle(a["kiralama_durumu"])
        araclar[aid] = arac
    for mid, m in veri.get("musteriler", {}).items():
        musteriler[mid] = Musteri(mid, m["ad"])
    kiralama_sistemi.kiralamalar = veri.get("kiralamalar", [])

def verileri_kaydet():
    veri = {
        "araclar": {
            aid: {
                "model": a.model,
                "ucret": a.ucret,
                "kiralama_durumu": a.kiralama_durumu
            } for aid, a in araclar.items()
        },
        "musteriler": {
            mid: {"ad": m.ad} for mid, m in musteriler.items()
        },
        "kiralamalar": kiralama_sistemi.kiralamalar
    }
    with open(VERI_DOSYASI, "w") as f:
        json.dump(veri, f, indent=4)

# --- Veri Yapıları ---
araclar = {}
musteriler = {}
kiralama_sistemi = Kiralama()
verileri_yukle()

# --- Ana Pencere ---
root = tk.Tk()
root.title("Araç Kiralama Sistemi")
root.geometry("1000x600")
root.configure(bg="#f0f2f5")

# --- Stil Ayarları ---
style = ttk.Style(root)
style.theme_use("clam")  # Modern, temiz tema

# Genel font ve renk ayarları
style.configure(".", font=("Segoe UI", 10))
style.configure("TLabel", background="#f0f2f5")
style.configure("TButton", padding=6)
style.configure("Treeview", 
                background="white",
                foreground="black",
                rowheight=25,
                fieldbackground="white",
                font=("Segoe UI", 10))
style.map("Treeview", background=[('selected', '#3874f2')], foreground=[('selected', 'white')])

style.configure("Treeview.Heading", font=("Segoe UI Semibold", 11), background="#3874f2", foreground="white")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=15, pady=15)

# --- Araç Ekleme Sekmesi ---
arac_frame = ttk.Frame(notebook)
notebook.add(arac_frame, text="Araçlar")

for widget in arac_frame.winfo_children():
    widget.configure(padding=8)

arac_id_entry = ttk.Entry(arac_frame, width=30)
model_entry = ttk.Entry(arac_frame, width=30)
ucret_entry = ttk.Entry(arac_frame, width=30)

def arac_ekle():
    aid = arac_id_entry.get()
    model = model_entry.get()
    try:
        ucret = float(ucret_entry.get())
    except ValueError:
        messagebox.showerror("Hata", "Ücret sayı olmalı")
        return
    if aid in araclar:
        messagebox.showerror("Hata", "Araç zaten var")
        return
    araclar[aid] = Arac(aid, model, ucret)
    guncelle_araclar()
    arac_id_entry.delete(0, tk.END)
    model_entry.delete(0, tk.END)
    ucret_entry.delete(0, tk.END)
    verileri_kaydet()

ttk.Label(arac_frame, text="Araç ID:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
ttk.Label(arac_frame, text="Model:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
ttk.Label(arac_frame, text="Ücret (günlük):").grid(row=2, column=0, sticky="w", padx=10, pady=5)

arac_id_entry.grid(row=0, column=1, padx=10, pady=5)
model_entry.grid(row=1, column=1, padx=10, pady=5)
ucret_entry.grid(row=2, column=1, padx=10, pady=5)

ttk.Button(arac_frame, text="Araç Ekle", command=arac_ekle).grid(row=3, column=0, columnspan=2, pady=15)

arac_tree = ttk.Treeview(arac_frame, columns=("id", "model", "ucret", "durum"), show="headings", selectmode="browse")
arac_tree.heading("id", text="ID", anchor="center")
arac_tree.heading("model", text="Model", anchor="center")
arac_tree.heading("ucret", text="Ücret", anchor="center")
arac_tree.heading("durum", text="Durum", anchor="center")
arac_tree.column("id", width=100, anchor="center")
arac_tree.column("model", width=250, anchor="w")
arac_tree.column("ucret", width=100, anchor="center")
arac_tree.column("durum", width=100, anchor="center")
arac_tree.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

arac_frame.rowconfigure(4, weight=1)
arac_frame.columnconfigure(1, weight=1)

# --- Müşteri Ekleme Sekmesi ---
musteri_frame = ttk.Frame(notebook)
notebook.add(musteri_frame, text="Müşteriler")

musteri_id_entry = ttk.Entry(musteri_frame, width=30)
ad_entry = ttk.Entry(musteri_frame, width=30)

def musteri_ekle():
    mid = musteri_id_entry.get()
    ad = ad_entry.get()
    if mid in musteriler:
        messagebox.showerror("Hata", "Müşteri zaten var")
        return
    musteriler[mid] = Musteri(mid, ad)
    guncelle_musteriler()
    musteri_id_entry.delete(0, tk.END)
    ad_entry.delete(0, tk.END)
    verileri_kaydet()

ttk.Label(musteri_frame, text="Müşteri ID:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
ttk.Label(musteri_frame, text="Ad:").grid(row=1, column=0, sticky="w", padx=10, pady=5)

musteri_id_entry.grid(row=0, column=1, padx=10, pady=5)
ad_entry.grid(row=1, column=1, padx=10, pady=5)

ttk.Button(musteri_frame, text="Müşteri Ekle", command=musteri_ekle).grid(row=2, column=0, columnspan=2, pady=15)

musteri_tree = ttk.Treeview(musteri_frame, columns=("id", "ad"), show="headings", selectmode="browse")
musteri_tree.heading("id", text="ID", anchor="center")
musteri_tree.heading("ad", text="Ad", anchor="center")
musteri_tree.column("id", width=150, anchor="center")
musteri_tree.column("ad", width=350, anchor="w")
musteri_tree.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

musteri_frame.rowconfigure(3, weight=1)
musteri_frame.columnconfigure(1, weight=1)

# --- Kiralama Sekmesi ---
kiralama_frame = ttk.Frame(notebook)
notebook.add(kiralama_frame, text="Kiralama")

kirala_mid = ttk.Entry(kiralama_frame, width=30)
kirala_aid = ttk.Entry(kiralama_frame, width=30)
kirala_basla = ttk.Entry(kiralama_frame, width=30)
kirala_bitis = ttk.Entry(kiralama_frame, width=30)

def kirala():
    mid = kirala_mid.get()
    aid = kirala_aid.get()
    try:
        basla = datetime.strptime(kirala_basla.get(), "%Y-%m-%d")
        bitis = datetime.strptime(kirala_bitis.get(), "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Hata", "Tarih formatı: YYYY-MM-DD")
        return
    if bitis <= basla:
        messagebox.showerror("Hata", "Bitiş tarihi başlangıçtan sonra olmalı")
        return
    if mid not in musteriler or aid not in araclar:
        messagebox.showerror("Hata", "Araç veya müşteri yok")
        return
    if kiralama_sistemi.kiralama_yap(musteriler[mid], araclar[aid], kirala_basla.get(), kirala_bitis.get()):
        guncelle_kiralamalar()
        guncelle_araclar()
        verileri_kaydet()
        gun = (bitis - basla).days
        ucret = gun * araclar[aid].ucret
        messagebox.showinfo("Kiralandı", f"Toplam ücret: {ucret} TL")
    else:
        messagebox.showerror("Hata", "Araç zaten kiralanmış")

def iptal_et():
    if kiralama_sistemi.kiralama_iptal_et(kirala_mid.get(), kirala_aid.get()):
        guncelle_kiralamalar()
        guncelle_araclar()
        verileri_kaydet()
        messagebox.showinfo("Tamam", "Kiralama iptal edildi")
    else:
        messagebox.showerror("Hata", "Kiralama bulunamadı")

ttk.Label(kiralama_frame, text="Müşteri ID:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
ttk.Label(kiralama_frame, text="Araç ID:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
ttk.Label(kiralama_frame, text="Başlangıç (YYYY-MM-DD):").grid(row=2, column=0, sticky="w", padx=10, pady=5)
ttk.Label(kiralama_frame, text="Bitiş (YYYY-MM-DD):").grid(row=3, column=0, sticky="w", padx=10, pady=5)

kirala_mid.grid(row=0, column=1, padx=10, pady=5)
kirala_aid.grid(row=1, column=1, padx=10, pady=5)
kirala_basla.grid(row=2, column=1, padx=10, pady=5)
kirala_bitis.grid(row=3, column=1, padx=10, pady=5)

ttk.Button(kiralama_frame, text="Kirala", command=kirala).grid(row=4, column=0, padx=10, pady=15)
ttk.Button(kiralama_frame, text="İptal", command=iptal_et).grid(row=4, column=1, padx=10, pady=15)

kiralama_tree = ttk.Treeview(kiralama_frame, columns=("mid", "mad", "aid", "amodel", "basla", "bitis"), show="headings", selectmode="browse")
for col, text in zip(kiralama_tree["columns"], ["Müşteri ID", "Müşteri Adı", "Araç ID", "Model", "Başlangıç", "Bitiş"]):
    kiralama_tree.heading(col, text=text, anchor="center")
kiralama_tree.column("mid", width=100, anchor="center")
kiralama_tree.column("mad", width=150, anchor="w")
kiralama_tree.column("aid", width=100, anchor="center")
kiralama_tree.column("amodel", width=150, anchor="w")
kiralama_tree.column("basla", width=120, anchor="center")
kiralama_tree.column("bitis", width=120, anchor="center")
kiralama_tree.grid(row=5, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

kiralama_frame.rowconfigure(5, weight=1)
kiralama_frame.columnconfigure(1, weight=1)

# --- Güncelleme Fonksiyonları ---
def guncelle_araclar():
    for i in arac_tree.get_children():
        arac_tree.delete(i)
    for aid, a in araclar.items():
        durum = "Kirada" if a.kiralama_durumu else "Uygun"
        arac_tree.insert("", "end", values=(aid, a.model, a.ucret, durum))

def guncelle_musteriler():
    for i in musteri_tree.get_children():
        musteri_tree.delete(i)
    for mid, m in musteriler.items():
        musteri_tree.insert("", "end", values=(mid, m.ad))

def guncelle_kiralamalar():
    for i in kiralama_tree.get_children():
        kiralama_tree.delete(i)
    for k in kiralama_sistemi.kiralamalar:
        kiralama_tree.insert("", "end", values=(k["musteri_id"], k["musteri_ad"], k["arac_id"], k["arac_model"], k["baslangic"], k["bitis"]))

# --- Başlangıçta Listeyi Güncelle ---
guncelle_araclar()
guncelle_musteriler()
guncelle_kiralamalar()

root.mainloop()
