import { Route, Routes } from "react-router-dom";
import Layout from '../components/Layout.jsx';
import ProtectedRoute from './ProtectedRoute.jsx';


// These are the place holders
import HomePage from '../pages/home/HomePage.jsx';
import LoginPage from '../pages/auth/LoginPage.jsx';
import SignupPage from '../pages/auth/SignupPage.jsx';
import SearchResultsPage from '../pages/search/SearchResultsPage.jsx';
import HostelDetailPage from '../pages/hostel/HostelDetailPage.jsx';
import BookingPage from '../pages/booking/BookingPage.jsx';
import ConfirmationPage from '../pages/booking/ConfirmationPage.jsx';
import DashboardLayout from '../pages/dashboard/DashboardLayout.jsx';
import BookingHistory from '../pages/dashboard/BookingHistory.jsx';
import Favorites from '../pages/dashboard/Favorites.jsx';

export default function AppRouter() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<HomePage />} />
        <Route path="/search" element={<SearchResultsPage />} />
        <Route path="/hostel/:id" element={<HostelDetailPage />} />

        {/* Auth */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />

        {/* Protected */}
        <Route element={<ProtectedRoute />}>
          <Route path="/booking/:hostelId" element={<BookingPage />} />
          <Route path="/booking/confirmation/:bookingId" element={<ConfirmationPage />} />
          <Route path="/dashboard" element={<DashboardLayout />}>
            <Route index element={<BookingHistory />} />
            <Route path="favorites" element={<Favorites />} />
          </Route>
        </Route>
      </Route>
    </Routes>
  );
}
