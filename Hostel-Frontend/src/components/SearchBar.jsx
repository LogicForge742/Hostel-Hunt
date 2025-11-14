import { useState, useRef, useEffect } from 'react';
import { AnimatePresence } from 'framer-motion';
import { motion } from 'framer-motion';
export const SearchBar = ({ onSearch, initialValues = {} }) => {
    //hold user current text input
    const [searchQuery, setSearchQuery] = useState(initialValues.query || '');
    const [showSuggestions, setShowSuggestions] = useState(false);
    //reference for detecting clicks outside the search input
    const searchRef = useRef(null);

    //university filters
    const universities = [
        { id: 1, name: 'University of Nairobi', short: 'UoN' },
        { id: 2, name: 'Kenyatta University', short: 'KU' },
        { id: 3, name: 'JKUAT', short: 'JKUAT' },
        { id: 4, name: 'Daystar University', short: 'Daystar' },
        { id: 5, name: 'Strathmore University', short: 'Strathmore' },
        { id: 6, name: 'USIU', short: 'USIU' }

    ];

    //location suggestions
    const suggestions = [
    { id: 1, name: 'Parklands - Near UoN', type: 'location' },
    { id: 2, name: 'Kahawa Wendani - KU Area', type: 'location'},
    { id: 3, name: 'Juja - JKUAT Gate', type: 'location' },
    { id: 4, name: 'University of Nairobi', type: 'university' },
    { id: 5, name: 'Kenyatta University', type: 'university'},
    { id: 6, name: 'JKUAT', type: 'university'}
    ];

    //filter logic for suggestions
    const filteredSuggestions = searchQuery
    ? suggestions.filter(s =>
        s.name.toLowerCase().includes(searchQuery.toLowerCase())
        )
    : suggestions.slice(0, 4);

    //close dropdown when clicking outside
    useEffect(() => {
    const handleClickOutside = (event) => {
        if (searchRef.current && !searchRef.current.contains(event.target)) {
            setShowSuggestions(false);
        }
    };

    document.addEventListener('mousedown', handleClickOutside);
    //cleanup event listener on unmount
    return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);
//EVENT HANDLERS
    //handle form submission
    const handleSubmit = (e) => {
        e.preventDefault();

    if (!searchQuery.trim()) {
        return; //do nothing if input is empty
    }

    onSearch({ query: searchQuery });
    setShowSuggestions(false);
    };
    //when a university filter is clicked
    const handleUniversityClick = (university) => {
    setSearchQuery(university.name);
    onSearch({ query: university.name, type: 'university' });
    };

    //when a suggestion from the dropdown is clicked
    const handleSuggestionClick = (suggestion) => {
    setSearchQuery(suggestion.name);
    setShowSuggestions(false);
    onSearch({ query: suggestion.name, type: suggestion.type });
    };
// RENDER
    return(
        <div className="w-full max-w-4xl mx-auto">
        {/* main search Container with dashed border */}
        <div className="bg-white rounded-3xl p-6 border-4 border-dashed border-purple-300 shadow-xl">
        <form onSubmit={handleSubmit}>
          {/* search input field */}
            <div className="relative mb-6" ref={searchRef}>
                <div className="relative">
                    <input
                    type="text"
                    value={searchQuery}
                    onChange={(e) => {
                        setSearchQuery(e.target.value);
                        setShowSuggestions(true);
                    }}
                    onFocus={() => setShowSuggestions(true)}
                    placeholder="Search by location or university..."
                    className="w-full pl-12 pr-4 py-4 bg-gray-50 border-2 border-gray-200 rounded-2xl focus:border-purple-500 focus:outline-none focus:ring-2 focus:ring-purple-200 transition-all text-gray-800 placeholder-gray-400 text-lg"
                    />
                    {/* search icon */}
                    <svg 
                    className="absolute left-4 top-1/2 -translate-y-1/2 w-6 h-6 text-purple-500"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    >
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                    </svg>

                    {/* search button (mobile) */}
                        <button
                        type="submit"
                        className="md:hidden absolute right-2 top-1/2 -translate-y-1/2 bg-gradient-to-r from-pink-500 to-orange-500 text-white px-6 py-2 rounded-xl font-bold hover:from-pink-600 hover:to-orange-600 transition-all"
                        >
                        Search
                        </button>
                </div>

                {/* autocomplete suggestions dropdown */}
                <AnimatePresence>
                    {showSuggestions && searchQuery && (
                    <motion.div
                        initial={{ opacity: 0, y: -10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -10 }}
                        transition={{ duration: 0.2 }}
                        className="absolute z-50 w-full mt-2 bg-white rounded-2xl shadow-2xl border-2 border-purple-100 overflow-hidden"
                    >
                        {filteredSuggestions.length > 0 ? (
                        filteredSuggestions.map((suggestion) => (
                            <button
                            key={suggestion.id}
                            type="button"
                            onClick={() => handleSuggestionClick(suggestion)}
                            className="w-full px-4 py-3 hover:bg-purple-50 transition-colors text-left flex items-center gap-3 group border-b border-gray-100 last:border-0"
                            >
                            <span className="text-2xl">{suggestion.icon}</span>
                            <div className="flex-1">
                                <div className="font-semibold text-gray-800 group-hover:text-purple-600 transition-colors">
                                {suggestion.name}
                                </div>
                                <div className="text-xs text-gray-500 capitalize">{suggestion.type}</div>
                            </div>
                            </button>
                        ))
                        ) : (
                        <div className="px-4 py-3 text-gray-500 text-center">
                            No results found
                        </div>
                        )}
                    </motion.div>
                    )}
                </AnimatePresence>
            </div>

            {/* university filters*/}
                <div className="flex flex-wrap gap-3 mb-4">
                {universities.map((uni) => (
                    <motion.button
                    key={uni.id}
                    type="button"
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => handleUniversityClick(uni)}
                    className={`px-5 py-2 rounded-full font-semibold border-2 transition-all ${
                    searchQuery === uni.name
                        ? 'bg-purple-600 text-white border-purple-600'
                        : 'bg-white text-purple-600 border-purple-300 hover:border-purple-500 hover:bg-purple-50'
                    }`}
                >
                    {uni.short}
                </motion.button>
                ))}
            </div>

            {/* main search button */}
            <motion.button
                type="submit"
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="hidden md:block w-full bg-gradient-to-r from-pink-500 to-orange-500 text-white py-4 rounded-2xl font-bold text-lg hover:from-pink-600 hover:to-orange-600 transition-all shadow-lg hover:shadow-xl border-2 border-black"
            >
                Search
            </motion.button>
        </form>
        </div>
    </div>
    );
};



    

