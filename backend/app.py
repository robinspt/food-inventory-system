from flask import Flask, request, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime, timedelta
from flask_cors import CORS # Import CORS

app = Flask(__name__)
CORS(app) # Enable CORS for all routes
app.config['SECRET_KEY'] = 'your_secret_key_here' # Change this to a strong, random key

DATABASE = 'site.db'

def get_db_connection():
    db_path = os.path.join(app.root_path, DATABASE)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row # This allows access to columns by name
    return conn

def calculate_expiration_date(production_date_str, expiry_period_value, expiry_period_unit):
    production_date = datetime.strptime(production_date_str, '%Y-%m-%d')
    if expiry_period_unit.lower() == 'days':
        expiration_date = production_date + timedelta(days=expiry_period_value)
    elif expiry_period_unit.lower() == 'months':
        # Simple month calculation, might need more robust logic for edge cases
        year = production_date.year + (production_date.month + expiry_period_value - 1) // 12
        month = (production_date.month + expiry_period_value - 1) % 12 + 1
        day = min(production_date.day, (datetime(year, month + 1, 1) - timedelta(days=1)).day if month < 12 else (datetime(year + 1, 1, 1) - timedelta(days=1)).day)
        expiration_date = datetime(year, month, day)
    else:
        raise ValueError("Invalid expiry_period_unit. Must be 'days' or 'months'.")
    return expiration_date.strftime('%Y-%m-%d')

@app.route('/')
def hello_world():
    return "Hello, World! This is the Food Inventory Backend."

@app.route('/api/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if username already exists
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    existing_user = cursor.fetchone()
    if existing_user:
        conn.close()
        return jsonify({'error': 'Username already exists'}), 409

    # Hash the password and insert new user
    hashed_password = generate_password_hash(password)
    try:
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                       (username, hashed_password))
        conn.commit()
        conn.close()
        return jsonify({'message': 'User registered successfully'}), 201
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'error': 'Database error during registration'}), 500

@app.route('/api/login', methods=['POST'])
def login_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if user and check_password_hash(user['password_hash'], password):
        # In a real application, you'd return a token here (e.g., JWT)
        return jsonify({'message': 'Login successful', 'username': user['username']}), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

@app.route('/api/food_items', methods=['POST'])
def add_food_item():
    data = request.get_json()

    name = data.get('name')
    quantity = data.get('quantity')
    storage_location = data.get('storage_location', '')

    production_date_str = None
    expiry_period_value = None
    expiry_period_unit = None
    expiration_date_str = None

    # Determine which date input method was used
    if 'expiration_date' in data and data['expiration_date']:
        # Case 1: Direct expiration date provided
        expiration_date_str = data['expiration_date']
        # For DB NOT NULL constraints, set dummy production date and expiry period
        production_date_str = data.get('production_date', expiration_date_str) # Could be same as expiry or current date
        expiry_period_value = data.get('expiry_period_value', 0)
        expiry_period_unit = data.get('expiry_period_unit', 'days')
    elif 'production_date' in data and data['production_date'] and \
         'expiry_period_value' in data and data['expiry_period_value'] is not None and \
         'expiry_period_unit' in data and data['expiry_period_unit']:
        # Case 2: Production date and expiry period provided
        production_date_str = data['production_date']
        expiry_period_value = data['expiry_period_value']
        expiry_period_unit = data['expiry_period_unit']
        try:
            expiration_date_str = calculate_expiration_date(production_date_str, expiry_period_value, expiry_period_unit)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
    else:
        return jsonify({'error': 'Missing required date fields (either production_date/expiry_period or expiration_date)'}), 400

    # Validate other required fields
    if not name or not quantity:
        return jsonify({'error': 'Missing required field: name or quantity'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO food_items (name, production_date, expiry_period_value, expiry_period_unit, quantity, storage_location, expiration_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (name, production_date_str, expiry_period_value, expiry_period_unit, quantity, storage_location, expiration_date_str))
        conn.commit()
        return jsonify({'message': 'Food item added successfully'}), 201
    except sqlite3.Error as e:
        return jsonify({'error': f'Database error: {e}'}), 500
    finally:
        conn.close()

@app.route('/api/food_items', methods=['GET'])
def get_food_items():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM food_items")
    food_items = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(food_items), 200

@app.route('/api/food_items/<int:item_id>', methods=['GET'])
def get_food_item(item_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM food_items WHERE id = ?", (item_id,))
    food_item = cursor.fetchone()
    conn.close()

    if food_item:
        return jsonify(dict(food_item)), 200
    else:
        return jsonify({'error': 'Food item not found'}), 404

@app.route('/api/food_items/<int:item_id>', methods=['PUT'])
def update_food_item(item_id):
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if item exists
    cursor.execute("SELECT * FROM food_items WHERE id = ?", (item_id,))
    existing_item = cursor.fetchone()
    if not existing_item:
        conn.close()
        return jsonify({'error': 'Food item not found'}), 404

    # Build update query dynamically
    set_clauses = []
    params = []
    update_expiration_date = False

    if 'name' in data: set_clauses.append("name = ?"); params.append(data['name'])
    if 'production_date' in data: 
        set_clauses.append("production_date = ?"); params.append(data['production_date'])
        update_expiration_date = True
    if 'expiry_period_value' in data: 
        set_clauses.append("expiry_period_value = ?"); params.append(data['expiry_period_value'])
        update_expiration_date = True
    if 'expiry_period_unit' in data: 
        set_clauses.append("expiry_period_unit = ?"); params.append(data['expiry_period_unit'])
        update_expiration_date = True
    if 'quantity' in data: set_clauses.append("quantity = ?"); params.append(data['quantity'])
    if 'storage_location' in data: set_clauses.append("storage_location = ?"); params.append(data['storage_location'])
    if 'status' in data: set_clauses.append("status = ?"); params.append(data['status'])

    if not set_clauses:
        return jsonify({'message': 'No fields to update'}), 400

    # Recalculate expiration date if relevant fields are updated
    if update_expiration_date:
        current_production_date = data.get('production_date', existing_item['production_date'])
        current_expiry_value = data.get('expiry_period_value', existing_item['expiry_period_value'])
        current_expiry_unit = data.get('expiry_period_unit', existing_item['expiry_period_unit'])
        try:
            new_expiration_date = calculate_expiration_date(current_production_date, current_expiry_value, current_expiry_unit)
            set_clauses.append("expiration_date = ?")
            params.append(new_expiration_date)
        except ValueError as e:
            conn.close()
            return jsonify({'error': str(e)}), 400

    set_clauses.append("updated_at = CURRENT_TIMESTAMP")

    query = f"UPDATE food_items SET { ', '.join(set_clauses)} WHERE id = ?"
    params.append(item_id)

    try:
        cursor.execute(query, tuple(params))
        conn.commit()
        return jsonify({'message': 'Food item updated successfully'}), 200
    except sqlite3.Error as e:
        return jsonify({'error': f'Database error: {e}'}), 500
    finally:
        conn.close()

@app.route('/api/food_items/<int:item_id>', methods=['DELETE'])
def delete_food_item(item_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM food_items WHERE id = ?", (item_id,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({'error': 'Food item not found'}), 404
        return jsonify({'message': 'Food item deleted successfully'}), 200
    except sqlite3.Error as e:
        return jsonify({'error': f'Database error: {e}'}), 500
    finally:
        conn.close()

@app.route('/api/notifications', methods=['GET'])
def get_notifications():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Fetch items that are 'warning' or 'expired'
    cursor.execute("SELECT * FROM food_items WHERE status = 'warning' OR status = 'expired' ORDER BY expiration_date ASC")
    notifications = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(notifications), 200

if __name__ == '__main__':
    app.run(debug=True) 