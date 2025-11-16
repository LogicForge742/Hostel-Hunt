from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.booking_service import BookingService
from ..services.notification_service import NotificationService
from ..services.payment_service import PaymentService
from ..middleware.auth_middleware import landlord_required
from ..utils.validator import is_valid_phone
from datetime import datetime

bookings_bp = Blueprint("bookings", __name__, url_prefix="/bookings")

@bookings_bp.post("/")
@jwt_required()
def create_booking():
    """Create a new booking"""
    user_id = get_jwt_identity()
    data = request.get_json()

    # Validate required fields
    required_fields = ['hostel_id', 'check_in', 'check_out', 'guests', 'phone_number']
    for field in required_fields:
        if field not in data:
            return jsonify({"message": f"{field} is required"}), 400

    # Validate phone number
    if not is_valid_phone(data['phone_number']):
        return jsonify({"message": "Invalid phone number"}), 400

    try:
        booking = BookingService.create_booking(
            user_id=user_id,
            hostel_id=data['hostel_id'],
            check_in=data['check_in'],
            check_out=data['check_out'],
            guests=data['guests']
        )

        # Send notifications
        NotificationService.notify_booking_created(booking)

        return jsonify({"message": "Booking created successfully", "booking": booking}), 201

    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": "Failed to create booking", "error": str(e)}), 500

@bookings_bp.get("/")
@jwt_required()
def get_user_bookings():
    """Get current user's bookings"""
    user_id = get_jwt_identity()

    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        status = request.args.get('status')

        result = BookingService.get_user_bookings(
            user_id=user_id,
            page=page,
            per_page=per_page,
            status=status
        )
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"message": "Failed to fetch bookings", "error": str(e)}), 500

@bookings_bp.get("/<int:booking_id>")
@jwt_required()
def get_booking(booking_id):
    """Get a specific booking"""
    user_id = get_jwt_identity()

    try:
        booking = BookingService.get_booking_by_id(booking_id, user_id)
        return jsonify(booking), 200
    except Exception as e:
        return jsonify({"message": "Booking not found"}), 404

@bookings_bp.put("/<int:booking_id>/cancel")
@jwt_required()
def cancel_booking(booking_id):
    """Cancel a booking"""
    user_id = get_jwt_identity()

    try:
        booking = BookingService.cancel_booking(booking_id, user_id)

        # Send cancellation notifications
        NotificationService.notify_booking_cancelled(booking)

        return jsonify({"message": "Booking cancelled successfully", "booking": booking}), 200

    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": "Failed to cancel booking", "error": str(e)}), 500

@bookings_bp.get("/hostel/<int:hostel_id>")
@jwt_required()
@landlord_required
def get_hostel_bookings(hostel_id):
    """Get bookings for a specific hostel (landlord only)"""
    user_id = get_jwt_identity()

    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))

        result = BookingService.get_hostel_bookings(
            hostel_id=hostel_id,
            landlord_id=user_id,
            page=page,
            per_page=per_page
        )
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"message": "Failed to fetch hostel bookings", "error": str(e)}), 500

@bookings_bp.put("/<int:booking_id>/status")
@jwt_required()
@landlord_required
def update_booking_status(booking_id):
    """Update booking status (landlord/admin only)"""
    user_id = get_jwt_identity()
    data = request.get_json()

    status = data.get('status')
    if not status:
        return jsonify({"message": "Status is required"}), 400

    try:
        booking = BookingService.update_booking_status(booking_id, status, user_id)
        return jsonify({"message": "Booking status updated successfully", "booking": booking}), 200

    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": "Failed to update booking status", "error": str(e)}), 500

@bookings_bp.get("/landlord/bookings")
@jwt_required()
@landlord_required
def get_landlord_bookings():
    """Get all bookings for all hostels owned by the landlord"""
    user_id = get_jwt_identity()

    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        status = request.args.get('status')

        result = BookingService.get_landlord_bookings(
            landlord_id=user_id,
            page=page,
            per_page=per_page,
            status=status
        )
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"message": "Failed to fetch landlord bookings", "error": str(e)}), 500

@bookings_bp.get("/stats/<int:hostel_id>")
@jwt_required()
@landlord_required
def get_booking_stats(hostel_id):
    """Get booking statistics for a hostel"""
    user_id = get_jwt_identity()

    try:
        stats = BookingService.get_booking_stats(hostel_id=hostel_id, landlord_id=user_id)
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({"message": "Failed to get booking stats", "error": str(e)}), 500

@bookings_bp.post("/<int:booking_id>/pay")
@jwt_required()
def initiate_payment(booking_id):
    """Initiate payment for a booking"""
    user_id = get_jwt_identity()
    data = request.get_json()

    phone_number = data.get('phone_number')
    if not phone_number:
        return jsonify({"message": "Phone number is required for payment"}), 400

    if not is_valid_phone(phone_number):
        return jsonify({"message": "Invalid phone number"}), 400

    try:
        # Verify booking belongs to user
        booking = BookingService.get_booking_by_id(booking_id, user_id)

        # Initiate M-Pesa payment
        payment_result = PaymentService.process_booking_payment(booking_id, phone_number)

        if 'error' in payment_result:
            return jsonify({"message": payment_result['error']}), 400

        return jsonify({
            "message": "Payment initiated successfully",
            "payment": payment_result
        }), 200

    except Exception as e:
        return jsonify({"message": "Failed to initiate payment", "error": str(e)}), 500

@bookings_bp.post("/payment/callback")
def mpesa_callback():
    """Handle M-Pesa payment callback"""
    try:
        callback_data = request.get_json()

        # Process the callback
        result = PaymentService.handle_mpesa_callback(callback_data)

        if result.get('success'):
            # Payment successful - could trigger notifications here
            return jsonify({"message": "Payment processed successfully"}), 200
        else:
            return jsonify({"message": result.get('message', 'Payment processing failed')}), 400

    except Exception as e:
        print(f"Callback processing error: {e}")
        return jsonify({"message": "Callback processing failed"}), 500

@bookings_bp.get("/payment/<int:booking_id>/status")
@jwt_required()
def check_payment_status(booking_id):
    """Check payment status for a booking"""
    user_id = get_jwt_identity()

    try:
        # Verify booking belongs to user
        booking = BookingService.get_booking_by_id(booking_id, user_id)

        # In a real implementation, you'd check the payment status from your payments table
        # For now, return a mock response
        return jsonify({
            "booking_id": booking_id,
            "status": "pending",  # This would be checked from your payment records
            "message": "Payment status checked"
        }), 200

    except Exception as e:
        return jsonify({"message": "Failed to check payment status", "error": str(e)}), 500
