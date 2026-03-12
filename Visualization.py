# === PASTE KODE INI DI CELL BARU (Cell 2) ===
import networkx as nx
import matplotlib.pyplot as plt

# 1. Mendefinisikan posisi koordinat agar bentuknya menyerupai peta Australia
pos = {
    'western australia': (0, 1),           # Kiri
    'northwest territories': (1, 2),       # Atas Tengah
    'southern australia': (1.2, 0.5),      # Bawah Tengah
    'queensland': (2.5, 1.5),              # Kanan Atas
    'new south wales': (2.4, 0.2),         # Kanan Tengah
    'victoria': (2.0, -0.8),               # Kanan Bawah
    'tasmania': (2.2, -2.0)                # Pulau terpisah di bawah
}

# Variabel global untuk menyimpan riwayat (history) setiap tebakan warna
riwayat_langkah = []

# 2. Fungsi modifikasi untuk merekam langkah tanpa mengubah fungsi asli di Cell 1
# Fungsi ini bekerja sama seperti solve(), tapi menyimpan state 'tebakan' setiap kali berubah
def solve_dengan_rekaman(graph, warna_tersedia, tebakan, depth):
    n = find_best_candidate(graph, tebakan)
    if n is None:
        return tebakan

    warna_tetangga = {tebakan[neigh] for neigh in graph[n] if neigh in tebakan}
    warna_valid = set(warna_tersedia).difference(warna_tetangga)

    for c in warna_valid:
        if n not in tebakan:
            # Coba berikan warna
            tebakan[n] = c
            # Rekam state ke dalam list (menggunakan .copy() agar tidak tertimpa)
            riwayat_langkah.append((tebakan.copy(), f"Isi {n} dengan {c}"))

            # Lanjut ke node berikutnya
            if solve_dengan_rekaman(graph, warna_tersedia, tebakan, depth + 1):
                return tebakan
            else:
                # Backtrack: hapus tebakan karena buntu
                del tebakan[n]
                # Rekam state saat backtrack dilakukan
                riwayat_langkah.append((tebakan.copy(), f"Backtrack: Hapus {n}"))

    return None

# 3. Jalankan algoritma rekaman
print("Mempersiapkan visualisasi step-by-step...")
riwayat_langkah.append((dict(), "State Awal (Kosong)")) # Rekam grid kosong di awal
solusi_akhir = solve_dengan_rekaman(australia, colors, dict(), 0)

if solusi_akhir:
    # 4. Inisialisasi Graph
    G = nx.Graph(australia)

    # 5. Loop untuk menggambar Graph di setiap langkah sebagai gambar TERPISAH
    for i, (state, deskripsi) in enumerate(riwayat_langkah):

        # Membuat figure baru untuk setiap satu gambar
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.set_title(f"Step {i}: {deskripsi}", fontsize=14, fontweight='bold', pad=15)

        # Tentukan warna node pada langkah ke-i, default abu-abu terang jika belum diwarnai
        warna_node = [state.get(node, 'lightgray') for node in G.nodes()]

        # Menggambar graph ke axis (ax) yang spesifik
        nx.draw(
            G, pos,
            ax=ax,
            with_labels=True,
            node_color=warna_node,
            node_size=4000,
            font_size=9,
            font_weight='bold',
            font_color='black',
            edgecolors='black',
            linewidths=2,
            edge_color='darkgray',
            width=2
        )

        # Menampilkan gambar tunggal ini
        plt.show()

        # MENGHAPUS/MENUTUP figure agar benar-benar terpisah dan tidak bertumpuk di memori
        plt.close(fig)

else:
    print("Tidak ada solusi yang ditemukan untuk divisualisasikan.")
