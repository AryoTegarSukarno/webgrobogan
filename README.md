# webgrobogan

Portal web resmi **Kabupaten Grobogan** – informasi daerah, layanan publik, dan pariwisata.

## ✨ Fitur

- **Desain Modern & Responsif** – tampil sempurna di desktop, tablet, maupun ponsel
- **Palet Warna Profesional** – biru, oranye/amber, abu-abu, dan putih (tanpa hijau)
- **Font Inter** – sans-serif yang bersih dan nyaman dibaca
- **Aksesibel** – markup semantik, ARIA labels, dan fokus yang jelas
- **Navigasi Hamburger** – menu mobile yang halus dan animatif
- **Smooth Scroll** – navigasi antar-seksi yang mulus

## 📁 Struktur Proyek

```
webgrobogan/
├── index.html   # Struktur HTML semantik
├── style.css    # Stylesheet (variabel CSS, responsif)
└── README.md    # Dokumentasi ini
```

## 🖼️ Seksi Halaman

| Seksi | Deskripsi |
|---|---|
| Header / Nav | Logo, tautan navigasi, tombol CTA amber; hamburger menu untuk mobile |
| Hero | Judul besar, sub-teks, statistik daerah, tombol aksi |
| Tentang | Tiga kartu ikon: Pertanian, Kekayaan Alam, Budaya |
| Layanan | Empat kartu layanan publik (administrasi, kesehatan, pendidikan, perizinan) |
| Wisata | Tiga kartu destinasi: Bledug Kuwu, Kedung Ombo, Goa Lawa |
| Berita | Tiga kartu berita terkini dengan tanggal dan tag kategori |
| CTA Banner | Ajakan hubungi kami dengan warna latar biru gelap |
| Kontak | Info kontak + formulir kirim pesan |
| Footer | Brand, tautan cepat, layanan, kontak darurat, hak cipta |

## 🎨 Palet Warna

| Peran | Token | Nilai |
|---|---|---|
| Primer | `--blue-700` | `#1d4ed8` |
| Primer gelap | `--blue-800` | `#1e3a8a` |
| Aksen | `--amber-500` | `#f59e0b` |
| Teks utama | `--gray-800` | `#1f2937` |
| Teks ringan | `--gray-600` | `#4b5563` |
| Latar utama | white | `#ffffff` |
| Latar alt | `--gray-50` | `#f9fafb` |

## 🚀 Cara Menjalankan

Buka `index.html` langsung di browser – tidak ada build step yang diperlukan.

```bash
# Atau gunakan server lokal sederhana:
npx serve .
# kemudian buka http://localhost:3000
```