-- Création de la table client
CREATE TABLE IF NOT EXISTS client (
    code_client INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    adresse_postale TEXT,
    membership_points INT DEFAULT 0,
    expiry_date DATE
);

-- Création de la table commande
CREATE TABLE IF NOT EXISTS commande (
    numero_commande INT AUTO_INCREMENT PRIMARY KEY,
    code_client INT NOT NULL,
    date_commande DATE NOT NULL,
    montant_commande DECIMAL(10,2) NOT NULL,
    promotion DECIMAL(5,2) DEFAULT 0,
    frais_livraison DECIMAL(10,2) DEFAULT 0,
    FOREIGN KEY (code_client) REFERENCES client(code_client) ON DELETE CASCADE
);

-- Insertion de données de test
INSERT INTO client (nom, adresse_postale, membership_points, expiry_date) VALUES
('Client Test 1', '123 Rue de Test', 100, '2025-12-31'),
('Client Test 2', '456 Avenue Example', 50, '2024-06-30');