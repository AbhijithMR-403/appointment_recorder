import { Outlet, Link, useLocation } from 'react-router-dom'

function Layout() {
  const location = useLocation()

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-slate-50">
      <main className="flex flex-col items-center justify-center w-full max-w-5xl px-4">
        <Outlet />
      </main>
    </div>
  )
}

export default Layout
