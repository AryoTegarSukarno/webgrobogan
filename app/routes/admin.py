from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from ..services import supabase_service as svc
from ..services.forms import AdminLoginForm, BeritaForm, HeroSlideForm
from ..models import User

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin.dashboard"))
    form = AdminLoginForm()
    if form.validate_on_submit():
        user_data = svc.admin_sign_in(form.email.data, form.password.data)
        if user_data:
            user = User(
                user_id=user_data["id"],
                email=user_data["email"],
                nama=user_data.get("nama", "Admin"),
                role=user_data.get("role", "admin"),
            )
            login_user(user, remember=True)
            flash("Selamat datang kembali!", "success")
            return redirect(url_for("admin.dashboard"))
        else:
            flash("Email atau password salah, atau layanan tidak tersedia.", "danger")
    return render_template("admin/login.html", form=form)


@admin_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Anda telah keluar.", "info")
    return redirect(url_for("admin.login"))


@admin_bp.route("/")
@login_required
def dashboard():
    stats = svc.get_stats()
    recent_pengaduan = svc.admin_get_all_pengaduan()[:5]
    recent_berita = svc.admin_get_all_berita()[:5]
    return render_template(
        "admin/dashboard.html",
        stats=stats,
        recent_pengaduan=recent_pengaduan,
        recent_berita=recent_berita,
    )


# ── Berita ──────────────────────────────────────────────────────────────────

@admin_bp.route("/berita")
@login_required
def berita_list():
    berita = svc.admin_get_all_berita()
    return render_template("admin/berita_list.html", berita_list=berita)


@admin_bp.route("/berita/new", methods=["GET", "POST"])
@login_required
def berita_new():
    form = BeritaForm()
    if form.validate_on_submit():
        data = {
            "judul": form.judul.data,
            "slug": form.slug.data,
            "konten": form.konten.data,
            "kategori": form.kategori.data or None,
            "status": form.status.data,
        }
        if form.thumbnail.data:
            import os, uuid
            from werkzeug.utils import secure_filename
            file = form.thumbnail.data
            ext = os.path.splitext(secure_filename(file.filename))[1]
            fname = f"berita/{uuid.uuid4()}{ext}"
            url = svc.upload_file("thumbnails", file, fname)
            if url:
                data["thumbnail"] = url
        result = svc.admin_create_berita(data)
        if result:
            flash("Berita berhasil dibuat.", "success")
            return redirect(url_for("admin.berita_list"))
        flash("Gagal membuat berita.", "danger")
    return render_template("admin/berita_form.html", form=form, action="Buat")


@admin_bp.route("/berita/<int:berita_id>/edit", methods=["GET", "POST"])
@login_required
def berita_edit(berita_id):
    berita = svc.admin_get_berita_by_id(berita_id)
    if not berita:
        flash("Berita tidak ditemukan.", "warning")
        return redirect(url_for("admin.berita_list"))
    form = BeritaForm(data=berita)
    if form.validate_on_submit():
        data = {
            "judul": form.judul.data,
            "slug": form.slug.data,
            "konten": form.konten.data,
            "kategori": form.kategori.data or None,
            "status": form.status.data,
        }
        if form.thumbnail.data:
            import os, uuid
            from werkzeug.utils import secure_filename
            file = form.thumbnail.data
            ext = os.path.splitext(secure_filename(file.filename))[1]
            fname = f"berita/{uuid.uuid4()}{ext}"
            url = svc.upload_file("thumbnails", file, fname)
            if url:
                data["thumbnail"] = url
        result = svc.admin_update_berita(berita_id, data)
        if result:
            flash("Berita berhasil diperbarui.", "success")
            return redirect(url_for("admin.berita_list"))
        flash("Gagal memperbarui berita.", "danger")
    return render_template("admin/berita_form.html", form=form, action="Edit", berita=berita)


@admin_bp.route("/berita/<int:berita_id>/delete", methods=["POST"])
@login_required
def berita_delete(berita_id):
    ok = svc.admin_delete_berita(berita_id)
    if ok:
        flash("Berita berhasil dihapus.", "success")
    else:
        flash("Gagal menghapus berita.", "danger")
    return redirect(url_for("admin.berita_list"))


# ── Hero Slides ──────────────────────────────────────────────────────────────

@admin_bp.route("/hero-slides")
@login_required
def hero_slides():
    slides = svc.admin_get_all_hero_slides()
    return render_template("admin/hero_slides.html", slides=slides)


@admin_bp.route("/hero-slides/new", methods=["GET", "POST"])
@login_required
def hero_slide_new():
    form = HeroSlideForm()
    if form.validate_on_submit():
        data = {
            "judul": form.judul.data,
            "deskripsi": form.deskripsi.data or None,
            "image_url": form.image_url.data,
            "link_url": form.link_url.data or None,
            "urutan": form.urutan.data,
            "aktif": form.aktif.data,
        }
        result = svc.admin_create_hero_slide(data)
        if result:
            flash("Hero slide berhasil dibuat.", "success")
            return redirect(url_for("admin.hero_slides"))
        flash("Gagal membuat hero slide.", "danger")
    return render_template("admin/hero_form.html", form=form, action="Buat")


@admin_bp.route("/hero-slides/<int:slide_id>/edit", methods=["GET", "POST"])
@login_required
def hero_slide_edit(slide_id):
    slide = svc.admin_get_hero_slide_by_id(slide_id)
    if not slide:
        flash("Slide tidak ditemukan.", "warning")
        return redirect(url_for("admin.hero_slides"))
    form = HeroSlideForm(data=slide)
    if form.validate_on_submit():
        data = {
            "judul": form.judul.data,
            "deskripsi": form.deskripsi.data or None,
            "image_url": form.image_url.data,
            "link_url": form.link_url.data or None,
            "urutan": form.urutan.data,
            "aktif": form.aktif.data,
        }
        result = svc.admin_update_hero_slide(slide_id, data)
        if result:
            flash("Hero slide berhasil diperbarui.", "success")
            return redirect(url_for("admin.hero_slides"))
        flash("Gagal memperbarui hero slide.", "danger")
    return render_template("admin/hero_form.html", form=form, action="Edit", slide=slide)


@admin_bp.route("/hero-slides/<int:slide_id>/delete", methods=["POST"])
@login_required
def hero_slide_delete(slide_id):
    ok = svc.admin_delete_hero_slide(slide_id)
    if ok:
        flash("Hero slide berhasil dihapus.", "success")
    else:
        flash("Gagal menghapus hero slide.", "danger")
    return redirect(url_for("admin.hero_slides"))


# ── Pengaduan ────────────────────────────────────────────────────────────────

@admin_bp.route("/pengaduan")
@login_required
def pengaduan_list():
    status_filter = request.args.get("status", None)
    pengaduan = svc.admin_get_all_pengaduan(status=status_filter)
    return render_template(
        "admin/pengaduan_list.html",
        pengaduan_list=pengaduan,
        status_filter=status_filter,
    )


@admin_bp.route("/pengaduan/<pengaduan_id>")
@login_required
def pengaduan_detail(pengaduan_id):
    pengaduan = svc.get_pengaduan_by_id(pengaduan_id)
    if not pengaduan:
        flash("Pengaduan tidak ditemukan.", "warning")
        return redirect(url_for("admin.pengaduan_list"))
    return render_template("admin/pengaduan_detail.html", pengaduan=pengaduan)


@admin_bp.route("/pengaduan/<pengaduan_id>/update", methods=["POST"])
@login_required
def pengaduan_update(pengaduan_id):
    new_status = request.form.get("status")
    tanggapan = request.form.get("tanggapan", "")
    if not new_status:
        flash("Status tidak valid.", "warning")
        return redirect(url_for("admin.pengaduan_detail", pengaduan_id=pengaduan_id))
    data = {"status": new_status, "tanggapan": tanggapan}
    result = svc.admin_update_pengaduan(pengaduan_id, data)
    if result:
        flash("Status pengaduan berhasil diperbarui.", "success")
    else:
        flash("Gagal memperbarui status pengaduan.", "danger")
    return redirect(url_for("admin.pengaduan_detail", pengaduan_id=pengaduan_id))
