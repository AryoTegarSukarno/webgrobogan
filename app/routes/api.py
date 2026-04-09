from flask import Blueprint, jsonify, request
from ..services import supabase_service as svc

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/pengaduan", methods=["POST"])
def api_submit_pengaduan():
    data = request.get_json(silent=True) or {}
    required = ["nama_pelapor", "email", "judul", "deskripsi"]
    for field in required:
        if not data.get(field):
            return jsonify({"error": f"Field '{field}' wajib diisi."}), 400
    payload = {
        "nama_pelapor": data["nama_pelapor"],
        "email": data["email"],
        "nomor_hp": data.get("nomor_hp"),
        "kategori": data.get("kategori"),
        "judul": data["judul"],
        "deskripsi": data["deskripsi"],
        "status": "masuk",
    }
    result = svc.create_pengaduan(payload)
    if result:
        return jsonify({"success": True, "id": result.get("id")}), 201
    return jsonify({"error": "Gagal menyimpan pengaduan."}), 500


@api_bp.route("/berita", methods=["GET"])
def api_get_berita():
    page = request.args.get("page", 1, type=int)
    limit = min(request.args.get("limit", 10, type=int), 50)
    kategori = request.args.get("kategori")
    offset = (page - 1) * limit
    items = svc.get_berita_list(limit=limit, offset=offset, kategori=kategori)
    total = svc.get_berita_count(kategori=kategori)
    return jsonify({
        "data": items,
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": max(1, -(-total // limit)),
    })


@api_bp.route("/layanan", methods=["GET"])
def api_get_layanan():
    kategori = request.args.get("kategori")
    items = svc.get_layanan_list(kategori=kategori)
    return jsonify({"data": items, "total": len(items)})
