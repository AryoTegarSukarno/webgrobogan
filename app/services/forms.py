from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField,
    TextAreaField,
    SelectField,
    PasswordField,
    IntegerField,
    BooleanField,
    SubmitField,
    EmailField,
)
from wtforms.validators import DataRequired, Email, Length, Optional, NumberRange


KATEGORI_PENGADUAN = [
    ("", "-- Pilih Kategori --"),
    ("infrastruktur", "Infrastruktur"),
    ("kesehatan", "Kesehatan"),
    ("pendidikan", "Pendidikan"),
    ("kependudukan", "Kependudukan"),
    ("keamanan", "Keamanan"),
    ("lingkungan", "Lingkungan"),
    ("lainnya", "Lainnya"),
]

KATEGORI_BERITA = [
    ("", "-- Pilih Kategori --"),
    ("berita", "Berita"),
    ("pengumuman", "Pengumuman"),
    ("agenda", "Agenda"),
    ("galeri", "Galeri"),
]

STATUS_BERITA = [
    ("draft", "Draft"),
    ("published", "Published"),
]


class PengaduanForm(FlaskForm):
    nama_pelapor = StringField(
        "Nama Lengkap",
        validators=[DataRequired(message="Nama wajib diisi."), Length(max=100)],
    )
    email = EmailField(
        "Email",
        validators=[DataRequired(message="Email wajib diisi."), Email()],
    )
    nomor_hp = StringField(
        "Nomor HP",
        validators=[Optional(), Length(max=20)],
    )
    kategori = SelectField(
        "Kategori Pengaduan",
        choices=KATEGORI_PENGADUAN,
        validators=[DataRequired(message="Pilih kategori pengaduan.")],
    )
    judul = StringField(
        "Judul Pengaduan",
        validators=[DataRequired(message="Judul wajib diisi."), Length(max=200)],
    )
    deskripsi = TextAreaField(
        "Deskripsi Lengkap",
        validators=[DataRequired(message="Deskripsi wajib diisi."), Length(max=5000)],
    )
    lampiran = FileField(
        "Lampiran (opsional)",
        validators=[FileAllowed(["jpg", "jpeg", "png", "pdf"], "Hanya jpg, png, pdf.")],
    )
    submit = SubmitField("Kirim Pengaduan")


class CekPengaduanForm(FlaskForm):
    nomor_id = StringField(
        "Nomor ID Pengaduan",
        validators=[DataRequired(message="Nomor ID wajib diisi.")],
    )
    email = EmailField(
        "Email",
        validators=[DataRequired(message="Email wajib diisi."), Email()],
    )
    submit = SubmitField("Cek Status")


class BeritaForm(FlaskForm):
    judul = StringField(
        "Judul Berita",
        validators=[DataRequired(), Length(max=300)],
    )
    slug = StringField(
        "Slug URL",
        validators=[DataRequired(), Length(max=300)],
    )
    konten = TextAreaField(
        "Konten",
        validators=[DataRequired()],
    )
    kategori = SelectField(
        "Kategori",
        choices=KATEGORI_BERITA,
        validators=[Optional()],
    )
    status = SelectField(
        "Status",
        choices=STATUS_BERITA,
        validators=[DataRequired()],
    )
    thumbnail = FileField(
        "Thumbnail",
        validators=[FileAllowed(["jpg", "jpeg", "png", "webp"], "Hanya gambar.")],
    )
    submit = SubmitField("Simpan")


class HeroSlideForm(FlaskForm):
    judul = StringField(
        "Judul Slide",
        validators=[DataRequired(), Length(max=200)],
    )
    deskripsi = TextAreaField(
        "Deskripsi",
        validators=[Optional(), Length(max=500)],
    )
    image_url = StringField(
        "URL Gambar",
        validators=[DataRequired(), Length(max=500)],
    )
    link_url = StringField(
        "URL Tautan (opsional)",
        validators=[Optional(), Length(max=500)],
    )
    urutan = IntegerField(
        "Urutan Tampil",
        validators=[DataRequired(), NumberRange(min=1, max=999)],
        default=1,
    )
    aktif = BooleanField("Aktif", default=True)
    submit = SubmitField("Simpan")


class AdminLoginForm(FlaskForm):
    email = EmailField(
        "Email",
        validators=[DataRequired(), Email()],
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired()],
    )
    submit = SubmitField("Login")
