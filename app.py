from flask import Flask, render_template, request, redirect, url_for, send_file, g
import mysql.connector
import pandas as pd
import os

app = Flask(__name__)

# Configuration de la base de données avec variables d'environnement
db_config = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', ''),
    'database': os.environ.get('DB_NAME', 'test_interface'),
    'port': int(os.environ.get('DB_PORT', 3306)),
    'autocommit': True,
    'pool_name': 'mypool',
    'pool_size': 5
}

def get_db():
    """Obtenir une connexion à la base de données"""
    if 'db' not in g:
        try:
            g.db = mysql.connector.connect(**db_config)
            g.cursor = g.db.cursor(dictionary=True)
        except mysql.connector.Error as err:
            print(f"Erreur de connexion: {err}")
            return None, None
    return g.db, g.cursor

@app.teardown_appcontext
def close_db(error):
    """Fermer la connexion à la fin de chaque requête"""
    db = g.pop('db', None)
    cursor = g.pop('cursor', None)
    if cursor is not None:
        cursor.close()
    if db is not None:
        db.close()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/clients", methods=["GET", "POST"])
def clients():
    db, cursor = get_db()
    if not db or not cursor:
        return "Erreur de connexion à la base de données", 500
        
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
    db, cursor = get_db()
    if not db or not cursor:
        return "Erreur de connexion", 500
        
    cursor.execute("DELETE FROM client WHERE code_client = %s", (id,))
    db.commit()
    return redirect(url_for("clients"))

@app.route("/clients/edit/<int:id>", methods=["GET", "POST"])
def edit_client(id):
    db, cursor = get_db()
    if not db or not cursor:
        return "Erreur de connexion", 500
        
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
    db, cursor = get_db()
    if not db or not cursor:
        return "Erreur de connexion", 500
        
    keyword = request.args.get("q", "")
    cursor.execute("""
        SELECT * FROM client
        WHERE nom LIKE %s OR code_client = %s
    """, (f"%{keyword}%", keyword if keyword.isdigit() else -1))
    clients = cursor.fetchall()
    return render_template("clients.html", clients=clients)

@app.route("/commandes", methods=["GET", "POST"])
def commandes():
    db, cursor = get_db()
    if not db or not cursor:
        return "Erreur de connexion à la base de données", 500
        
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
    db, cursor = get_db()
    if not db or not cursor:
        return "Erreur de connexion", 500
        
    cursor.execute(
        "DELETE FROM commande WHERE numero_commande = %s",
        (id,)
    )
    db.commit()
    return redirect(url_for("commandes"))

@app.route("/commandes/edit/<int:id>", methods=["GET", "POST"])
def edit_commande(id):
    db, cursor = get_db()
    if not db or not cursor:
        return "Erreur de connexion", 500
        
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
    db, cursor = get_db()
    if not db or not cursor:
        return "Erreur de connexion", 500
        
    cursor.execute("""
        SELECT c.numero_commande, c.date_commande, c.montant_commande,
               cl.nom
        FROM commande c
        JOIN client cl ON c.code_client = cl.code_client
    """)
    data = cursor.fetchall()

    df = pd.DataFrame(data)
    
    # Sauvegarder dans le dossier exports
    file_path = "exports/commandes.xlsx"
    df.to_excel(file_path, index=False)

    return send_file(file_path, as_attachment=True)

@app.route("/facture/<int:id>")
def facture(id):
    db, cursor = get_db()
    if not db or not cursor:
        return "Erreur de connexion", 500
        
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
    app.run(debug=True, host='0.0.0.0', port=5000)