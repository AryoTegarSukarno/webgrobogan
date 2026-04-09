# Portal Informasi & Layanan Pemerintah Kabupaten Grobogan

Portal resmi Pemerintah Kabupaten Grobogan — berbasis Flask dengan integrasi Supabase.

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11+, Flask 3.0 |
| Frontend | Jinja2, Tailwind CSS v3 (CDN), Alpine.js v3, Lucide Icons |
| Database/Auth | Supabase (PostgreSQL + GoTrue Auth) |
| Deployment | Gunicorn (WSGI) |

## Setup

### 1. Clone & install dependencies

```bash
git clone <repo-url>
cd webgrobogan
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env with your Supabase credentials
```

### 3. Environment variables

| Variable | Description |
|---|---|
| `FLASK_SECRET_KEY` | Secret key for sessions & CSRF |
| `SUPABASE_URL` | Your Supabase project URL |
| `SUPABASE_ANON_KEY` | Supabase anon/public key |
| `SUPABASE_SERVICE_KEY` | Supabase service role key (admin operations) |
| `FLASK_ENV` | `development` or `production` |

### 4. Supabase Tables Required

Create the following tables in your Supabase project:

- `hero_slides` (id, judul, deskripsi, image_url, link_url, urutan, aktif)
- `berita` (id, judul, slug, konten, kategori, thumbnail, status, created_at)
- `layanan` (id, nama, deskripsi, kategori, icon, link_url, aktif)
- `pengumuman` (id, judul, konten, tanggal_mulai, tanggal_selesai, aktif, created_at)
- `bencana` (id, judul, lokasi, deskripsi, jenis, tanggal, kontak_darurat, aktif)
- `pariwisata` (id, nama, lokasi, deskripsi, kategori, thumbnail, aktif)
- `pengaduan` (id uuid, nama_pelapor, email, nomor_hp, kategori, judul, deskripsi, lampiran_url, status, tanggapan, created_at, updated_at)

## Running the App

### Development

```bash
python run.py
```

App runs at `http://localhost:5000`

### Production (Gunicorn)

```bash
gunicorn wsgi:app --workers 4 --bind 0.0.0.0:8000
```

## Project Structure

```
webgrobogan/
├── app/
│   ├── __init__.py          # App factory
│   ├── config.py            # Configuration & Supabase client
│   ├── models.py            # Data models & Flask-Login User
│   ├── routes/
│   │   ├── public.py        # Public-facing routes
│   │   ├── admin.py         # Admin panel routes
│   │   └── api.py           # REST API routes
│   ├── services/
│   │   ├── supabase_service.py  # All DB operations
│   │   └── forms.py         # Flask-WTF forms
│   ├── templates/           # Jinja2 templates
│   └── static/              # CSS, JS, images
├── run.py                   # Dev server entry point
├── wsgi.py                  # Production WSGI entry point
└── requirements.txt
```

## Admin Panel

Access at `/admin/login`. Requires a Supabase Auth user.

The app degrades gracefully — all pages render with empty/default content when Supabase is not configured.