import { Link, Outlet, useLocation } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext.jsx';

export default function DashboardLayout() {
  const { user, logout } = useAuth();
  const location = useLocation();

  //NE
  // Define tabs based on user role - landlords get different navigation
  const getTabsForRole = () => {
    // NE  Landlord-specific tabs for property management
    if (user?.role === 'landlord') {
      return [
        { id: 'my-hostels', label: 'My Hostels', path: '/dashboard/my-hostels' },
        { id: 'hostel-bookings', label: 'Hostel Bookings', path: '/dashboard/hostel-bookings' },
        { id: 'analytics', label: 'Analytics', path: '/dashboard/analytics' }
      ];
    }
    
    // OOO Default tabs for students/regular users (preserved)
    return [
      { id: 'bookings', label: 'My Bookings', path: '/dashboard' },
      { id: 'favorites', label: 'Favorites', path: '/dashboard/favorites' }
    ];
  };

  // NE Get tabs dynamically based on user role
  const tabs = getTabsForRole();
  // END NEW CODE

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link to="/" className="text-xl font-bold text-gray-900">
              Hostel Hunt
            </Link>
            <div className="flex items-center space-x-4">
              {/* NE Enhanced user info section with role badge */}
              <div className="flex items-center space-x-2">
                <span className="text-gray-700">Welcome, {user?.name}</span>
                {/* NE Landlord badge indicator */}
                {user?.role === 'landlord' && (
                  <span className="px-2 py-1 text-xs font-semibold text-purple-600 bg-purple-100 rounded-full">
                    Landlord
                  </span>
                )}
              </div>
              {/* OOO Logout button (preserved) */}
              <button
                onClick={logout}
                className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700 transition-colors"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white rounded-lg shadow">
          {/* Tabs */}
          <div className="border-b border-gray-200">
            {/* NE  Added overflow-x-auto for mobile responsiveness */}
            <nav className="flex -mb-px overflow-x-auto">
              {/* OOO Tab mapping logic (preserved) */}
              {tabs.map((tab) => (
                <Link
                  key={tab.id}
                  to={tab.path}
                  className={`px-6 py-4 text-sm font-medium border-b-2 transition-colors whitespace-nowrap ${
                    location.pathname === tab.path
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  {tab.label}
                </Link>
              ))}
            </nav>
          </div>

          {/* Content */}
          <div className="p-6">
            {/*OO Outlet for nested routes (preserved) */}
            <Outlet />
          </div>
        </div>
      </div>
    </div>
  );
}