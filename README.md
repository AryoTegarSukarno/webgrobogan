# WebGrobogan 🏛️

Portal informasi resmi **Kabupaten Grobogan**, Jawa Tengah. Dibuat sebagai Tugas Besar (Tubes) mata kuliah **Aplikasi Berbasis Platform**.

## 📄 Halaman

| Halaman | Deskripsi |
|---------|-----------|
| `index.html` | Beranda – hero, profil kabupaten, wisata unggulan, kuliner, budaya, berita, layanan publik |
| `wisata.html` | Daftar destinasi wisata lengkap beserta tips berwisata |
| `budaya.html` | Seni pertunjukan, tradisi adat, dan kerajinan tangan |
| `kuliner.html` | Makanan utama, jajanan pasar, dan lokasi kuliner populer |
| `kontak.html` | Formulir kontak, informasi kantor, peta lokasi, dan FAQ |

## 🗂️ Struktur Proyek

```
webgrobogan/
├── index.html
├── wisata.html
├── budaya.html
├── kuliner.html
├── kontak.html
└── assets/
    ├── css/
    │   └── style.css      # Stylesheet utama (responsive)
    └── js/
        └── main.js        # JavaScript interaktivitas
```

## 🚀 Cara Menjalankan

Cukup buka file `index.html` di browser, atau gunakan server lokal:

```bash
# Python
python -m http.server 8080

# Node.js (npx)
npx serve .
```

Lalu buka `http://localhost:8080` di browser.

## ✨ Fitur

- **Desain responsif** – tampil optimal di desktop, tablet, dan mobile
- **Navbar adaptif** – transparan di hero, solid saat scroll
- **Animasi scroll reveal** – elemen muncul saat masuk viewport
- **Formulir kontak** – validasi client-side dengan feedback sukses
- **Back-to-top** – tombol kembali ke atas yang muncul saat scroll

## 🛠️ Teknologi

- HTML5, CSS3 (Custom Properties, Flexbox, Grid)
- Vanilla JavaScript (ES6+)
- [Font Awesome 6](https://fontawesome.com/) – ikon

## 👥 Tim Pengembang

Tugas Besar Aplikasi Berbasis Platform – Universitas / Politeknik.
