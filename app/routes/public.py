from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..services import supabase_service as svc
from ..services.forms import PengaduanForm, CekPengaduanForm

public_bp = Blueprint("public", __name__)


@public_bp.route("/")
def index():
    hero_slides = svc.get_hero_slides()
    berita_list = svc.get_berita_list(limit=6)
    layanan_list = svc.get_layanan_list()
    pengumuman_list = svc.get_pengumuman_list(limit=5)
    pariwisata_list = svc.get_pariwisata_list()[:4]
    return render_template(
        "public/index.html",
        hero_slides=hero_slides,
        berita_list=berita_list,
        layanan_list=layanan_list,
        pengumuman_list=pengumuman_list,
        pariwisata_list=pariwisata_list,
    )


@public_bp.route("/profil")
def profil():
    return render_template("public/profil.html")


@public_bp.route("/layanan")
def layanan():
    layanan_list = svc.get_layanan_list()
    return render_template("public/layanan.html", layanan_list=layanan_list)


@public_bp.route("/layanan/kependudukan")
def layanan_kependudukan():
    items = svc.get_layanan_list(kategori="kependudukan")
    return render_template("public/layanan/kependudukan.html", items=items)


@public_bp.route("/layanan/kesehatan")
def layanan_kesehatan():
    items = svc.get_layanan_list(kategori="kesehatan")
    return render_template("public/layanan/kesehatan.html", items=items)


@public_bp.route("/layanan/kebencanaan")
def layanan_kebencanaan():
    bencana_list = svc.get_bencana_list()
    return render_template("public/layanan/kebencanaan.html", bencana_list=bencana_list)


@public_bp.route("/layanan/pariwisata")
def layanan_pariwisata():
    pariwisata_list = svc.get_pariwisata_list()
    return render_template("public/layanan/pariwisata.html", pariwisata_list=pariwisata_list)


@public_bp.route("/berita")
def berita():
    page = request.args.get("page", 1, type=int)
    kategori = request.args.get("kategori", None)
    per_page = 9
    offset = (page - 1) * per_page
    berita_list = svc.get_berita_list(limit=per_page, offset=offset, kategori=kategori)
    total = svc.get_berita_count(kategori=kategori)
    total_pages = max(1, -(-total // per_page))
    return render_template(
        "public/berita.html",
        berita_list=berita_list,
        page=page,
        total_pages=total_pages,
        kategori=kategori,
    )


@public_bp.route("/berita/<slug>")
def berita_detail(slug):
    berita = svc.get_berita_by_slug(slug)
    if not berita:
        from flask import abort
        abort(404)
    related = svc.get_berita_list(limit=3)
    return render_template("public/berita_detail.html", berita=berita, related=related)


@public_bp.route("/pengaduan", methods=["GET", "POST"])
def pengaduan():
    form = PengaduanForm()
    success_id = None
    if form.validate_on_submit():
        data = {
            "nama_pelapor": form.nama_pelapor.data,
            "email": form.email.data,
            "nomor_hp": form.nomor_hp.data or None,
            "kategori": form.kategori.data,
            "judul": form.judul.data,
            "deskripsi": form.deskripsi.data,
            "status": "masuk",
        }
        # Handle file upload
        if form.lampiran.data:
            import os, uuid
            from werkzeug.utils import secure_filename
            file = form.lampiran.data
            ext = os.path.splitext(secure_filename(file.filename))[1]
            fname = f"pengaduan/{uuid.uuid4()}{ext}"
            url = svc.upload_file("lampiran", file, fname)
            if url:
                data["lampiran_url"] = url

        result = svc.create_pengaduan(data)
        if result:
            success_id = result.get("id")
            flash(
                f"Pengaduan berhasil dikirim! Nomor ID Anda: <strong>{success_id}</strong>. "
                "Simpan nomor ini untuk mengecek status pengaduan.",
                "success",
            )
            return redirect(url_for("public.pengaduan"))
        else:
            flash(
                "Maaf, terjadi kesalahan saat mengirim pengaduan. Silakan coba lagi.",
                "danger",
            )
    return render_template("public/pengaduan.html", form=form)


@public_bp.route("/pengaduan/cek", methods=["GET", "POST"])
def pengaduan_cek():
    form = CekPengaduanForm()
    result = None
    if form.validate_on_submit():
        result = svc.check_pengaduan_status(form.nomor_id.data.strip(), form.email.data.strip())
        if not result:
            flash("Pengaduan tidak ditemukan. Periksa kembali Nomor ID dan email Anda.", "warning")
    return render_template("public/pengaduan_cek.html", form=form, result=result)
