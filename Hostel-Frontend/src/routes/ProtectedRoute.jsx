// src/routes/ProtectedRoute.jsx
import { Navigate, Outlet, useLocation } from "react-router-dom";
import { useAuth } from "../hooks/useAuth.jsx"; // Custom hook from AuthContext

export default function ProtectedRoute() {
  const { user, loading } = useAuth(); // Access user + loading from context
  const location = useLocation(); // Get current route location

  // While auth state is still being restored (e.g., from localStorage)
  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <p className="text-gray-500">Checking authentication...</p>
      </div>
    );
  }

  // If user is authenticated, render nested routes
  // Otherwise, redirect to login and remember the route they came from
  return user ? (
    <Outlet />
  ) : (
    <Navigate to="/login" replace state={{ from: location }} />
  );
}
