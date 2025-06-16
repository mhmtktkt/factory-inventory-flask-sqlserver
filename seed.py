from app import create_app, db
from app.models import User, Departmanlar, StokKartlari

app = create_app()

with app.app_context():
    if not Departmanlar.query.first():
        dep = Departmanlar(DEPARTMANADI='Admin')
        db.session.add(dep)
        db.session.commit()
    else:
        dep = Departmanlar.query.first()
    if not User.query.filter_by(KULLANICIADI='admin').first():
        user = User(KULLANICIADI='admin', DEPARTMANID=dep.DEPARTMANID)
        user.set_password('admin')
        db.session.add(user)
    if not StokKartlari.query.first():
        item = StokKartlari(StokKodu='STK001', UrunAdi='Demo Ürün', Birim='Adet')
        db.session.add(item)
    db.session.commit()
    print('Seed data inserted.')
