import { Routes, Route } from 'react-router-dom'
import Layout from './components/layout/Layout'
import Home from './pages/Home'
import Dashboard from './pages/Dashboard'
import Editor from './pages/Editor'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout><Home /></Layout>} />
      <Route path="/dashboard" element={<Layout><Dashboard /></Layout>} />
      <Route path="/editor/:projectId" element={<Editor />} />
    </Routes>
  )
}

export default App
