import { createContext, useState, useEffect } from 'react';
import { mockBookings, mockHostels } from '../mocks/bookingData.js';

const BookingContext = createContext();

export function BookingProvider({ children }) {
  const [bookings, setBookings] = useState([]);
  const [favorites, setFavorites] = useState([]);

  useEffect(() => {
    // Load mock data
    setBookings(mockBookings);
    setFavorites([1, 3]); // Mock favorites
  }, []);

  const createBooking = (bookingData) => {
    const newBooking = {
      id: Date.now(),
      ...bookingData,
      status: 'confirmed',
      bookingDate: new Date().toISOString().split('T')[0]
    };
    setBookings(prev => [...prev, newBooking]);
    return newBooking.id;
  };

  const toggleFavorite = (hostelId) => {
    setFavorites(prev =>
      prev.includes(hostelId)
        ? prev.filter(id => id !== hostelId)
        : [...prev, hostelId]
    );
  };

  const getHostelById = (id) => {
    return mockHostels.find(hostel => hostel.id === parseInt(id));
  };

  const getBookingById = (id) => {
    return bookings.find(booking => booking.id === parseInt(id));
  };

  const value = {
    bookings,
    favorites,
    createBooking,
    toggleFavorite,
    getHostelById,
    getBookingById
  };

  return (
    <BookingContext.Provider value={value}>
      {children}
    </BookingContext.Provider>
  );
}

export { BookingContext };
