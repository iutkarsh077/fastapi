import { Outlet } from "react-router-dom"
import Navbar from "./components/Navbar"

function App() {
  return (
    <div className="min-h-screen bg-gray-900">
      <Navbar />
      <main className="text-white max-w-full">
        <Outlet />
      </main>
    </div>
  )
}

export default App

