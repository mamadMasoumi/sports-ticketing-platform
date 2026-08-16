import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { submitReport } from "../api/reports";

export default function SubmitReportPage() {
  const navigate = useNavigate();
  const [reportType, setReportType] = useState("reservation");
  const [reservationId, setReservationId] = useState("");
  const [ticketId, setTicketId] = useState("");
  const [category, setCategory] = useState("");
  const [description, setDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    const payload = {
      category,
      description,
    };

    if (reportType === "reservation") {
      if (!reservationId) {
        setError("Reservation ID is required.");
        setLoading(false);
        return;
      }
      payload.reservation_id = Number(reservationId);
    } else {
      if (!ticketId) {
        setError("Ticket ID is required.");
        setLoading(false);
        return;
      }
      payload.ticket_id = Number(ticketId);
    }

    try {
      await submitReport(payload);
      navigate("/reports", {
        state: { message: "Report submitted successfully." },
      });
    } catch (err) {
      setError(err.response?.data?.error || "Failed to submit report.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mx-auto max-w-lg px-4 py-8">
      <h1 className="mb-6 text-2xl font-bold">Submit a Report</h1>

      <form
        onSubmit={handleSubmit}
        className="space-y-4 rounded border bg-white p-6 shadow"
      >
        {error && <p className="text-sm text-red-600">{error}</p>}

        <div>
          <label className="mb-1 block text-sm font-medium">Report type</label>
          <div className="flex gap-4">
            <label className="flex items-center gap-2">
              <input
                type="radio"
                value="reservation"
                checked={reportType === "reservation"}
                onChange={() => setReportType("reservation")}
              />
              Reservation issue
            </label>
            <label className="flex items-center gap-2">
              <input
                type="radio"
                value="ticket"
                checked={reportType === "ticket"}
                onChange={() => setReportType("ticket")}
              />
              Ticket issue
            </label>
          </div>
        </div>

        {reportType === "reservation" ? (
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
            />
          </div>
        ) : (
          <div>
            <label className="mb-1 block text-sm font-medium">Ticket ID</label>
            <input
              type="number"
              value={ticketId}
              onChange={(e) => setTicketId(e.target.value)}
              className="w-full rounded border px-3 py-2 text-sm"
              placeholder="Enter ticket ID"
            />
          </div>
        )}

        <div>
          <label className="mb-1 block text-sm font-medium">Category</label>
          <input
            type="text"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="w-full rounded border px-3 py-2 text-sm"
            placeholder="e.g. Payment, Seat, Cancellation"
            required
          />
        </div>

        <div>
          <label className="mb-1 block text-sm font-medium">Description</label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full rounded border px-3 py-2 text-sm"
            rows="4"
            placeholder="Describe the issue..."
            required
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full rounded bg-blue-600 py-2 text-white hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? "Submitting..." : "Submit Report"}
        </button>
      </form>
    </div>
  );
}
