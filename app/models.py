from dataclasses import dataclass, field
from typing import Optional
from flask_login import UserMixin
from .config import login_manager
from .services.supabase_service import get_user_by_id


@dataclass
class HeroSlide:
    id: int
    judul: str
    deskripsi: Optional[str]
    image_url: str
    link_url: Optional[str]
    urutan: int
    aktif: bool


@dataclass
class Berita:
    id: int
    judul: str
    slug: str
    konten: str
    kategori: Optional[str]
    thumbnail: Optional[str]
    status: str
    created_at: Optional[str]
    updated_at: Optional[str]


@dataclass
class Pengaduan:
    id: str
    nama_pelapor: str
    email: str
    nomor_hp: Optional[str]
    kategori: Optional[str]
    judul: str
    deskripsi: str
    lampiran_url: Optional[str]
    status: str
    tanggapan: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]


@dataclass
class Layanan:
    id: int
    nama: str
    deskripsi: Optional[str]
    kategori: Optional[str]
    icon: Optional[str]
    link_url: Optional[str]
    aktif: bool


@dataclass
class Bencana:
    id: int
    judul: str
    lokasi: str
    deskripsi: Optional[str]
    jenis: Optional[str]
    tanggal: Optional[str]
    kontak_darurat: Optional[str]
    aktif: bool


@dataclass
class Pariwisata:
    id: int
    nama: str
    lokasi: Optional[str]
    deskripsi: Optional[str]
    kategori: Optional[str]
    thumbnail: Optional[str]
    aktif: bool


@dataclass
class Pengumuman:
    id: int
    judul: str
    konten: str
    tanggal_mulai: Optional[str]
    tanggal_selesai: Optional[str]
    aktif: bool
    created_at: Optional[str]


class User(UserMixin):
    def __init__(self, user_id: str, email: str, nama: str = "", role: str = "admin"):
        self.id = user_id
        self.email = email
        self.nama = nama
        self.role = role

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


@login_manager.user_loader
def load_user(user_id):
    user_data = get_user_by_id(user_id)
    if user_data:
        return User(
            user_id=user_data.get("id", user_id),
            email=user_data.get("email", ""),
            nama=user_data.get("nama", "Admin"),
            role=user_data.get("role", "admin"),
        )
    return None
