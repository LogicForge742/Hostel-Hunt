import React, { useState } from "react";

const HostelBookings = () => {

  const initialBookings = [
    {
      id: 1,
      hostel: "Golden Plate Hostel",
      room: "Room 12A",
      customerName: "Agnes Mwangi",
      customerEmail: "agnesm@example.com",
      checkIn: "2025-02-10",
      checkOut: "2025-02-15",
      status: "pending",
    },
    {
      id: 2,
      hostel: "Oceania Apartments",
      room: "Room 3B",
      customerName: "Amina Mohammed",
      customerEmail: "amina@gmail.com",
      checkIn: "2025-03-01",
      checkOut: "2025-03-10",
      status: "confirmed",
    },
    {
      id: 3,
      hostel: "Step Hill",
      room: "Room 8C",
      customerName: "William Onyango",
      customerEmail: "willyo@gmail.com",
      checkIn: "2025-01-22",
      checkOut: "2025-09-25",
      status: "completed",
    },
        {
      id: 4,
      hostel: "Ebenezer Plaza",
      room: "Room 17D",
      customerName: "Mary Njau",
      customerEmail: "maryn@gmail.com",
      checkIn: "2025-03-19",
      checkOut: "2025-03-25",
      status: "confirmed",
    },
        {
      id: 5,
      hostel: "Green Eden",
      room: "Room 3A",
      customerName: "Jackline Waweru",
      customerEmail: "jackw@gmail.com",
      checkIn: "2025-05-5",
      checkOut: "2025-10-19",
      status: "completed",
    },
        {
      id: 6,
      hostel: "Orchid",
      room: "Room 6B",
      customerName: "Lucy Wairimu",
      customerEmail: "lucyw@gmail.com",
      checkIn: "2025-03-22",
      checkOut: "2025-01-25",
      status: "cancelled",
    },
        {
      id: 7,
      hostel: "Barbados",
      room: "Room 15F",
      customerName: "Milcah Nthenya",
      customerEmail: "milcahn@gmail.com",
      checkIn: "2025-02-22",
      checkOut: "2025-07-25",
      status: "completed",
    },
        {
      id: 8,
      hostel: "Gateway",
      room: "Room 4A",
      customerName: "Brian Kariuki",
      customerEmail: "briank@gmail.com",
      checkIn: "2025-01-15",
      checkOut: "2025--25",
      status: "completed",
    },
        {
      id: 9,
      hostel: "Yellow Hostel",
      room: "Room 16F",
      customerName: "Jane Moraa",
      customerEmail: "janem@gmail.com",
      checkIn: "2025-04-16",
      checkOut: "2025-04-25",
      status: "cancelled",
    },
        {
      id: 10,
      hostel: "Red Hills",
      room: "Room 3G",
      customerName: "Alice Waithera",
      customerEmail: "alicew@gmail.com",
      checkIn: "2025-01-22",
      checkOut: "2025-09-25",
      status: "completed",
    },
  ];

  const [bookings, setBookings] = useState(initialBookings);

  // ---------------------------
  // HANDLE STATUS CHANGE
  // ---------------------------
  const updateStatus = (id, newStatus) => {
    const updated = bookings.map((b) =>
      b.id === id ? { ...b, status: newStatus } : b
    );
    setBookings(updated);
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Hostel Bookings</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {bookings.map((booking) => (
          <div
            key={booking.id}
            className="border rounded-lg p-5 shadow-sm bg-white"
          >
            <h2 className="text-xl font-semibold mb-2">
              {booking.hostel} - {booking.room}
            </h2>

            <p>
              <strong>Customer:</strong> {booking.customerName}
            </p>
            <p>
              <strong>Email:</strong> {booking.customerEmail}
            </p>
            <p>
              <strong>Check-In:</strong> {booking.checkIn}
            </p>
            <p>
              <strong>Check-Out:</strong> {booking.checkOut}
            </p>

            <p className="mt-3">
              <strong>Status: </strong>
              <span
                className={`px-3 py-1 rounded text-white ${
                  booking.status === "pending"
                    ? "bg-yellow-500"
                    : booking.status === "confirmed"
                    ? "bg-blue-600"
                    : booking.status === "completed"
                    ? "bg-green-600"
                    : booking.status === "cancelled"
                    ? "bg-red-600"
                    : ""
                }`}
              >
                {booking.status.toUpperCase()}
              </span>
            </p>

            {/* ACTION BUTTONS */}
            <div className="flex gap-3 mt-4">
              {booking.status === "pending" && (
                <>
                  <button
                    onClick={() => updateStatus(booking.id, "confirmed")}
                    className="bg-blue-600 text-white px-4 py-1 rounded"
                  >
                    Confirm
                  </button>
                  <button
                    onClick={() => updateStatus(booking.id, "cancelled")}
                    className="bg-red-600 text-white px-4 py-1 rounded"
                  >
                    Cancel
                  </button>
                </>
              )}

              {booking.status === "confirmed" && (
                <button
                  onClick={() => updateStatus(booking.id, "completed")}
                  className="bg-green-600 text-white px-4 py-1 rounded"
                >
                  Complete
                </button>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default HostelBookings;
