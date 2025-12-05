# main.py
import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime


# KELAS UTAMA APLIKASI
class AppOlahraga:
    # Konstruktor (method yang dipanggil saat objek dibuat)
    def __init__(self):                                    
        # Membuat jendela utama Tkinter
        self.root = tk.Tk()
        self.root.title("Aplikasi Pencatat Aktivitas Olahraga Harian")
        self.root.geometry("900x700")
        self.root.configure(bg="#2c3e50")                   # warna latar belakang gelap

        # Data utama aplikasi
        self.target = 600                                   # target kalori per hari ini (kcal)
        self.log = []                                       # list yang menyimpan semua aktivitas hari ini
        self.daftar = {                                     # dictionary kalori per menit tiap olahraga
            "Lari": 10, "Jalan": 5, "Push-up": 8, "Sit-up": 8,
            "Sepeda": 8, "Renang": 13, "Lompat Tali": 12, "Yoga": 4
        }

        # Memanggil method untuk membuat tampilan dan memuat data lama
        self.gui()                                          # untuk semua widget
        self.load()                                         # baca data.json kalau ada
        self.root.mainloop()                                # untuk memulai loop utama Tkinter


    # METHOD UNTUK MEMBUAT TAMPILAN (GUI)
    def gui(self):
        # Judul besar
        tk.Label(self.root, text="PENCATAT OLAHRAGA", font=("Arial", 30, "bold"),
                 bg="#2c3e50", fg="#e74c3c").pack(pady=20)

        # Label target harian
        tk.Label(self.root, text=f"Target Harian: {self.target} kcal", font=("Arial", 16),
                 bg="#2c3e50", fg="#f39c12").pack(pady=(0,10))

        # Progress bar (memakai style custom agar tebal dan hijau)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TProgressbar", thickness=30, background="#27ae60")

        self.pb = ttk.Progressbar(self.root, length=600, mode="determinate", style="TProgressbar")
        self.pb.pack(pady=10)

        # Label yang menampilkan kalori saat ini
        self.lbl = tk.Label(self.root, text="0 / 600 kcal", font=("Arial", 24, "bold"),
                            bg="#2c3e50", fg="white")
        self.lbl.pack(pady=10)

        # Tombol reset hari ini
        tk.Button(self.root, text="RESET HARI INI", font=("Arial", 14, "bold"),
                  bg="#c0392b", fg="white", width=20, height=3,
                  command=self.reset_hari_ini).pack(pady=15)

        # Frame untuk input olahraga
        frame = tk.Frame(self.root, bg="#34495e", relief="ridge", bd=10)
        frame.pack(pady=20, padx=100, fill="x")

        # Label + Combobox pilihan olahraga
        tk.Label(frame, text="Olahraga:", bg="#34495e", fg="white", font=("Arial",14)) \
            .grid(row=0, column=0, pady=15, padx=10, sticky="w")

        self.cb = ttk.Combobox(frame, values=list(self.daftar.keys()), state="readonly",
                               font=("Arial",14), width=15)
        self.cb.set("Lari")                                 # nilai default
        self.cb.grid(row=0, column=1, pady=15, padx=20)

        # Label + Entry durasi
        tk.Label(frame, text="Durasi (menit):", bg="#34495e", fg="white", font=("Arial",14)) \
            .grid(row=1, column=0, pady=15, padx=10, sticky="w")

        self.entry = tk.Entry(frame, font=("Arial",14), width=10, justify="center")
        self.entry.grid(row=1, column=1, pady=15, padx=20)
        self.entry.focus()                                   # langsung fokus ke entry saat buka

        # Tombol TAMBAH
        tk.Button(frame, text="TAMBAH", font=("Arial",16,"bold"), bg="#e74c3c", fg="white",
                  width=15, height=2, command=self.tambah) \
            .grid(row=2, column=0, columnspan=2, pady=20)

        # Listbox untuk menampilkan semua aktivitas hari ini
        self.listbox = tk.Listbox(self.root, font=("Courier", 12), height=12,
                              bg="#2c3e50", fg="#ecf0f1",
                              selectbackground="#3498db", relief="sunken", bd=5)
        self.listbox.pack(pady=20, padx=100, fill="both", expand=True)


    # METHOD KETIKA TOMBOL "TAMBAH" DIKLIK
    def tambah(self):
        try:
            durasi = int(self.entry.get().strip())
            if durasi <= 0:
                raise ValueError

            jenis = self.cb.get()                                   # ambil olahraga yang dipilih
            kcal = durasi * self.daftar[jenis]                        # hitung kalori
            waktu = datetime.now().strftime("%H:%M")                  # jam:menit sekarang

            # Simpan ke log (list of dict)
            self.log.append({"waktu": waktu, "jenis": jenis, "durasi": durasi, "kcal": kcal})

            # Update progress bar & label
            total = sum(item["kcal"] for item in self.log)
            self.pb["value"] = total
            self.lbl.config(text=f"{total} / {self.target} kcal")

            # Refresh listbox & simpan ke file
            self.update_list()
            self.save()

            # Kosongkan entry & beri selamat kalau target tercapai
            self.entry.delete(0, tk.END)
            if total >= self.target:
                messagebox.showinfo("Selamat!", "Target harian tercapai!")

        except:
            messagebox.showerror("Error", "Masukkan angka positif yang valid!")


    # METHOD UNTUK MENGUPDATE LISTBOX
    def update_list(self):
        self.listbox.delete(0, tk.END)
        if not self.log:
            self.listbox.insert(tk.END, " Belum ada aktivitas hari ini...")
            return

        total = 0
        for item in self.log:
            total += item["kcal"]
            self.listbox.insert(tk.END,
                f"{item['waktu']} | {item['jenis']:12} | {item['durasi']:3} menit → {item['kcal']:4} kcal")
        self.listbox.insert(tk.END, "")
        self.listbox.insert(tk.END, f" TOTAL: {total} kcal")


    # METHOD RESET HARI INI
    def reset_hari_ini(self):
        if messagebox.askyesno("Reset Hari Ini", "Yakin hapus semua data hari ini?"):
            self.log.clear()                                      # hapus semua data
            self.pb["value"] = 0
            self.lbl.config(text="0 / 600 kcal")
            self.update_list()
            self.save()
            messagebox.showinfo("Sukses", "Data hari ini sudah direset!")



    # METHOD MENYIMPAN DATA KE FILE JSON
    def save(self):
        try:
            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(self.log, f, indent=2)
        except Exception as e:
            print("Gagal menyimpan:", e)   # kalau ada error tidak mengganggu user



    # METHOD MEMBACA DATA DARI FILE JSON SAAT APLIKASI DIBUKA
    def load(self):
        try:
            with open("data.json", encoding="utf-8") as f:
                self.log = json.load(f)

            total = sum(item["kcal"] for item in self.log)
            self.pb["value"] = total
            self.lbl.config(text=f"{total} / {self.target} kcal")
            self.update_list()
        except:
            self.update_list()   # kalau file tidak ada / rusak, tetap tampilkan list kosong

# MENJALANKAN APLIKASI
if __name__ == "__main__":        
    AppOlahraga()                   