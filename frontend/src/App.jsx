import './App.css'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import AssistantPage from './pages/assistantPage'
import axios from 'axios'

axios.defaults.baseURL = 'http://localhost:8000'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<AssistantPage />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
