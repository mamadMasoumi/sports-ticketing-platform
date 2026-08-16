import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { getMyBookings } from "../api/matches";
import { getMyReports } from "../api/reports";

export default function DashboardPage() {
  const { user } = useAuth();

  const [bookings, setBookings] = useState(null);
  const [reports, setReports] = useState(null);
  const [loading, setLoading] = useState(true);
  const [bookingError, setBookingError] = useState("");
  const [reportError, setReportError] = useState("");

  useEffect(() => {
    let cancelled = false;

    const loadData = async () => {
      const [bookingsResult, reportsResult] = await Promise.allSettled([
        getMyBookings(),
        getMyReports(),
      ]);

      if (cancelled) return;

      if (bookingsResult.status === "fulfilled") {
        setBookings(bookingsResult.value.data || []);
      } else {
        setBookingError("Could not load bookings.");
      }

      if (reportsResult.status === "fulfilled") {
        setReports(reportsResult.value.data || []);
      } else {
        setReportError("Could not load reports.");
      }

      setLoading(false);
    };

    loadData();

    return () => {
      cancelled = true;
    };
  }, []);

  const bookingsList = bookings || [];
  const reportsList = reports || [];

  const countStatus = (status) =>
    bookingsList.filter((booking) => booking.status === status).length;

  const totalBookings = bookingsList.length;
  const pendingReports = reportsList.filter(
    (report) => report.status === "Pending",
  ).length;
  const totalReports = reportsList.length;

  const isSupportOrAdmin = user?.role === "support" || user?.role === "admin";

  return (
    <div className="mx-auto max-w-5xl px-4 py-8">
      <h1 className="mb-2 text-2xl font-bold">
        Welcome back, {user?.first_name || "there"}!
      </h1>
      <p className="mb-6 text-sm text-gray-600">
        Here&apos;s a quick overview of your account.
      </p>

      {loading ? (
        <p className="text-gray-500">Loading your dashboard...</p>
      ) : (
        <>
          {bookingError && (
            <p className="mb-4 rounded bg-red-50 p-3 text-sm text-red-700">
              {bookingError}
            </p>
          )}
          {reportError && (
            <p className="mb-4 rounded bg-red-50 p-3 text-sm text-red-700">
              {reportError}
            </p>
          )}

          {/* Booking stats */}
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
            <div className="rounded border bg-white p-4 shadow-sm">
              <p className="text-3xl font-bold">{totalBookings}</p>
              <p className="text-sm text-gray-600">Total Bookings</p>
            </div>
            <div className="rounded border bg-white p-4 shadow-sm">
              <p className="text-3xl font-bold">{countStatus("Reserved")}</p>
              <p className="text-sm text-gray-600">Reserved</p>
            </div>
            <div className="rounded border bg-white p-4 shadow-sm">
              <p className="text-3xl font-bold">{countStatus("Paid")}</p>
              <p className="text-sm text-gray-600">Paid</p>
            </div>
            <div className="rounded border bg-white p-4 shadow-sm">
              <p className="text-3xl font-bold">{countStatus("Canceled")}</p>
              <p className="text-sm text-gray-600">Canceled</p>
            </div>
            <div className="rounded border bg-white p-4 shadow-sm">
              <p className="text-3xl font-bold">{countStatus("Expired")}</p>
              <p className="text-sm text-gray-600">Expired</p>
            </div>
          </div>

          {/* Report stats */}
          <div className="mt-4 grid gap-4 sm:grid-cols-2">
            <div className="rounded border bg-white p-4 shadow-sm">
              <p className="text-3xl font-bold">{totalReports}</p>
              <p className="text-sm text-gray-600">Total Reports</p>
              <p className="mt-1 text-xs text-gray-500">
                {pendingReports} pending review
              </p>
            </div>
          </div>

          {/* Quick actions */}
          <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            <Link
              to="/tickets"
              className="rounded border bg-white p-4 shadow-sm transition hover:shadow-md"
            >
              <h2 className="font-semibold">Search Tickets</h2>
              <p className="mt-1 text-sm text-gray-600">
                Browse available tickets and reserve your seat.
              </p>
            </Link>
            <Link
              to="/bookings"
              className="rounded border bg-white p-4 shadow-sm transition hover:shadow-md"
            >
              <h2 className="font-semibold">My Bookings</h2>
              <p className="mt-1 text-sm text-gray-600">
                View and manage your reservations.
              </p>
            </Link>
            <Link
              to="/reports/new"
              className="rounded border bg-white p-4 shadow-sm transition hover:shadow-md"
            >
              <h2 className="font-semibold">Submit a Report</h2>
              <p className="mt-1 text-sm text-gray-600">
                Report an issue with a ticket or reservation.
              </p>
            </Link>
            {isSupportOrAdmin && (
              <Link
                to="/admin/reports"
                className="rounded border bg-white p-4 shadow-sm transition hover:shadow-md"
              >
                <h2 className="font-semibold">Admin: Reports</h2>
                <p className="mt-1 text-sm text-gray-600">
                  Review and manage user reports.
                </p>
              </Link>
            )}
          </div>
        </>
      )}
    </div>
  );
}
