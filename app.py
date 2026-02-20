from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import pandas as pd
from flask import send_file
app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="test_interface"
)   

cursor = db.cursor(dictionary=True)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/clients", methods=["GET", "POST"])
def clients():
    if request.method == "POST":
        nom = request.form["nom"]
        adresse = request.form["adresse"]
        points = request.form["points"]
        expiry = request.form["expiry"]

        cursor.execute("""
            INSERT INTO client (nom, adresse_postale, membership_points, expiry_date)
            VALUES (%s, %s, %s, %s)
        """, (nom, adresse, points, expiry if expiry else None))

        db.commit()
        return redirect(url_for("clients"))

    cursor.execute("SELECT * FROM client")
    clients = cursor.fetchall()
    return render_template("clients.html", clients=clients)



@app.route("/clients/delete/<int:id>")
def delete_client(id):
    cursor.execute("DELETE FROM client WHERE code_client = %s", (id,))
    db.commit()
    return redirect(url_for("clients"))


@app.route("/clients/edit/<int:id>", methods=["GET", "POST"])
def edit_client(id):
    if request.method == "POST":
        cursor.execute("""
            UPDATE client
            SET nom=%s, adresse_postale=%s, membership_points=%s, expiry_date=%s
            WHERE code_client=%s
        """, (
            request.form["nom"],
            request.form["adresse"],
            request.form["points"],
            request.form["expiry"] if request.form["expiry"] else None,
            id
        ))
        db.commit()
        return redirect(url_for("clients"))

    cursor.execute("SELECT * FROM client WHERE code_client=%s", (id,))
    client = cursor.fetchone()
    return render_template("edit_client.html", client=client)



@app.route("/clients/search", methods=["GET"])
def search_client():
    keyword = request.args.get("q", "")
    cursor.execute("""
        SELECT * FROM client
        WHERE nom LIKE %s OR code_client = %s
    """, (f"%{keyword}%", keyword if keyword.isdigit() else -1))
    clients = cursor.fetchall()
    return render_template("clients.html", clients=clients)



@app.route("/commandes", methods=["GET", "POST"])
def commandes():
    if request.method == "POST":
        cursor.execute("""
            INSERT INTO commande 
            (code_client, date_commande, montant_commande, promotion, frais_livraison)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            request.form["code_client"],
            request.form["date_commande"],
            request.form["montant"],
            request.form["promotion"],
            request.form["frais"]
        ))

        db.commit()
        return redirect(url_for("commandes"))

    cursor.execute("""
        SELECT c.numero_commande, c.date_commande, c.montant_commande,
               c.promotion, c.frais_livraison, cl.nom
        FROM commande c
        JOIN client cl ON c.code_client = cl.code_client
    """)
    commandes = cursor.fetchall()

    cursor.execute("SELECT code_client, nom FROM client")
    clients = cursor.fetchall()

    return render_template("commandes.html",
                           commandes=commandes,
                           clients=clients)



@app.route("/commandes/delete/<int:id>")
def delete_commande(id):
    cursor.execute(
        "DELETE FROM commande WHERE numero_commande = %s",
        (id,)
    )
    db.commit()
    return redirect(url_for("commandes"))


@app.route("/commandes/edit/<int:id>", methods=["GET", "POST"])
def edit_commande(id):
    if request.method == "POST":
        cursor.execute("""
            UPDATE commande
            SET code_client=%s,
                date_commande=%s,
                montant_commande=%s,
                promotion=%s,
                frais_livraison=%s
            WHERE numero_commande=%s
        """, (
            request.form["code_client"],
            request.form["date_commande"],
            request.form["montant"],
            request.form["promotion"],
            request.form["frais"],
            id
        ))
        db.commit()
        return redirect(url_for("commandes"))

    cursor.execute(
        "SELECT * FROM commande WHERE numero_commande=%s",
        (id,)
    )
    commande = cursor.fetchone()

    cursor.execute("SELECT code_client, nom FROM client")
    clients = cursor.fetchall()

    return render_template(
        "edit_commande.html",
        commande=commande,
        clients=clients
    )


@app.route("/commandes/export")
def export_commandes():
    cursor.execute("""
        SELECT c.numero_commande, c.date_commande, c.montant_commande,
               cl.nom
        FROM commande c
        JOIN client cl ON c.code_client = cl.code_client
    """)
    data = cursor.fetchall()

    df = pd.DataFrame(data)
    file_path = "commandes.xlsx"
    df.to_excel(file_path, index=False)

    return send_file(file_path, as_attachment=True)




@app.route("/facture/<int:id>")
def facture(id):
    cursor.execute("""
        SELECT c.numero_commande, c.date_commande, c.montant_commande,
               c.frais_livraison, cl.nom
        FROM commande c
        JOIN client cl ON c.code_client = cl.code_client
        WHERE c.numero_commande = %s
    """, (id,))
    facture = cursor.fetchone()
    return render_template("facture.html", facture=facture)
if __name__ == "__main__":
    app.run(debug=True)
