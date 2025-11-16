// src/components/Card.jsx - FINAL WORKING VERSION
import { useState } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';

const Card = ({ room, index = 0 }) => {
  const [imgLoaded, setImgLoaded] = useState(false);
  const [imgError, setImgError] = useState(false);

  if (!room) return null;

  const {
    slug,
    title,
    location,
    price,
    currency = 'KES',
    images,
    roomType,
    amenities = [],
    landlord,
    features = {},
    availability,
    featured,
    verified,
    borderColor = 'border-gray-200'
  } = room;

  // Fallback image
  const displayImage = imgError 
    ? 'https://via.placeholder.com/400x300?text=No+Image'
    : images?.[0] || 'https://via.placeholder.com/400x300?text=Room+Image';

  // Format price
  const formatPrice = (amount) => {
    return new Intl.NumberFormat('en-KE').format(amount);
  };

  // Top amenities
  const topAmenities = amenities.slice(0, 3);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, delay: index * 0.05 }}
      className="h-full"
    >
      <Link 
        to={`/hostel/${slug}`}
        className="block h-full group"
      >
        <div className={`
          bg-white rounded-lg shadow-md overflow-hidden 
          border-2 ${borderColor}
          hover:shadow-xl transition-all duration-300
          ${featured ? 'ring-2 ring-yellow-400 ring-offset-2' : ''}
          h-full flex flex-col
        `}>
          {/* Image Container */}
          <div className="relative h-48 bg-gray-200 overflow-hidden flex-shrink-0">
            {/* Loading State */}
            {!imgLoaded && !imgError && (
              <div className="absolute inset-0 animate-pulse bg-gray-300" />
            )}
            
            {/* Image */}
            <img
              src={displayImage}
              alt={title}
              onLoad={() => setImgLoaded(true)}
              onError={() => setImgError(true)}
              className={`
                w-full h-full object-cover 
                group-hover:scale-110 transition-transform duration-500
                ${imgLoaded ? 'opacity-100' : 'opacity-0'}
              `}
            />

            {/* Badges Row */}
            <div className="absolute top-2 left-2 flex gap-2">
              {featured && (
                <span className="bg-yellow-500 text-white text-xs font-bold px-2 py-1 rounded shadow-md">
                  Featured
                </span>
              )}
              {verified && (
                <span className="bg-green-500 text-white text-xs font-bold px-2 py-1 rounded shadow-md flex items-center gap-1">
                  <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  Verified
                </span>
              )}
            </div>

            {/* Availability Badge */}
            {availability?.available && (
              <span className="absolute top-2 right-2 bg-blue-500 text-white text-xs font-bold px-2 py-1 rounded shadow-md">
                Available
              </span>
            )}

            {/* Price Tag */}
            <div className="absolute bottom-2 right-2 bg-black bg-opacity-75 text-white px-3 py-1.5 rounded-full shadow-lg">
              <div className="flex items-baseline gap-1">
                <span className="text-sm font-semibold">{currency}</span>
                <span className="text-lg font-bold">{formatPrice(price)}</span>
                <span className="text-xs">/mo</span>
              </div>
            </div>
          </div>

          {/* Content Section */}
          <div className="p-4 flex-1 flex flex-col">
            {/* Title & Room Type */}
            <div className="flex items-start justify-between gap-2 mb-2">
              <h3 className="text-lg font-semibold text-gray-800 group-hover:text-blue-600 transition-colors line-clamp-2 flex-1">
                {title}
              </h3>
              <span className="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded-full whitespace-nowrap flex-shrink-0">
                {roomType}
              </span>
            </div>

            {/* Location */}
            <div className="flex items-center gap-1 text-sm text-gray-600 mb-3">
              <svg className="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              <span className="line-clamp-1">
                {location?.area}, {location?.city}
                {location?.distance && ` • ${location.distance}`}
              </span>
            </div>

            {/* Amenities */}
            {topAmenities.length > 0 && (
              <div className="flex flex-wrap gap-1 mb-3">
                {topAmenities.map((amenity, idx) => (
                  <span 
                    key={idx}
                    className="text-xs bg-blue-50 text-blue-700 px-2 py-1 rounded"
                  >
                    {amenity}
                  </span>
                ))}
                {amenities.length > 3 && (
                  <span className="text-xs text-gray-500 px-2 py-1">
                    +{amenities.length - 3} more
                  </span>
                )}
              </div>
            )}

            {/* Features */}
            {features && (
              <div className="flex items-center gap-3 text-xs text-gray-500 mb-3 pb-3 border-b">
                {features.bedrooms !== undefined && (
                  <span className="flex items-center gap-1">
                    🛏️ {features.bedrooms > 0 ? `${features.bedrooms} BR` : 'Studio'}
                  </span>
                )}
                {features.bathrooms && (
                  <span className="flex items-center gap-1">
                    🚿 {features.bathrooms} BA
                  </span>
                )}
                {features.furnished && (
                  <span className="flex items-center gap-1">
                    🪑 Furnished
                  </span>
                )}
              </div>
            )}

            {/* Landlord Info - Pushed to bottom */}
            {landlord && (
              <div className="flex items-center justify-between mt-auto">
                <div className="flex items-center gap-2">
                  <div className="w-8 h-8 bg-gradient-to-br from-blue-400 to-purple-500 rounded-full flex items-center justify-center text-white font-bold text-sm flex-shrink-0">
                    {landlord.name?.charAt(0) || 'L'}
                  </div>
                  <div className="min-w-0">
                    <p className="text-sm font-medium text-gray-800 truncate">
                      {landlord.name || 'Landlord'}
                    </p>
                    {landlord.verified && (
                      <p className="text-xs text-gray-500">Verified Landlord</p>
                    )}
                  </div>
                </div>

                {/* Rating */}
                {landlord.rating && (
                  <div className="flex items-center gap-1 flex-shrink-0">
                    <svg className="w-4 h-4 text-yellow-400 fill-current" viewBox="0 0 20 20">
                      <path d="M10 15l-5.878 3.09 1.123-6.545L.489 6.91l6.572-.955L10 0l2.939 5.955 6.572.955-4.756 4.635 1.123 6.545z" />
                    </svg>
                    <span className="text-sm font-semibold text-gray-700">
                      {landlord.rating.toFixed(1)}
                    </span>
                    {landlord.reviewCount && (
                      <span className="text-xs text-gray-500">
                        ({landlord.reviewCount})
                      </span>
                    )}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </Link>
    </motion.div>
  );
};

export default Card;