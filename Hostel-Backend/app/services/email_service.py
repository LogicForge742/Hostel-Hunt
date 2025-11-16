import os
from flask import render_template_string
from ..extensions import mail
from flask_mail import Message

class EmailService:
    @staticmethod
    def send_email(to, subject, html_body, text_body=None):
        """Send an email"""
        try:
            msg = Message(
                subject=subject,
                recipients=[to] if isinstance(to, str) else to,
                html=html_body,
                body=text_body
            )
            mail.send(msg)
            return True
        except Exception as e:
            print(f"Email sending failed: {e}")
            return False

    @staticmethod
    def send_booking_confirmation(user_email, booking_data):
        """Send booking confirmation email"""
        subject = f"Booking Confirmed - {booking_data['hostel']['name']}"

        html_template = """
        <html>
        <body>
            <h2>Booking Confirmation</h2>
            <p>Dear {{ booking.user.name }},</p>
            <p>Your booking has been confirmed! Here are the details:</p>

            <div style="border: 1px solid #ddd; padding: 15px; margin: 15px 0;">
                <h3>{{ booking.hostel.name }}</h3>
                <p><strong>Location:</strong> {{ booking.hostel.location }}</p>
                <p><strong>Check-in:</strong> {{ booking.check_in }}</p>
                <p><strong>Check-out:</strong> {{ booking.check_out }}</p>
                <p><strong>Guests:</strong> {{ booking.guests }}</p>
                <p><strong>Total Price:</strong> {{ booking.currency }} {{ booking.total_price }}</p>
                <p><strong>Booking ID:</strong> {{ booking.id }}</p>
            </div>

            <p>Please arrive on time for check-in. Contact the landlord if you need to make changes.</p>

            <p>Best regards,<br>The Hostel Hunt Team</p>
        </body>
        </html>
        """

        html_body = render_template_string(html_template, booking=booking_data)

        return EmailService.send_email(user_email, subject, html_body)

    @staticmethod
    def send_booking_cancellation(user_email, booking_data):
        """Send booking cancellation email"""
        subject = f"Booking Cancelled - {booking_data['hostel']['name']}"

        html_template = """
        <html>
        <body>
            <h2>Booking Cancellation</h2>
            <p>Dear {{ booking.user.name }},</p>
            <p>Your booking has been cancelled. Here are the details:</p>

            <div style="border: 1px solid #ddd; padding: 15px; margin: 15px 0;">
                <h3>{{ booking.hostel.name }}</h3>
                <p><strong>Booking ID:</strong> {{ booking.id }}</p>
                <p><strong>Check-in:</strong> {{ booking.check_in }}</p>
                <p><strong>Check-out:</strong> {{ booking.check_out }}</p>
            </div>

            <p>If this was a mistake or you need assistance, please contact us.</p>

            <p>Best regards,<br>The Hostel Hunt Team</p>
        </body>
        </html>
        """

        html_body = render_template_string(html_template, booking=booking_data)

        return EmailService.send_email(user_email, subject, html_body)

    @staticmethod
    def send_welcome_email(user_email, user_name):
        """Send welcome email to new users"""
        subject = "Welcome to Hostel Hunt!"

        html_template = """
        <html>
        <body>
            <h2>Welcome to Hostel Hunt!</h2>
            <p>Dear {{ user_name }},</p>
            <p>Thank you for joining Hostel Hunt! We're excited to help you find the perfect accommodation.</p>

            <p>Here's what you can do:</p>
            <ul>
                <li>Browse and book hostels</li>
                <li>Read and write reviews</li>
                <li>Manage your bookings</li>
                <li>Contact landlords directly</li>
            </ul>

            <p>Get started by exploring our hostel listings!</p>

            <p>Best regards,<br>The Hostel Hunt Team</p>
        </body>
        </html>
        """

        html_body = render_template_string(html_template, user_name=user_name)

        return EmailService.send_email(user_email, subject, html_body)

    @staticmethod
    def send_password_reset_email(user_email, reset_token):
        """Send password reset email"""
        subject = "Password Reset Request"

        reset_url = f"{os.getenv('FRONTEND_URL', 'http://localhost:3000')}/reset-password?token={reset_token}"

        html_template = """
        <html>
        <body>
            <h2>Password Reset Request</h2>
            <p>You requested a password reset for your Hostel Hunt account.</p>
            <p>Click the link below to reset your password:</p>

            <p><a href="{{ reset_url }}" style="background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Reset Password</a></p>

            <p>This link will expire in 1 hour.</p>
            <p>If you didn't request this reset, please ignore this email.</p>

            <p>Best regards,<br>The Hostel Hunt Team</p>
        </body>
        </html>
        """

        html_body = render_template_string(html_template, reset_url=reset_url)

        return EmailService.send_email(user_email, subject, html_body)

    @staticmethod
    def send_landlord_notification(landlord_email, booking_data):
        """Send notification to landlord about new booking"""
        subject = f"New Booking - {booking_data['hostel']['name']}"

        html_template = """
        <html>
        <body>
            <h2>New Booking Notification</h2>
            <p>You have a new booking for your hostel!</p>

            <div style="border: 1px solid #ddd; padding: 15px; margin: 15px 0;">
                <h3>{{ booking.hostel.name }}</h3>
                <p><strong>Guest:</strong> {{ booking.user.name }} ({{ booking.user.email }})</p>
                <p><strong>Check-in:</strong> {{ booking.check_in }}</p>
                <p><strong>Check-out:</strong> {{ booking.check_out }}</p>
                <p><strong>Guests:</strong> {{ booking.guests }}</p>
                <p><strong>Total Price:</strong> {{ booking.currency }} {{ booking.total_price }}</p>
                <p><strong>Booking ID:</strong> {{ booking.id }}</p>
            </div>

            <p>Please confirm the booking and prepare for the guest's arrival.</p>

            <p>Best regards,<br>The Hostel Hunt Team</p>
        </body>
        </html>
        """

        html_body = render_template_string(html_template, booking=booking_data)

        return EmailService.send_email(landlord_email, subject, html_body)

    @staticmethod
    def send_contact_form_email(contact_data):
        """Send contact form submission to admin"""
        subject = f"Contact Form: {contact_data['subject']}"

        html_template = """
        <html>
        <body>
            <h2>New Contact Form Submission</h2>

            <div style="border: 1px solid #ddd; padding: 15px; margin: 15px 0;">
                <p><strong>From:</strong> {{ contact.name }} ({{ contact.email }})</p>
                <p><strong>Subject:</strong> {{ contact.subject }}</p>
                <p><strong>Message:</strong></p>
                <p>{{ contact.message }}</p>
            </div>

            <p>Please respond to this inquiry as soon as possible.</p>
        </body>
        </html>
        """

        html_body = render_template_string(html_template, contact=contact_data)

        admin_email = os.getenv('ADMIN_EMAIL', 'admin@hostelhunt.com')
        return EmailService.send_email(admin_email, subject, html_body)
