import React, { useState, useEffect } from "react";
import axios from "axios";
import { API_BASE_URL } from "../../utils/api";

const HostelBookings = () => {
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchBookings();
  }, []);

  const fetchBookings = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem("token");
      const res = await axios.get(`${API_BASE_URL}/bookings/landlord/bookings`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setBookings(res.data.bookings || []);
    } catch (err) {
      console.error("Failed to fetch bookings:", err);
      setError("Failed to load bookings");
    } finally {
      setLoading(false);
    }
  };

  // ---------------------------
  // HANDLE STATUS CHANGE
  // ---------------------------
  const updateStatus = async (id, newStatus) => {
    try {
      const token = localStorage.getItem("token");
      await axios.put(`${API_BASE_URL}/bookings/${id}/status`, {
        status: newStatus
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });

      // Update local state
      const updated = bookings.map((b) =>
        b.id === id ? { ...b, status: newStatus } : b
      );
      setBookings(updated);
    } catch (err) {
      console.error("Failed to update booking status:", err);
      setError("Failed to update booking status");
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Hostel Bookings</h1>
      {error && <p className="text-red-500 mb-4">{error}</p>}

      {bookings.length === 0 ? (
        <p>No bookings found.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {bookings.map((booking) => (
            <div
              key={booking.id}
              className="border rounded-lg p-5 shadow-sm bg-white"
            >
              <h2 className="text-xl font-semibold mb-2">
                {booking.hostel_name}
              </h2>

              <p>
                <strong>Customer:</strong> {booking.customer_name}
              </p>
              <p>
                <strong>Email:</strong> {booking.customer_email}
              </p>
              <p>
                <strong>Check-In:</strong> {booking.check_in}
              </p>
              <p>
                <strong>Check-Out:</strong> {booking.check_out}
              </p>
              <p>
                <strong>Guests:</strong> {booking.guests}
              </p>

              <p className="mt-3">
                <strong>Status: </strong>
                <span
                  className={`px-3 py-1 rounded text-white ${
                    booking.status === "confirmed"
                      ? "bg-blue-600"
                      : booking.status === "completed"
                      ? "bg-green-600"
                      : booking.status === "cancelled"
                      ? "bg-red-600"
                      : "bg-gray-500"
                  }`}
                >
                  {booking.status.toUpperCase()}
                </span>
              </p>

              {/* ACTION BUTTONS */}
              <div className="flex gap-3 mt-4">
                {booking.status === "confirmed" && (
                  <button
                    onClick={() => updateStatus(booking.id, "completed")}
                    className="bg-green-600 text-white px-4 py-1 rounded"
                  >
                    Complete
                  </button>
                )}
                {booking.status === "confirmed" && (
                  <button
                    onClick={() => updateStatus(booking.id, "cancelled")}
                    className="bg-red-600 text-white px-4 py-1 rounded"
                  >
                    Cancel
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default HostelBookings;
