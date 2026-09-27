from flask import Flask, request, render_template_string
import sqlite3
import random
import string
from datetime import datetime, timedelta

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('licenses.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS licenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            duration_days INTEGER NOT NULL,
            is_active BOOLEAN NOT NULL DEFAULT 1,
            expiry_date TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# دالة لتوليد كود عشوائي فريد
def generate_random_code(prefix):
    chars = string.ascii_uppercase + string.digits
    suffix = ''.join(random.choices(chars, k=6))
    return f"SNAP-{prefix}-{suffix}"

# دالة لتوليد الأكواد بالجملة (10 من كل نوع)
def generate_bulk_codes():
    conn = sqlite3.connect('licenses.db')
    cursor = conn.cursor()
    
    # الفترات: (الاسم المختصر، عدد الأيام)
    categories = [
        ('DAY', 1),
        ('WEEK', 7),
        ('MONTH', 30),
        ('YEAR', 365)
    ]
    
    for prefix, days in categories:
        for _ in range(10): # توليد 10 أكواد لكل فئة
            code = generate_random_code(prefix)
            try:
                cursor.execute("INSERT INTO licenses (code, duration_days) VALUES (?, ?)", (code, days))
                conn.commit()
            except:
                pass # لو الكود موجود مسبقاً يتخطاه
                
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('licenses.db')
    cursor = conn.cursor()
    cursor.execute("SELECT code, duration_days, is_active, expiry_date FROM licenses ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    
    rows_html = ""
    for r in rows:
        status = 'نشط' if r[2] else 'معطل'
        expiry = r[3] if r[3] else 'لم يُستخدم بعد'
        rows_html += f"<tr><td>{r[0]}</td><td>{r[1]} يوم</td><td>{status}</td><td>{expiry}</td></tr>"

    return f"""
    <html lang='ar' dir='rtl'>
    <head><meta charset='UTF-8'><title>لوحة التحكم - الأكواد التلقائية</title></head>
    <body style='font-family: Tahoma; padding: 20px; background: #f4f7f6;'>
        <h2>لوحة تحكم اشتراكات سناب (الأكواد التلقائية)</h2>
        
        <div style='background: white; padding: 15px; border-radius: 6px; width: 400px; margin-bottom: 20px;'>
            <h3>توليد تلقائي بالجملة</h3>
            <p>اضغط للأسفل لتوليد (10 أيام، 10 أسابيع، 10 شهور، 10 سنين) دفعة واحدة تلقائياً!</p>
            <form action='/auto-gen' method='POST'>
                <button type='submit' style='padding: 12px; width: 100%; background: #28a745; color: white; border: none; border-radius: 4px; cursor: pointer; font-weight: bold;'>توليد دفعة جديدة تلقائياً</button>
            </form>
        </div>

        <h3>جميع الأكواد الحالية:</h3>
        <table border='1' style='width: 100%; background: white; border-collapse: collapse; text-align: center;'>
            <tr style='background: #007bff; color: white; padding: 10px;'><th>الكود</th><th>المدة</th><th>الحالة</th><th>التاريخ</th></tr>
            {rows_html}
        </table>
    </body>
    </html>
    """

@app.route('/auto-gen', methods=['POST'])
def auto_gen():
    generate_bulk_codes()
    return "<script>window.location='/';</script>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)