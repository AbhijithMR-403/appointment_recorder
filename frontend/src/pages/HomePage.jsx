import { useEffect, useState } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'

const API_BASE_URL = 'http://localhost:8000/api/ghl_integration/contacts/'
const MIN_QUERY_LENGTH = 2

function HomePage() {
  const navigate = useNavigate()
  const [searchParams, setSearchParams] = useSearchParams()

  const [locationId, setLocationId] = useState(searchParams.get('location_id') || '')
  const [nameQuery, setNameQuery] = useState('')
  const [contacts, setContacts] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [showDropdown, setShowDropdown] = useState(false)

  // Keep URL query param in sync with locationId input
  useEffect(() => {
    const params = new URLSearchParams(searchParams.toString())
    if (locationId.trim()) {
      params.set('location_id', locationId.trim())
    } else {
      params.delete('location_id')
    }
    setSearchParams(params)
  }, [locationId, searchParams, setSearchParams])

  // Fetch contacts when name / locationId change
  useEffect(() => {
    const trimmedName = nameQuery.trim()

    if (trimmedName.length < MIN_QUERY_LENGTH) {
      setContacts([])
      setShowDropdown(false)
      setLoading(false)
      setError(null)
      return
    }

    setLoading(true)
    setError(null)
    setShowDropdown(true)

    const controller = new AbortController()
    const timeoutId = setTimeout(() => {
      const params = new URLSearchParams()
      params.set('name', trimmedName)
      if (locationId.trim()) {
        params.set('location_id', locationId.trim())
      }

      const url = `${API_BASE_URL}?${params.toString()}`

      fetch(url, { signal: controller.signal })
        .then(async (res) => {
          if (!res.ok) {
            const text = await res.text()
            throw new Error(text || 'Failed to fetch contacts')
          }
          return res.json()
        })
        .then((data) => {
          setContacts(Array.isArray(data.contacts) ? data.contacts : [])
          setLoading(false)
        })
        .catch((err) => {
          if (err.name === 'AbortError') return
          setError('Could not load contacts. Please try again.')
          setLoading(false)
        })
    }, 350)

    return () => {
      clearTimeout(timeoutId)
      controller.abort()
    }
  }, [nameQuery, locationId])

  const handleSelectContact = (contact) => {
    setShowDropdown(false)
    if (!contact) return
    const contactId = contact.contact_id || contact.id
    if (contactId) {
      navigate(`/recording?contact_id=${encodeURIComponent(contactId)}`, { state: { contact } })
    } else {
      navigate('/recording', { state: { contact } })
    }
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-start pt-10 px-4 bg-slate-50">
      <div className="w-full max-w-md bg-white rounded-xl shadow-md p-6 space-y-5">
        <h1 className="text-xl font-semibold text-slate-900">Select contact to start recording</h1>

        <div className="space-y-2">
          <label className="block text-sm font-medium text-slate-700" htmlFor="location-id-input">
            Location ID (optional)
          </label>
          <input
            id="location-id-input"
            type="text"
            value={locationId}
            onChange={(e) => setLocationId(e.target.value)}
            placeholder="Ylw5R20TuGK6NVbMXEkM"
            className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          />
          <p className="text-xs text-slate-400">
            If left empty, the search will not filter by location.
          </p>
        </div>

        <div className="space-y-2 relative">
          <label className="block text-sm font-medium text-slate-700" htmlFor="contact-name-input">
            Contact name
          </label>
          <input
            id="contact-name-input"
            type="text"
            value={nameQuery}
            onChange={(e) => setNameQuery(e.target.value)}
            placeholder="Type at least 2 characters"
            className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          />
          <p className="text-xs text-slate-400">
            Minimum {MIN_QUERY_LENGTH} characters. Results show contact ID and name.
          </p>

          {showDropdown && (
            <div className="absolute z-10 mt-1 w-full bg-white border border-slate-200 rounded-md shadow-lg max-h-64 overflow-y-auto">
              {loading && (
                <div className="px-3 py-2 text-sm text-slate-500">Loading contacts…</div>
              )}
              {!loading && error && (
                <div className="px-3 py-2 text-sm text-red-500">{error}</div>
              )}
              {!loading && !error && contacts.length === 0 && (
                <div className="px-3 py-2 text-sm text-slate-500">No contacts found.</div>
              )}
              {!loading &&
                !error &&
                contacts.map((c) => {
                  const fullName = [c.first_name, c.last_name].filter(Boolean).join(' ') || 'Unnamed contact'
                  return (
                    <button
                      key={c.id ?? c.contact_id}
                      type="button"
                      onClick={() => handleSelectContact(c)}
                      className="w-full text-left px-3 py-2 text-sm hover:bg-slate-100 focus:bg-slate-100 focus:outline-none"
                    >
                      <div className="font-medium text-slate-900">
                        {c.contact_id} &mdash; {fullName}
                      </div>
                      {c.phone && (
                        <div className="text-xs text-slate-500">
                          {c.phone}
                        </div>
                      )}
                    </button>
                  )
                })}
            </div>
          )}
        </div>

        <p className="text-xs text-slate-500">
          Select a contact from the list to continue. You cannot proceed to recording without a selected
          contact.
        </p>
      </div>
    </div>
  )
}

export default HomePage
