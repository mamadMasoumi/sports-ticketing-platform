import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

export default function Navbar() {
  const { user, isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  const isSupportOrAdmin = user?.role === "support" || user?.role === "admin";

  return (
    <nav className="w-full bg-gray-900 text-white shadow">
      <div className="mx-auto flex max-w-5xl items-center justify-between px-4 py-3">
        <Link to="/" className="text-lg font-semibold">
          Sports Tickets
        </Link>

        <div className="flex items-center gap-4">
          <Link to="/matches" className="text-sm hover:text-gray-300">
            Matches
          </Link>
          <Link to="/tickets" className="text-sm hover:text-gray-300">
            Search Tickets
          </Link>

          {isAuthenticated && user ? (
            <>
              <Link to="/bookings" className="text-sm hover:text-gray-300">
                My Bookings
              </Link>
              <Link to="/reports" className="text-sm hover:text-gray-300">
                My Reports
              </Link>

              {isSupportOrAdmin && (
                <>
                  <Link
                    to="/admin/reports"
                    className="text-sm hover:text-gray-300"
                  >
                    Admin: Reports
                  </Link>
                  <Link
                    to="/admin/reservations"
                    className="text-sm hover:text-gray-300"
                  >
                    Admin: Reservations
                  </Link>
                </>
              )}

              <Link to="/profile" className="text-sm hover:text-gray-300">
                {user.first_name} {user.last_name}
              </Link>
              <button
                onClick={handleLogout}
                className="rounded bg-red-600 px-3 py-1 text-sm hover:bg-red-700"
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="text-sm hover:text-gray-300">
                Login
              </Link>
              <Link to="/register" className="text-sm hover:text-gray-300">
                Register
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}
