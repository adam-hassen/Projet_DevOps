import os
import mysql.connector

def test_environment_variables():
    """Test que les variables d'environnement sont définies"""
    assert os.environ.get('DB_HOST') is not None
    assert os.environ.get('DB_USER') is not None
    assert os.environ.get('DB_PASSWORD') is not None
    assert os.environ.get('DB_NAME') is not None
    print("Variables d'environnement OK")

def test_mysql_connection():
    """Test la connexion à MySQL"""
    try:
        conn = mysql.connector.connect(
            host=os.environ.get('DB_HOST', 'localhost'),
            user=os.environ.get('DB_USER', 'root'),
            password=os.environ.get('DB_PASSWORD', ''),
            database=os.environ.get('DB_NAME', 'test_interface')
        )
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        assert result[0] == 1
        cursor.close()
        conn.close()
        print("Connexion MySQL OK")
    except Exception as e:
        print(f"Erreur MySQL: {e}")
        raise

if __name__ == "__main__":
    test_environment_variables()
    test_mysql_connection()
    print("Tous les tests passés!")