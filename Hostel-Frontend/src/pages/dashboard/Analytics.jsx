import { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';

export default function Analytics() {
  const { user } = useAuth();
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    try {
      setLoading(true);
      // TODO: Replace with actual API call when backend endpoint is ready
      // const response = await fetch('/api/landlord/analytics', {
      //   headers: { Authorization: `Bearer ${token}` }
      // });
      // const data = await response.json();

      // Mock data for now
      const mockData = {
        totalRevenue: 125000,
        monthlyRevenue: 15000,
        totalBookings: 45,
        activeBookings: 12,
        occupancyRate: 78,
        averageRating: 4.2,
        topHostel: {
          name: "Sunset Apartments",
          revenue: 35000,
          bookings: 15
        },
        monthlyTrend: [
          { month: 'Jan', revenue: 12000, bookings: 8 },
          { month: 'Feb', revenue: 15000, bookings: 12 },
          { month: 'Mar', revenue: 18000, bookings: 15 },
          { month: 'Apr', revenue: 22000, bookings: 10 }
        ]
      };

      setAnalytics(mockData);
    } catch (err) {
      setError('Failed to load analytics data');
      console.error('Analytics fetch error:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <p className="text-red-600 mb-4">{error}</p>
        <button
          onClick={fetchAnalytics}
          className="bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700"
        >
          Try Again
        </button>
      </div>
    );
  }

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Analytics Dashboard</h1>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-gradient-to-r from-blue-500 to-blue-600 rounded-lg p-6 text-white">
          <h3 className="text-sm font-medium opacity-90">Total Revenue</h3>
          <p className="text-3xl font-bold">KES {analytics.totalRevenue.toLocaleString()}</p>
          <p className="text-sm opacity-75 mt-2">+12% from last month</p>
        </div>

        <div className="bg-gradient-to-r from-green-500 to-green-600 rounded-lg p-6 text-white">
          <h3 className="text-sm font-medium opacity-90">Monthly Revenue</h3>
          <p className="text-3xl font-bold">KES {analytics.monthlyRevenue.toLocaleString()}</p>
          <p className="text-sm opacity-75 mt-2">Current month</p>
        </div>

        <div className="bg-gradient-to-r from-purple-500 to-purple-600 rounded-lg p-6 text-white">
          <h3 className="text-sm font-medium opacity-90">Total Bookings</h3>
          <p className="text-3xl font-bold">{analytics.totalBookings}</p>
          <p className="text-sm opacity-75 mt-2">All time</p>
        </div>

        <div className="bg-gradient-to-r from-orange-500 to-orange-600 rounded-lg p-6 text-white">
          <h3 className="text-sm font-medium opacity-90">Occupancy Rate</h3>
          <p className="text-3xl font-bold">{analytics.occupancyRate}%</p>
          <p className="text-sm opacity-75 mt-2">Average across properties</p>
        </div>
      </div>

      {/* Charts and Detailed Analytics */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* Revenue Trend Chart */}
        <div className="bg-white border rounded-lg p-6">
          <h3 className="text-lg font-semibold mb-4">Revenue Trend</h3>
          <div className="h-64 flex items-end justify-between space-x-2">
            {analytics.monthlyTrend.map((data, index) => (
              <div key={index} className="flex-1 flex flex-col items-center">
                <div
                  className="bg-blue-500 w-full rounded-t"
                  style={{ height: `${(data.revenue / 25000) * 200}px` }}
                ></div>
                <span className="text-xs mt-2 text-gray-600">{data.month}</span>
                <span className="text-xs text-gray-500">KES {data.revenue.toLocaleString()}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Top Performing Hostel */}
        <div className="bg-white border rounded-lg p-6">
          <h3 className="text-lg font-semibold mb-4">Top Performing Property</h3>
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="font-medium">{analytics.topHostel.name}</span>
              <span className="text-green-600 font-semibold">★ Top</span>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="text-center">
                <p className="text-2xl font-bold text-blue-600">{analytics.topHostel.bookings}</p>
                <p className="text-sm text-gray-600">Bookings</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold text-green-600">KES {analytics.topHostel.revenue.toLocaleString()}</p>
                <p className="text-sm text-gray-600">Revenue</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Additional Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white border rounded-lg p-6">
          <h3 className="text-lg font-semibold mb-2">Active Bookings</h3>
          <p className="text-3xl font-bold text-purple-600">{analytics.activeBookings}</p>
          <p className="text-sm text-gray-600 mt-1">Currently occupied</p>
        </div>

        <div className="bg-white border rounded-lg p-6">
          <h3 className="text-lg font-semibold mb-2">Average Rating</h3>
          <div className="flex items-center">
            <span className="text-3xl font-bold text-yellow-500 mr-2">{analytics.averageRating}</span>
            <div className="flex">
              {[...Array(5)].map((_, i) => (
                <span key={i} className={`text-lg ${i < Math.floor(analytics.averageRating) ? 'text-yellow-400' : 'text-gray-300'}`}>
                  ★
                </span>
              ))}
            </div>
          </div>
          <p className="text-sm text-gray-600 mt-1">Across all properties</p>
        </div>

        <div className="bg-white border rounded-lg p-6">
          <h3 className="text-lg font-semibold mb-2">Growth Rate</h3>
          <p className="text-3xl font-bold text-green-600">+15%</p>
          <p className="text-sm text-gray-600 mt-1">Month over month</p>
        </div>
      </div>

      {/* Note about mock data */}
      <div className="mt-8 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
        <p className="text-yellow-800 text-sm">
          <strong>Note:</strong> This analytics dashboard is currently displaying mock data.
          Backend API endpoints for real analytics data need to be implemented.
        </p>
      </div>
    </div>
  );
}
