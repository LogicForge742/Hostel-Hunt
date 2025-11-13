import { useState, useEffect, useCallback } from 'react';
import { useSearchParams } from 'react-router-dom';

/** 
 * @param {number} delay - Debounce delay in milliseconds (default: 500)
 * @returns {object} Search state and methods
 */
const useSearch = (delay = 500) => {
    const [searchParams, setSearchParams] = useSearchParams();
    // the raw search input value (user typing)
    const [searchTerm, setSearchTerm] = useState('');
    // the debounced search term used for actual searching
    const [debouncedTerm, setDebouncedTerm] = useState('');
    // indicates whether a search is currently in progress
    const [isSearching, setIsSearching] = useState(false);

  // initialize from URL params
    useEffect(() => {
        const location = searchParams.get('location') || '';
        setSearchTerm(location);
        setDebouncedTerm(location);
    }, [searchParams]);

  // debounce search term
    useEffect(() => {
        //start a timer to update debounced term after delay
        const timer = setTimeout(() => {
        setDebouncedTerm(searchTerm);
        setIsSearching(false);
        }, delay);

    // set searching state immediately when term changes
        if (searchTerm !== debouncedTerm) {
        setIsSearching(true);
        }
        //cleanup function to clear timer if term changes before delay
        return () => clearTimeout(timer);
    }, [searchTerm, delay, debouncedTerm]);

    //update search term
    const updateSearchTerm = useCallback((term) => {
        setSearchTerm(term);
    }, []);

    /* update URL search params*/
    const updateSearchParams = useCallback((params) => {
        const newParams = new URLSearchParams(searchParams);
        
        Object.entries(params).forEach(([key, value]) => {
        if (value) {
            newParams.set(key, value);
        } else {
            newParams.delete(key);
        }
        });

        setSearchParams(newParams);
    }, [searchParams, setSearchParams]);

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
        setSearchParams(new URLSearchParams());
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
        updateSearchTerm,
        updateSearchParams,
        executeSearch,
        clearSearch
    };
    };

export default useSearch;