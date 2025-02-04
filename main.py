import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import json

class FilmDiziUygulamasi:

    def __init__(self, root):
        self.root = root
        self.root.title("Film ve Dizi İzleme Takibi")
        self.root.geometry("800x600")
        self.root.minsize(800, 600)

        # Arka plan resmi yükleme
        self.arka_plan_resmi = Image.open("background.jpg")
        self.arka_plan_foto = None
        self.araba_arka_plan_label = tk.Label(self.root)
        self.araba_arka_plan_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.filmler_diziler = []
        self.siralama_ters = False

        # Başlık
        self.baslik_label = tk.Label(self.root, text="Film & Dizi Kayıt Uygulaması", bg="#0824c4", fg="#ecf0f1",
                                     font=("Helvetica", 16, "bold"), pady=10)
        self.baslik_label.pack(fill=tk.X)

        # Sağ üst köşeye 'Hakkında' butonunu ekleme
        self.hakkinda_buton = tk.Button(self.root, text="Hakkında", command=self.hakkinda_penceresini_ac, bg="#27ae60",
                                        fg="#ecf0f1", font=("Helvetica", 10))
        self.hakkinda_buton.place(relx=1.0, x=-10, y=10, anchor="ne")

        # Arayüz elemanlarını oluşturma
        self.arayuz_olustur()
        self.verileri_yukle()

        # Pencere yeniden boyutlandırıldığında arka planı güncelle
        self.root.bind("<Configure>", self.arka_plani_uygula)
        self.arka_plani_uygula(None)

        # Temizle butonu
        self.temizle_butonu = tk.Button(self.root, text="Temizle", command=self.filmler_diziler_temizle,
                                      bg="#2980b9", fg="white", font=("Helvetica", 10))
        self.temizle_butonu.place(relx=0.0, x=10, y=10, anchor="nw")

    def filmler_diziler_temizle(self):

        self.filmler_diziler.clear()  # Film/Dizi listesini temizle
        self.guncelle_liste()  # Arayüzdeki listeyi güncelle

        messagebox.showinfo("Temizle", "Başarıyla liste temizlendi.")

    def arka_plani_uygula(self, event):
        genislik = self.root.winfo_width()
        yukseklik = self.root.winfo_height()
        yeniden_boyutlanmis_resim = self.arka_plan_resmi.resize((genislik, yukseklik), Image.LANCZOS)
        self.arka_plan_foto = ImageTk.PhotoImage(yeniden_boyutlanmis_resim)
        self.araba_arka_plan_label.config(image=self.arka_plan_foto)

    def hakkinda_penceresini_ac(self):
        # Hakkında penceresini açma
        hakkinda_pencere = tk.Toplevel(self.root)
        hakkinda_pencere.title("Hakkında")
        hakkinda_pencere.geometry("550x550")  # Pencere boyutlarını belirleyin
        hakkinda_pencere.config(bg="white")

        # "Uygulama Yönergesi" başlığını ortalayarak ekleyelim
        uygulama_yonergesi_label = tk.Label(hakkinda_pencere, text="◄ Uygulama Yönergesi ►", font=("Helvetica", 12, "bold"),
                                            fg="black", bg="white")
        uygulama_yonergesi_label.place(relx=0.5, rely=0.1, anchor="center")

        # Text widget'ı ve kaydırma çubuğu ekleyelim
        text_frame = tk.Frame(hakkinda_pencere, bg="white")
        text_frame.place(relx=0.05, rely=0.2, relwidth=0.9, relheight=0.6)

        # Text widget'ı oluşturma
        hakkinda_metni = tk.Text(text_frame, wrap="word", font=("Helvetica", 10), fg="black", bg="white", bd=0, padx=5,
                                 pady=5, spacing1=5, spacing2=5,
                                 spacing3=5)  # Satır aralığını artırmak için spacing parametreleri eklendi
        hakkinda_metni.insert(tk.END,
                              "Bu uygulama seçilen film veya diziye ait özellikleri listeleyerek tabloya kayıt edilmesini sağlamaktadır.\n\n")
        hakkinda_metni.insert(tk.END,
                              "• Uygulamada film veya dizi bilgileri için 'Ad, Tür, Durum, Yıldız, Tema ve Açıklama' alanları bulunmaktadır.\n")
        hakkinda_metni.insert(tk.END,
                              "• Özellik bilgi kutucukları doldurulduktan sonra 'Ekle' butonuna basarak listeye ekleme yapabilirsiniz.\n")
        hakkinda_metni.insert(tk.END,
                              "• Tabloda seçilen verinin güncellenmesi veya silinmesi için film veya dizi adını listeden seçtikten sonra 'Güncelle' veya 'Sil' butonlarına tıklanmalıdır.\n")
        hakkinda_metni.insert(tk.END,
                              "• Tablodaki verilerin uygulama kapatıldığında kaydedilmesi isteniyorsa 'Kaydet' butonuna basılmalıdır.\n")
        hakkinda_metni.insert(tk.END,
                              "• Uygulamada istenen film veya dizinin aranabilmesi için 'Ad' arama kutucuğu ve 'Tür' liste seçim kutucuğu bulunmaktadır.\n")
        hakkinda_metni.insert(tk.END,
                              "• Tabloda yazılı olan film veya dizi kayıt bilgilerinin bulunması için ad veya tür bilgileri seçilerek 'Ara' butonu ile arama işlemleri gerçekleştirilebilir.\n")
        hakkinda_metni.insert(tk.END,
                              "• Arama ayarının temizlenmesi için 'Temizle' butonuna basılması gerekmektedir.\n")

        # Text widget'ını düzenle
        hakkinda_metni.config(state=tk.DISABLED)  # Metin düzenlenemez yapıldı

        # Kaydırma çubuğu ekleyelim
        scrollbar = tk.Scrollbar(text_frame, command=hakkinda_metni.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Kaydırma çubuğunun Text widget'ı ile bağlantısını sağla
        hakkinda_metni.config(yscrollcommand=scrollbar.set)
        hakkinda_metni.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Kaydırma çubuğunun uzunluğunu artırmak için
        hakkinda_metni.bind("<Configure>",
                            lambda e: hakkinda_metni.yview_moveto(0))  # Kaydırmayı üstten başlat

    def arayuz_olustur(self):
        # Arama çubuğu için bir çerçeve oluşturulur
        self.arama_frame = tk.Frame(self.root, bg="#0824c4", pady=10)
        self.arama_frame.pack(fill=tk.X, pady=10, padx=10)

        # "Arama" etiketi ve giriş kutusu eklenir
        self.arama_label = tk.Label(self.arama_frame, text="Arama:", bg="#0824c4", fg="#ecf0f1", font=("Helvetica", 10))
        self.arama_label.grid(row=0, column=0, padx=5, pady=5)
        self.arama_entry = tk.Entry(self.arama_frame, bg="#ecf0f1", fg="#2c3e50", font=("Helvetica", 10), width=30)
        self.arama_entry.grid(row=0, column=1, padx=5, pady=5)

        # Tür seçimi için bir etiket ve combobox eklenir
        self.tema_label = tk.Label(self.arama_frame, text="Tür:", bg="#0824c4", fg="#ecf0f1", font=("Helvetica", 10))
        self.tema_label.grid(row=0, column=2, padx=5, pady=5)
        self.arama_tur_combobox = ttk.Combobox(self.arama_frame, values=["Film", "Dizi", "Tüm Türler"],
                                               state="readonly")
        self.arama_tur_combobox.set("Tüm Türler")
        self.arama_tur_combobox.grid(row=0, column=3, padx=5, pady=5)

        # Arama ve Temizle butonları eklenir
        self.arama_butonu = tk.Button(self.arama_frame, text="Ara", command=self.filtrele, bg="#2980b9", fg="#ecf0f1",
                                      font=("Helvetica", 10))
        self.arama_butonu.grid(row=0, column=4, padx=5, pady=5)
        self.temizle_butonu = tk.Button(self.arama_frame, text="Temizle", command=self.temizle, bg="#c0392b",
                                        fg="#ecf0f1", font=("Helvetica", 10))
        self.temizle_butonu.grid(row=0, column=5, padx=5, pady=5)

        # Film/Dizi listesini göstermek için bir çerçeve oluşturulur
        self.liste_frame = tk.Frame(self.root, bg="#2c3e50")
        self.liste_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Listeye kaydırma çubuğu eklenir
        self.scrollbar = tk.Scrollbar(self.liste_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Liste oluşturulur ve başlıkları tanımlanır
        self.tree = ttk.Treeview(self.liste_frame, columns=("ad", "tur", "durum", "yildiz", "tema", "aciklama"),
                                 show="headings", yscrollcommand=self.scrollbar.set)
        self.tree.heading("ad", text="Ad", command=lambda: self.sirala("ad"))
        self.tree.heading("tur", text="Tür", command=lambda: self.sirala("tur"))
        self.tree.heading("durum", text="Durum", command=lambda: self.sirala("durum"))
        self.tree.heading("yildiz", text="Yıldız")
        self.tree.heading("tema", text="Tema")
        self.tree.heading("aciklama", text="Açıklama")

        # Sütun genişlikleri ayarlanır
        self.tree.column("ad", width=150, anchor="w")
        self.tree.column("tur", width=100, anchor="w")
        self.tree.column("durum", width=100, anchor="w")
        self.tree.column("yildiz", width=100, anchor="w")
        self.tree.column("tema", width=100, anchor="w")
        self.tree.column("aciklama", width=200, anchor="w")

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.tree.yview)

        # Sil, Güncelle, Ekle ve Kaydet butonları için bir çerçeve oluşturulur
        self.button_frame = tk.Frame(self.root, bg="#6c0b56", pady=5)
        self.button_frame.pack(pady=10, padx=10, fill=tk.X)

        # İşlem butonları eklenir
        self.sil_butonu = tk.Button(self.button_frame, text="Sil", command=self.sil, bg="#e74c3c", fg="#ecf0f1",
                                    font=("Helvetica", 10))
        self.sil_butonu.pack(side=tk.LEFT, padx=10, pady=5)
        self.guncelle_butonu = tk.Button(self.button_frame, text="Güncelle", command=self.guncelle, bg="#27ae60",
                                         fg="#ecf0f1", font=("Helvetica", 10))
        self.guncelle_butonu.pack(side=tk.LEFT, padx=10, pady=5)
        self.ekle_butonu = tk.Button(self.button_frame, text="Ekle", command=self.ekle, bg="#27ae60", fg="#ecf0f1",
                                     font=("Helvetica", 10))
        self.ekle_butonu.pack(side=tk.LEFT, padx=10, pady=5)
        self.kaydet_butonu = tk.Button(self.button_frame, text="Kaydet", command=self.verileri_kaydet, bg="#f39c12",
                                       fg="#ecf0f1", font=("Helvetica", 10))
        self.kaydet_butonu.pack(side=tk.LEFT, padx=10, pady=5)

        # İncele butonunu ekleyelim
        self.incele_butonu = tk.Button(self.button_frame, text="İncele", command=self.incele, bg="#2980b9",
                                       fg="#ecf0f1",
                                       font=("Helvetica", 10))
        self.incele_butonu.pack(side=tk.LEFT, padx=10, pady=5)

        # Form alanları için bir çerçeve oluşturulur
        self.form_frame = tk.Frame(self.root, bg="#bb0939")
        self.form_frame.pack(pady=10, padx=10, fill=tk.X)

        # Form alanları (Ad, Tür, Durum vb.) etiket ve giriş kutuları eklenir
        self.ad_label = tk.Label(self.form_frame, text="Ad:", bg="#bb0939", fg="#ecf0f1", font=("Helvetica", 10))
        self.ad_label.grid(row=0, column=0, padx=5, pady=5)
        self.ad_entry = tk.Entry(self.form_frame, bg="#ecf0f1", fg="#2c3e50", font=("Helvetica", 10))
        self.ad_entry.grid(row=0, column=1, padx=5, pady=5)

        self.tur_label = tk.Label(self.form_frame, text="Tür:", bg="#bb0939", fg="#ecf0f1", font=("Helvetica", 10))
        self.tur_label.grid(row=0, column=2, padx=5, pady=5)
        self.tur_combobox = ttk.Combobox(self.form_frame, values=["Film", "Dizi"], state="readonly")
        self.tur_combobox.grid(row=0, column=3, padx=5, pady=5)

        self.durum_label = tk.Label(self.form_frame, text="Durum:", bg="#bb0939", fg="#ecf0f1", font=("Helvetica", 10))
        self.durum_label.grid(row=1, column=0, padx=5, pady=5)
        self.durum_combobox = ttk.Combobox(self.form_frame, values=["İzlendi", "İzlenecek", "Bekleniyor"],
                                           state="readonly")
        self.durum_combobox.grid(row=1, column=1, padx=5, pady=5)

        self.yildiz_label = tk.Label(self.form_frame, text="Yıldız Derecesi:", bg="#bb0939", fg="#ecf0f1",
                                     font=("Helvetica", 10))
        self.yildiz_label.grid(row=1, column=2, padx=5, pady=5)
        self.yildiz_entry = tk.Entry(self.form_frame, bg="#ecf0f1", fg="#2c3e50", font=("Helvetica", 10))
        self.yildiz_entry.grid(row=1, column=3, padx=5, pady=5)

        self.tema_label = tk.Label(self.form_frame, text="Tema:", bg="#bb0939", fg="#ecf0f1", font=("Helvetica", 10))
        self.tema_label.grid(row=2, column=0, padx=5, pady=5)
        self.tema_combobox = ttk.Combobox(self.form_frame,
                                          values=["Romantik", "Macera", "Korku", "Komedi", "Dram", "Aksiyon"],
                                          state="readonly")
        self.tema_combobox.grid(row=2, column=1, padx=5, pady=5)

        self.aciklama_label = tk.Label(self.form_frame, text="Açıklama:", bg="#bb0939", fg="#ecf0f1",
                                       font=("Helvetica", 10))
        self.aciklama_label.grid(row=2, column=2, padx=5, pady=5)
        self.aciklama_entry = tk.Entry(self.form_frame, bg="#ecf0f1", fg="#2c3e50", font=("Helvetica", 10))
        self.aciklama_entry.grid(row=2, column=3, padx=5, pady=5)

    def sil(self):
        # Kullanıcının seçtiği öğeyi al
        secilen_item = self.tree.selection()

        # Eğer hiçbir öğe seçilmediyse, kullanıcıya uyarı göster
        if not secilen_item:
            messagebox.showwarning("Uyarı", "Lütfen silmek için bir öğe seçin!")
            return

        # Silme işlemi için onay kutusu göster
        sonuc = messagebox.askyesno("Onay", "Seçili öğeyi silmek istediğinizden emin misiniz?")

        if sonuc:  # Kullanıcı "Evet"e tıkladıysa
            # Seçilen öğenin indeksini al ve listeden sil
            secilen_indeks = self.tree.index(secilen_item)
            del self.filmler_diziler[secilen_indeks]

            # Listeyi güncelle
            self.guncelle_liste()
            messagebox.showinfo("Bilgi", "Seçili öğe başarıyla silindi.")
        else:  # Kullanıcı "Hayır"a tıkladıysa
            messagebox.showinfo("Bilgi", "Silme işlemi iptal edildi.")

    def ekle(self):
        # Kullanıcının girdiği verileri al
        ad = self.ad_entry.get()
        tur = self.tur_combobox.get()
        durum = self.durum_combobox.get()
        yildiz = self.yildiz_entry.get()
        tema = self.tema_combobox.get()
        aciklama = self.aciklama_entry.get()

        # Zorunlu alanların doldurulup doldurulmadığını kontrol et
        if not ad or not tur or not durum or not yildiz or not tema:
            messagebox.showwarning("Uyarı", "Lütfen tüm alanları doldurun!")
            return

        # Yıldız değerlendirmesini kontrol et
        try:
            yildiz = int(yildiz)
            if yildiz < 1 or yildiz > 5:
                messagebox.showwarning("Uyarı", "Lütfen 1-5 aralığında yıldız değerlendirmesi yapınız!")
                return
        except ValueError:
            messagebox.showwarning("Uyarı", "Yıldız alanına sadece sayı girilebilir!")
            return

        # Açıklama alanı boş bırakıldıysa varsayılan bir değer ata
        if not aciklama:
            aciklama = "Açıklama yok"

        # Yeni bir film veya dizi nesnesi oluştur ve listeye ekle
        yeni_film_dizi = {
            "ad": ad,
            "tur": tur,
            "durum": durum,
            "yildiz": yildiz,
            "tema": tema,
            "aciklama": aciklama
        }
        self.filmler_diziler.append(yeni_film_dizi)

        # Listeyi güncelle
        self.guncelle_liste()
        messagebox.showinfo("Bilgi", "Listeye başarıyla eklendi.")

        self.guncelle_liste()

    def guncelle(self):
        # Kullanıcının seçtiği öğeyi al
        secilen_item = self.tree.selection()

        # Eğer hiçbir öğe seçilmediyse, kullanıcıya uyarı göster
        if not secilen_item:
            messagebox.showwarning("Uyarı", "Lütfen bir öğe seçin!")
            return

        # Seçilen öğenin indeksini al
        secilen_indeks = self.tree.index(secilen_item)

        # Kullanıcının girdiği yeni verileri al
        ad = self.ad_entry.get()
        tur = self.tur_combobox.get()
        durum = self.durum_combobox.get()
        yildiz = self.yildiz_entry.get()
        tema = self.tema_combobox.get()
        aciklama = self.aciklama_entry.get()

        # Zorunlu alanların doldurulup doldurulmadığını kontrol et
        if not ad or not tur or not durum or not yildiz or not tema:
            messagebox.showwarning("Uyarı", "Lütfen tüm alanları doldurun!")
            return

        # Yıldız değerlendirmesini kontrol et
        try:
            yildiz = int(yildiz)
            if yildiz < 1 or yildiz > 5:
                messagebox.showwarning("Uyarı", "Lütfen 1-5 aralığında yıldız değerlendirmesi yapınız!")
                return
        except ValueError:
            messagebox.showwarning("Uyarı", "Yıldız alanına sadece sayı girilebilir!")
            return

        # Açıklama alanı boş bırakıldıysa varsayılan bir değer ata
        if not aciklama:
            aciklama = "Açıklama yok"

        # Seçilen öğeyi güncelle
        self.filmler_diziler[secilen_indeks] = {
            "ad": ad,
            "tur": tur,
            "durum": durum,
            "yildiz": yildiz,
            "tema": tema,
            "aciklama": aciklama
        }

        # Listeyi güncelle
        self.guncelle_liste()

    def guncelle_liste(self):
        # Treeview'daki mevcut tüm öğeleri sil
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Güncellenmiş listeyi Treeview'e ekle
        for film_dizi in self.filmler_diziler:
            self.tree.insert("", "end", values=(film_dizi["ad"], film_dizi["tur"], film_dizi["durum"],
                                                film_dizi["yildiz"], film_dizi["tema"], film_dizi["aciklama"]))

    def filtrele(self):
        # Arama terimini ve tür filtresini al
        arama_terimi = self.arama_entry.get().lower()
        tur_filter = self.arama_tur_combobox.get()

        # Tür filtresine ve arama terimine göre listeyi filtrele
        if tur_filter == "Tüm Türler":
            filtrelenmis = [item for item in self.filmler_diziler if arama_terimi in item["ad"].lower()]
        else:
            filtrelenmis = [item for item in self.filmler_diziler if
                            arama_terimi in item["ad"].lower() and item["tur"] == tur_filter]

        # Treeview'daki mevcut öğeleri temizle
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Filtrelenmiş öğeleri Treeview'e ekle
        for film_dizi in filtrelenmis:
            self.tree.insert("", "end", values=(film_dizi["ad"], film_dizi["tur"], film_dizi["durum"],
                                                film_dizi["yildiz"], film_dizi["tema"], film_dizi["aciklama"]))

    def temizle(self):
        # Arama alanını temizle ve tür filtresini varsayılan değere ayarla
        self.arama_entry.delete(0, tk.END)
        self.arama_tur_combobox.set("Tüm Türler")

        # Listeyi güncelle
        self.guncelle_liste()

    def verileri_kaydet(self):
        try:
            with open("filmler_diziler.json", "w", encoding="utf-8") as file:
                json.dump(self.filmler_diziler, file, indent=4, ensure_ascii=False)
            messagebox.showinfo("Bilgi", "Veriler başarıyla kaydedildi!")
        except Exception as e:
            messagebox.showerror("Hata", f"Veriler kaydedilemedi: {str(e)}")

    def verileri_yukle(self):
        # JSON dosyasından verileri yükle
        try:
            with open("filmler_diziler.json", "r", encoding="utf-8") as file:
                self.filmler_diziler = json.load(file)
            # Listeyi güncelle
            self.guncelle_liste()
        except FileNotFoundError:
            # Dosya bulunamazsa boş bir liste oluştur
            self.filmler_diziler = []

    def sirala(self, kolon):
        # Seçilen sütuna göre listeyi sırala
        self.siralama_ters = not self.siralama_ters
        self.filmler_diziler.sort(key=lambda x: x[kolon], reverse=self.siralama_ters)

        # Listeyi güncelle
        self.guncelle_liste()

    def incele(self):
        # Film ve dizi verilerini sayalım
        film_sayisi = len([item for item in self.filmler_diziler if item["tur"] == "Film"])
        dizi_sayisi = len([item for item in self.filmler_diziler if item["tur"] == "Dizi"])

        # Tüm verilerin sayısı
        toplam_sayi = len(self.filmler_diziler)

        # İncele penceresini açma
        incele_pencere = tk.Toplevel(self.root)
        incele_pencere.title("Veriler")
        incele_pencere.geometry("300x200")
        incele_pencere.config(bg="white")

        # Başlık
        incele_baslik_label = tk.Label(incele_pencere, text="Analiz", font=("Helvetica", 12, "bold"),
                                       bg="white")
        incele_baslik_label.pack(pady=10)

        # Veri sayıları metni
        veri_sayilari_label = tk.Label(incele_pencere,
                                       text=f"Toplam Veri Sayısı: {toplam_sayi}\nFilm Sayısı: {film_sayisi}\nDizi Sayısı: {dizi_sayisi}",
                                       font=("Helvetica", 10), bg="white")
        veri_sayilari_label.pack(pady=20)


if __name__ == "__main__":
    root = tk.Tk()
    app = FilmDiziUygulamasi(root)
    root.mainloop()
