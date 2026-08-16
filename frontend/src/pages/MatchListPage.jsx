import { useEffect, useState } from "react";
import { getMatches } from "../api/matches";

export default function MatchListPage() {
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    getMatches()
      .then((res) => setMatches(res.data || []))
      .catch((err) =>
        setError(err.response?.data?.error || "Failed to load matches."),
      )
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="p-8 text-center text-gray-500">Loading matches...</div>
    );
  }

  return (
    <div className="mx-auto max-w-5xl px-4 py-8">
      <h1 className="mb-6 text-2xl font-bold">Upcoming Matches</h1>

      {error && <p className="mb-4 text-red-600">{error}</p>}

      {matches.length === 0 && !error && (
        <p className="text-gray-600">No matches found.</p>
      )}

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {matches.map((match) => (
          <div key={match.id} className="rounded border bg-white p-4 shadow-sm">
            <p className="font-semibold">
              {match.home_team} vs {match.away_team}
            </p>
            <p className="text-sm text-gray-600">
              {match.sport_name} · {match.venue_name}
            </p>
            <p className="mt-2 text-sm text-gray-800">
              {new Date(match.match_date).toLocaleString()}
            </p>
            <span
              className={`mt-3 inline-block rounded px-2 py-1 text-xs ${
                match.status === "Scheduled"
                  ? "bg-green-100 text-green-700"
                  : "bg-gray-200 text-gray-700"
              }`}
            >
              {match.status}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
