// src/utils/api.js
export const API_BASE_URL = 'https://hostel-hunt-a0v4.onrender.com';

/**
 * Helper function to make API requests
 * @param {string} endpoint - API endpoint
 * @param {Object} options - Fetch options
 * @returns {Promise<Object>} Response data
 */
const apiRequest = async (endpoint, options = {}) => {
  const url = `${API_BASE_URL}${endpoint}`;
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  // Add auth token if available
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  try {
    const response = await fetch(url, config);
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.message || `HTTP error! status: ${response.status}`);
    }

    return data;
  } catch (error) {
    console.error(`API request failed: ${endpoint}`, error);
    throw error;
  }
};

/**
 * Fetch all hostels/rooms with optional filters
 * @param {Object} filters - Filter options
 * @returns {Promise<Object>} Filtered rooms and metadata
 */
export const fetchRooms = async (filters = {}) => {
  const params = new URLSearchParams();

  // Build query parameters
  if (filters.page) params.append('page', filters.page);
  if (filters.per_page || filters.limit) params.append('per_page', filters.per_page || filters.limit || 12);
  if (filters.location) params.append('location', filters.location);
  if (filters.minPrice !== null && filters.minPrice !== undefined) params.append('min_price', filters.minPrice);
  if (filters.maxPrice !== null && filters.maxPrice !== undefined) params.append('max_price', filters.maxPrice);
  if (filters.roomType && filters.roomType.length > 0) {
    filters.roomType.forEach(type => params.append('room_type', type));
  }
  if (filters.amenities && filters.amenities.length > 0) {
    filters.amenities.forEach(amenity => params.append('amenities', amenity));
  }
  if (filters.furnished !== undefined) params.append('furnished', filters.furnished);
  if (filters.verified_only) params.append('verified_only', filters.verified_only);
  if (filters.featured_only) params.append('featured_only', filters.featured_only);
  if (filters.sortBy) {
    // Map frontend sort options to backend
    const sortMap = {
      'price-asc': 'price_asc',
      'price-desc': 'price_desc',
      'rating': 'rating',
      'featured': 'newest', // fallback
      'relevance': 'newest'
    };
    params.append('sort_by', sortMap[filters.sortBy] || 'newest');
  }

  const response = await apiRequest(`/hostels/?${params}`);

  // Normalize backend hostel objects into the richer shape expected by Card/SearchResultsPage
  const normalizeHostel = (hostel) => {
    if (!hostel) return null;

    // Location: backend likely returns a simple string like "Area, City"
    const rawLocation = hostel.location || '';
    const [area = '', city = ''] = rawLocation.split(',').map(part => part.trim());

    return {
      // Keep original id and also expose slug/id for routing
      id: hostel.id,
      slug: hostel.id, // Card links to `/hostel/${slug}`; detail page accepts an id param

      // Basic text fields
      title: hostel.name || hostel.title || 'Hostel',
      description: hostel.description || '',

      // Location object used by Card
      location: {
        area,
        city,
        // If backend later adds distance, Card will display it; default empty for now
        distance: hostel.distance || ''
      },

      // Pricing
      price: hostel.price,
      currency: hostel.currency || 'KES',

      // Room meta
      roomType: hostel.room_type || hostel.roomType || 'Room',

      // Images: ensure we always give Card an array
      images: Array.isArray(hostel.images) ? hostel.images : (hostel.images ? [hostel.images] : []),

      // Amenities: backend may store as JSON/dict; flatten keys with truthy values into nice labels
      amenities: (() => {
        const src = hostel.amenities;
        if (!src) return [];
        if (Array.isArray(src)) return src;
        if (typeof src === 'object') {
          return Object.entries(src)
            .filter(([, value]) => Boolean(value))
            .map(([key]) => key.replace(/_/g, ' '));
        }
        return [];
      })(),

      // Landlord summary (optional)
      landlord: hostel.landlord ? {
        name: hostel.landlord.name || hostel.landlord.business_name || 'Landlord',
        verified: Boolean(hostel.landlord.is_verified ?? hostel.landlord.verified),
        rating: typeof hostel.landlord.rating === 'number' ? hostel.landlord.rating : undefined,
        reviewCount: typeof hostel.landlord.reviewCount === 'number' ? hostel.landlord.reviewCount : undefined
      } : undefined,

      // Feature flags & badges
      features: hostel.features || {},
      availability: hostel.availability || {},
      featured: Boolean(hostel.is_featured ?? hostel.featured),
      verified: Boolean(hostel.is_verified ?? hostel.verified),

      // Optional per-card styling hook
      borderColor: hostel.borderColor || 'border-purple-400'
    };
  };

  const normalizedRooms = (response.hostels || [])
    .map(normalizeHostel)
    .filter(Boolean);

  return {
    rooms: normalizedRooms,
    total: response.total || 0,
    page: response.current_page || 1,
    limit: response.per_page || 12,
    totalPages: response.pages || 0,
    hasMore: (response.current_page || 1) < (response.pages || 0)
  };
};

/**
 * Fetch single room by ID or slug
 * @param {string|number} identifier - Room ID or slug
 * @returns {Promise<Object|null>} Room data or null
 */
export const fetchRoomById = async (identifier) => {
  const response = await apiRequest(`/hostels/${identifier}`);

  // Transform backend response to match frontend expectations
  return {
    ...response,
    // Add any frontend-specific transformations here
    similarRooms: [] // Backend doesn't provide similar rooms yet
  };
};

/**
 * Fetch featured/recommended rooms
 * @param {number} limit - Number of rooms to fetch
 * @returns {Promise<Array>} Featured rooms
 */
export const fetchFeaturedRooms = async (limit = 6) => {
  const response = await apiRequest(`/hostels/?featured_only=true&per_page=${limit}`);
  return response.hostels || [];
};

/**
 * Fetch filter options from backend
 * @returns {Promise<Object>} Available filters
 */
export const fetchFilterOptions = async () => {
  const response = await apiRequest('/search/filters');

  return {
    priceRanges: response.price_ranges || { min_price: 0, max_price: 50000 },
    roomTypes: response.room_types || [],
    amenities: response.amenities || [],
    areas: [], // Backend doesn't provide areas yet
    universities: [] // Backend doesn't provide universities yet
  };
};

/**
 * Search autocomplete suggestions
 * @param {string} query - Search query
 * @returns {Promise<Array>} Suggestions
 */
export const fetchSearchSuggestions = async (query) => {
  if (!query || query.length < 2) return [];

  try {
    const response = await apiRequest(`/search/suggestions?q=${encodeURIComponent(query)}`);
    return response.suggestions || [];
  } catch (error) {
    console.error('Search suggestions failed:', error);
    return [];
  }
};

export default {
  fetchRooms,
  fetchRoomById,
  fetchFeaturedRooms,
  fetchFilterOptions,
  fetchSearchSuggestions
};
