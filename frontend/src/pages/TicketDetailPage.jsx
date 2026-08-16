import { useEffect, useState } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { getTicketDetail } from "../api/tickets";
import { reserveTicket } from "../api/matches";
import { useAuth } from "../hooks/useAuth";

export default function TicketDetailPage() {
  const { ticketId } = useParams();
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();

  const [ticket, setTicket] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [actionLoading, setActionLoading] = useState(false);
  const [actionError, setActionError] = useState("");

  useEffect(() => {
    if (!ticketId) return;
    getTicketDetail(ticketId)
      .then((res) => setTicket(res.data))
      .catch((err) =>
        setError(err.response?.data?.error || "Ticket not found."),
      )
      .finally(() => setLoading(false));
  }, [ticketId]);

  const handleReserve = async () => {
    setActionError("");
    setActionLoading(true);
    try {
      const res = await reserveTicket(Number(ticketId));
      navigate("/bookings", {
        state: {
          message: `Reservation created (ID: ${res.reservation_id}). Complete payment to confirm.`,
        },
      });
    } catch (err) {
      setActionError(err.response?.data?.error || "Reservation failed.");
    } finally {
      setActionLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="p-8 text-center text-gray-500">Loading ticket...</div>
    );
  }

  if (error || !ticket) {
    return (
      <div className="p-8 text-center">
        <p className="text-red-600">{error || "Ticket not found."}</p>
        <Link to="/tickets" className="text-blue-600 hover:underline">
          Back to search
        </Link>
      </div>
    );
  }

  const details = ticket.details || {};

  return (
    <div className="mx-auto max-w-3xl px-4 py-8">
      <Link to="/tickets" className="text-blue-600 hover:underline">
        ← Back to search
      </Link>

      <div className="mt-4 rounded border bg-white p-6 shadow">
        <h1 className="text-2xl font-bold">
          {ticket.home_team} vs {ticket.away_team}
        </h1>
        <p className="text-gray-600">
          {ticket.sport_name} · {ticket.venue_name} · {ticket.venue_city}
        </p>
        <p className="text-gray-600">{ticket.venue_address}</p>
        <p className="mt-2 text-lg">
          {new Date(ticket.match_date).toLocaleString()}
        </p>
        <p className="mt-2 text-xl font-bold">
          {Number(ticket.price).toLocaleString()} Toman
        </p>
        <p className="text-sm text-gray-600">Type: {ticket.ticket_type}</p>
        <p className="text-sm text-gray-600">
          Remaining capacity: {ticket.remaining_capacity}
        </p>

        {Object.keys(details).length > 0 && (
          <div className="mt-4 border-t pt-4">
            <h2 className="font-semibold">Additional Details</h2>
            <dl className="mt-2 grid grid-cols-2 gap-2 text-sm">
              {Object.entries(details).map(([key, value]) => (
                <div key={key} className="flex justify-between">
                  <dt className="font-medium capitalize">
                    {key.replace(/_/g, " ")}
                  </dt>
                  <dd>
                    {typeof value === "boolean"
                      ? value
                        ? "Yes"
                        : "No"
                      : value}
                  </dd>
                </div>
              ))}
            </dl>
          </div>
        )}

        {actionError && <p className="mt-4 text-red-600">{actionError}</p>}

        <div className="mt-6">
          {isAuthenticated ? (
            ticket.remaining_capacity > 0 ? (
              <button
                onClick={handleReserve}
                disabled={actionLoading}
                className="rounded bg-blue-600 px-6 py-2 text-white hover:bg-blue-700 disabled:opacity-50"
              >
                {actionLoading ? "Reserving..." : "Reserve this ticket"}
              </button>
            ) : (
              <p className="text-red-600">Sold out</p>
            )
          ) : (
            <Link
              to="/login"
              className="rounded bg-blue-600 px-6 py-2 text-white hover:bg-blue-700"
            >
              Log in to reserve
            </Link>
          )}
        </div>
      </div>
    </div>
  );
}
