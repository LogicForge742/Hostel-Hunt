// src/utils/api.js
import hostelsData from '../mocks/hostels.json';

/**
 * Simulates API delay for realistic mock behavior
 * @param {number} ms - Delay in milliseconds
 */
const delay = (ms = 500) => new Promise(resolve => setTimeout(resolve, ms));

/**
 * Fetch all hostels/rooms with optional filters
 * @param {Object} filters - Filter options
 * @returns {Promise<Object>} Filtered rooms and metadata
 */
export const fetchRooms = async (filters = {}) => {
  await delay(300);
  
  let filtered = [...hostelsData.rooms];
  
  // Filter by location/search term
  if (filters.location) {
    const term = filters.location.toLowerCase();
    filtered = filtered.filter(room => 
      room.location.area.toLowerCase().includes(term) ||
      room.location.city.toLowerCase().includes(term) ||
      room.university.toLowerCase().includes(term) ||
      room.title.toLowerCase().includes(term)
    );
  }
  
  // Filter by price range
  if (filters.minPrice !== null && filters.minPrice !== undefined) {
    filtered = filtered.filter(room => room.price >= filters.minPrice);
  }
  if (filters.maxPrice !== null && filters.maxPrice !== undefined) {
    filtered = filtered.filter(room => room.price <= filters.maxPrice);
  }
  
  // Filter by room type
  if (filters.roomType && filters.roomType.length > 0) {
    filtered = filtered.filter(room => filters.roomType.includes(room.roomType));
  }
  
  // Filter by amenities
  if (filters.amenities && filters.amenities.length > 0) {
    filtered = filtered.filter(room =>
      filters.amenities.every(amenity => room.amenities.includes(amenity))
    );
  }
  
  // Filter by university
  if (filters.university) {
    filtered = filtered.filter(room => 
      room.universityShort === filters.university || 
      room.university === filters.university
    );
  }
  
  // Filter by availability
  if (filters.availableOnly) {
    filtered = filtered.filter(room => room.availability.available);
  }
  
  // Filter by features
  if (filters.furnished !== undefined) {
    filtered = filtered.filter(room => room.features.furnished === filters.furnished);
  }
  if (filters.parking) {
    filtered = filtered.filter(room => room.features.parking === true);
  }
  
  // Sort results
  switch (filters.sortBy) {
    case 'price-asc':
      filtered.sort((a, b) => a.price - b.price);
      break;
    case 'price-desc':
      filtered.sort((a, b) => b.price - a.price);
      break;
    case 'rating':
      filtered.sort((a, b) => b.landlord.rating - a.landlord.rating);
      break;
    case 'featured':
      filtered.sort((a, b) => (b.featured ? 1 : 0) - (a.featured ? 1 : 0));
      break;
    default: // 'relevance'
      // Keep original order (featured first already in mock data)
      break;
  }
  
  // Pagination
  const page = filters.page || 1;
  const limit = filters.limit || 12;
  const startIdx = (page - 1) * limit;
  const endIdx = startIdx + limit;
  const paginated = filtered.slice(startIdx, endIdx);
  
  return {
    rooms: paginated,
    total: filtered.length,
    page,
    limit,
    totalPages: Math.ceil(filtered.length / limit),
    hasMore: endIdx < filtered.length
  };
};

/**
 * Fetch single room by ID or slug
 * @param {string|number} identifier - Room ID or slug
 * @returns {Promise<Object|null>} Room data or null
 */
export const fetchRoomById = async (identifier) => {
  await delay(200);
  
  const room = hostelsData.rooms.find(
    r => r.id === Number(identifier) || r.slug === identifier
  );
  
  if (!room) {
    throw new Error('Room not found');
  }
  
  // Simulate fetching related/similar rooms
  const similar = hostelsData.rooms
    .filter(r => 
      r.id !== room.id && 
      (r.university === room.university || r.location.area === room.location.area)
    )
    .slice(0, 3);
  
  return {
    ...room,
    similarRooms: similar
  };
};

/**
 * Fetch featured/recommended rooms
 * @param {number} limit - Number of rooms to fetch
 * @returns {Promise<Array>} Featured rooms
 */
export const fetchFeaturedRooms = async (limit = 6) => {
  await delay(300);
  
  return hostelsData.rooms
    .filter(room => room.featured)
    .slice(0, limit);
};

/**
 * Fetch filter options from data
 * @returns {Promise<Object>} Available filters
 */
export const fetchFilterOptions = async () => {
  await delay(100);
  
  return {
    priceRanges: hostelsData.filters.priceRanges,
    roomTypes: hostelsData.filters.roomTypes,
    amenities: hostelsData.filters.popularAmenities,
    areas: hostelsData.filters.areas,
    universities: hostelsData.universities
  };
};

/**
 * Search autocomplete suggestions
 * @param {string} query - Search query
 * @returns {Promise<Array>} Suggestions
 */
export const fetchSearchSuggestions = async (query) => {
  await delay(150);
  
  if (!query || query.length < 2) return [];
  
  const term = query.toLowerCase();
  const suggestions = [];
  
  // University suggestions
  hostelsData.universities.forEach(uni => {
    if (uni.name.toLowerCase().includes(term) || uni.short.toLowerCase().includes(term)) {
      suggestions.push({
        type: 'university',
        label: uni.name,
        value: uni.short
      });
    }
  });
  
  // Area suggestions
  hostelsData.filters.areas.forEach(area => {
    if (area.toLowerCase().includes(term)) {
      suggestions.push({
        type: 'area',
        label: area,
        value: area
      });
    }
  });
  
  // Room suggestions (by title)
  hostelsData.rooms.forEach(room => {
    if (room.title.toLowerCase().includes(term)) {
      suggestions.push({
        type: 'room',
        label: room.title,
        value: room.slug,
        price: room.price
      });
    }
  });
  
  return suggestions.slice(0, 8);
};

export default {
  fetchRooms,
  fetchRoomById,
  fetchFeaturedRooms,
  fetchFilterOptions,
  fetchSearchSuggestions
};