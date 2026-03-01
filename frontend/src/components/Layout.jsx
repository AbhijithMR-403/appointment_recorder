import { Outlet, Link } from 'react-router-dom'

function Layout() {
  return (
    <div>
      <header>
        <nav>
          <Link to="/">Home</Link>
          {' | '}
          <Link to="/about">About</Link>
        </nav>
      </header>
      <main>
        <Outlet />
      </main>
    </div>
  )
}

export default Layout
