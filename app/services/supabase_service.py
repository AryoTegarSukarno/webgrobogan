"""Supabase data-access service.

All functions return safe defaults (empty lists / None) when Supabase is not
configured or when a network/API error occurs so the app still renders.
"""
from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional

from ..config import get_supabase_client, get_supabase_service_client


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _client():
    return get_supabase_client()


def _service():
    return get_supabase_service_client()


# ---------------------------------------------------------------------------
# Public – Hero Slides
# ---------------------------------------------------------------------------

def get_hero_slides() -> List[Dict]:
    try:
        sb = _client()
        if not sb:
            return []
        res = (
            sb.table("hero_slides")
            .select("*")
            .eq("aktif", True)
            .order("urutan")
            .execute()
        )
        return res.data or []
    except Exception:
        return []


# ---------------------------------------------------------------------------
# Public – Berita
# ---------------------------------------------------------------------------

def get_berita_list(limit: int = 10, offset: int = 0, kategori: Optional[str] = None) -> List[Dict]:
    try:
        sb = _client()
        if not sb:
            return []
        q = (
            sb.table("berita")
            .select("*")
            .eq("status", "published")
            .order("created_at", desc=True)
            .range(offset, offset + limit - 1)
        )
        if kategori:
            q = q.eq("kategori", kategori)
        res = q.execute()
        return res.data or []
    except Exception:
        return []


def get_berita_by_slug(slug: str) -> Optional[Dict]:
    try:
        sb = _client()
        if not sb:
            return None
        res = sb.table("berita").select("*").eq("slug", slug).single().execute()
        return res.data
    except Exception:
        return None


def get_berita_count(kategori: Optional[str] = None) -> int:
    try:
        sb = _client()
        if not sb:
            return 0
        q = sb.table("berita").select("id", count="exact").eq("status", "published")
        if kategori:
            q = q.eq("kategori", kategori)
        res = q.execute()
        return res.count or 0
    except Exception:
        return 0


# ---------------------------------------------------------------------------
# Public – Layanan
# ---------------------------------------------------------------------------

def get_layanan_list(kategori: Optional[str] = None) -> List[Dict]:
    try:
        sb = _client()
        if not sb:
            return []
        q = sb.table("layanan").select("*").eq("aktif", True).order("nama")
        if kategori:
            q = q.eq("kategori", kategori)
        res = q.execute()
        return res.data or []
    except Exception:
        return []


# ---------------------------------------------------------------------------
# Public – Pengumuman
# ---------------------------------------------------------------------------

def get_pengumuman_list(limit: int = 5) -> List[Dict]:
    try:
        sb = _client()
        if not sb:
            return []
        res = (
            sb.table("pengumuman")
            .select("*")
            .eq("aktif", True)
            .order("created_at", desc=True)
            .limit(limit)
            .execute()
        )
        return res.data or []
    except Exception:
        return []


# ---------------------------------------------------------------------------
# Public – Bencana
# ---------------------------------------------------------------------------

def get_bencana_list() -> List[Dict]:
    try:
        sb = _client()
        if not sb:
            return []
        res = (
            sb.table("bencana")
            .select("*")
            .eq("aktif", True)
            .order("tanggal", desc=True)
            .execute()
        )
        return res.data or []
    except Exception:
        return []


# ---------------------------------------------------------------------------
# Public – Pariwisata
# ---------------------------------------------------------------------------

def get_pariwisata_list(kategori: Optional[str] = None) -> List[Dict]:
    try:
        sb = _client()
        if not sb:
            return []
        q = sb.table("pariwisata").select("*").eq("aktif", True).order("nama")
        if kategori:
            q = q.eq("kategori", kategori)
        res = q.execute()
        return res.data or []
    except Exception:
        return []


# ---------------------------------------------------------------------------
# Public – Pengaduan
# ---------------------------------------------------------------------------

def create_pengaduan(data: Dict) -> Optional[Dict]:
    try:
        sb = _client()
        if not sb:
            return None
        data["id"] = str(uuid.uuid4())
        data.setdefault("status", "masuk")
        res = sb.table("pengaduan").insert(data).execute()
        return res.data[0] if res.data else None
    except Exception:
        return None


def get_pengaduan_by_id(pengaduan_id: str) -> Optional[Dict]:
    try:
        sb = _client()
        if not sb:
            return None
        res = sb.table("pengaduan").select("*").eq("id", pengaduan_id).single().execute()
        return res.data
    except Exception:
        return None


def check_pengaduan_status(pengaduan_id: str, email: str) -> Optional[Dict]:
    try:
        sb = _client()
        if not sb:
            return None
        res = (
            sb.table("pengaduan")
            .select("*")
            .eq("id", pengaduan_id)
            .eq("email", email)
            .single()
            .execute()
        )
        return res.data
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Admin – Pengaduan
# ---------------------------------------------------------------------------

def admin_get_all_pengaduan(status: Optional[str] = None) -> List[Dict]:
    try:
        sb = _service() or _client()
        if not sb:
            return []
        q = sb.table("pengaduan").select("*").order("created_at", desc=True)
        if status:
            q = q.eq("status", status)
        res = q.execute()
        return res.data or []
    except Exception:
        return []


def admin_update_pengaduan(pengaduan_id: str, data: Dict) -> Optional[Dict]:
    try:
        sb = _service() or _client()
        if not sb:
            return None
        res = sb.table("pengaduan").update(data).eq("id", pengaduan_id).execute()
        return res.data[0] if res.data else None
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Admin – Berita
# ---------------------------------------------------------------------------

def admin_get_all_berita() -> List[Dict]:
    try:
        sb = _service() or _client()
        if not sb:
            return []
        res = sb.table("berita").select("*").order("created_at", desc=True).execute()
        return res.data or []
    except Exception:
        return []


def admin_get_berita_by_id(berita_id: int) -> Optional[Dict]:
    try:
        sb = _service() or _client()
        if not sb:
            return None
        res = sb.table("berita").select("*").eq("id", berita_id).single().execute()
        return res.data
    except Exception:
        return None


def admin_create_berita(data: Dict) -> Optional[Dict]:
    try:
        sb = _service() or _client()
        if not sb:
            return None
        res = sb.table("berita").insert(data).execute()
        return res.data[0] if res.data else None
    except Exception:
        return None


def admin_update_berita(berita_id: int, data: Dict) -> Optional[Dict]:
    try:
        sb = _service() or _client()
        if not sb:
            return None
        res = sb.table("berita").update(data).eq("id", berita_id).execute()
        return res.data[0] if res.data else None
    except Exception:
        return None


def admin_delete_berita(berita_id: int) -> bool:
    try:
        sb = _service() or _client()
        if not sb:
            return False
        sb.table("berita").delete().eq("id", berita_id).execute()
        return True
    except Exception:
        return False


# ---------------------------------------------------------------------------
# Admin – Hero Slides
# ---------------------------------------------------------------------------

def admin_get_all_hero_slides() -> List[Dict]:
    try:
        sb = _service() or _client()
        if not sb:
            return []
        res = sb.table("hero_slides").select("*").order("urutan").execute()
        return res.data or []
    except Exception:
        return []


def admin_get_hero_slide_by_id(slide_id: int) -> Optional[Dict]:
    try:
        sb = _service() or _client()
        if not sb:
            return None
        res = sb.table("hero_slides").select("*").eq("id", slide_id).single().execute()
        return res.data
    except Exception:
        return None


def admin_create_hero_slide(data: Dict) -> Optional[Dict]:
    try:
        sb = _service() or _client()
        if not sb:
            return None
        res = sb.table("hero_slides").insert(data).execute()
        return res.data[0] if res.data else None
    except Exception:
        return None


def admin_update_hero_slide(slide_id: int, data: Dict) -> Optional[Dict]:
    try:
        sb = _service() or _client()
        if not sb:
            return None
        res = sb.table("hero_slides").update(data).eq("id", slide_id).execute()
        return res.data[0] if res.data else None
    except Exception:
        return None


def admin_delete_hero_slide(slide_id: int) -> bool:
    try:
        sb = _service() or _client()
        if not sb:
            return False
        sb.table("hero_slides").delete().eq("id", slide_id).execute()
        return True
    except Exception:
        return False


# ---------------------------------------------------------------------------
# Storage
# ---------------------------------------------------------------------------

def upload_file(bucket: str, file_obj: Any, filename: str) -> Optional[str]:
    try:
        sb = _service() or _client()
        if not sb:
            return None
        data = file_obj.read()
        sb.storage.from_(bucket).upload(filename, data)
        url = sb.storage.from_(bucket).get_public_url(filename)
        return url
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Auth / User
# ---------------------------------------------------------------------------

def get_user_by_id(user_id: str) -> Optional[Dict]:
    """Return minimal user dict for Flask-Login's user_loader."""
    try:
        sb = _service()
        if not sb:
            return None
        res = sb.auth.admin.get_user_by_id(user_id)
        if res and res.user:
            u = res.user
            meta = u.user_metadata or {}
            return {
                "id": u.id,
                "email": u.email,
                "nama": meta.get("nama", "Admin"),
                "role": meta.get("role", "admin"),
            }
        return None
    except Exception:
        return None


def admin_sign_in(email: str, password: str) -> Optional[Dict]:
    try:
        sb = _client()
        if not sb:
            return None
        res = sb.auth.sign_in_with_password({"email": email, "password": password})
        if res and res.user:
            u = res.user
            meta = u.user_metadata or {}
            return {
                "id": u.id,
                "email": u.email,
                "nama": meta.get("nama", "Admin"),
                "role": meta.get("role", "admin"),
            }
        return None
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Dashboard Stats
# ---------------------------------------------------------------------------

def get_stats() -> Dict[str, int]:
    defaults = {
        "total_berita": 0,
        "total_pengaduan": 0,
        "pengaduan_masuk": 0,
        "pengaduan_proses": 0,
        "pengaduan_selesai": 0,
        "total_hero_slides": 0,
        "total_layanan": 0,
    }
    try:
        sb = _service() or _client()
        if not sb:
            return defaults

        berita_res = sb.table("berita").select("id", count="exact").execute()
        pengaduan_res = sb.table("pengaduan").select("id", count="exact").execute()
        pengaduan_masuk = sb.table("pengaduan").select("id", count="exact").eq("status", "masuk").execute()
        pengaduan_proses = sb.table("pengaduan").select("id", count="exact").eq("status", "proses").execute()
        pengaduan_selesai = sb.table("pengaduan").select("id", count="exact").eq("status", "selesai").execute()
        hero_res = sb.table("hero_slides").select("id", count="exact").execute()
        layanan_res = sb.table("layanan").select("id", count="exact").execute()

        return {
            "total_berita": berita_res.count or 0,
            "total_pengaduan": pengaduan_res.count or 0,
            "pengaduan_masuk": pengaduan_masuk.count or 0,
            "pengaduan_proses": pengaduan_proses.count or 0,
            "pengaduan_selesai": pengaduan_selesai.count or 0,
            "total_hero_slides": hero_res.count or 0,
            "total_layanan": layanan_res.count or 0,
        }
    except Exception:
        return defaults
