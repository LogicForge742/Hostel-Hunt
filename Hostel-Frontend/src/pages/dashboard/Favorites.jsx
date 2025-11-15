import { Link } from 'react-router-dom';
import { useBooking } from '../../context/BookingContext.jsx';
import { useState, useEffect } from 'react';

export default function Favorites() {
  const { favorites, toggleFavorite, getHostelById } = useBooking();
  const [favoriteHostels, setFavoriteHostels] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadFavoriteHostels = async () => {
      if (favorites.length === 0) {
        setLoading(false);
        return;
      }

      try {
        const hostelPromises = favorites.map(id => getHostelById(id));
        const hostels = await Promise.all(hostelPromises);
        const validHostels = hostels.filter(hostel => hostel !== null);
        setFavoriteHostels(validHostels);
      } catch (error) {
        console.error('Failed to load favorite hostels:', error);
        setFavoriteHostels([]);
      } finally {
        setLoading(false);
      }
    };

    loadFavoriteHostels();
  }, [favorites, getHostelById]);

  if (loading) {
    return (
      <div className="flex justify-center items-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
      </div>
    );
  }

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">My Favorites</h1>

      {favoriteHostels.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-500 mb-4">You haven't added any favorites yet.</p>
          <Link
            to="/"
            className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700"
          >
            Explore Hostels
          </Link>
        </div>
      ) : (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {favoriteHostels.map((hostel) => (
            <div key={hostel.id} className="bg-white border rounded-lg overflow-hidden shadow-sm">
              <img
                src={hostel.images && hostel.images.length > 0 ? hostel.images[0] : '/placeholder.jpg'}
                alt={hostel.name}
                className="w-full h-48 object-cover"
              />
              <div className="p-6">
                <div className="flex justify-between items-start mb-2">
                  <h3 className="text-xl font-semibold">{hostel.name}</h3>
                  <button
                    onClick={() => toggleFavorite(hostel.id)}
                    className="text-2xl text-red-500 hover:text-red-600"
                  >
                    ♥
                  </button>
                </div>
                <p className="text-gray-600 mb-2">{hostel.location}</p>
                <div className="flex justify-between items-center mb-4">
                  <span className="text-2xl font-bold">KES {hostel.price?.toLocaleString() || 'N/A'}/mo</span>
                  <span className="text-yellow-500">★ {hostel.rating || 'N/A'}</span>
                </div>
                <p className="text-sm text-gray-600 mb-4">{hostel.description || 'No description available'}</p>
                <div className="flex space-x-2">
                  <Link
                    to={`/hostel/${hostel.id}`}
                    className="flex-1 text-center bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition-colors"
                  >
                    View Details
                  </Link>
                  <Link
                    to={`/booking/${hostel.id}`}
                    className="flex-1 text-center bg-green-600 text-white py-2 rounded hover:bg-green-700 transition-colors"
                  >
                    Book Now
                  </Link>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
