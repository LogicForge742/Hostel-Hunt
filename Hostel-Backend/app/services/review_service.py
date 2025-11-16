from ..extensions import db
from ..models.review import Review
from ..models.booking import Booking
from datetime import datetime
from sqlalchemy import func

class ReviewService:
    @staticmethod
    def create_review(user_id, hostel_id, rating, comment=None):
        """Create a new review"""
        # Validate rating
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")

        # Check if user has stayed at the hostel (has a completed booking)
        completed_booking = Booking.query.filter(
            Booking.user_id == user_id,
            Booking.hostel_id == hostel_id,
            Booking.status == 'completed',
            Booking.check_out <= datetime.utcnow().date()
        ).first()

        if not completed_booking:
            raise ValueError("You can only review hostels you've stayed at")

        # Check if user already reviewed this hostel
        existing_review = Review.query.filter_by(
            user_id=user_id,
            hostel_id=hostel_id
        ).first()

        if existing_review:
            raise ValueError("You have already reviewed this hostel")

        try:
            review = Review(
                user_id=user_id,
                hostel_id=hostel_id,
                rating=rating,
                comment=comment
            )

            db.session.add(review)
            db.session.commit()

            # Update landlord rating
            ReviewService.update_landlord_rating(hostel_id)

            return review.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def update_review(review_id, user_id, rating=None, comment=None):
        """Update an existing review"""
        review = Review.query.filter_by(
            id=review_id,
            user_id=user_id
        ).first_or_404()

        try:
            if rating is not None:
                if not (1 <= rating <= 5):
                    raise ValueError("Rating must be between 1 and 5")
                review.rating = rating

            if comment is not None:
                review.comment = comment

            review.updated_at = datetime.utcnow()
            db.session.commit()

            # Update landlord rating
            ReviewService.update_landlord_rating(review.hostel_id)

            return review.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_review(review_id, user_id):
        """Delete a review"""
        review = Review.query.filter_by(
            id=review_id,
            user_id=user_id
        ).first_or_404()

        hostel_id = review.hostel_id

        try:
            db.session.delete(review)
            db.session.commit()

            # Update landlord rating
            ReviewService.update_landlord_rating(hostel_id)

            return True
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_hostel_reviews(hostel_id, page=1, per_page=20):
        """Get all reviews for a hostel"""
        reviews = Review.query.filter_by(hostel_id=hostel_id)\
            .order_by(Review.created_at.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)

        # Calculate average rating
        avg_rating = db.session.query(func.avg(Review.rating))\
            .filter(Review.hostel_id == hostel_id)\
            .scalar() or 0.0

        return {
            'reviews': [review.to_dict() for review in reviews.items],
            'total': reviews.total,
            'pages': reviews.pages,
            'current_page': reviews.page,
            'average_rating': float(avg_rating)
        }

    @staticmethod
    def get_user_reviews(user_id, page=1, per_page=20):
        """Get all reviews by a user"""
        reviews = Review.query.filter_by(user_id=user_id)\
            .order_by(Review.created_at.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)

        return {
            'reviews': [review.to_dict() for review in reviews.items],
            'total': reviews.total,
            'pages': reviews.pages,
            'current_page': reviews.page
        }

    @staticmethod
    def get_review_by_id(review_id):
        """Get a specific review"""
        review = Review.query.get_or_404(review_id)
        return review.to_dict()

    @staticmethod
    def update_landlord_rating(hostel_id):
        """Update the average rating for the landlord of a hostel"""
        from ..models.hostel import Hostel
        from ..models.landlord import Landlord

        hostel = Hostel.query.get(hostel_id)
        if not hostel or not hostel.landlord:
            return

        # Calculate average rating across all hostels for this landlord
        landlord_hostels = Hostel.query.filter_by(landlord_id=hostel.landlord.id).all()
        hostel_ids = [h.id for h in landlord_hostels]

        avg_rating = db.session.query(func.avg(Review.rating))\
            .filter(Review.hostel_id.in_(hostel_ids))\
            .scalar() or 0.0

        review_count = Review.query.filter(Review.hostel_id.in_(hostel_ids)).count()

        try:
            hostel.landlord.rating = float(avg_rating)
            hostel.landlord.review_count = review_count
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_reviews_stats(hostel_id=None, landlord_id=None):
        """Get review statistics"""
        query = Review.query

        if hostel_id:
            query = query.filter_by(hostel_id=hostel_id)
        elif landlord_id:
            # Get all reviews for landlord's hostels
            from ..models.hostel import Hostel
            hostels = Hostel.query.filter_by(landlord_id=landlord_id).all()
            hostel_ids = [h.id for h in hostels]
            query = query.filter(Review.hostel_id.in_(hostel_ids))

        total_reviews = query.count()
        avg_rating = db.session.query(func.avg(Review.rating)).scalar() or 0.0

        # Rating distribution
        rating_counts = {}
        for rating in range(1, 6):
            count = query.filter_by(rating=rating).count()
            rating_counts[f'{rating}_star'] = count

        return {
            'total_reviews': total_reviews,
            'average_rating': float(avg_rating),
            'rating_distribution': rating_counts
        }
