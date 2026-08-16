import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { searchTickets } from '../api/tickets'
import { getCities, getVenues } from '../api/locations'

const SPORTS = [
  { id: 1, name: 'Football' },
  { id: 2, name: 'Basketball' },
  { id: 3, name: 'Volleyball' },
]

export default function TicketSearchPage() {
  const [cities, setCities] = useState([])
  const [venues, setVenues] = useState([])
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [hasSearched, setHasSearched] = useState(false)

  const [filters, setFilters] = useState({
    sport_id: '',
    city_id: '',
    venue_id: '',
    date_from: '',
    date_to: '',
    min_price: '',
    max_price: '',
  })

  // Load cities once on mount
  useEffect(() => {
    getCities()
      .then((res) => setCities(res.data || []))
      .catch(() => setCities([]))
  }, [])

  // Fetch venues whenever the selected city changes.
  // No synchronous setState in the effect body — only async data fetching.
  useEffect(() => {
    if (filters.city_id) {
      getVenues(filters.city_id)
        .then((res) => setVenues(res.data || []))
        .catch(() => setVenues([]))
    }
  }, [filters.city_id])

  const handleChange = (e) => {
    const { name, value } = e.target

    // Handle city change specially to reset the dependent venue field
    if (name === 'city_id') {
      // Clear venues immediately (user event, not effect) to avoid stale options
      setVenues([])
      // Also reset venue_id to '' whenever the city changes
      setFilters((prev) => ({
        ...prev,
        city_id: value,
        venue_id: '',
      }))
      return
    }

    setFilters((prev) => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    setHasSearched(true)

    try {
      const res = await searchTickets(filters)
      setResults(res.data || [])
    } catch (err) {
      setError(err.response?.data?.error || 'Search failed.')
      setResults([])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="mx-auto max-w-5xl px-4 py-8">
      <h1 className="mb-6 text-2xl font-bold">Search Tickets</h1>

      <form onSubmit={handleSubmit} className="mb-8 rounded border bg-white p-6 shadow">
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          <div>
            <label className="mb-1 block text-sm font-medium">Sport</label>
            <select
              name="sport_id"
              value={filters.sport_id}
              onChange={handleChange}
              className="w-full rounded border px-3 py-2 text-sm"
            >
              <option value="">All sports</option>
              {SPORTS.map((sport) => (
                <option key={sport.id} value={sport.id}>
                  {sport.name}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="mb-1 block text-sm font-medium">City</label>
            <select
              name="city_id"
              value={filters.city_id}
              onChange={handleChange}
              className="w-full rounded border px-3 py-2 text-sm"
            >
              <option value="">All cities</option>
              {cities.map((city) => (
                <option key={city.id} value={city.id}>
                  {city.province} - {city.city_name}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="mb-1 block text-sm font-medium">Venue</label>
            <select
              name="venue_id"
              value={filters.venue_id}
              onChange={handleChange}
              disabled={!filters.city_id}
              className="w-full rounded border px-3 py-2 text-sm disabled:bg-gray-100"
            >
              <option value="">All venues</option>
              {venues.map((venue) => (
                <option key={venue.id} value={venue.id}>
                  {venue.venue_name}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="mb-1 block text-sm font-medium">Date from</label>
            <input
              type="datetime-local"
              name="date_from"
              value={filters.date_from}
              onChange={handleChange}
              className="w-full rounded border px-3 py-2 text-sm"
            />
          </div>

          <div>
            <label className="mb-1 block text-sm font-medium">Date to</label>
            <input
              type="datetime-local"
              name="date_to"
              value={filters.date_to}
              onChange={handleChange}
              className="w-full rounded border px-3 py-2 text-sm"
            />
          </div>

          <div className="grid grid-cols-2 gap-2">
            <div>
              <label className="mb-1 block text-sm font-medium">Min price</label>
              <input
                type="number"
                name="min_price"
                value={filters.min_price}
                onChange={handleChange}
                placeholder="0"
                className="w-full rounded border px-3 py-2 text-sm"
              />
            </div>
            <div>
              <label className="mb-1 block text-sm font-medium">Max price</label>
              <input
                type="number"
                name="max_price"
                value={filters.max_price}
                onChange={handleChange}
                placeholder="Any"
                className="w-full rounded border px-3 py-2 text-sm"
              />
            </div>
          </div>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="mt-4 rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? 'Searching...' : 'Search'}
        </button>
      </form>

      {error && <p className="mb-4 text-red-600">{error}</p>}

      {hasSearched && !loading && results.length === 0 && !error && (
        <p className="text-gray-600">No tickets found matching your filters.</p>
      )}

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {results.map((ticket) => (
          <Link
            to={`/tickets/${ticket.ticket_id}`}
            key={ticket.ticket_id}
            className="rounded border bg-white p-4 shadow-sm transition hover:shadow-md"
          >
            <p classname="front-semibold">
              ticket id: {ticket.ticket_id}
            </p>
            <p className="font-semibold">
              {ticket.home_team} vs {ticket.away_team}
            </p>
            <p className="text-sm text-gray-600">
              {ticket.sport_name} · {ticket.venue_name} · {ticket.venue_city}
            </p>
            <p className="mt-2 text-sm">
              {new Date(ticket.match_date).toLocaleString()}
            </p>
            <p className="mt-2 text-lg font-bold">
              {Number(ticket.price).toLocaleString()} Toman
            </p>
            <p className="text-sm text-gray-600">
              Type: {ticket.ticket_type} · Remaining: {ticket.remaining_capacity}
            </p>
          </Link>
        ))}
      </div>
    </div>
  )
}