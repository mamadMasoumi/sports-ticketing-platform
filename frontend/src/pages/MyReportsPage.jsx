import { useEffect, useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { getMyReports } from '../api/reports'

export default function MyReportsPage() {
  const location = useLocation()
  const [reports, setReports] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [successMsg] = useState(location.state?.message || '')

  useEffect(() => {
    getMyReports()
      .then((res) => setReports(res.data || []))
      .catch((err) => setError(err.response?.data?.error || 'Failed to load reports.'))
      .finally(() => setLoading(false))
  }, [])

  if (loading) {
    return <div className="p-8 text-center text-gray-500">Loading reports...</div>
  }

  return (
    <div className="mx-auto max-w-3xl px-4 py-8">
      <div className="mb-6 flex items-center justify-between">
        <h1 className="text-2xl font-bold">My Reports</h1>
        <Link
          to="/reports/new"
          className="rounded bg-blue-600 px-4 py-2 text-sm text-white hover:bg-blue-700"
        >
          New Report
        </Link>
      </div>

      {successMsg && (
        <p className="mb-4 rounded bg-green-50 p-3 text-sm text-green-700">{successMsg}</p>
      )}
      {error && <p className="mb-4 rounded bg-red-50 p-3 text-sm text-red-700">{error}</p>}

      {reports.length === 0 ? (
        <p className="text-gray-600">No reports found.</p>
      ) : (
        <div className="space-y-4">
          {reports.map((report) => (
            <div key={report.id} className="rounded border bg-white p-4 shadow-sm">
              <div className="flex items-start justify-between">
                <div>
                  <p className="font-semibold">{report.category}</p>
                  <p className="mt-1 text-sm text-gray-600">{report.description}</p>
                  <p className="mt-2 text-xs text-gray-500">
                    {new Date(report.created_at).toLocaleString()}
                  </p>
                </div>
                <span
                  className={`rounded px-2 py-1 text-xs font-medium ${
                    report.status === 'Pending'
                      ? 'bg-yellow-100 text-yellow-700'
                      : 'bg-green-100 text-green-700'
                  }`}
                >
                  {report.status}
                </span>
              </div>
              {(report.reservation_id || report.ticket_id) && (
                <p className="mt-2 text-xs text-gray-500">
                  {report.reservation_id && `Reservation #${report.reservation_id}`}
                  {report.reservation_id && report.ticket_id && ' · '}
                  {report.ticket_id && `Ticket #${report.ticket_id}`}
                </p>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}