import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import Layout from '../components/Layout'
import HomePage from '../pages/HomePage'
import AboutPage from '../pages/AboutPage'
import RecordingPage from '../pages/RecordingPage'
import RecordTesting from '../pages/RecordTesting'

const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />,
    children: [
      { index: true, element: <HomePage /> },
      { path: 'about', element: <AboutPage /> },
    ],
  },
  { path: '/recording', element: <RecordingPage /> },
  { path: '/record-testing', element: <RecordTesting /> },
])

function Routes() {
  return <RouterProvider router={router} />
}

export default Routes
