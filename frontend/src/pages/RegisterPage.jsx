import { useEffect, useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { register } from '../api/auth'
import { getCities } from '../api/locations'

export default function RegisterPage() {
  const navigate = useNavigate()
  const [cities, setCities] = useState([])
  const [loadingCities, setLoadingCities] = useState(true)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const [form, setForm] = useState({
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    password: '',
    city_id: '',
    birth_date: '',
  })

  useEffect(() => {
    getCities()
      .then((res) => setCities(res.data || []))
      .catch(() => setCities([]))
      .finally(() => setLoadingCities(false))
  }, [])

  const handleChange = (e) => {
    const { name, value } = e.target
    setForm((prev) => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    const payload = {
      first_name: form.first_name,
      last_name: form.last_name,
      email: form.email,
      phone: form.phone,
      password: form.password,
      city_id: Number(form.city_id),
      birth_date: form.birth_date || null,
    }

    try {
      await register(payload)
      navigate('/login', { state: { message: 'Registration successful. Please log in.' } })
    } catch (err) {
      setError(err.response?.data?.error || 'Registration failed.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="mx-auto max-w-md px-4 py-10">
      <h1 className="mb-6 text-center text-2xl font-bold">Create Account</h1>

      <form onSubmit={handleSubmit} className="space-y-4 rounded border bg-white p-6 shadow">
        {error && <p className="text-sm text-red-600">{error}</p>}

        <input
          type="text"
          name="first_name"
          value={form.first_name}
          onChange={handleChange}
          placeholder="First name"
          required
          className="w-full rounded border px-3 py-2 text-sm"
        />
        <input
          type="text"
          name="last_name"
          value={form.last_name}
          onChange={handleChange}
          placeholder="Last name"
          required
          className="w-full rounded border px-3 py-2 text-sm"
        />
        <input
          type="email"
          name="email"
          value={form.email}
          onChange={handleChange}
          placeholder="Email"
          required
          className="w-full rounded border px-3 py-2 text-sm"
        />
        <input
          type="tel"
          name="phone"
          value={form.phone}
          onChange={handleChange}
          placeholder="09XXXXXXXXX"
          pattern="09[0-9]{9}"
          title="Phone must start with 09 and have 11 digits"
          required
          className="w-full rounded border px-3 py-2 text-sm"
        />
        <input
          type="password"
          name="password"
          value={form.password}
          onChange={handleChange}
          placeholder="Password (min 8 chars)"
          minLength={8}
          required
          className="w-full rounded border px-3 py-2 text-sm"
        />

        <select
          name="city_id"
          value={form.city_id}
          onChange={handleChange}
          required
          className="w-full rounded border px-3 py-2 text-sm"
        >
          <option value="">Select city</option>
          {loadingCities ? (
            <option disabled>Loading cities...</option>
          ) : (
            cities.map((city) => (
              <option key={city.id} value={city.id}>
                {city.province} - {city.city_name}
              </option>
            ))
          )}
        </select>

        <input
          type="date"
          name="birth_date"
          value={form.birth_date}
          onChange={handleChange}
          className="w-full rounded border px-3 py-2 text-sm"
        />

        <button
          type="submit"
          disabled={loading}
          className="w-full rounded bg-blue-600 py-2 text-white hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? 'Loading...' : 'Register'}
        </button>

        <p className="text-center text-sm">
          Already have an account?{' '}
          <Link to="/login" className="text-blue-600 hover:underline">
            Login
          </Link>
        </p>
      </form>
    </div>
  )
}