import { useState, useEffect, useCallback, useMemo } from 'react';
import { useSearchParams } from 'react-router-dom';

const useSearch = (delay = 500) => {
    const [searchParams, setSearchParams] = useSearchParams();
    // the raw search input value (user typing) - initialize lazily from URL once
    const [searchTerm, setSearchTerm] = useState(() => searchParams.get('location') || '');
    // the debounced search term used for actual searching - initialize from URL once
    const [debouncedTerm, setDebouncedTerm] = useState(() => searchParams.get('location') || '');
    // indicates whether a search is currently in progress
    const [isSearching, setIsSearching] = useState(false);

  // derive current location from URL params; avoid syncing state in an effect
    const currentLocation = useMemo(() => searchParams.get('location') || '', [searchParams]);
    // If URL location changes (navigation), reflect it by updating input state at update time
    // Consumers should use "searchParams.location" for the authoritative URL-derived value.

  // debounce search term
    useEffect(() => {
        //start a timer to update debounced term after delay
        const timer = setTimeout(() => {
            setDebouncedTerm(searchTerm);
            setIsSearching(false);
        }, delay);
        //cleanup function to clear timer if term changes before delay
        return () => clearTimeout(timer);
    }, [searchTerm, delay]);

    //update search term
    const updateSearchTerm = useCallback((term) => {
        setSearchTerm(term);
        // mark searching immediately on user input
        setIsSearching(true);
    }, []);

    /* update URL search params*/
    const updateSearchParams = useCallback((params) => {
        setSearchParams(prev => {
            const newParams = new URLSearchParams(prev);
            Object.entries(params).forEach(([key, value]) => {
                if (value !== undefined && value !== null && value !== '') {
                    newParams.set(key, Array.isArray(value) ? value.join(',') : String(value));
                } else {
                    newParams.delete(key);
                }
            });
            return newParams;
        });
    }, [setSearchParams]);

    /*get current search params as object*/
    const getSearchParams = () => ({
        location: searchParams.get('location') || '',
        checkIn: searchParams.get('checkIn') || '',
        checkOut: searchParams.get('checkOut') || '',
        guests: parseInt(searchParams.get('guests')) || 1,
        minPrice: parseFloat(searchParams.get('minPrice')) || null,
        maxPrice: parseFloat(searchParams.get('maxPrice')) || null,
        rating: parseFloat(searchParams.get('rating')) || null,
        amenities: searchParams.get('amenities')?.split(',').filter(Boolean) || [],
        sortBy: searchParams.get('sortBy') || 'relevance'
    });

    /*clear all search params*/
    const clearSearch = useCallback(() => {
        setSearchParams(() => new URLSearchParams());
        setSearchTerm('');
        setDebouncedTerm('');
    }, [setSearchParams]);

    /*execute search with full parameters*/
    const executeSearch = useCallback((params) => {
        updateSearchParams(params);
    }, [updateSearchParams]);
        //return the hook's public API for use in components
        return {
        searchTerm,
        debouncedTerm,
        isSearching,
        searchParams: getSearchParams(),
        // expose the URL-derived current location separately to avoid effect syncing
        urlLocation: currentLocation,
        updateSearchTerm,
        updateSearchParams,
        executeSearch,
        clearSearch
    };
    };

export default useSearch;