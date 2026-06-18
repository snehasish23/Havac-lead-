import { useState } from 'react'
import Header from './components/Header.jsx'
import Hero from './components/Hero.jsx'
import ProblemSolution from './components/ProblemSolution.jsx'
import Modules from './components/Modules.jsx'
import Pricing from './components/Pricing.jsx'
import CTABanner from './components/CTABanner.jsx'
import Footer from './components/Footer.jsx'
import ChatDemo from './components/ChatDemo.jsx'

function App() {
  const [chatOpen, setChatOpen] = useState(false)

  return (
    <div className="min-h-screen bg-white">
      <Header />
      <main>
        <Hero onOpenChat={() => setChatOpen(true)} />
        <ProblemSolution />
        <Modules />
        <Pricing />
        <CTABanner onOpenChat={() => setChatOpen(true)} />
      </main>
      <Footer />
      
      {/* Demo Chat Button */}
      <button
        onClick={() => setChatOpen(true)}
        className="fixed bottom-6 right-6 z-40 w-14 h-14 bg-hvac-accent-500 rounded-full shadow-xl hover:bg-hvac-accent-600 transition-all duration-200 flex items-center justify-center group"
        aria-label="Try the AI demo"
      >
        <svg className="w-7 h-7 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
        </svg>
        <span className="absolute -top-2 -right-2 w-5 h-5 bg-green-500 rounded-full border-2 border-white animate-ping" />
      </button>

      {/* Floating demo chat */}
      <ChatDemo isOpen={chatOpen} onClose={() => setChatOpen(false)} />
    </div>
  )
}

export default App