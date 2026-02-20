function Footer({ patientRecordId = '8291', version = 'v2.4.1' }) {
  return (
    <footer className="text-center w-full max-w-[560px] md:max-w-[640px] px-4">
      <p className="m-0 mb-1 text-sm text-slate-500">
        Recording is automatically saved to <strong className="text-slate-700">Patient Record #{patientRecordId}</strong>
      </p>
      <p className="m-0 text-xs text-slate-400">
        Secure HIPAA Compliant Recording Bridge &bull; {version}
      </p>
    </footer>
  )
}

export default Footer
