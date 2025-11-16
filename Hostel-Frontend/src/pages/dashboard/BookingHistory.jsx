import { Link } from 'react-router-dom';
import { useBooking } from '../../context/BookingContext.jsx';

export default function BookingHistory() {
  const { bookings, getHostelById } = useBooking();

  const getStatusColor = (status) => {
    switch (status) {
      case 'confirmed':
        return 'text-green-600 bg-green-100';
      case 'upcoming':
        return 'text-blue-600 bg-blue-100';
      case 'completed':
        return 'text-gray-600 bg-gray-100';
      case 'cancelled':
        return 'text-red-600 bg-red-100';
      default:
        return 'text-gray-600 bg-gray-100';
    }
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">My Bookings</h1>

      {bookings.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-500 mb-4">You haven't made any bookings yet.</p>
          <Link
            to="/"
            className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700"
          >
            Start Exploring
          </Link>
        </div>
      ) : (
        <div className="space-y-6">
          {bookings.map((booking) => {
            const hostel = getHostelById(booking.hostelId);
            if (!hostel) return null;

            return (
              <div key={booking.id} className="bg-white border rounded-lg p-6 shadow-sm">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="text-xl font-semibold">{hostel.name}</h3>
                    <p className="text-gray-600">{hostel.location}</p>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(booking.status)}`}>
                    {booking.status.charAt(0).toUpperCase() + booking.status.slice(1)}
                  </span>
                </div>

                <div className="grid md:grid-cols-4 gap-4 mb-4">
                  <div>
                    <p className="text-sm text-gray-500">Check-in</p>
                    <p className="font-medium">{booking.check_in ? new Date(booking.check_in).toLocaleDateString() : 'Invalid date'}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-500">Check-out</p>
                    <p className="font-medium">{booking.check_out ? new Date(booking.check_out).toLocaleDateString() : 'Invalid date'}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-500">Guests</p>
                    <p className="font-medium">{booking.guests}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-500">Total</p>
                    <p className="font-medium">KSh {booking.total_price || booking.totalPrice || 'N/A'}</p>
                  </div>
                </div>

                <div className="flex justify-between items-center">
                  <p className="text-sm text-gray-500">
                    Booked on {new Date(booking.bookingDate).toLocaleDateString()}
                  </p>
                  {booking.status === 'upcoming' && (
                    <Link
                      to={`/booking/${booking.hostelId}`}
                      className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 text-sm"
                    >
                      Modify Booking
                    </Link>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
