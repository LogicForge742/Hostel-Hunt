import { Link } from 'react-router-dom';
import { mockHostels } from '../../mocks/bookingData.js';
import { useBooking } from '../../contexts/BookingContext.jsx';

export default function HomePage() {
  const { favorites, toggleFavorite } = useBooking();

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-blue-600 to-purple-700 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <h1 className="text-5xl font-bold mb-6">
            Find Your Perfect Hostel
          </h1>
          <p className="text-xl mb-8">
            Discover amazing hostels worldwide and book your next adventure
          </p>
          <Link
            to="/search"
            className="bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors"
          >
            Start Exploring
          </Link>
        </div>
      </section>

      {/* Featured Hostels */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">Featured Hostels</h2>
          <div className="grid md:grid-cols-3 gap-8">
            {mockHostels.map((hostel) => (
              <div
                key={hostel.id}
                className="bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden"
              >
                <img
                  src={hostel.image}
                  alt={hostel.name}
                  className="w-full h-48 object-cover"
                />
                <div className="p-6">
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="text-xl font-semibold">{hostel.name}</h3>
                    <button
                      onClick={() => toggleFavorite(hostel.id)}
                      className={`text-2xl ${favorites.includes(hostel.id) ? 'text-red-500' : 'text-gray-400'}`}
                    >
                      ♥
                    </button>
                  </div>
                  <p className="text-gray-600 dark:text-gray-400 mb-2">{hostel.location}</p>
                  <div className="flex justify-between items-center mb-4">
                    <span className="text-2xl font-bold">${hostel.price}/night</span>
                    <span className="text-yellow-500">★ {hostel.rating}</span>
                  </div>
                  <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">{hostel.description}</p>
                  <Link
                    to={`/hostel/${hostel.id}`}
                    className="block text-center bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition-colors"
                  >
                    View Details
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
