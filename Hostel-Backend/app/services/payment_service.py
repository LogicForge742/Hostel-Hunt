import os
import requests
from datetime import datetime
from ..extensions import db
from ..models.booking import Booking

class PaymentService:
    # M-Pesa Daraja API configuration
    MPESA_CONSUMER_KEY = os.getenv('MPESA_CONSUMER_KEY')
    MPESA_CONSUMER_SECRET = os.getenv('MPESA_CONSUMER_SECRET')
    MPESA_SHORTCODE = os.getenv('MPESA_SHORTCODE', '174379')
    MPESA_PASSKEY = os.getenv('MPESA_PASSKEY')
    MPESA_BASE_URL = 'https://sandbox.safaricom.co.ke' if os.getenv('MPESA_ENV') == 'sandbox' else 'https://api.safaricom.co.ke'

    @staticmethod
    def get_access_token():
        """Get M-Pesa access token"""
        try:
            response = requests.get(
                f"{PaymentService.MPESA_BASE_URL}/oauth/v1/generate?grant_type=client_credentials",
                auth=(PaymentService.MPESA_CONSUMER_KEY, PaymentService.MPESA_CONSUMER_SECRET)
            )
            response.raise_for_status()
            return response.json()['access_token']
        except Exception as e:
            print(f"Failed to get access token: {e}")
            return None

    @staticmethod
    def initiate_stk_push(phone_number, amount, account_reference, transaction_desc):
        """Initiate M-Pesa STK Push"""
        access_token = PaymentService.get_access_token()
        if not access_token:
            return {'error': 'Failed to get access token'}

        # Format phone number (remove + and ensure it starts with 254)
        phone_number = phone_number.replace('+', '')
        if phone_number.startswith('0'):
            phone_number = '254' + phone_number[1:]
        elif not phone_number.startswith('254'):
            phone_number = '254' + phone_number

        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = PaymentService.generate_password(timestamp)

        payload = {
            "BusinessShortCode": PaymentService.MPESA_SHORTCODE,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone_number,
            "PartyB": PaymentService.MPESA_SHORTCODE,
            "PhoneNumber": phone_number,
            "CallBackURL": os.getenv('MPESA_CALLBACK_URL', 'https://yourdomain.com/mpesa/callback'),
            "AccountReference": account_reference,
            "TransactionDesc": transaction_desc
        }

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        try:
            response = requests.post(
                f"{PaymentService.MPESA_BASE_URL}/mpesa/stkpush/v1/processrequest",
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"STK Push failed: {e}")
            return {'error': str(e)}

    @staticmethod
    def generate_password(timestamp):
        """Generate M-Pesa password"""
        import base64
        password_str = PaymentService.MPESA_SHORTCODE + PaymentService.MPESA_PASSKEY + timestamp
        return base64.b64encode(password_str.encode()).decode()

    @staticmethod
    def process_booking_payment(booking_id, phone_number):
        """Process payment for a booking"""
        booking = Booking.query.get_or_404(booking_id)

        if booking.status != 'confirmed':
            return {'error': 'Booking is not in confirmed status'}

        # Check if payment already processed
        # In a real implementation, you'd check a payment table
        if hasattr(booking, 'payment_status') and booking.payment_status == 'paid':
            return {'error': 'Payment already processed'}

        amount = int(booking.total_price)  # M-Pesa expects integer
        account_reference = f"Booking-{booking.id}"
        transaction_desc = f"Payment for {booking.hostel.name}"

        stk_response = PaymentService.initiate_stk_push(
            phone_number, amount, account_reference, transaction_desc
        )

        if 'error' in stk_response:
            return stk_response

        # Store payment initiation details
        # In a real app, you'd save this to a payments table
        payment_data = {
            'booking_id': booking.id,
            'checkout_request_id': stk_response.get('CheckoutRequestID'),
            'merchant_request_id': stk_response.get('MerchantRequestID'),
            'amount': amount,
            'currency': booking.currency,
            'phone_number': phone_number,
            'status': 'pending',
            'initiated_at': datetime.utcnow()
        }

        return {
            'success': True,
            'message': 'Payment initiated. Please check your phone to complete the transaction.',
            'checkout_request_id': stk_response.get('CheckoutRequestID'),
            'payment_data': payment_data
        }

    @staticmethod
    def handle_mpesa_callback(callback_data):
        """Handle M-Pesa callback"""
        try:
            # Extract callback data
            result_code = callback_data['Body']['stkCallback']['ResultCode']
            result_desc = callback_data['Body']['stkCallback']['ResultDesc']
            checkout_request_id = callback_data['Body']['stkCallback']['CheckoutRequestID']

            if result_code == 0:
                # Payment successful
                callback_metadata = callback_data['Body']['stkCallback']['CallbackMetadata']['Item']

                # Extract payment details
                amount = None
                mpesa_receipt_number = None
                transaction_date = None
                phone_number = None

                for item in callback_metadata:
                    if item['Name'] == 'Amount':
                        amount = item['Value']
                    elif item['Name'] == 'MpesaReceiptNumber':
                        mpesa_receipt_number = item['Value']
                    elif item['Name'] == 'TransactionDate':
                        transaction_date = item['Value']
                    elif item['Name'] == 'PhoneNumber':
                        phone_number = item['Value']

                # Update booking payment status
                # In a real implementation, you'd update the payments table and booking
                # For now, we'll just log the successful payment
                print(f"Payment successful: {mpesa_receipt_number}, Amount: {amount}")

                return {'success': True, 'message': 'Payment processed successfully'}

            else:
                # Payment failed
                print(f"Payment failed: {result_desc}")
                return {'success': False, 'message': result_desc}

        except Exception as e:
            print(f"Callback processing failed: {e}")
            return {'success': False, 'message': 'Callback processing failed'}

    @staticmethod
    def check_payment_status(checkout_request_id):
        """Check payment status (query M-Pesa)"""
        access_token = PaymentService.get_access_token()
        if not access_token:
            return {'error': 'Failed to get access token'}

        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = PaymentService.generate_password(timestamp)

        payload = {
            "BusinessShortCode": PaymentService.MPESA_SHORTCODE,
            "Password": password,
            "Timestamp": timestamp,
            "CheckoutRequestID": checkout_request_id
        }

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        try:
            response = requests.post(
                f"{PaymentService.MPESA_BASE_URL}/mpesa/stkpushquery/v1/query",
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Payment status check failed: {e}")
            return {'error': str(e)}

    @staticmethod
    def process_refund(booking_id, reason):
        """Process refund for a booking"""
        booking = Booking.query.get_or_404(booking_id)

        # Check if booking is eligible for refund
        if booking.status not in ['confirmed', 'cancelled']:
            return {'error': 'Booking not eligible for refund'}

        if booking.check_in <= datetime.utcnow().date():
            return {'error': 'Cannot refund booking that has already checked in'}

        # Calculate refund amount (full refund if cancelled before check-in)
        refund_amount = booking.total_price

        # In a real implementation, you'd initiate the refund through M-Pesa
        # For now, we'll just mark the booking as refunded
        booking.status = 'refunded'

        try:
            db.session.commit()

            return {
                'success': True,
                'message': 'Refund processed successfully',
                'refund_amount': refund_amount,
                'booking_id': booking.id
            }
        except Exception as e:
            db.session.rollback()
            return {'error': 'Failed to process refund'}

    @staticmethod
    def get_payment_history(user_id=None, booking_id=None, page=1, per_page=20):
        """Get payment history"""
        # In a real implementation, you'd query a payments table
        # For now, return mock data
        return {
            'payments': [],
            'total': 0,
            'pages': 0,
            'current_page': page
        }

    @staticmethod
    def validate_payment_amount(booking_id, amount):
        """Validate payment amount against booking total"""
        booking = Booking.query.get_or_404(booking_id)

        if float(amount) != booking.total_price:
            return False, f"Payment amount {amount} does not match booking total {booking.total_price}"

        return True, "Amount validated successfully"
