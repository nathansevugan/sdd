import './App.css'
import { QueryProvider } from './hooks/queryClient.jsx'
import LandingPage from './pages/LandingPage'

function App() {
  return (
    <QueryProvider>
      <LandingPage />
    </QueryProvider>
  )
}

export default App
