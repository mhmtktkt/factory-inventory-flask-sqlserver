from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import db, login_manager


class BirimKartlari(db.Model):
    __tablename__ = 'BirimKartlari'
    ID = db.Column(db.Integer, primary_key=True)
    BIRIMKODU = db.Column(db.String(50), unique=True, nullable=False)
    NOT = db.Column(db.String(200))
    DURUM = db.Column(db.Boolean, default=True)


class Departmanlar(db.Model):
    __tablename__ = 'Departmanlar'
    DEPARTMANID = db.Column(db.Integer, primary_key=True)
    DEPARTMANADI = db.Column(db.String(50), unique=True, nullable=False)


class DepartmanYetki(db.Model):
    __tablename__ = 'DepartmanYetki'
    id = db.Column(db.Integer, primary_key=True)
    DEPARTMANID = db.Column(db.Integer, db.ForeignKey('Departmanlar.DEPARTMANID'))
    MENUNAME = db.Column(db.String(100))
    ACCESS = db.Column(db.Boolean, default=False)
    YETKIETKLE = db.Column(db.Boolean, default=False)
    YETKIDUZENLE = db.Column(db.Boolean, default=False)
    YETKIIPTAL = db.Column(db.Boolean, default=False)
    YETKIRAPOR = db.Column(db.Boolean, default=False)


class User(UserMixin, db.Model):
    __tablename__ = 'Kullanicilar'
    ID = db.Column(db.Integer, primary_key=True)
    KULLANICIADI = db.Column(db.String(50), unique=True, nullable=False)
    SIFRE_HASH = db.Column(db.String(128))
    AKTIF = db.Column(db.Boolean, default=True)
    DEPARTMANID = db.Column(db.Integer, db.ForeignKey('Departmanlar.DEPARTMANID'))
    SONGIRISTARIHI = db.Column(db.DateTime)
    def set_password(self, password):
        self.SIFRE_HASH = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.SIFRE_HASH, password)

    def get_id(self):
        return str(self.ID)

    @property
    def id(self):
        return self.ID

    @property
    def is_active(self):
        return self.AKTIF

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




class StokKartlari(db.Model):
    __tablename__ = 'StokKartlari'
    ID = db.Column(db.Integer, primary_key=True)
    StokKodu = db.Column(db.String(50), unique=True, nullable=False)
    Barkod = db.Column(db.String(50))
    UrunAdi = db.Column(db.String(100))
    Kategori = db.Column(db.String(50))
    Marka = db.Column(db.String(50))
    Birim = db.Column(db.String(20))
    MinStok = db.Column(db.Integer)
    MaxStok = db.Column(db.Integer)
    MakinaAdi = db.Column(db.String(100))
    Istasyon = db.Column(db.String(100))
    Aciklama = db.Column(db.String(200))
    Durum = db.Column(db.Boolean, default=True)


class ActionLog(db.Model):
    __tablename__ = 'ActionLog'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50))
    action = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
