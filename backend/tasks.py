from celery_app import make_celery
from models.models import db, Booking, Trek, User
import csv
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def register_tasks(celery, app):
    
    @celery.task
    def export_bookings_csv(user_id):
        with app.app_context():
            bookings =Booking.query.filter_by(user_id= user_id).all()
            filename = f'exports/bookings_user_{user_id}.csv'
            os.makedirs('exports', exist_ok=True)

            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['User' ,'Trek Name', 'Location', 'Status', 'Booking Date'])

                for b in bookings:
                    trek = Trek.query.get(b.trek_id)
                    writer.writerow([b.user_id,trek.name, trek.location, b.status, b.booking_date ])


    
    

    @celery.task
    def send_monthly_report():
        with app.app_context():
            total_treks = Trek.query.count()
            total_bookings = Booking.query.count()
            
            # Popular treks — jisme sabse zyada bookings hain
            treks = Trek.query.all()
            popular = []
            for t in treks:
                count = Booking.query.filter_by(trek_id=t.id).count()
                popular.append((t.name, count))
            popular.sort(key=lambda x: x[1], reverse=True)
            
            html_content = f"""
            <h2>Monthly Trekking Report</h2>
            <p>Total Treks: {total_treks}</p>
            <p>Total Bookings: {total_bookings}</p>
            <h3>Popular Treks</h3>
            <ul>
            """
            for name, count in popular[:5]:
                html_content += f"<li>{name} — {count} bookings</li>"
            html_content += "</ul>"
            
            msg = MIMEMultipart()
            msg['From'] = app.config['EMAIL_ADDRESS']
            msg['To'] = app.config['EMAIL_ADDRESS']  
            msg['Subject'] = 'Monthly Trekking Report'
            msg.attach(MIMEText(html_content, 'html'))
            
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(app.config['EMAIL_ADDRESS'], app.config['EMAIL_PASSWORD'])
                server.send_message(msg)


    return export_bookings_csv, send_monthly_report            

      