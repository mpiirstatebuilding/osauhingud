from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Osauhing, Osanik, Osa, FyysilineIsik, JuriidilineIsik
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///OSAÜHINGUD.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret'
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def avaleht():
    results = Osauhing.query
    nimi = request.args.get('nimi', '')
    registrikood = request.args.get('registrikood', '')
    osaniku_nimi = request.args.get('osaniku_nimi', '')
    osaniku_kood = request.args.get('osaniku_kood', '')

    if nimi:
        results = results.filter(
            (Osauhing.nimi.ilike(f"%{nimi}%"))
        )

    if registrikood:
        results = results.filter(
            (Osauhing.registrikood.ilike(registrikood))
        )

    results = results.all()

    if osaniku_nimi:
        filtered = []
        for ou in results:
            match = False
            for osa in ou.osad:
                if osa.osanik.tyyp == 'füüsiline' and (osaniku_nimi.lower() in osa.osanik.fyysiline_isik.eesnimi.lower() or osaniku_nimi.lower() in osa.osanik.fyysiline_isik.perekonnanimi.lower()):
                    match = True
                    break
                elif osa.osanik.tyyp == 'juriidiline' and osaniku_nimi.lower() in osa.osanik.juriidiline_isik.nimi.lower():
                    match = True
                    break
            if match:
               filtered.append(ou)
        results = filtered

    if osaniku_kood:
        filtered = []
        for ou in results:
            match = False
            for osa in ou.osad:
                if (osa.osanik.tyyp == 'füüsiline' and osa.osanik.fyysiline_isik.isikukood == osaniku_kood) or (osa.osanik.tyyp == 'juriidiline' and osa.osanik.juriidiline_isik.registrikood == osaniku_kood):
                    match = True
                    break
            if match:
                filtered.append(ou)
        results = filtered

    return render_template('avaleht.html', tulemused=results, nimi=nimi, registrikood=registrikood, osaniku_nimi=osaniku_nimi, osaniku_kood=osaniku_kood)

@app.route('/osauhing/<int:id>')
def osauhing_vaade(id):
    ou = Osauhing.query.get_or_404(id)
    return render_template('osauhing_vaade.html', ou=ou)

@app.route('/asutamine', methods=['GET', 'POST'])
def asutamine():
    if request.method == 'POST':
        try:
            nimi = request.form['nimi']
            registrikood = request.form['registrikood']
            asutamiskuupaev = date.fromisoformat(request.form['asutamiskuupaev'])
            kogukapital = int(request.form['kogukapital'])
            osanikud = request.form.getlist('osanik_id')
            suurused = request.form.getlist('osa_suurus')

            osade_summa = sum(map(int, suurused))
            if osade_summa != kogukapital:
                flash("Osade summa peab võrduma kogukapitaliga.")
                return redirect(url_for('asutamine'))

            ou = Osauhing(
                nimi=nimi,
                registrikood=registrikood,
                asutamiskuupaev=asutamiskuupaev,
                kogukapital=kogukapital
            )
            db.session.add(ou)
            db.session.flush()

            for osanik_id, osa_suurus in zip(osanikud, suurused):
                osa = Osa(
                    osauhing_id=ou.id,
                    osanik_id=int(osanik_id),
                    suurus=int(osa_suurus),
                    on_asutaja=True
                )
                db.session.add(osa)

            db.session.commit()
            return redirect(url_for('osauhing_vaade', id=ou.id))

        except Exception as e:
            flash(f"Viga: {e}")
            return redirect(url_for('asutamine'))

    osanikud = Osanik.query.all()
    return render_template('asutamine.html', osanikud=osanikud)

if __name__ == '__main__':
    app.run(debug=True)
