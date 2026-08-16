    import { useState } from "react";
import { adminCancelReservation } from "../api/admin";

export default function AdminReservationsPage() {
  const [reservationId, setReservationId] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setResult(null);
    setLoading(true);

    try {
      const res = await adminCancelReservation(Number(reservationId));
      setResult(res.data);
    } catch (err) {
      setError(err.response?.data?.error || "Cancellation failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mx-auto max-w-lg px-4 py-8">
      <h1 className="mb-6 text-2xl font-bold">
        Admin: Force Cancel Reservation
      </h1>
      <p className="mb-4 text-sm text-gray-600">
        Use this to cancel reservations flagged via reports or suspected issues.
      </p>

      <form
        onSubmit={handleSubmit}
        className="space-y-4 rounded border bg-white p-6 shadow"
      >
        {error && <p className="text-sm text-red-600">{error}</p>}
        {result && (
          <div className="rounded bg-green-50 p-3 text-sm text-green-700">
            Reservation #{result.reservation_id} cancelled. Refund amount:{" "}
            {Number(result.refund_amount).toLocaleString()} Toman
          </div>
        )}

        <div>
          <label className="mb-1 block text-sm font-medium">
            Reservation ID
          </label>
          <input
            type="number"
            value={reservationId}
            onChange={(e) => setReservationId(e.target.value)}
            className="w-full rounded border px-3 py-2 text-sm"
            placeholder="Enter reservation ID"
            required
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full rounded bg-red-600 py-2 text-white hover:bg-red-700 disabled:opacity-50"
        >
          {loading ? "Cancelling..." : "Force Cancel"}
        </button>
      </form>
    </div>
  );
}
