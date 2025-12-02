from ..extensions import db
from .email_service import EmailService
from ..models.user import User
from ..models.booking import Booking
from datetime import datetime, timedelta
import json

class NotificationService:
    @staticmethod
    def notify_booking_created(booking_obj):
        """Send notifications when a booking is created"""
        try:
            # Check if relationships are loaded
            if not booking_obj.user:
                print(f"Notification failed: User not found for booking {booking_obj.id}")
                return False

            if not booking_obj.hostel:
                print(f"Notification failed: Hostel not found for booking {booking_obj.id}")
                return False

            if not booking_obj.hostel.landlord:
                print(f"Notification failed: Landlord not found for hostel {booking_obj.hostel.id}")
                return False

            # Use the booking object to get related data safely
            booking_data_dict = booking_obj.to_dict()

            # Notify user
            EmailService.send_booking_confirmation(
                booking_obj.user.email,
                booking_data_dict
            )

            # Notify landlord - with proper null checks
            landlord_email = None
            if booking_obj.hostel.landlord.contact_email:
                landlord_email = booking_obj.hostel.landlord.contact_email
            elif booking_obj.hostel.landlord.user and booking_obj.hostel.landlord.user.email:
                landlord_email = booking_obj.hostel.landlord.user.email

            if not landlord_email:
                print(f"Notification failed: No email found for landlord of booking {booking_obj.id}")
                return False

            EmailService.send_landlord_notification(landlord_email, booking_data_dict)

            return True
        except Exception as e:
            print(f"Notification failed: {e}")
            return False

    @staticmethod
    def notify_booking_cancelled(booking_data):
        """Send notifications when a booking is cancelled"""
        try:
            # Notify user
            EmailService.send_booking_cancellation(
                booking_data['user']['email'],
                booking_data
            )

            # Notify landlord
            landlord_email = booking_data['hostel']['landlord']['contact_email'] or booking_data['hostel']['landlord']['user']['email']

            # Send cancellation notification to landlord
            subject = f"Booking Cancelled - {booking_data['hostel']['name']}"
            html_body = f"""
            <html>
            <body>
                <h2>Booking Cancellation Notice</h2>
                <p>A booking for your hostel has been cancelled.</p>
                <div style="border: 1px solid #ddd; padding: 15px; margin: 15px 0;">
                    <h3>{booking_data['hostel']['name']}</h3>
                    <p><strong>Guest:</strong> {booking_data['user']['name']}</p>
                    <p><strong>Booking ID:</strong> {booking_data['id']}</p>
                    <p><strong>Check-in:</strong> {booking_data['check_in']}</p>
                    <p><strong>Check-out:</strong> {booking_data['check_out']}</p>
                </div>
                <p>Best regards,<br>The Hostel Hunt Team</p>
            </body>
            </html>
            """

            EmailService.send_email(landlord_email, subject, html_body)

            return True
        except Exception as e:
            print(f"Notification failed: {e}")
            return False

    @staticmethod
    def notify_upcoming_checkins():
        """Send reminders for upcoming check-ins (run daily)"""
        tomorrow = datetime.utcnow().date() + timedelta(days=1)

        upcoming_bookings = Booking.query.filter(
            Booking.check_in == tomorrow,
            Booking.status == 'confirmed'
        ).all()

        notifications_sent = 0
        for booking in upcoming_bookings:
            try:
                subject = f"Check-in Reminder - {booking.hostel.name}"

                html_template = """
                <html>
                <body>
                    <h2>Check-in Reminder</h2>
                    <p>Dear {{ booking.user.name }},</p>
                    <p>This is a reminder that you have a check-in tomorrow!</p>

                    <div style="border: 1px solid #ddd; padding: 15px; margin: 15px 0;">
                        <h3>{{ booking.hostel.name }}</h3>
                        <p><strong>Location:</strong> {{ booking.hostel.location }}</p>
                        <p><strong>Check-in:</strong> {{ booking.check_in }}</p>
                        <p><strong>Check-out:</strong> {{ booking.check_out }}</p>
                        <p><strong>Booking ID:</strong> {{ booking.id }}</p>
                    </div>

                    <p>Please arrive on time and bring valid ID for check-in.</p>

                    <p>Best regards,<br>The Hostel Hunt Team</p>
                </body>
                </html>
                """

                html_body = f"""
                <html>
                <body>
                    <h2>Check-in Reminder</h2>
                    <p>Dear {booking.user.name},</p>
                    <p>This is a reminder that you have a check-in tomorrow!</p>

                    <div style="border: 1px solid #ddd; padding: 15px; margin: 15px 0;">
                        <h3>{booking.hostel.name}</h3>
                        <p><strong>Location:</strong> {booking.hostel.location}</p>
                        <p><strong>Check-in:</strong> {booking.check_in}</p>
                        <p><strong>Check-out:</strong> {booking.check_out}</p>
                        <p><strong>Booking ID:</strong> {booking.id}</p>
                    </div>

                    <p>Please arrive on time and bring valid ID for check-in.</p>

                    <p>Best regards,<br>The Hostel Hunt Team</p>
                </body>
                </html>
                """

                EmailService.send_email(booking.user.email, subject, html_body)
                notifications_sent += 1

            except Exception as e:
                print(f"Failed to send reminder for booking {booking.id}: {e}")

        return notifications_sent

    @staticmethod
    def notify_checkout_reminders():
        """Send reminders for upcoming check-outs (run daily)"""
        today = datetime.utcnow().date()

        checkout_bookings = Booking.query.filter(
            Booking.check_out == today,
            Booking.status == 'confirmed'
        ).all()

        notifications_sent = 0
        for booking in checkout_bookings:
            try:
                subject = f"Check-out Reminder - {booking.hostel.name}"

                html_body = f"""
                <html>
                <body>
                    <h2>Check-out Reminder</h2>
                    <p>Dear {booking.user.name},</p>
                    <p>This is a reminder that today is your check-out day.</p>

                    <div style="border: 1px solid #ddd; padding: 15px; margin: 15px 0;">
                        <h3>{booking.hostel.name}</h3>
                        <p><strong>Location:</strong> {booking.hostel.location}</p>
                        <p><strong>Check-out:</strong> {booking.check_out}</p>
                        <p><strong>Booking ID:</strong> {booking.id}</p>
                    </div>

                    <p>Please ensure you check out on time. Contact the landlord if you need a late check-out.</p>

                    <p>Best regards,<br>The Hostel Hunt Team</p>
                </body>
                </html>
                """

                EmailService.send_email(booking.user.email, subject, html_body)
                notifications_sent += 1

            except Exception as e:
                print(f"Failed to send checkout reminder for booking {booking.id}: {e}")

        return notifications_sent

    @staticmethod
    def notify_review_reminder():
        """Send reminders to leave reviews after checkout (run daily)"""
        three_days_ago = datetime.utcnow().date() - timedelta(days=3)

        completed_bookings = Booking.query.filter(
            Booking.check_out == three_days_ago,
            Booking.status == 'completed'
        ).all()

        notifications_sent = 0
        for booking in completed_bookings:
            # Check if user already reviewed
            from ..models.review import Review
            existing_review = Review.query.filter_by(
                user_id=booking.user_id,
                hostel_id=booking.hostel_id
            ).first()

            if existing_review:
                continue

            try:
                subject = f"How was your stay at {booking.hostel.name}?"

                html_body = f"""
                <html>
                <body>
                    <h2>How was your stay?</h2>
                    <p>Dear {booking.user.name},</p>
                    <p>We hope you enjoyed your stay at {booking.hostel.name}!</p>
                    <p>Your feedback helps other students find great accommodation.</p>

                    <div style="border: 1px solid #ddd; padding: 15px; margin: 15px 0;">
                        <h3>{booking.hostel.name}</h3>
                        <p><strong>Check-out:</strong> {booking.check_out}</p>
                        <p><strong>Booking ID:</strong> {booking.id}</p>
                    </div>

                    <p><a href="#" style="background-color: #28a745; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Leave a Review</a></p>

                    <p>Best regards,<br>The Hostel Hunt Team</p>
                </body>
                </html>
                """

                EmailService.send_email(booking.user.email, subject, html_body)
                notifications_sent += 1

            except Exception as e:
                print(f"Failed to send review reminder for booking {booking.id}: {e}")

        return notifications_sent

    @staticmethod
    def notify_hostel_approval(hostel_data):
        """Notify landlord when hostel is approved"""
        try:
            landlord_email = hostel_data['landlord']['contact_email'] or hostel_data['landlord']['user']['email']

            subject = f"Your hostel has been approved - {hostel_data['name']}"

            html_body = f"""
            <html>
            <body>
                <h2>Hostel Approved!</h2>
                <p>Dear {hostel_data['landlord']['business_name'] or hostel_data['landlord']['user']['name']},</p>
                <p>Congratulations! Your hostel listing has been approved and is now live on Hostel Hunt.</p>

                <div style="border: 1px solid #ddd; padding: 15px; margin: 15px 0;">
                    <h3>{hostel_data['name']}</h3>
                    <p><strong>Location:</strong> {hostel_data['location']}</p>
                    <p><strong>Price:</strong> {hostel_data['currency']} {hostel_data['price']}</p>
                </div>

                <p>Students can now book your hostel. Check your dashboard for new bookings!</p>

                <p>Best regards,<br>The Hostel Hunt Team</p>
            </body>
            </html>
            """

            return EmailService.send_email(landlord_email, subject, html_body)
        except Exception as e:
            print(f"Approval notification failed: {e}")
            return False

    @staticmethod
    def notify_payment_received(booking_data, payment_data):
        """Notify user and landlord of successful payment"""
        try:
            # Notify user
            subject = f"Payment Confirmed - Booking {booking_data['id']}"
            html_body = f"""
            <html>
            <body>
                <h2>Payment Confirmed</h2>
                <p>Dear {booking_data['user']['name']},</p>
                <p>Your payment has been processed successfully!</p>

                <div style="border: 1px solid #ddd; padding: 15px; margin: 15px 0;">
                    <h3>{booking_data['hostel']['name']}</h3>
                    <p><strong>Amount Paid:</strong> {payment_data['currency']} {payment_data['amount']}</p>
                    <p><strong>Transaction ID:</strong> {payment_data['transaction_id']}</p>
                    <p><strong>Booking ID:</strong> {booking_data['id']}</p>
                </div>

                <p>Best regards,<br>The Hostel Hunt Team</p>
            </body>
            </html>
            """

            EmailService.send_email(booking_data['user']['email'], subject, html_body)

            # Notify landlord
            landlord_email = booking_data['hostel']['landlord']['contact_email'] or booking_data['hostel']['landlord']['user']['email']

            html_body = f"""
            <html>
            <body>
                <h2>Payment Received</h2>
                <p>Dear {booking_data['hostel']['landlord']['business_name'] or booking_data['hostel']['landlord']['user']['name']},</p>
                <p>You have received a payment for your hostel booking.</p>

                <div style="border: 1px solid #ddd; padding: 15px; margin: 15px 0;">
                    <h3>{booking_data['hostel']['name']}</h3>
                    <p><strong>Amount Received:</strong> {payment_data['currency']} {payment_data['amount']}</p>
                    <p><strong>Transaction ID:</strong> {payment_data['transaction_id']}</p>
                    <p><strong>Guest:</strong> {booking_data['user']['name']}</p>
                </div>

                <p>Best regards,<br>The Hostel Hunt Team</p>
            </body>
            </html>
            """

            EmailService.send_email(landlord_email, subject, html_body)

            return True
        except Exception as e:
            print(f"Payment notification failed: {e}")
            return False
