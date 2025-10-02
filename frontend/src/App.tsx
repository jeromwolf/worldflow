import { Routes, Route } from 'react-router-dom'
import Layout from './components/layout/Layout'
import Home from './pages/Home'

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Home />} />
        {/* TODO: Add more routes as pages are created */}
      </Routes>
    </Layout>
  )
}

export default App
