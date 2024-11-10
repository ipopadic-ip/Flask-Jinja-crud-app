import flask
from flask import Flask
from flaskext.mysql import MySQL
import pymysql

from datetime import datetime

app = Flask(__name__, static_url_path="/")
mysql = MySQL(app, cursorclass=pymysql.cursors.DictCursor)

app.config["MYSQL_DATABASE_USER"] = "***"
app.config["MYSQL_DATABASE_PASSWORD"] = "***"
app.config["MYSQL_DATABASE_DB"] = "hotel"


@app.route("/")
def home():
    gosti = []
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM gost")
    gosti = cursor.fetchall()

    return flask.render_template("home.tpl.html", gosti=gosti)

@app.route("/forma")
def forma():
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM gost")
    gost = cursor.fetchall()
    return flask.render_template("formaZaDodavanje.tpl.html", gosti=gost)

@app.route("/uklanjanje")
def uklanjanje():
    id_gosta = flask.request.args.get("id_gosta")
    db = mysql.get_db()
    cursor = db.cursor()
    
    row_count = cursor.execute("DELETE FROM gost WHERE id = %s", (id_gosta,))
    db.commit()

    if row_count < 1:
        return "Gost nije pronadjen!", 404
    
    return flask.redirect("/")

@app.route("/izmenaForma", methods=["GET"])
def izmena_forma():
    id_gosta = flask.request.args.get("id_gosta")
    db = mysql.get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM gost WHERE id = %s", (id_gosta,))
    gost = cursor.fetchone()

    if gost is not None:
        cursor.execute("SELECT * FROM gost")
        return flask.render_template("formaZaIzmenu.tpl.html", gost=gost)
    return "Gost nije pronadjen!", 404

@app.route("/izmeni", methods=["POST"])
def izmena():
    id_gosta = flask.request.args.get("id_gosta")
    gost = dict(flask.request.form)
    gost["id"] = id_gosta

    db = mysql.get_db()
    cursor = db.cursor()
    row_count = cursor.execute("UPDATE gost SET ime=%(ime)s, prezime=%(prezime)s, email=%(email)s, telefon=%(telefon)s WHERE id = %(id)s", gost)
    db.commit()
    if row_count < 1:
        return "Gost nije pronadjen!", 404
    return flask.redirect("/")

@app.route("/dodaj", methods=["POST"])
def dodavanje():
    gost = dict(flask.request.form)

    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO gost( ime, prezime, email, telefon) VALUES(%(ime)s, %(prezime)s, %(email)s, %(telefon)s)", gost)
    db.commit()

    return flask.redirect("/")


@app.route("/soba")
def homeSoba():
    sobe = []
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM soba")
    sobe = cursor.fetchall()

    return flask.render_template("soba.tpl.html", sobe=sobe)

@app.route("/sobaForma")
def formaSoba():
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM soba")
    soba = cursor.fetchall()
    return flask.render_template("sobaFormaZaDodavanje.tpl.html", sobe=soba)

@app.route("/sobaUklanjanje")
def uklanjanjeSoba():
    id_soba = flask.request.args.get("id_soba")
    db = mysql.get_db()
    cursor = db.cursor()
    
    # row_count = cursor.execute("DELETE FROM soba WHERE id = %s", (id_soba,))
    # db.commit()

    cursor.execute("DELETE FROM rezervacija WHERE soba_id = %s", (id_soba,))
    db.commit()
    
    row_count = cursor.execute("DELETE FROM soba WHERE id = %s", (id_soba,))
    db.commit()

    if row_count < 1:
        return "Soba nije pronadjen!", 404
    
    return flask.redirect("/")

@app.route("/sobaIzmenaForma", methods=["GET"])
def sobaIzmena_forma():
    id_soba = flask.request.args.get("id_soba")
    db = mysql.get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM soba WHERE id = %s", (id_soba,))
    soba = cursor.fetchone()

    if soba is not None:
        cursor.execute("SELECT * FROM soba")
        return flask.render_template("sobaFormaZaIzmenu.tpl.html", soba=soba)
    return "Soba nije pronadjena!", 404

@app.route("/sobaIzmeni", methods=["POST"])
def sobaIzmena():
    id_soba = flask.request.args.get("id_soba")
    soba = dict(flask.request.form)
    soba["id"] = id_soba

    db = mysql.get_db()
    cursor = db.cursor()
    row_count = cursor.execute("UPDATE soba SET naziv=%(naziv)s, broj_kreveta=%(broj_kreveta)s, cena=%(cena)s WHERE id = %(id)s", soba)
    db.commit()
    if row_count < 1:
        return "Soba nije pronadjena!", 404
    return flask.redirect("/")

@app.route("/sobaDodaj", methods=["POST"])
def sobaDodavanje():
    soba = dict(flask.request.form)

    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO soba( naziv, broj_kreveta, cena) VALUES(%(naziv)s, %(broj_kreveta)s, %(cena)s)", soba)
    db.commit()

    return flask.redirect("/")


# rezervacija


@app.route("/rezervacija")
def rezervacijaHome():
    rezervacije = []
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM rezervacija JOIN soba ON rezervacija.soba_id = soba.id JOIN gost ON rezervacija.gost_id = gost.id;")
    rezervacije = cursor.fetchall()

    return flask.render_template("rezervacija.tpl.html", rezervacije=rezervacije)

@app.route("/rezervacijaForma")
def rezervacijaForma():
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM soba")
    sobe = cursor.fetchall()
    cursor.execute("SELECT * FROM gost")
    gosti = cursor.fetchall()
    return flask.render_template("rezervacijaFormaZaDodavanje.tpl.html", sobe=sobe, gosti=gosti)

@app.route("/rezervacijaUklanjanje")
def rezervacijaUklanjanje():
    id_rezervacija = flask.request.args.get("id_rezervacija")
    db = mysql.get_db()
    cursor = db.cursor()
    
    row_count = cursor.execute("DELETE FROM rezervacija WHERE id = %s", (id_rezervacija,))
    db.commit()

    if row_count < 1:
        return "Rezervacija nije pronadjen!", 404
    
    return flask.redirect("/")

@app.route("/rezervacijaIzmenaForma", methods=["GET"])
def rezervacijaIzmena_forma():
    id_rezervacija = flask.request.args.get("id_rezervacija")
    db = mysql.get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM rezervacija WHERE id = %s", (id_rezervacija,))
    rezervacija = cursor.fetchone()

    if rezervacija is not None:
        cursor.execute("SELECT * FROM soba")
        sobe = cursor.fetchall()
        cursor.execute("SELECT * FROM gost")
        gosti = cursor.fetchall()
        return flask.render_template("rezervacijaFormaZaIzmenu.tpl.html", rezervacija=rezervacija, sobe=sobe, gosti=gosti)
    return "Rezervacija nije pronadjen!", 404

@app.route("/rezervacijaIzmeni", methods=["POST"])
def rezervacijaIzmena():
    id_rezervacija = flask.request.args.get("id_rezervacija")
    rezervacija = dict(flask.request.form)
    rezervacija["id"] = id_rezervacija

    db = mysql.get_db()
    cursor = db.cursor()
    row_count = cursor.execute("UPDATE rezervacija SET soba_id=%(soba_id)s, gost_id=%(gost_id)s, datum_od=%(datum_od)s, datum_do=%(datum_do)s, cena=%(cena)s WHERE id = %(id)s", rezervacija)
    db.commit()
    if row_count < 1:
        return "Rezervacija nije pronadjen!", 404
    return flask.redirect("/")

@app.route("/rezervacijaDodaj", methods=["POST"])
def rezervacijaDodavanje():
    rezervacija = dict(flask.request.form)

    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO student(soba_id, gost_id, datum_od, datum_do, cena) VALUES(%(soba_id)s, %(gost_id)s, %(datum_od)s, %(datum_do)s, %(cena)s)", rezervacija)
    db.commit()

    return flask.redirect("/")

def validate_dates(datum_od, datum_do):
    if datum_od < datetime.now().date():
        return "Datum početka rezervacije ne može biti u prošlosti!"
    if datum_do < datum_od:
        return "Datum kraja rezervacije ne može biti pre datuma početka!"
    return None



if __name__ == "__main__":
    app.run()
