import tkinter as tk
from tkinter import PhotoImage, Canvas
import random
import csv
import os
import sys

# Dosya yolunu belirlemek için yardımcı fonksiyon
def resource_path(relative_path):
    try:
        # PyInstaller tarafından oluşturulan .exe dosyası için
        base_path = sys._MEIPASS
    except Exception:
        # Geliştirme ortamında çalışırken
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Veritabanını yükleyelim
def load_data():
    hastaliklar = []
    with open(resource_path('hastaliklar.csv'), 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            hastaliklar.append(row)
    return hastaliklar

# Semptomları rastgele sırayla soran fonksiyon
def sorulari_sor():
    global semptomlar, hastaliklar, soru_canvas

    if len(semptomlar) == 0 or len(hastaliklar) == 1:
        # Başlangıç ve sonuç ekranı elemanlarını gizle
        baslik_label.pack_forget()
        resim_label.pack_forget()
        bilgi_label.pack_forget()
        soru_canvas.pack_forget()
        evet_butonu.pack_forget()
        hayir_butonu.pack_forget()

        if len(hastaliklar) == 1:
            sonuc_label.config(text=f"Hastalığınız: {hastaliklar[0]['Hastalık']}", )
        else:
            sonuc_label.config(text="Hastalığınız belirlenemedi.")
        
        # Sadece sonuç ve "Tekrar Başla" butonu kalacak
        sonuc_label.pack(pady=20)
        tekrar_basla_butonu.pack(pady=20)
        
        return

    semptom = random.choice(semptomlar)
    semptomlar.remove(semptom)
    
    soru_text = f"Hastada {semptom} görülmekte midir?"
    soru_canvas.itemconfig(soru_text_item, text=soru_text)

    # Sorular ekranında arka plan resmi göster
    root.configure(bg="#ADD8E6")  # Sorular ekranı arka plan rengi mavi
    soru_canvas.pack(fill="both", expand=True)

def evet():
    global hastaliklar
    semptom = soru_canvas.itemcget(soru_text_item, "text").replace("Hastada ", "").replace(" görülmekte midir?", "")
    hastaliklar = [h for h in hastaliklar if h[semptom] == '1']
    sorulari_sor()

def hayir():
    global hastaliklar
    semptom = soru_canvas.itemcget(soru_text_item, "text").replace("Hastada ", "").replace(" görülmekte midir?", "")
    hastaliklar = [h for h in hastaliklar if h[semptom] == '0']
    sorulari_sor()

# Tekrar Başla butonuna basıldığında çalışacak fonksiyon
def tekrar_basla():
    tekrar_basla_butonu.pack_forget()
    sonuc_label.config(text="")
    basla()

# Başla butonuna basıldığında çalışacak fonksiyon
def basla():
    global hastaliklar, semptomlar
    hastaliklar = load_data()
    semptomlar = list(hastaliklar[0].keys())[1:]  # İlk sütun hariç tüm semptomlar
    
    # Başlangıç ekranı elemanlarını gizle
    baslik_label.pack_forget()
    resim_label.pack_forget()
    bilgi_label.pack_forget()
    basla_butonu.pack_forget()  # Başla butonunu kaldır
    
    soru_canvas.pack(fill="both", expand=True)
    sorulari_sor()

# Tkinter penceresini oluşturma
root = tk.Tk()
root.title("Hastalık Tespiti")
root.configure(bg="#98FB98")  # Başlangıç ekranı arkaplan rengi yeşil

# Başlık
baslik_label = tk.Label(root, text="Hastalık Bul", font=("Arial", 24, "bold"), bg="#98FB98")
baslik_label.pack(pady=10)

# Başlangıç Resmi
baslangic_resmi = PhotoImage(file=resource_path("Baslangic.png")).subsample(2, 2)  # Resmi küçültme
resim_label = tk.Label(root, image=baslangic_resmi, bg="#98FB98")
resim_label.pack(pady=10)

# Bilgilendirici Yazı
bilgi_label = tk.Label(root, text="Başlat butonuna basınız, ve seçilen hastalığın semptomlarına cevap veriniz.", font=("Arial", 14), bg="#98FB98")
bilgi_label.pack(pady=10)

# Başla butonu oluşturma (güzel tasarımlı ve yeşil)
basla_butonu = tk.Button(root, text="Başlat", command=basla, font=("Arial", 16, "bold"), bg="green", fg="white", padx=20, pady=10)
basla_butonu.pack(pady=20)

# Tekrar Başla butonu oluşturma (daha büyük ve yeşil)
tekrar_basla_butonu = tk.Button(root, text="Tekrar Başla", command=tekrar_basla, font=("Arial", 16, "bold"), bg="green", fg="white", padx=20, pady=10)

# Sonuç etiketi
sonuc_label = tk.Label(root, text="", font=("Arial", 20, "bold"), bg="#ADD8E6", fg="black")
sonuc_label.pack(pady=20)

# Soru arka plan resmi ve metni Canvas üzerinde göstermek
soru_arka_plan_resmi = PhotoImage(file=resource_path("soru.png")).zoom(1, 1)  # Resmi büyütme
soru_canvas = Canvas(root, width=soru_arka_plan_resmi.width(), height=soru_arka_plan_resmi.height(), bg="#ADD8E6")
soru_canvas.create_image(0, 0, image=soru_arka_plan_resmi, anchor="nw")

# Soruyu resmin ortasında daha küçük ve biraz daha sağa kaydırarak yerleştirme
soru_text_item = soru_canvas.create_text(
    soru_arka_plan_resmi.width()//2 + 90, soru_arka_plan_resmi.height()//2, 
    text="", font=("Arial", 11), fill="black"
)

# Evet ve Hayır butonlarını resmin içine yerleştirme ve boyutlarını büyütme
evet_butonu = tk.Button(root, text="Evet", command=evet, bg="green", fg="white", padx=15, pady=10, font=("Arial", 12, "bold"))
evet_butonu_window = soru_canvas.create_window(
    200, soru_arka_plan_resmi.height() - 40, anchor="sw", window=evet_butonu
)

hayir_butonu = tk.Button(root, text="Hayır", command=hayir, bg="red", fg="white", padx=15, pady=10, font=("Arial", 12, "bold"))
hayir_butonu_window = soru_canvas.create_window(
    soru_arka_plan_resmi.width() - 20, soru_arka_plan_resmi.height() - 40, anchor="se", window=hayir_butonu
)

root.mainloop()
