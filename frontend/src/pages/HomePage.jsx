import { Link, Navigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

export default function HomePage() {
  const { isAuthenticated } = useAuth();

  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  return (
    <div className="mx-auto max-w-4xl px-4 py-16 text-center">
      <h1 className="text-4xl font-bold">Sports Ticket Reservations</h1>
      <p className="mt-4 text-lg text-gray-600">
        Football, Basketball, Volleyball — book your seat in seconds.
      </p>
      <div className="mt-8 flex justify-center gap-4">
        <Link
          to="/matches"
          className="rounded bg-blue-600 px-6 py-3 text-white hover:bg-blue-700"
        >
          Browse Matches
        </Link>
        <Link
          to="/tickets"
          className="rounded border border-blue-600 px-6 py-3 text-blue-600 hover:bg-blue-50"
        >
          Search Tickets
        </Link>
      </div>
    </div>
  );
}
