// src/pages/hostel/HostelDetailPage.jsx
import { useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { motion } from 'framer-motion';
import { fetchRoomById } from '../../utils/api';
import Card from '../../components/Card';

export default function HostelDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [currentImageIndex, setCurrentImageIndex] = useState(0);
  const [showAllAmenities, setShowAllAmenities] = useState(false);

  const { data: roomData, isLoading, isError, error } = useQuery({
    queryKey: ['room', id],
    queryFn: () => fetchRoomById(id),
  });

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading room details...</p>
        </div>
      </div>
    );
  }

  if (isError || !roomData) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
        <div className="bg-white rounded-lg shadow-md p-8 max-w-md text-center">
          <svg className="w-16 h-16 text-red-500 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <h2 className="text-2xl font-bold text-gray-800 mb-2">Room Not Found</h2>
          <p className="text-gray-600 mb-6">{error?.message || 'The room you\'re looking for doesn\'t exist.'}</p>
          <button
            onClick={() => navigate('/search')}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Back to Search
          </button>
        </div>
      </div>
    );
  }

  const room = roomData;
  const displayImages = room.images && room.images.length > 0 
    ? room.images 
    : ['https://via.placeholder.com/800x600?text=No+Image'];

  const nextImage = () => {
    setCurrentImageIndex((prev) => (prev + 1) % displayImages.length);
  };

  const prevImage = () => {
    setCurrentImageIndex((prev) => (prev - 1 + displayImages.length) % displayImages.length);
  };

  const displayedAmenities = showAllAmenities ? room.amenities : room.amenities.slice(0, 8);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Back Button */}
      <div className="bg-white border-b">
        <div className="container mx-auto px-4 py-4">
          <button
            onClick={() => navigate(-1)}
            className="flex items-center gap-2 text-gray-600 hover:text-gray-800 transition-colors"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            Back to Search
          </button>
        </div>
      </div>

      <div className="container mx-auto px-4 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Image Gallery */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-white rounded-lg shadow-md overflow-hidden"
            >
              <div className="relative h-96 bg-gray-200">
                <img
                  src={displayImages[currentImageIndex]}
                  alt={`${room.title} - Image ${currentImageIndex + 1}`}
                  className="w-full h-full object-cover"
                  onError={(e) => {
                    e.target.src = 'https://via.placeholder.com/800x600?text=Image+Not+Available';
                  }}
                />

                {/* Navigation Arrows */}
                {displayImages.length > 1 && (
                  <>
                    <button
                      onClick={prevImage}
                      className="absolute left-4 top-1/2 -translate-y-1/2 bg-black bg-opacity-50 hover:bg-opacity-75 text-white p-2 rounded-full transition-all"
                    >
                      <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                      </svg>
                    </button>
                    <button
                      onClick={nextImage}
                      className="absolute right-4 top-1/2 -translate-y-1/2 bg-black bg-opacity-50 hover:bg-opacity-75 text-white p-2 rounded-full transition-all"
                    >
                      <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                      </svg>
                    </button>
                  </>
                )}

                {/* Image Counter */}
                <div className="absolute bottom-4 right-4 bg-black bg-opacity-75 text-white px-3 py-1 rounded-full text-sm">
                  {currentImageIndex + 1} / {displayImages.length}
                </div>

                {/* Badges */}
                <div className="absolute top-4 left-4 flex gap-2">
                  {room.featured && (
                    <span className="bg-yellow-500 text-white text-sm font-bold px-3 py-1 rounded">
                      Featured
                    </span>
                  )}
                  {room.verified && (
                    <span className="bg-green-500 text-white text-sm font-bold px-3 py-1 rounded">
                      Verified
                    </span>
                  )}
                </div>
              </div>

              {/* Thumbnail Gallery */}
              {displayImages.length > 1 && (
                <div className="flex gap-2 p-4 overflow-x-auto">
                  {displayImages.map((img, idx) => (
                    <button
                      key={idx}
                      onClick={() => setCurrentImageIndex(idx)}
                      className={`flex-shrink-0 w-20 h-20 rounded-lg overflow-hidden border-2 transition-all ${
                        idx === currentImageIndex ? 'border-blue-600 scale-105' : 'border-gray-300'
                      }`}
                    >
                      <img
                        src={img}
                        alt={`Thumbnail ${idx + 1}`}
                        className="w-full h-full object-cover"
                        onError={(e) => {
                          e.target.src = 'https://via.placeholder.com/80x80?text=No+Image';
                        }}
                      />
                    </button>
                  ))}
                </div>
              )}
            </motion.div>

            {/* Room Details */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="bg-white rounded-lg shadow-md p-6"
            >
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h1 className="text-3xl font-bold text-gray-800 mb-2">{room.title}</h1>
                  <div className="flex items-center text-gray-600">
                    <svg className="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    </svg>
                    <span>{room.location.area}, {room.location.city}</span>
                  </div>
                  <p className="text-sm text-gray-500 mt-1">{room.location.distance}</p>
                </div>
                <div className="text-right">
                  <div className="text-3xl font-bold text-blue-600">
                    {room.currency} {new Intl.NumberFormat('en-KE').format(room.price)}
                  </div>
                  <div className="text-sm text-gray-600">per month</div>
                </div>
              </div>

              <div className="flex items-center gap-4 py-4 border-t border-b mb-4">
                <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-semibold">
                  {room.roomType}
                </span>
                <span className="text-gray-600">•</span>
                <span className="text-gray-700">
                  {room.features.bedrooms > 0 ? `${room.features.bedrooms} Bedroom` : 'Studio'}
                </span>
                <span className="text-gray-600">•</span>
                <span className="text-gray-700">{room.features.bathrooms} Bathroom</span>
                {room.features.furnished && (
                  <>
                    <span className="text-gray-600">•</span>
                    <span className="text-gray-700">Furnished</span>
                  </>
                )}
              </div>

              <p className="text-gray-700 leading-relaxed">{room.description}</p>
            </motion.div>

            {/* Amenities */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="bg-white rounded-lg shadow-md p-6"
            >
              <h2 className="text-2xl font-bold text-gray-800 mb-4">Amenities</h2>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                {displayedAmenities.map((amenity, idx) => (
                  <div key={idx} className="flex items-center gap-2">
                    <svg className="w-5 h-5 text-green-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    <span className="text-gray-700">{amenity}</span>
                  </div>
                ))}
              </div>
              {room.amenities.length > 8 && (
                <button
                  onClick={() => setShowAllAmenities(!showAllAmenities)}
                  className="mt-4 text-blue-600 hover:text-blue-700 font-medium"
                >
                  {showAllAmenities ? 'Show Less' : `Show All ${room.amenities.length} Amenities`}
                </button>
              )}
            </motion.div>

            {/* What's Included */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="bg-white rounded-lg shadow-md p-6"
            >
              <h2 className="text-2xl font-bold text-gray-800 mb-4">What's Included in Rent</h2>
              <div className="flex flex-wrap gap-2">
                {room.priceIncludes.map((item, idx) => (
                  <span key={idx} className="bg-green-50 text-green-700 px-4 py-2 rounded-lg">
                    ✓ {item}
                  </span>
                ))}
              </div>
            </motion.div>

            {/* Map Placeholder */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
              className="bg-white rounded-lg shadow-md p-6"
            >
              <h2 className="text-2xl font-bold text-gray-800 mb-4">Location</h2>
              <div className="w-full h-64 bg-gray-200 rounded-lg flex items-center justify-center">
                <div className="text-center">
                  <svg className="w-12 h-12 text-gray-400 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  </svg>
                  <p className="text-gray-600">Map Integration Coming Soon</p>
                  <p className="text-sm text-gray-500 mt-1">{room.location.description}</p>
                </div>
              </div>
            </motion.div>

            {/* Similar Rooms */}
            {room.similarRooms && room.similarRooms.length > 0 && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5 }}
                className="bg-white rounded-lg shadow-md p-6"
              >
                <h2 className="text-2xl font-bold text-gray-800 mb-4">Similar Rooms</h2>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {room.similarRooms.map((similarRoom, idx) => (
                    <Card key={similarRoom.id} room={similarRoom} index={idx} />
                  ))}
                </div>
              </motion.div>
            )}
          </div>

          {/* Sidebar */}
          <div className="lg:col-span-1">
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              className="bg-white rounded-lg shadow-md p-6 sticky top-24"
            >
              {/* Availability */}
              <div className="mb-6">
                {room.availability.available ? (
                  <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                    <div className="flex items-center gap-2 text-green-800 font-semibold mb-2">
                      <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                      </svg>
                      Available Now
                    </div>
                    <p className="text-sm text-green-700">
                      Move-in from: {new Date(room.availability.availableFrom).toLocaleDateString()}
                    </p>
                  </div>
                ) : (
                  <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                    <p className="text-red-800 font-semibold">Currently Unavailable</p>
                  </div>
                )}
              </div>

              {/* Booking Info */}
              <div className="space-y-3 mb-6">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Minimum Stay:</span>
                  <span className="font-semibold">{room.availability.minimumStay}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Deposit Required:</span>
                  <span className="font-semibold">
                    {room.currency} {new Intl.NumberFormat('en-KE').format(room.availability.deposit)}
                  </span>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="space-y-3">
                <Link
                  to={`/booking/${room.id}`}
                  className="block w-full bg-blue-600 text-white text-center py-3 rounded-lg hover:bg-blue-700 transition-colors font-semibold"
                >
                  Book This Room
                </Link>
                <button className="w-full border-2 border-gray-300 text-gray-700 py-3 rounded-lg hover:border-gray-400 transition-colors font-semibold">
                  Save to Favorites
                </button>
              </div>

              {/* Landlord Info */}
              {room.landlord && (
                <div className="mt-6 pt-6 border-t">
                  <h3 className="font-bold text-gray-800 mb-3">Landlord</h3>
                  <div className="flex items-center gap-3 mb-4">
                    <div className="w-12 h-12 bg-gradient-to-br from-blue-400 to-purple-500 rounded-full flex items-center justify-center text-white font-bold text-xl">
                      {room.landlord.name.charAt(0)}
                    </div>
                    <div>
                      <p className="font-semibold text-gray-800">{room.landlord.name}</p>
                      {room.landlord.verified && (
                        <p className="text-xs text-green-600 flex items-center gap-1">
                          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                          </svg>
                          Verified Landlord
                        </p>
                      )}
                    </div>
                  </div>

                  {room.landlord.rating && (
                    <div className="flex items-center gap-2 mb-4">
                      <div className="flex items-center gap-1">
                        <svg className="w-5 h-5 text-yellow-400 fill-current" viewBox="0 0 20 20">
                          <path d="M10 15l-5.878 3.09 1.123-6.545L.489 6.91l6.572-.955L10 0l2.939 5.955 6.572.955-4.756 4.635 1.123 6.545z" />
                        </svg>
                        <span className="font-semibold">{room.landlord.rating.toFixed(1)}</span>
                      </div>
                      <span className="text-sm text-gray-600">({room.landlord.reviewCount} reviews)</span>
                    </div>
                  )}

                  <button className="w-full bg-gray-100 text-gray-700 py-2 rounded-lg hover:bg-gray-200 transition-colors font-medium">
                    Contact Landlord
                  </button>
                </div>
              )}
            </motion.div>
          </div>
        </div>
      </div>
    </div>
  );
}