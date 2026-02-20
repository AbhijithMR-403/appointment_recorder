function Header({ isRecording = true }) {
  return (
    <header className="w-full max-w-[560px] md:max-w-[640px] flex items-center justify-between">
      <div className="flex items-center gap-3">
        <div className="w-9 h-9 md:w-11 md:h-11 rounded-[10px] bg-blue-600 text-white flex items-center justify-center shrink-0">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
            <path d="M6 12h2v6H6v-6zm4-3h2v9h-2V9zm4-3h2v12h-2V6z" fill="currentColor"/>
            <path d="M14 6h-4v12h4V6z" fill="currentColor" opacity="0.7"/>
          </svg>
        </div>
        <span className="text-lg md:text-xl font-semibold text-slate-800 tracking-tight">
          MedRecord Bridge
        </span>
      </div>
      {isRecording && (
        <div
          className="inline-flex items-center gap-2 text-[0.65rem] sm:text-xs font-semibold text-red-600 uppercase tracking-wide bg-red-50 px-2.5 sm:px-3 py-1 rounded-full whitespace-nowrap"
          aria-live="polite"
        >
          <span className="w-1.5 h-1.5 rounded-full bg-red-600 animate-pulse" />
          RECORDING
        </div>
      )}
    </header>
  )
}

export default Header
