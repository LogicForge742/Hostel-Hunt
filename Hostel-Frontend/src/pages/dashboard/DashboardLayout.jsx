import { Link, Outlet, useLocation } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext.jsx';

export default function DashboardLayout() {
  const { user, logout } = useAuth();
  const location = useLocation();

  const tabs = [
    { id: 'bookings', label: 'My Bookings', path: '/dashboard' },
    { id: 'favorites', label: 'Favorites', path: '/dashboard/favorites' }
  ];

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
              <span className="text-gray-700">Welcome, {user?.name}</span>
              <button
                onClick={logout}
                className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
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
            <nav className="flex">
              {tabs.map((tab) => (
                <Link
                  key={tab.id}
                  to={tab.path}
                  className={`px-6 py-4 text-sm font-medium border-b-2 transition-colors ${
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
            <Outlet />
          </div>
        </div>
      </div>
    </div>
  );
}
