function RecordingControls({ onCancel, onPause, onNext, isRecording = true, isPaused = false }) {
  return (
    <div className="flex flex-col items-center gap-5 md:gap-7">
      {/* REC button */}
      <div className="flex justify-center">
        <button
          type="button"
          className={`
            w-[68px] h-[68px] sm:w-[80px] sm:h-[80px] md:w-[90px] md:h-[90px]
            rounded-full border-none flex flex-col items-center justify-center gap-1
            cursor-pointer transition-transform duration-200
            ${isRecording
              ? 'bg-red-100 text-red-600 animate-[rec-glow_1.5s_ease-in-out_infinite]'
              : 'bg-slate-100 text-slate-500 hover:scale-[1.02]'}
          `}
          aria-label={isRecording ? 'Stop recording' : 'Start recording'}
          aria-pressed={isRecording}
        >
          <span className="flex items-center justify-center" aria-hidden="true">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5 sm:w-7 sm:h-7 md:w-8 md:h-8" aria-hidden="true">
              <rect x="6" y="6" width="12" height="12" rx="2"/>
            </svg>
          </span>
          <span className="text-[0.7rem] font-bold uppercase tracking-wider">REC</span>
        </button>
      </div>

      {/* Action buttons */}
      <div className="flex flex-col sm:flex-row flex-wrap justify-center gap-2 sm:gap-3 md:gap-4 w-full sm:w-auto">
        <button
          type="button"
          className="inline-flex items-center justify-center gap-2 px-4 md:px-5 py-2.5 rounded-[10px] text-sm font-semibold bg-red-100 text-red-600 border-none cursor-pointer transition-all duration-200 hover:bg-red-200 hover:-translate-y-px"
          onClick={(e) => {
            e.preventDefault()
            e.stopPropagation()
            if (typeof onCancel === 'function') onCancel()
          }}
          aria-label="Cancel recording"
        >
          <span className="flex items-center justify-center" aria-hidden="true">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <polyline points="3 6 5 6 21 6"/>
              <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
              <line x1="10" y1="11" x2="10" y2="17"/>
              <line x1="14" y1="11" x2="14" y2="17"/>
            </svg>
          </span>
          Cancel
        </button>
        <button
          type="button"
          className="inline-flex items-center justify-center gap-2 px-4 md:px-5 py-2.5 rounded-[10px] text-sm font-semibold bg-slate-100 text-slate-600 border-none cursor-pointer transition-all duration-200 hover:bg-slate-200 hover:-translate-y-px disabled:opacity-60 disabled:cursor-not-allowed disabled:hover:translate-y-0 disabled:hover:bg-slate-100"
          onClick={(e) => {
            e.preventDefault()
            e.stopPropagation()
            if (typeof onPause === 'function') onPause()
          }}
          disabled={!isRecording && !isPaused}
          aria-label={isPaused ? 'Resume recording' : 'Pause recording'}
        >
          <span className="flex items-center justify-center" aria-hidden="true">
            {isPaused ? (
              <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                <polygon points="6,4 20,12 6,20" />
              </svg>
            ) : (
              <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                <rect x="6" y="4" width="4" height="16"/>
                <rect x="14" y="4" width="4" height="16"/>
              </svg>
            )}
          </span>
          {isPaused ? 'Play' : 'Pause'}
        </button>
        <button
          type="button"
          className="inline-flex items-center justify-center gap-2 px-4 md:px-5 py-2.5 rounded-[10px] text-sm md:text-[0.9rem] font-semibold bg-blue-600 text-white border-none cursor-pointer transition-all duration-200 hover:bg-blue-700 hover:-translate-y-px"
          onClick={(e) => {
            e.preventDefault()
            e.stopPropagation()
            if (typeof onNext === 'function') onNext()
          }}
          aria-label="Next"
        >
          <span className="flex items-center justify-center" aria-hidden="true">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <polyline points="9 18 15 12 9 6"/>
            </svg>
          </span>
          Next
        </button>
      </div>
    </div>
  )
}

export default RecordingControls
