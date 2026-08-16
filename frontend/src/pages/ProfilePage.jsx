import { useEffect, useState } from 'react'
import { useAuth } from '../hooks/useAuth'
import { updateProfile } from '../api/auth'
import { getCities } from '../api/locations'

export default function ProfilePage() {
  const { user, updateUser } = useAuth()
  const [cities, setCities] = useState([])
  const [loadingCities, setLoadingCities] = useState(true)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  const [form, setForm] = useState({
    first_name: user?.first_name || '',
    last_name: user?.last_name || '',
    email: user?.email || '',
    phone: user?.phone || '',
    city_id: user?.city_id || '',
    birth_date: user?.birth_date || '',
    profile_image: user?.profile_image || '',
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
    setSuccess('')
    setLoading(true)

    // Build payload conditionally – only include fields with non‑empty values.
    // This avoids sending `null` for optional fields that the backend rejects.
    const payload = {}

    const first_name = form.first_name.trim()
    if (first_name) payload.first_name = first_name

    const last_name = form.last_name.trim()
    if (last_name) payload.last_name = last_name

    const email = form.email.trim()
    if (email) payload.email = email

    const phone = form.phone.trim()
    if (phone) payload.phone = phone

    if (form.city_id) payload.city_id = Number(form.city_id)

    if (form.birth_date) payload.birth_date = form.birth_date

    const profile_image = form.profile_image.trim()
    if (profile_image) payload.profile_image = profile_image

    try {
      const res = await updateProfile(payload)
      updateUser(res.data)
      setSuccess('Profile updated successfully.')
    } catch (err) {
      setError(err.response?.data?.error || 'Update failed.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="mx-auto max-w-md px-4 py-10">
      <h1 className="mb-6 text-center text-2xl font-bold">Profile</h1>

      <form onSubmit={handleSubmit} className="space-y-4 rounded border bg-white p-6 shadow">
        {error && <p className="text-sm text-red-600">{error}</p>}
        {success && <p className="text-sm text-green-600">{success}</p>}

        <input
          type="text"
          name="first_name"
          value={form.first_name}
          onChange={handleChange}
          placeholder="First name"
          className="w-full rounded border px-3 py-2 text-sm"
        />
        <input
          type="text"
          name="last_name"
          value={form.last_name}
          onChange={handleChange}
          placeholder="Last name"
          className="w-full rounded border px-3 py-2 text-sm"
        />
        <input
          type="email"
          name="email"
          value={form.email}
          onChange={handleChange}
          placeholder="Email"
          className="w-full rounded border px-3 py-2 text-sm"
        />
        <input
          type="tel"
          name="phone"
          value={form.phone}
          onChange={handleChange}
          placeholder="09XXXXXXXXX"
          pattern="09[0-9]{9}"
          className="w-full rounded border px-3 py-2 text-sm"
        />

        <select
          name="city_id"
          value={form.city_id}
          onChange={handleChange}
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

        <input
          type="text"
          name="profile_image"
          value={form.profile_image}
          onChange={handleChange}
          placeholder="Profile image URL"
          className="w-full rounded border px-3 py-2 text-sm"
        />

        <button
          type="submit"
          disabled={loading}
          className="w-full rounded bg-blue-600 py-2 text-white hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? 'Loading...' : 'Update Profile'}
        </button>
      </form>
    </div>
  )
}