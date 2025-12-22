import mysql.connector

def create_database():
    try:
        # Connect to MySQL server (no database selected)
        cnx = mysql.connector.connect(
            user='root',
            password='9640351007Ajay@',
            host='127.0.0.1',
            port=3306
        )
        cursor = cnx.cursor()
        
        # Create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS myrush")
        print("✅ Database 'myrush' created or already exists")
        
        cursor.close()
        cnx.close()
    except Exception as e:
        print(f"❌ Error creating database: {e}")

if __name__ == "__main__":
    create_database()
