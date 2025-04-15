from app import app
from models import *

with app.app_context():
    db.drop_all()
    db.create_all()

    f1 = FyysilineIsik(eesnimi="Mari", perekonnanimi="Mets", isikukood="49002010987")
    f2 = FyysilineIsik(eesnimi="Jaan", perekonnanimi="Tamm", isikukood="38001020123")
    j1 = JuriidilineIsik(nimi="Test AS", registrikood="1234567")

    os1 = Osanik(tyyp='füüsiline', fyysiline_isik=f1)
    os2 = Osanik(tyyp='füüsiline', fyysiline_isik=f2)
    os3 = Osanik(tyyp='juriidiline', juriidiline_isik=j1)

    db.session.add_all([os1, os2, os3])
    db.session.commit()
