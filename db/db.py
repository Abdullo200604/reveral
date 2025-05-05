import psycopg2


def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        password="1",
        database="postgres",
        user="postgres"
    )


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        user_id VARCHAR(255) UNIQUE,
        ism VARCHAR(50),
        fam VARCHAR(50),
        tel_nomer VARCHAR(15),
        referrals INT DEFAULT 0
    );
    """)
    conn.commit()
    cursor.close()
    conn.close()


def add_user_if_not_exists(user_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO users (user_id) 
    VALUES (%s) 
    ON CONFLICT (user_id) DO NOTHING
    """, (user_id,))

    conn.commit()
    cursor.close()
    conn.close()


def increment_referral(user_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE users 
    SET referrals = referrals + 1 
    WHERE user_id = %s
    """, (user_id,))

    conn.commit()
    cursor.close()
    conn.close()


def get_user_referrals(user_id: str) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT referrals FROM users WHERE user_id = %s
    """, (user_id,))

    result = cursor.fetchone()
    cursor.close()
    conn.close()

    return result[0] if result else 0


if __name__ == "__main__":
    init_db()

    user_id = "7222453221"

    add_user_if_not_exists(user_id)

    increment_referral(user_id)

    referral_count = get_user_referrals(user_id)
    print(f"Foydalanuvchining referallari soni: {referral_count}")