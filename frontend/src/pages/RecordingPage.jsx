import { useState, useCallback, useEffect } from 'react'
import { useLocation, useNavigate, useSearchParams } from 'react-router-dom'
import { useReactMediaRecorder } from 'react-media-recorder'
import { Header, ContactInfoCard, RecordingControls, MicrophoneInput, Footer } from '../components/recording'

const CONTACTS_API_BASE = 'http://localhost:8000/api/ghl_integration/contacts/'

const formatDuration = (seconds) => {
  const h = Math.floor(seconds / 3600)
  const m = Math.floor((seconds % 3600) / 60)
  const s = seconds % 60
  return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`
}

function RecordingPage() {
  const location = useLocation()
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const contactFromState = location.state?.contact
  const contactIdFromQuery = searchParams.get('contact_id')

  const hasAnyContactInfo = !!contactFromState || !!contactIdFromQuery

  const [fetchedContact, setFetchedContact] = useState(null)
  const [contactFetchStatus, setContactFetchStatus] = useState(null) // null | 'loading' | 'success' | 'invalid'
  const [elapsedSeconds, setElapsedSeconds] = useState(0)

  const needsFetch = !!contactIdFromQuery && !contactFromState
  const hasValidContact =
    !!contactFromState || (!!contactIdFromQuery && !!fetchedContact)
  const invalidContactId = needsFetch && contactFetchStatus === 'invalid'
  const contactStillLoading = needsFetch && contactFetchStatus === 'loading'

  // When only contact_id is in URL, fetch contact from API
  useEffect(() => {
    if (!contactIdFromQuery || contactFromState) return
    const url = `${CONTACTS_API_BASE}?contact_id=${encodeURIComponent(contactIdFromQuery)}`
    setContactFetchStatus('loading')
    fetch(url)
      .then((res) => {
        if (!res.ok) throw new Error('Failed to fetch contact')
        return res.json()
      })
      .then((data) => {
        const list = data?.contacts
        if (Array.isArray(list) && list.length > 0) {
          setFetchedContact(list[0])
          setContactFetchStatus('success')
        } else {
          setFetchedContact(null)
          setContactFetchStatus('invalid')
        }
      })
      .catch(() => setContactFetchStatus('invalid'))
  }, [contactIdFromQuery, contactFromState])

  const {
    status,
    startRecording,
    stopRecording,
    pauseRecording,
    resumeRecording,
    mediaBlobUrl,
    clearBlobUrl,
  } = useReactMediaRecorder({ audio: true })

  const isRecording = status === 'recording'
  const isPaused = status === 'paused'
  const isStopped = status === 'stopped'

  // Redirect back to contact selection if no contact information was provided
  useEffect(() => {
    if (!hasAnyContactInfo) {
      navigate('/', { replace: true })
    }
  }, [hasAnyContactInfo, navigate])

  // Start recording only when we have a resolved contact (from state or successful fetch)
  useEffect(() => {
    if (!hasValidContact) return
    startRecording()
  }, [hasValidContact, startRecording])

  useEffect(() => {
    if (!isRecording) return
    const id = setInterval(() => setElapsedSeconds((s) => s + 1), 1000)
    return () => clearInterval(id)
  }, [isRecording])

  const handlePause = useCallback(() => {
    if (isRecording) pauseRecording()
    else if (isPaused) resumeRecording()
  }, [isRecording, isPaused, pauseRecording, resumeRecording])

  const handleNext = useCallback(() => {
    stopRecording()
  }, [stopRecording])

  const handleProceedSummarize = useCallback(() => {
    // TODO: navigate or submit recording (e.g. upload blob, then go to summary)
  }, [])

  const handleCancel = useCallback(() => {
    if (!window.confirm('Discard this recording and start over?')) return
    stopRecording()
    clearBlobUrl()
    setElapsedSeconds(0)
    setTimeout(() => startRecording(), 0)
  }, [stopRecording, clearBlobUrl, startRecording])

  const handleBackToRecording = useCallback(() => {
    if (!window.confirm('Discard this recording and go back to record again?')) return
    clearBlobUrl()
    setElapsedSeconds(0)
    startRecording()
  }, [clearBlobUrl, startRecording])

  if (!hasAnyContactInfo) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50">
        <p className="text-sm text-slate-600">Redirecting to contact selection…</p>
      </div>
    )
  }

  if (invalidContactId) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center gap-4 bg-slate-50 px-4">
        <p className="text-lg font-semibold text-red-600">Invalid contact</p>
        <p className="text-sm text-slate-600 text-center max-w-md">
          No contact found for ID <strong className="font-mono text-slate-800">{contactIdFromQuery}</strong>. Please check the link or select a contact from the home page.
        </p>
        <button
          type="button"
          onClick={() => navigate('/', { replace: true })}
          className="px-4 py-2 rounded-lg bg-blue-600 text-white text-sm font-medium hover:bg-blue-700"
        >
          Back to contact selection
        </button>
      </div>
    )
  }

  if (contactStillLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50">
        <p className="text-sm text-slate-600">Loading contact…</p>
      </div>
    )
  }

  const displayContact = contactFromState || fetchedContact
  const resolvedContactId =
    (displayContact && (displayContact.contact_id || displayContact.id)) || contactIdFromQuery || 'N/A'
  const contactFullName = displayContact
    ? ([displayContact.first_name, displayContact.last_name].filter(Boolean).join(' ') || 'Unknown contact')
    : 'Unknown contact'
  const contactId = resolvedContactId

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-100 via-slate-50 to-slate-200 px-3 sm:px-4 md:px-8 pt-4 sm:pt-6 md:pt-8 pb-6 sm:pb-8 md:pb-10 flex flex-col items-center gap-4 sm:gap-5 md:gap-7">
      <Header isRecording={isRecording} />
      <div className="w-full max-w-[560px] md:max-w-[640px] bg-white rounded-xl sm:rounded-2xl shadow-[0_4px_24px_rgba(0,0,0,0.06),0_1px_3px_rgba(0,0,0,0.04)] px-4 sm:px-7 md:px-10 py-5 sm:py-8 md:py-9 flex flex-col gap-5 sm:gap-7 md:gap-8">
        <ContactInfoCard
          contactName={contactFullName}
          appointmentType={`Contact ID: ${contactId}`}
          sessionDuration={formatDuration(elapsedSeconds)}
        />
        {!isStopped ? (
          <>
            <RecordingControls
              isRecording={isRecording}
              isPaused={isPaused}
              onCancel={handleCancel}
              onPause={handlePause}
              onNext={handleNext}
            />
            <MicrophoneInput isActive={isRecording} />
          </>
        ) : (
          mediaBlobUrl && (
            <div className="pt-3 border-t border-slate-100 flex flex-col gap-4">
              <div className="flex flex-col gap-2">
                <span className="text-xs text-slate-400">Listen to your recording</span>
                <audio src={mediaBlobUrl} controls className="w-full" />
              </div>
              <div className="flex flex-col sm:flex-row justify-center gap-2 sm:gap-3">
                <button
                  type="button"
                  className="inline-flex items-center justify-center gap-2 px-4 md:px-5 py-2.5 rounded-[10px] text-sm font-semibold bg-slate-100 text-slate-600 border-none cursor-pointer transition-all duration-200 hover:bg-slate-200 hover:-translate-y-px"
                  onClick={handleBackToRecording}
                  aria-label="Back to recording"
                >
                  <span className="flex items-center justify-center" aria-hidden="true">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <polyline points="15 18 9 12 15 6"/>
                    </svg>
                  </span>
                  Back
                </button>
                <button
                  type="button"
                  className="inline-flex items-center justify-center gap-2 px-4 md:px-5 py-2.5 rounded-[10px] text-sm md:text-[0.9rem] font-semibold bg-blue-600 text-white border-none cursor-pointer transition-all duration-200 hover:bg-blue-700 hover:-translate-y-px"
                  onClick={handleProceedSummarize}
                  aria-label="Proceed and summarize"
                >
                  <span className="flex items-center justify-center" aria-hidden="true">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M12 3l1.5 4.5L18 9l-4.5 1.5L12 15l-1.5-4.5L6 9l4.5-1.5L12 3z"/>
                      <path d="M5 16l1.5 2L9 17.5 7.5 19.5 9 22"/>
                      <path d="M19 16l-1.5 2L15 17.5l1.5-2L15 14"/>
                    </svg>
                  </span>
                  Proceed &amp; Summarize
                </button>
              </div>
            </div>
          )
        )}
      </div>
      <Footer patientRecordId={contactId} version="v2.4.1" />
    </div>
  )
}

export default RecordingPage
