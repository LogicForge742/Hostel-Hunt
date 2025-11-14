import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import SearchBar from '../../components/SearchBar';

const HomePage = () => {
    const navigate = useNavigate();
    const [featuredRooms, setFeaturedRooms] = useState([]);

  // mock featured rooms - replace with actual API call
    useEffect(() => {
        const loadRooms = () => {
        const mockRooms = [
            {
            id: 1,
            title: 'Cozy Studio near UoN Main Campus',
            location: 'Parklands, 5 min walk to campus',
            university: 'University of Nairobi',
            price: 12000,
            image: '/assets/room1.jpg',
            borderColor: 'border-purple-400',
            featured: true
            },
            {
            id: 2,
            title: 'Modern Single Room - KU Campus',
            location: 'Kahawa Wendani, 10 min from KU',
            university: 'Kenyatta University',
            price: 8500,
            image: '/assets/room2.jpg',
            borderColor: 'border-pink-400',
            featured: true
            },
            {
            id: 3,
            title: 'Affordable Bedsitter JKUAT',
            location: 'Juja, near JKUAT Gate',
            university: 'JKUAT',
            price: 7000,
            image: '/assets/room3.jpg',
            borderColor: 'border-yellow-400',
            featured: false
            },
            {
            id: 4,
            title: 'Shared Room near Daystar',
            location: 'Athi River, Walking distance',
            university: 'Daystar University',
            price: 5000,
            image: '/assets/room4.jpg',
            borderColor: 'border-blue-400',
            featured: false
            },
            {
            id: 5,
            title: 'Spacious 1BR near Strathmore',
            location: 'Madaraka, 15 min to campus',
            university: 'Strathmore University',
            price: 18000,
            image: '/assets/room5.jpg',
            borderColor: 'border-green-400',
            featured: false
            },
            {
            id: 6,
            title: 'Budget Single Room USIU',
            location: 'Kasarani, Near USIU',
            university: 'USIU',
            price: 6500,
            image: '/assets/room6.jpg',
            borderColor: 'border-orange-400',
            featured: false
            }
        ];
        //set mock data to state
        setFeaturedRooms(mockRooms);
        };

        loadRooms();
    }, []);
    //triggered when search is performed in SearchBar
    const handleSearch = (searchParams) => {
        //convert search parameters into a query string and redirects the user to the search page
        const params = new URLSearchParams(searchParams);
        navigate(`/search?${params.toString()}`);
    };

    return (
      <div className="min-h-screen bg-linear-to-b from-pink-50 via-white to-purple-50">
        {/* Hero Section */}
        <section className="relative pt-16 pb-32 px-4 w-full">
            <div className="w-full max-w-7xl mx-auto">
            <motion.div
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6 }}
                className="flex justify-center mb-8"
            >
                <div className="bg-yellow-200 border-3 border-black rounded-full px-6 py-3 flex items-center gap-2 shadow-lg">
                <span className="font-semibold text-gray-800">47,000+ Students Trust Us</span>
                </div>
            </motion.div>

            {/* Hero Title */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2, duration: 0.6 }}
                className="text-center mb-6"
            >
                <h1 className="text-5xl md:text-7xl font-bold mb-4 leading-tight">
                <span className="bg-gradient-to-r from-purple-600 via-pink-500 to-orange-500 bg-clip-text text-transparent">
                    Find Your Perfect Student Hostel
                </span>
                </h1>
                <p className="text-gray-700 text-lg md:text-xl max-w-3xl mx-auto">
                No brokers. No hassle. Connect directly with landlords for affordable hostel under 20K near Nairobi's top universities.
                </p>
            </motion.div>

            {/* search bar */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4, duration: 0.6 }}
                className="mt-12"
            >
                <SearchBar onSearch={handleSearch} />
            </motion.div>
            </div>
        </section>

        {/* Featured rooms section */}
        <section className="container mx-auto px-4 pb-16">
            <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            >
            {/* section header */}
            <div className="flex justify-between items-center mb-8">
                <div className="flex items-center gap-2">
                <h2 className="text-3xl md:text-4xl font-bold bg-linear-to-r from-purple-600 to-pink-500 bg-clip-text text-transparent">
                    Featured Rooms
                </h2>
                </div>
                <button
                onClick={() => navigate('/search')}
                className="flex items-center gap-2 px-6 py-3 border-2 border-purple-600 text-purple-600 rounded-full font-semibold hover:bg-purple-600 hover:text-white transition-all duration-300"
                >
                View All
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                </svg>
                </button>
            </div>

            <p className="text-gray-600 mb-8">Fresh listings from trusted landlords</p>

            {/* hostels grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {featuredRooms.map((room, index) => (
                <motion.div
                    key={room.id}
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ delay: index * 0.1, duration: 0.5 }}
                    whileHover={{ y: -8, transition: { duration: 0.2 } }}
                    onClick={() => navigate(`/hostel/${room.id}`)}
                    className={`bg-white rounded-3xl overflow-hidden cursor-pointer border-4 ${room.borderColor} shadow-lg hover:shadow-2xl transition-all duration-300 relative group`}
                >
                    {/* bookmark icon */}
                    <div className="absolute top-4 left-4 z-10">
                    <div className="w-10 h-10 bg-yellow-400 rounded-full flex items-center justify-center border-2 border-black shadow-md">
                        <svg className="w-5 h-5 text-black" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M5 4a2 2 0 012-2h6a2 2 0 012 2v14l-5-2.5L5 18V4z" />
                        </svg>
                    </div>
                    </div>

                    {/* price badge */}
                    <div className="absolute top-4 right-4 z-10">
                    <div className="bg-gradient-to-r from-purple-600 to-pink-500 text-white px-4 py-2 rounded-full font-bold shadow-lg border-2 border-white">
                        KES {room.price.toLocaleString()}/mo
                    </div>
                    </div>

                    {/* room image */}
                    <div className="relative h-64 bg-linear-to-br from-gray-100 to-gray-200 overflow-hidden">
                    <div className="absolute inset-0 flex items-center justify-center text-gray-400">
                        <svg className="w-20 h-20" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" clipRule="evenodd" />
                        </svg>
                    </div>

                    {/* hover overlay */}
                    <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-10 transition-all duration-300" />
                    </div>

                    {/* room details */}
                    <div className="p-6">
                    <h3 className="text-xl font-bold text-gray-900 mb-3 line-clamp-1 group-hover:text-purple-600 transition-colors">
                        {room.title}
                    </h3>

                    <div className="flex items-start gap-2 mb-4 text-gray-600">
                        <svg className="w-5 h-5 mt-0.5 shrink-0" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd" />
                        </svg>
                        <span className="text-sm">{room.location}</span>
                    </div>

                    <div className="inline-block">
                        <span className="bg-yellow-200 text-yellow-800 px-3 py-1 rounded-full text-xs font-semibold border border-yellow-300">
                        {room.university}
                        </span>
                    </div>
                    </div>
                </motion.div>
                ))}
            </div>
            </motion.div>
        </section>

        {/* Why Choose Us Section */}
        <section className="bg-linear-to-br from-purple-50 to-pink-50 py-16">
            <div className="container mx-auto px-4">
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6 }}
                className="text-center mb-12"
            >
                <h2 className="text-3xl md:text-4xl font-bold mb-4 bg-gradient-to-r from-purple-600 to-pink-500 bg-clip-text text-transparent">
                Why Students Love Us
                </h2>
                <p className="text-gray-700 max-w-2xl mx-auto">
                Making student accommodation search easier and safer
                </p>
            </motion.div>

            <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
                {[
                {
                    
                    title: 'Direct Connect',
                    description: 'No middlemen or broker fees. Chat directly with verified landlords',
                    color: 'from-purple-400 to-purple-600'
                },
                {
                    
                    title: 'Affordable Options',
                    description: 'Find rooms under 20K near your university with transparent pricing',
                    color: 'from-pink-400 to-pink-600'
                },
                {
                    
                    title: 'Verified Listings',
                    description: 'All landlords verified. Read reviews from fellow students',
                    color: 'from-orange-400 to-orange-600'
                }
                ].map((feature, index) => (
                <motion.div
                    key={index}
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ delay: index * 0.2, duration: 0.6 }}
                    whileHover={{ y: -5 }}
                    className="bg-white rounded-2xl p-8 text-center shadow-lg hover:shadow-xl transition-all duration-300 border-2 border-gray-100"
                >
                    <div className="text-5xl mb-4">{feature.icon}</div>
                    <h3 className={`text-xl font-bold mb-3 bg-linear-to-r ${feature.color} bg-clip-text text-transparent`}>
                    {feature.title}
                    </h3>
                    <p className="text-gray-600 leading-relaxed">{feature.description}</p>
                </motion.div>
                ))}
            </div>
            </div>
        </section>
        

        {/* Floating Post Room Button */}
        <motion.button
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 1, type: "spring", stiffness: 260, damping: 20 }}
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            onClick={() => navigate('/dashboard')}
            className="fixed bottom-8 right-8 bg-linear-to-r from-orange-500 to-pink-500 text-white px-6 py-4 rounded-full font-bold shadow-2xl flex items-center gap-2 border-3 border-black hover:shadow-3xl transition-all duration-300 z-50"
        >
            <span className="hidden md:inline">Post Your Room</span>
        </motion.button>
      </div>
    );
    };

export default HomePage;
