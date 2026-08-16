import { useEffect, useState } from 'react'
import { getAllReports, reviewReport } from '../api/reports'

const STATUS_TABS = [
  { label: 'All', value: '' },
  { label: 'Pending', value: 'Pending' },
  { label: 'Reviewed', value: 'Reviewed' },
]

export default function AdminReportsPage() {
  const [activeTab, setActiveTab] = useState('')
  const [reports, setReports] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [successMsg, setSuccessMsg] = useState('')
  const [actionLoadingId, setActionLoadingId] = useState(null)

  const fetchReports = () => {
    getAllReports(activeTab)
      .then((res) => setReports(res.data || []))
      .catch((err) => setError(err.response?.data?.error || 'Failed to load reports.'))
      .finally(() => setLoading(false))
  }

  useEffect(() => {
    fetchReports()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [activeTab])

  const handleTabChange = (tab) => {
    setLoading(true)
    setError('')
    setSuccessMsg('')
    setActiveTab(tab)
  }

  const handleReview = async (reportId) => {
    setActionLoadingId(reportId)
    setError('')
    setSuccessMsg('')
    try {
      await reviewReport(reportId)
      setSuccessMsg('Report marked as reviewed.')
      fetchReports()
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to review report.')
    } finally {
      setActionLoadingId(null)
    }
  }

  if (loading && reports.length === 0) {
    return <div className="p-8 text-center text-gray-500">Loading reports...</div>
  }

  return (
    <div className="mx-auto max-w-4xl px-4 py-8">
      <h1 className="mb-6 text-2xl font-bold">Admin: Reports</h1>

      {successMsg && (
        <p className="mb-4 rounded bg-green-50 p-3 text-sm text-green-700">{successMsg}</p>
      )}
      {error && <p className="mb-4 rounded bg-red-50 p-3 text-sm text-red-700">{error}</p>}

      <div className="mb-6 flex flex-wrap gap-2">
        {STATUS_TABS.map((tab) => (
          <button
            key={tab.value}
            onClick={() => handleTabChange(tab.value)}
            className={`rounded px-4 py-1 text-sm ${
              activeTab === tab.value ? 'bg-blue-600 text-white' : 'bg-gray-200'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {reports.length === 0 ? (
        <p className="text-gray-600">No reports found.</p>
      ) : (
        <div className="space-y-4">
          {reports.map((report) => (
            <div key={report.id} className="rounded border bg-white p-4 shadow-sm">
              <div className="flex items-start justify-between">
                <div>
                  <p className="font-semibold">{report.category}</p>
                  <p className="text-sm text-gray-600">
                    {report.first_name} {report.last_name} ({report.email})
                  </p>
                  <p className="mt-1 text-sm text-gray-700">{report.description}</p>
                  <p className="mt-2 text-xs text-gray-500">
                    {new Date(report.created_at).toLocaleString()}
                  </p>
                  {(report.reservation_id || report.ticket_id) && (
                    <p className="mt-1 text-xs text-gray-500">
                      {report.reservation_id && `Reservation #${report.reservation_id}`}
                      {report.reservation_id && report.ticket_id && ' · '}
                      {report.ticket_id && `Ticket #${report.ticket_id}`}
                    </p>
                  )}
                </div>
                <div className="flex flex-col items-end gap-2">
                  <span
                    className={`rounded px-2 py-1 text-xs font-medium ${
                      report.status === 'Pending'
                        ? 'bg-yellow-100 text-yellow-700'
                        : 'bg-green-100 text-green-700'
                    }`}
                  >
                    {report.status}
                  </span>
                  {report.status === 'Pending' && (
                    <button
                      onClick={() => handleReview(report.id)}
                      disabled={actionLoadingId === report.id}
                      className="rounded bg-blue-600 px-3 py-1 text-xs text-white hover:bg-blue-700 disabled:opacity-50"
                    >
                      {actionLoadingId === report.id ? 'Working...' : 'Mark Reviewed'}
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}