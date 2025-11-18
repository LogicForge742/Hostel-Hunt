import { Link, useNavigate } from 'react-router-dom';
import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useAuth } from '../context/AuthContext';

export default function Header() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  return (
    <header className="sticky top-0 bg-white shadow-sm z-50 border-b border-gray-100">
      <div className="w-full px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-20">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-3 hover:opacity-80 transition-opacity">
            
            <span className="text-2xl font-bold text-primary">
              Hostel Hunt
            </span>
          </Link>

          {/* Desktop Nav */}
          <nav className="hidden md:flex items-center gap-8">
            {user ? (
              <>
                <span className="text-text-body font-medium">
                  Welcome, {user.name}
                </span>
                <button
                  onClick={logout}
                  className="bg-red-500 text-white px-6 py-2.5 rounded-full font-semibold hover:bg-red-600 transition-all duration-300"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link
                  to="/login"
                  className="text-text-body hover:text-hover font-medium transition-colors"
                >
                  Login
                </Link>
                <button
                  onClick={() => navigate('/signup')}
                  className="bg-primary text-white px-6 py-2.5 rounded-full font-semibold hover:bg-hover transition-all duration-300"
                >
                  Register
                </button>
              </>
            )}
          </nav>

          {/* Mobile Hamburger */}
          <button
            onClick={() => setMobileOpen(!mobileOpen)}
            className="md:hidden relative w-10 h-10 flex items-center justify-center rounded-lg hover:bg-gray-100 transition-colors"
            aria-label="Toggle menu"
          >
            <div className="w-6 flex flex-col gap-1.5">
              <motion.span
                animate={mobileOpen ? { rotate: 45, y: 8 } : { rotate: 0, y: 0 }}
                className="w-full h-0.5 bg-gray-800 rounded-full transition-all"
              />
              <motion.span
                animate={mobileOpen ? { opacity: 0 } : { opacity: 1 }}
                className="w-full h-0.5 bg-gray-800 rounded-full transition-all"
              />
              <motion.span
                animate={mobileOpen ? { rotate: -45, y: -8 } : { rotate: 0, y: 0 }}
                className="w-full h-0.5 bg-gray-800 rounded-full transition-all"
              />
            </div>
          </button>
        </div>

        {/* Mobile Menu */}
        <AnimatePresence>
          {mobileOpen && (
            <motion.nav
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              transition={{ duration: 0.2 }}
              className="md:hidden border-t border-gray-100 py-4 space-y-1 overflow-hidden"
            >
              <Link
                to="/"
                onClick={() => setMobileOpen(false)}
                className="block px-4 py-3 text-text-body hover:bg-highlight hover:text-primary rounded-lg transition-colors font-medium"
              >
                Home
              </Link>

              {user ? (
                <>
                  <span className="block px-4 py-3 text-text-body font-medium">
                    Welcome, {user.name}
                  </span>
                  <button
                    onClick={() => {
                      logout();
                      setMobileOpen(false);
                    }}
                    className="w-full text-left px-4 py-3 bg-red-500 text-white rounded-lg font-semibold mt-2 hover:bg-red-600"
                  >
                    Logout
                  </button>
                </>
              ) : (
                <>
                  <Link
                    to="/login"
                    onClick={() => setMobileOpen(false)}
                    className="block px-4 py-3 text-text-body hover:bg-highlight hover:text-primary rounded-lg transition-colors font-medium"
                  >
                    Login
                  </Link>
                  <button
                    onClick={() => {
                      setMobileOpen(false);
                      navigate('/signup');
                    }}
                    className="w-full text-left px-4 py-3 bg-primary text-white rounded-lg font-semibold mt-2 hover:bg-hover"
                  >
                    Register
                  </button>
                </>
              )}
            </motion.nav>
          )}
        </AnimatePresence>
      </div>
    </header>
  );
}