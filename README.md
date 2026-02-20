# Application de Gestion de Clients et Commandes

![CI/CD Pipeline](https://github.com/adam-hassen/Projet_DevOps/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![Flask](https://img.shields.io/badge/Flask-2.3-green)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange)
![Docker](https://img.shields.io/badge/Docker-✓-blue)

## 📝 Description du projet

Application web développée avec **Flask (Python)** et **MySQL** pour gérer facilement des clients et leurs commandes. Elle permet d'effectuer toutes les opérations CRUD (Créer, Lire, Modifier, Supprimer) sur les clients et les commandes, avec génération de factures et export Excel.

## ✨ Fonctionnalités

### Gestion des clients
-  Ajouter un client (nom, adresse, points fidélité, date d'expiration)
-  Modifier un client
-  Supprimer un client
-  Rechercher un client par nom ou code
-  Lister tous les clients

### Gestion des commandes
-  Créer une commande liée à un client
-  Modifier une commande
-  Supprimer une commande
-  Voir toutes les commandes avec le nom du client
-  Export des commandes au format Excel
-  Génération de facture détaillée

## 🎯 Comment ça marche ?

### 1. L'architecture
L'application est composée de deux parties :
- **Frontend** : Pages HTML avec Bootstrap 5 (interface utilisateur)
- **Backend** : Serveur Flask (Python) qui gère la logique métier
- **Base de données** : MySQL qui stocke les clients et commandes

### 2. Le fonctionnement
1. L'utilisateur navigue sur les pages web
2. Flask reçoit les requêtes (GET, POST)
3. Flask interroge la base de données MySQL
4. Les résultats sont affichés dans les pages HTML

### 3. Les routes principales
| Route | Action |
|-------|--------|
| `/` | Page d'accueil |
| `/clients` | Liste et ajout de clients |
| `/clients/edit/1` | Modifier le client n°1 |
| `/clients/delete/1` | Supprimer le client n°1 |
| `/commandes` | Liste et ajout de commandes |
| `/commandes/edit/1` | Modifier la commande n°1 |
| `/commandes/export` | Télécharger les commandes en Excel |
| `/facture/1` | Voir la facture de la commande n°1 |

### 4. Exemple de scénario
1. Je vais sur `/clients` et j'ajoute "Jean Dupont"
2. Je vais sur `/commandes` et je crée une commande pour Jean Dupont de 150€
3. Je clique sur "Facture" pour voir le détail
4. J'exporte toutes les commandes en Excel pour les archiver

##  Installation et démarrage

### Méthode 1 : Avec Docker 

```bash
# 1. Récupérer le projet
git clone https://github.com/adam-hassen/Projet_DevOps.git
cd Projet_DevOps

# 2. Lancer avec Docker
docker-compose up --build

# 3. Ouvrir le navigateur
# http://localhost:5000
