import { Link } from 'react-router-dom'
import { useAppSelector } from '../hooks/useAppSelector'
import { useAppDispatch } from '../hooks/useAppDispatch'
import { setLoading } from '../store/slices/appSlice'

function HomePage() {
  const loading = useAppSelector((state) => state.app.loading)
  const dispatch = useAppDispatch()

  return (
    <div>
      <nav>
        <Link to="/about">About</Link>
      </nav>
      <h1>Home</h1>
      <p>Loading: {loading ? 'Yes' : 'No'}</p>
      <button onClick={() => dispatch(setLoading(!loading))}>Toggle loading</button>
    </div>
  )
}

export default HomePage
