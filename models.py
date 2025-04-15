import re
from datetime import date

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Osauhing(db.Model):
    __tablename__ = 'osaühingud'
    id = db.Column(db.Integer, primary_key=True)
    nimi = db.Column(db.String(100), nullable=False)
    registrikood = db.Column(db.String(7), unique=True, nullable=False)
    asutamiskuupaev = db.Column(db.Date, nullable=False)
    kogukapital = db.Column(db.Integer, nullable=False)

    osad = db.relationship('Osa', back_populates='osauhing')

    @validates('nimi')
    def validate_nimi(self, key, value):
        if not (3 <= len(value) <= 100):
            raise ValueError("Nimi peab olema 3 kuni 100 tähemärki.")
        if not re.match(r'^[A-Za-z0-9ÄÖÜäöüõÕ\s\-]+$', value):
            raise ValueError("Nimi tohib sisaldada ainult tähti, numbreid, tühikuid ja sidekriipse.")
        return value

    @validates('registrikood')
    def validate_registrikood(self, key, value):
        if not re.fullmatch(r'\d{7}', value):
            raise ValueError("Registrikood peab olema täpselt 7 numbrit.")
        return value

    @validates('asutamiskuupaev')
    def validate_asutamiskuupaev(self, key, value):
        if value > date.today():
            raise ValueError("Asutamiskuupäev ei saa olla tulevikus.")
        return value

    @validates('kogukapital')
    def validate_kogukapital(self, key, value):
        if value < 2500:
            raise ValueError("Kogukapitali suurus peab olema vähemalt 2500 eurot.")
        return value


class Osanik(db.Model):
    __tablename__ = 'osanikud'
    id = db.Column(db.Integer, primary_key=True)
    tyyp = db.Column(db.Enum('füüsiline', 'juriidiline', name='osaniku_tüüp'), nullable=False)

    fyysiline_isik = db.relationship('FyysilineIsik', uselist=False, back_populates='osanik')
    juriidiline_isik = db.relationship('JuriidilineIsik', uselist=False, back_populates='osanik')
    osad = db.relationship('Osa', back_populates='osanik')


class FyysilineIsik(db.Model):
    __tablename__ = 'füüsilised_isikud'
    osanik_id = db.Column(db.Integer, db.ForeignKey('osanikud.id'), primary_key=True)
    eesnimi = db.Column(db.String, nullable=False)
    perekonnanimi = db.Column(db.String, nullable=False)
    isikukood = db.Column(db.String, unique=True, nullable=False)

    osanik = db.relationship('Osanik', back_populates='fyysiline_isik')


class JuriidilineIsik(db.Model):
    __tablename__ = 'juriidilised_isikud'
    osanik_id = db.Column(db.Integer, db.ForeignKey('osanikud.id'), primary_key=True)
    nimi = db.Column(db.String, nullable=False)
    registrikood = db.Column(db.String, unique=True, nullable=False)

    osanik = db.relationship('Osanik', back_populates='juriidiline_isik')


class Osa(db.Model):
    __tablename__ = 'osad'
    id = db.Column(db.Integer, primary_key=True)
    osauhing_id = db.Column(db.Integer, db.ForeignKey('osaühingud.id'), nullable=False)
    osanik_id = db.Column(db.Integer, db.ForeignKey('osanikud.id'), nullable=False)
    suurus = db.Column(db.Integer, nullable=False)
    on_asutaja = db.Column(db.Boolean, default=False, nullable=False)

    osauhing = db.relationship('Osauhing', back_populates='osad')
    osanik = db.relationship('Osanik', back_populates='osad')

    @validates('suurus')
    def validate_suurus(self, key, value):
        if value < 1:
            raise ValueError("Osaniku osa suurus peab olema vähemalt 1 euro.")
        return value
