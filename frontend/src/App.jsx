import './App.css'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import AssistantPage from '../pages/assistantPage'

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
