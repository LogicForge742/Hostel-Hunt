import { Link } from 'react-router-dom';
import { useState } from 'react';
import { motion } from 'framer-motion';

export default function Header() {
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <header className="sticky top-0 bg-white dark:bg-gray-900 shadow-md z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Simple text logo */}
          <Link to="/" className="text-2xl font-bold">
            HostelHunt
          </Link>

          {/* Desktop Nav */}
          <nav className="hidden md:flex items-center space-x-6">
            <Link to="/" className="hover:text-blue-600 dark:hover:text-blue-400">Home</Link>
            <Link to="/search" className="hover:text-blue-600 dark:hover:text-blue-400">Explore</Link>
            <Link to="/login" className="hover:text-blue-600 dark:hover:text-blue-400">Login</Link>
            <Link to="/signup" className="px-4 py-2 bg-gray-200 dark:bg-gray-700 rounded hover:bg-gray-300 dark:hover:bg-gray-600">
              Sign Up
            </Link>
          </nav>

          {/* Mobile Toggle */}
          <button
            onClick={() => setMobileOpen(!mobileOpen)}
            className="md:hidden text-2xl"
          >
            {mobileOpen ? 'Close' : 'Menu'}
          </button>
        </div>

        {/* Mobile Menu */}
        <motion.nav
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: mobileOpen ? 1 : 0, y: mobileOpen ? 0 : -10 }}
          className={`md:hidden border-t py-4 space-y-2 ${mobileOpen ? 'block' : 'hidden'}`}
        >
          <Link to="/" className="block px-4 py-2">Home</Link>
          <Link to="/search" className="block px-4 py-2">Explore</Link>
          <Link to="/login" className="block px-4 py-2">Login</Link>
          <Link to="/signup" className="block px-4 py-2 font-medium">Sign Up</Link>
        </motion.nav>
      </div>
    </header>
  );
}
