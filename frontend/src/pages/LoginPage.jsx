import { useState } from 'react'
import { useNavigate, useLocation, Link } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'
import { loginWithPassword, requestOtp, verifyOtp } from '../api/auth'

export default function LoginPage() {
  const navigate = useNavigate()
  const location = useLocation()
  const { login } = useAuth()

  const [tab, setTab] = useState('password')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [info, setInfo] = useState(location.state?.message || '')

  // Password tab fields
  const [identifier, setIdentifier] = useState('')
  const [password, setPassword] = useState('')

  // OTP tab fields
  const [phone, setPhone] = useState('')
  const [code, setCode] = useState('')
  const [devCode, setDevCode] = useState('')
  const [otpSent, setOtpSent] = useState(false)

  const handlePasswordSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setInfo('')
    setLoading(true)
    try {
      const data = await loginWithPassword(identifier, password)
      login(data.user, data.token)
      navigate('/dashboard')
    } catch (err) {
      setError(err.response?.data?.error || 'Login failed.')
    } finally {
      setLoading(false)
    }
  }

  const handleSendOtp = async (e) => {
    e.preventDefault()
    setError('')
    setInfo('')
    setLoading(true)
    try {
      const data = await requestOtp(phone)
      setDevCode(data.code_dev_only || '')
      setOtpSent(true)
      setInfo(
        data.code_dev_only
          ? `Development OTP: ${data.code_dev_only}`
          : data.message || 'OTP sent successfully'
      )
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to send OTP.')
    } finally {
      setLoading(false)
    }
  }

  const handleVerifyOtp = async (e) => {
    e.preventDefault()
    setError('')
    setInfo('')
    setLoading(true)
    try {
      const data = await verifyOtp(phone, code)
      login(data.user, data.token)
      navigate('/dashboard')
    } catch (err) {
      setError(err.response?.data?.error || 'OTP verification failed.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="mx-auto max-w-md px-4 py-10">
      <h1 className="mb-6 text-center text-2xl font-bold">Login</h1>

      <div className="mb-4 flex justify-center gap-3">
        <button
          onClick={() => setTab('password')}
          className={`rounded px-4 py-1 text-sm ${
            tab === 'password' ? 'bg-blue-600 text-white' : 'bg-gray-200'
          }`}
        >
          Password
        </button>
        <button
          onClick={() => setTab('otp')}
          className={`rounded px-4 py-1 text-sm ${
            tab === 'otp' ? 'bg-blue-600 text-white' : 'bg-gray-200'
          }`}
        >
          OTP
        </button>
      </div>

      {info && <p className="mb-4 rounded bg-green-50 p-3 text-sm text-green-700">{info}</p>}
      {error && <p className="mb-4 rounded bg-red-50 p-3 text-sm text-red-700">{error}</p>}

      {tab === 'password' ? (
        <form onSubmit={handlePasswordSubmit} className="space-y-4 rounded border bg-white p-6 shadow">
          <input
            type="text"
            value={identifier}
            onChange={(e) => setIdentifier(e.target.value)}
            placeholder="Email or phone"
            required
            className="w-full rounded border px-3 py-2 text-sm"
          />
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Password"
            required
            className="w-full rounded border px-3 py-2 text-sm"
          />
          <button
            type="submit"
            disabled={loading}
            className="w-full rounded bg-blue-600 py-2 text-white hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? 'Loading...' : 'Login'}
          </button>
        </form>
      ) : (
        <div className="space-y-4 rounded border bg-white p-6 shadow">
          {!otpSent ? (
            <form onSubmit={handleSendOtp} className="space-y-4">
              <input
                type="tel"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                placeholder="09XXXXXXXXX"
                pattern="09[0-9]{9}"
                required
                className="w-full rounded border px-3 py-2 text-sm"
              />
              <button
                type="submit"
                disabled={loading}
                className="w-full rounded bg-blue-600 py-2 text-white hover:bg-blue-700 disabled:opacity-50"
              >
                {loading ? 'Loading...' : 'Send code'}
              </button>
            </form>
          ) : (
            <form onSubmit={handleVerifyOtp} className="space-y-4">
              <p className="text-sm text-gray-600">Phone: {phone}</p>
              {devCode && (
                <p className="rounded bg-yellow-50 p-2 text-xs text-yellow-700">
                  Development mode only — OTP: {devCode}
                </p>
              )}
              <input
                type="text"
                value={code}
                onChange={(e) => setCode(e.target.value)}
                placeholder="6-digit code"
                required
                maxLength={6}
                className="w-full rounded border px-3 py-2 text-sm"
              />
              <button
                type="submit"
                disabled={loading}
                className="w-full rounded bg-blue-600 py-2 text-white hover:bg-blue-700 disabled:opacity-50"
              >
                {loading ? 'Loading...' : 'Verify'}
              </button>
              <button
                type="button"
                onClick={() => {
                  setOtpSent(false)
                  setCode('')
                  setDevCode('')
                  setError('')
                  setInfo('')
                }}
                className="w-full text-sm text-blue-600 hover:underline"
              >
                Change phone number
              </button>
            </form>
          )}
        </div>
      )}

      <p className="mt-4 text-center text-sm">
        Don&apos;t have an account?{' '}
        <Link to="/register" className="text-blue-600 hover:underline">
          Register
        </Link>
      </p>
    </div>
  )
}