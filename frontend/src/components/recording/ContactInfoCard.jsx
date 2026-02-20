function ContactInfoCard({ contactName = 'John Smith', appointmentType = 'Follow-up Consultation', sessionDuration = '00:14:32' }) {
  const initials = contactName
    .split(' ')
    .map((n) => n[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)

  return (
    <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-3 sm:gap-4">
      <div className="flex items-center gap-3 sm:gap-4 min-w-0">
        <div
          className="w-11 h-11 md:w-13 md:h-13 rounded-full bg-blue-100 text-blue-700 text-sm md:text-base font-semibold flex items-center justify-center shrink-0"
          aria-hidden="true"
        >
          {initials}
        </div>
        <div className="min-w-0">
          <h2 className="m-0 mb-1 text-lg md:text-xl font-bold text-slate-900 leading-tight truncate">
            {contactName}
          </h2>
          <p className="m-0 text-sm text-slate-500 flex items-center gap-1.5">
            <span className="inline-flex text-slate-400 shrink-0" aria-hidden="true">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                <line x1="16" y1="2" x2="16" y2="6"/>
                <line x1="8" y1="2" x2="8" y2="6"/>
                <line x1="3" y1="10" x2="21" y2="10"/>
              </svg>
            </span>
            <span className="text-green-500 font-semibold" aria-hidden="true">✓</span>
            {appointmentType}
          </p>
        </div>
      </div>
      <div className="flex sm:flex-col items-baseline sm:items-end gap-2 sm:gap-0 sm:text-right shrink-0">
        <span className="text-[0.7rem] font-semibold text-slate-400 uppercase tracking-wider sm:mb-1">
          SESSION DURATION
        </span>
        <p className="m-0 text-2xl md:text-3xl font-bold text-slate-900 tabular-nums tracking-wide" aria-live="polite">
          {sessionDuration}
        </p>
      </div>
    </div>
  )
}

export default ContactInfoCard
