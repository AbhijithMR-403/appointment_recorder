function AboutPage() {
  return (
    <div className="flex-1 px-4 sm:px-6 py-6 sm:py-8 pb-[max(1.5rem,env(safe-area-inset-bottom))]">
      <div className="w-full max-w-2xl mx-auto">
        <h1 className="text-2xl sm:text-3xl font-bold text-slate-900 mb-4">About</h1>
        <p className="text-slate-600 text-base sm:text-lg leading-relaxed">
          Appointment Recorder helps you capture and summarize appointment recordings and link them to your contacts.
        </p>
      </div>
    </div>
  )
}

export default AboutPage
