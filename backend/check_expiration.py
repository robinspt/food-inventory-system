import sqlite3
import os
from datetime import datetime, timedelta

DATABASE = 'site.db'
WARNING_DAYS = 7 # Number of days before expiration to set status to 'warning'

def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), DATABASE)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def check_expiration_status():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get all food items
    cursor.execute("SELECT id, expiration_date, status FROM food_items")
    food_items = cursor.fetchall()

    today = datetime.now().date()

    for item in food_items:
        item_id = item['id']
        expiration_date_str = item['expiration_date']
        current_status = item['status']

        expiration_date = datetime.strptime(expiration_date_str, '%Y-%m-%d').date()

        new_status = current_status # Default to current status

        if expiration_date <= today:
            new_status = 'expired'
        elif expiration_date <= today + timedelta(days=WARNING_DAYS):
            new_status = 'warning'
        else:
            new_status = 'active'
        
        # Only update if status has changed
        if new_status != current_status:
            cursor.execute("UPDATE food_items SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                           (new_status, item_id))
            print(f"Food item ID {item_id}: Status changed from '{current_status}' to '{new_status}'.")

    conn.commit()
    conn.close()
    print("Expiration status check completed.")

if __name__ == '__main__':
    check_expiration_status() 