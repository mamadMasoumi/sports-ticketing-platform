import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { getMyBookings, cancelReservation } from "../api/matches";
import { payForReservation } from "../api/payments";

const STATUS_TABS = [
  { label: "All", value: "" },
  { label: "Reserved", value: "Reserved" },
  { label: "Paid", value: "Paid" },
  { label: "Canceled", value: "Canceled" },
  { label: "Expired", value: "Expired" },
];

export default function MyBookingsPage() {
  const location = useLocation();
  const [activeTab, setActiveTab] = useState("");
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [successMsg, setSuccessMsg] = useState(location.state?.message || "");
  const [actionLoadingId, setActionLoadingId] = useState(null);
  const [payMethodFor, setPayMethodFor] = useState(null);
  const [selectedMethod, setSelectedMethod] = useState("BankCard");

  const fetchBookings = () => {
    getMyBookings(activeTab)
      .then((res) => setBookings(res.data || []))
      .catch((err) =>
        setError(err.response?.data?.error || "Failed to load bookings."),
      )
      .finally(() => setLoading(false));
  };

  // Load bookings whenever the active tab changes.
  // No setState() is called synchronously inside the effect body.
  useEffect(() => {
    fetchBookings();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [activeTab]);

  const handleTabChange = (tab) => {
    setLoading(true);
    setError("");
    setActiveTab(tab);
  };

  const handleCancel = async (reservationId) => {
    setActionLoadingId(reservationId);
    setError("");
    try {
      await cancelReservation(reservationId);
      setSuccessMsg("Reservation cancelled successfully.");
      fetchBookings();
    } catch (err) {
      setError(err.response?.data?.error || "Cancellation failed.");
    } finally {
      setActionLoadingId(null);
    }
  };

  const handlePay = async (reservationId, method) => {
    setActionLoadingId(reservationId);
    setError("");
    try {
      await payForReservation(reservationId, method);
      setSuccessMsg("Payment successful.");
      setPayMethodFor(null);
      fetchBookings();
    } catch (err) {
      setError(err.response?.data?.error || "Payment failed.");
    } finally {
      setActionLoadingId(null);
    }
  };

  if (loading && bookings.length === 0) {
    return (
      <div className="p-8 text-center text-gray-500">Loading bookings...</div>
    );
  }

  return (
    <div className="mx-auto max-w-4xl px-4 py-8">
      <h1 className="mb-6 text-2xl font-bold">My Bookings</h1>

      {successMsg && (
        <p className="mb-4 rounded bg-green-50 p-3 text-sm text-green-700">
          {successMsg}
        </p>
      )}
      {error && (
        <p className="mb-4 rounded bg-red-50 p-3 text-sm text-red-700">
          {error}
        </p>
      )}

      <div className="mb-6 flex flex-wrap gap-2">
        {STATUS_TABS.map((tab) => (
          <button
            key={tab.value}
            onClick={() => handleTabChange(tab.value)}
            className={`rounded px-4 py-1 text-sm ${
              activeTab === tab.value ? "bg-blue-600 text-white" : "bg-gray-200"
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {bookings.length === 0 ? (
        <p className="text-gray-600">No bookings found.</p>
      ) : (
        <div className="space-y-4">
          {bookings.map((booking) => (
            <div
              key={booking.reservation_id}
              className="rounded border bg-white p-4 shadow-sm"
            >
              <div className="flex items-start justify-between">
                <div>
                  <p classname="front-semibold">
                    Ticket id: {booking.ticket_id}
                  </p>
                  <p classname="front-semibold">
                    Reservation id: {booking.reservation_id}
                  </p>
                  <p className="font-semibold">
                    {booking.home_team} vs {booking.away_team}
                  </p>
                  <p className="text-sm text-gray-600">
                    {booking.sport_name} · {booking.venue_name}
                  </p>
                  <p className="text-sm text-gray-600">
                    {new Date(booking.match_date).toLocaleString()}
                  </p>
                  <p className="text-sm text-gray-600">
                    Ticket: {booking.ticket_type} · Price:{" "}
                    {Number(booking.ticket_price).toLocaleString()} Toman
                  </p>
                  <p className="text-sm text-gray-600">
                    Reserved at:{" "}
                    {new Date(booking.reserve_time).toLocaleString()}
                  </p>
                </div>
                <span
                  className={`rounded px-2 py-1 text-xs font-medium ${
                    booking.status === "Paid"
                      ? "bg-green-100 text-green-700"
                      : booking.status === "Reserved"
                        ? "bg-yellow-100 text-yellow-700"
                        : "bg-gray-200 text-gray-700"
                  }`}
                >
                  {booking.status}
                </span>
              </div>

              {booking.payment_status && (
                <p className="mt-2 text-sm text-gray-500">
                  Payment: {booking.payment_status}
                  {booking.payment_amount &&
                    ` · ${Number(booking.payment_amount).toLocaleString()} Toman`}
                </p>
              )}

              <div className="mt-3 flex flex-wrap gap-2">
                {booking.status === "Reserved" && (
                  <>
                    {payMethodFor === booking.reservation_id ? (
                      <div className="flex items-center gap-2">
                        <select
                          value={selectedMethod}
                          onChange={(e) => setSelectedMethod(e.target.value)}
                          className="rounded border px-2 py-1 text-sm"
                        >
                          <option value="BankCard">BankCard</option>
                          <option value="Wallet">Wallet</option>
                          <option value="Crypto">Crypto</option>
                        </select>
                        <button
                          onClick={() =>
                            handlePay(booking.reservation_id, selectedMethod)
                          }
                          disabled={actionLoadingId === booking.reservation_id}
                          className="rounded bg-green-600 px-3 py-1 text-sm text-white hover:bg-green-700 disabled:opacity-50"
                        >
                          {actionLoadingId === booking.reservation_id
                            ? "Processing..."
                            : "Confirm Pay"}
                        </button>
                        <button
                          onClick={() => setPayMethodFor(null)}
                          className="text-sm text-gray-600 hover:underline"
                        >
                          Cancel
                        </button>
                      </div>
                    ) : (
                      <button
                        onClick={() => setPayMethodFor(booking.reservation_id)}
                        disabled={actionLoadingId === booking.reservation_id}
                        className="rounded bg-green-600 px-3 py-1 text-sm text-white hover:bg-green-700 disabled:opacity-50"
                      >
                        Pay
                      </button>
                    )}
                    <button
                      onClick={() => handleCancel(booking.reservation_id)}
                      disabled={actionLoadingId === booking.reservation_id}
                      className="rounded bg-red-600 px-3 py-1 text-sm text-white hover:bg-red-700 disabled:opacity-50"
                    >
                      Cancel
                    </button>
                  </>
                )}
                {booking.status === "Paid" && (
                  <button
                    onClick={() => handleCancel(booking.reservation_id)}
                    disabled={actionLoadingId === booking.reservation_id}
                    className="rounded bg-red-600 px-3 py-1 text-sm text-white hover:bg-red-700 disabled:opacity-50"
                  >
                    Cancel (refund per policy)
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
