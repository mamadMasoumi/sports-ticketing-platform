import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider } from "./context/AuthProvider";
import Navbar from "./components/Navbar";
import ProtectedRoute from "./routes/ProtectedRoute";
import SupportRoute from "./routes/SupportRoute";
import RegisterPage from "./pages/RegisterPage";
import LoginPage from "./pages/LoginPage";
import ProfilePage from "./pages/ProfilePage";
import DashboardPage from "./pages/DashboardPage";
import HomePage from "./pages/HomePage";
import MatchListPage from "./pages/MatchListPage";
import TicketSearchPage from "./pages/TicketSearchPage";
import TicketDetailPage from "./pages/TicketDetailPage";
import MyBookingsPage from "./pages/MyBookingsPage";
import MyReportsPage from "./pages/MyReportsPage";
import SubmitReportPage from "./pages/SubmitReportPage";
import AdminReportsPage from "./pages/AdminReportsPage";
import AdminReservationsPage from "./pages/AdminReservationsPage";

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <div className="min-h-screen bg-gray-100">
          <Navbar />
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route
              path="/dashboard"
              element={
                <ProtectedRoute>
                  <DashboardPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/profile"
              element={
                <ProtectedRoute>
                  <ProfilePage />
                </ProtectedRoute>
              }
            />
            <Route path="/matches" element={<MatchListPage />} />
            <Route path="/tickets" element={<TicketSearchPage />} />
            <Route path="/tickets/:ticketId" element={<TicketDetailPage />} />
            <Route
              path="/bookings"
              element={
                <ProtectedRoute>
                  <MyBookingsPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/reports"
              element={
                <ProtectedRoute>
                  <MyReportsPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/reports/new"
              element={
                <ProtectedRoute>
                  <SubmitReportPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/admin/reports"
              element={
                <SupportRoute>
                  <AdminReportsPage />
                </SupportRoute>
              }
            />
            <Route
              path="/admin/reservations"
              element={
                <SupportRoute>
                  <AdminReservationsPage />
                </SupportRoute>
              }
            />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </div>
      </AuthProvider>
    </BrowserRouter>
  );
}
