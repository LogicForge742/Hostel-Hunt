// src/pages/search/SearchResultsPage.jsx
import { useState, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { motion, AnimatePresence } from 'framer-motion';
import useSearch from '../../hooks/useSearch';
import { fetchRooms, fetchFilterOptions } from '../../utils/api';
import Card from '../../components/Card';

const SearchResultsPage = () => {
  const { searchParams, updateSearchParams } = useSearch();
  const [page, setPage] = useState(1);
  const [showFilters, setShowFilters] = useState(false);

  const [filters, setFilters] = useState({
    minPrice: searchParams.minPrice || null,
    maxPrice: searchParams.maxPrice || null,
    roomType: [],
    amenities: searchParams.amenities || [],
    university: '',
    furnished: undefined,
    parking: false,
    availableOnly: true
  });

  const { data, isLoading, isError, error } = useQuery({
    queryKey: ['rooms', searchParams, page, filters],
    queryFn: () => fetchRooms({
      ...searchParams,
      ...filters,
      page,
      limit: 12
    }),
    keepPreviousData: true
  });

  const { data: filterOptions } = useQuery({
    queryKey: ['filterOptions'],
    queryFn: fetchFilterOptions
  });

  useEffect(() => {
    setPage(1);
  }, [searchParams, filters]);

  const applyFilters = () => {
    updateSearchParams({
      ...searchParams,
      ...filters,
      page: 1
    });
    setShowFilters(false);
  };

  const resetFilters = () => {
    setFilters({
      minPrice: null,
      maxPrice: null,
      roomType: [],
      amenities: [],
      university: '',
      furnished: undefined,
      parking: false,
      availableOnly: true
    });
    setPage(1);
  };

  const handleSortChange = (sortBy) => {
    updateSearchParams({ ...searchParams, sortBy });
  };

  const toggleAmenity = (amenity) => {
    setFilters(prev => ({
      ...prev,
      amenities: prev.amenities.includes(amenity)
        ? prev.amenities.filter(a => a !== amenity)
        : [...prev.amenities, amenity]
    }));
  };

  const toggleRoomType = (type) => {
    setFilters(prev => ({
      ...prev,
      roomType: prev.roomType.includes(type)
        ? prev.roomType.filter(t => t !== type)
        : [...prev.roomType, type]
    }));
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-white shadow-sm border-b sticky top-0 z-10">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-800">
                {searchParams.location ? `Rooms in ${searchParams.location}` : 'All Rooms'}
              </h1>
              {!isLoading && data && (
                <p className="text-sm text-gray-600 mt-1">
                  {data.total} {data.total === 1 ? 'room' : 'rooms'} found
                </p>
              )}
            </div>

            <div className="flex items-center gap-3">
              <select
                value={searchParams.sortBy || 'relevance'}
                onChange={(e) => handleSortChange(e.target.value)}
                className="px-4 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="relevance">Sort: Relevance</option>
                <option value="price-asc">Price: Low to High</option>
                <option value="price-desc">Price: High to Low</option>
                <option value="rating">Highest Rated</option>
                <option value="featured">Featured First</option>
              </select>

              <button
                onClick={() => setShowFilters(!showFilters)}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" />
                </svg>
                Filters
                {(filters.amenities.length > 0 || filters.roomType.length > 0) && (
                  <span className="bg-white text-blue-600 rounded-full px-2 py-0.5 text-xs font-bold">
                    {filters.amenities.length + filters.roomType.length}
                  </span>
                )}
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-6">
        <div className="flex gap-6">
          <AnimatePresence>
            {showFilters && (
              <motion.aside
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                className="w-80 flex-shrink-0"
              >
                <div className="bg-white rounded-lg shadow-md p-6 sticky top-24">
                  <div className="flex items-center justify-between mb-4">
                    <h2 className="text-lg font-bold text-gray-800">Filters</h2>
                    <button onClick={resetFilters} className="text-sm text-blue-600 hover:text-blue-700">
                      Clear All
                    </button>
                  </div>

                  <div className="space-y-6">
                    <div>
                      <h3 className="font-semibold text-gray-700 mb-3">Price Range (KES)</h3>
                      <div className="grid grid-cols-2 gap-3">
                        <input
                          type="number"
                          placeholder="Min"
                          value={filters.minPrice || ''}
                          onChange={(e) => setFilters(prev => ({ ...prev, minPrice: e.target.value ? Number(e.target.value) : null }))}
                          className="px-3 py-2 border border-gray-300 rounded-lg text-sm"
                        />
                        <input
                          type="number"
                          placeholder="Max"
                          value={filters.maxPrice || ''}
                          onChange={(e) => setFilters(prev => ({ ...prev, maxPrice: e.target.value ? Number(e.target.value) : null }))}
                          className="px-3 py-2 border border-gray-300 rounded-lg text-sm"
                        />
                      </div>
                    </div>

                    <div>
                      <h3 className="font-semibold text-gray-700 mb-3">Room Type</h3>
                      <div className="space-y-2">
                        {filterOptions?.roomTypes.map(type => (
                          <label key={type} className="flex items-center gap-2 cursor-pointer">
                            <input
                              type="checkbox"
                              checked={filters.roomType.includes(type)}
                              onChange={() => toggleRoomType(type)}
                              className="rounded text-blue-600 focus:ring-blue-500"
                            />
                            <span className="text-sm text-gray-700">{type}</span>
                          </label>
                        ))}
                      </div>
                    </div>

                    <div>
                      <h3 className="font-semibold text-gray-700 mb-3">Amenities</h3>
                      <div className="space-y-2">
                        {filterOptions?.amenities.slice(0, 6).map(amenity => (
                          <label key={amenity} className="flex items-center gap-2 cursor-pointer">
                            <input
                              type="checkbox"
                              checked={filters.amenities.includes(amenity)}
                              onChange={() => toggleAmenity(amenity)}
                              className="rounded text-blue-600 focus:ring-blue-500"
                            />
                            <span className="text-sm text-gray-700">{amenity}</span>
                          </label>
                        ))}
                      </div>
                    </div>

                    <div>
                      <h3 className="font-semibold text-gray-700 mb-3">University</h3>
                      <select
                        value={filters.university}
                        onChange={(e) => setFilters(prev => ({ ...prev, university: e.target.value }))}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm"
                      >
                        <option value="">All Universities</option>
                        {filterOptions?.universities.map(uni => (
                          <option key={uni.id} value={uni.short}>{uni.name}</option>
                        ))}
                      </select>
                    </div>

                    <div>
                      <h3 className="font-semibold text-gray-700 mb-3">Quick Filters</h3>
                      <div className="space-y-2">
                        <label className="flex items-center gap-2 cursor-pointer">
                          <input
                            type="checkbox"
                            checked={filters.furnished || false}
                            onChange={(e) => setFilters(prev => ({ ...prev, furnished: e.target.checked ? true : undefined }))}
                            className="rounded text-blue-600 focus:ring-blue-500"
                          />
                          <span className="text-sm text-gray-700">Furnished Only</span>
                        </label>
                        <label className="flex items-center gap-2 cursor-pointer">
                          <input
                            type="checkbox"
                            checked={filters.parking}
                            onChange={(e) => setFilters(prev => ({ ...prev, parking: e.target.checked }))}
                            className="rounded text-blue-600 focus:ring-blue-500"
                          />
                          <span className="text-sm text-gray-700">Parking Available</span>
                        </label>
                      </div>
                    </div>

                    <button
                      onClick={applyFilters}
                      className="w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 transition-colors font-semibold"
                    >
                      Apply Filters
                    </button>
                  </div>
                </div>
              </motion.aside>
            )}
          </AnimatePresence>

          <div className="flex-1">
            {isLoading && (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {[...Array(6)].map((_, i) => (
                  <div key={i} className="bg-white rounded-lg shadow-md overflow-hidden animate-pulse">
                    <div className="h-48 bg-gray-300" />
                    <div className="p-4 space-y-3">
                      <div className="h-4 bg-gray-300 rounded w-3/4" />
                      <div className="h-3 bg-gray-300 rounded w-1/2" />
                      <div className="h-3 bg-gray-300 rounded w-full" />
                    </div>
                  </div>
                ))}
              </div>
            )}

            {isError && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
                <p className="text-red-800 font-semibold">Error loading rooms</p>
                <p className="text-red-600 text-sm mt-2">{error?.message}</p>
              </div>
            )}

            {!isLoading && data && data.rooms.length === 0 && (
              <div className="bg-white rounded-lg shadow-md p-12 text-center">
                <svg className="w-16 h-16 mx-auto text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <h3 className="text-xl font-semibold text-gray-800 mb-2">No rooms found</h3>
                <p className="text-gray-600 mb-4">Try adjusting your filters or search criteria</p>
                <button
                  onClick={resetFilters}
                  className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  Clear Filters
                </button>
              </div>
            )}

            {!isLoading && data && data.rooms.length > 0 && (
              <>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {data.rooms.map((room, index) => (
                    <Card key={room.id} room={room} index={index} />
                  ))}
                </div>

                {data.totalPages > 1 && (
                  <div className="flex justify-center items-center gap-2 mt-8">
                    <button
                      onClick={() => setPage(p => Math.max(1, p - 1))}
                      disabled={page === 1}
                      className="px-4 py-2 border border-gray-300 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
                    >
                      Previous
                    </button>
                    
                    <div className="flex gap-1">
                      {[...Array(data.totalPages)].map((_, i) => (
                        <button
                          key={i}
                          onClick={() => setPage(i + 1)}
                          className={`px-4 py-2 rounded-lg ${
                            page === i + 1
                              ? 'bg-blue-600 text-white'
                              : 'border border-gray-300 hover:bg-gray-50'
                          }`}
                        >
                          {i + 1}
                        </button>
                      ))}
                    </div>

                    <button
                      onClick={() => setPage(p => Math.min(data.totalPages, p + 1))}
                      disabled={page === data.totalPages}
                      className="px-4 py-2 border border-gray-300 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
                    >
                      Next
                    </button>
                  </div>
                )}
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default SearchResultsPage;