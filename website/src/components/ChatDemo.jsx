import { useState, useRef, useEffect } from 'react'

// Simulated AI responses for the demo
const aiResponses = {
  greeting: "Hi there! Welcome to HVAC AI Employee. I'm your virtual assistant. How can I help you with your HVAC needs today?",
  ac_repair: {
    question: "I'd be happy to help with your AC repair! First, could you tell me what's happening with your AC? Is it not cooling, making unusual noises, or something else?",
    followup: "Thanks for the details! And what city and zip code are you located in? I'll check if you're in our service area.",
    schedule: "Great, we serve your area! I have a technician available tomorrow morning at 9 AM or afternoon at 2 PM. Which works better for you?",
    confirm: "Excellent! I've booked you for tomorrow at 9 AM. You'll receive a confirmation text shortly. Is there anything else I can help with?",
  },
  furnace: {
    question: "I can help with your furnace issue! Can you describe what's going on? Is it not heating, turning on and off frequently, or making strange sounds?",
    followup: "Got it. And what area are you in? I'll check our availability there.",
    schedule: "Perfect, we cover your area! Our technician can come by Thursday between 10 AM and 2 PM. Does that work for you?",
    confirm: "Booked! Your appointment is set for Thursday at 10 AM. You'll get a reminder text. Need anything else?",
  },
  maintenance: {
    question: "Great idea! A maintenance membership keeps your system running efficiently year-round. Our plans start at just $19/month and include spring tune-up, fall inspection, priority service, and 15% off repairs. Would you like to sign up?",
    followup: "Wonderful! What's your name and email so I can get your membership set up?",
    confirm: "You're all set! Welcome to HVAC AI Employee's Maintenance Membership Program. Your first seasonal tune-up is scheduled for next month. Any other questions?",
  },
  reactivation: {
    question: "I see you haven't had service in a while! We'd love to help you get back on our regular maintenance schedule. Would you like me to check when your last visit was and schedule a tune-up?",
    followup: "Our records show it's been about 14 months since your last service. I'd recommend a full system check-up. How does this Friday look for you?",
    schedule: "Perfect, I've got you down for Friday at 11 AM. We'll send a reminder. Welcome back!",
  },
  pricing: {
    question: "Here's what we offer:\n\n🌟 Starter — $299/mo: Lead capture, instant response, basic qualification\n🚀 Growth — $599/mo: Everything in Starter + missed call recovery, booking recovery, CRM integrations\n🏆 Scale — $999/mo: Everything in Growth + customer reactivation, maintenance membership engine, white-labeling\n\nWhich tier sounds right for your business? I can walk you through the details!",
  },
  emergency: {
    response: "🚨 I'm detecting a potential emergency situation. For your safety, I'm immediately connecting you with our emergency dispatch team. Please stay safe and follow any safety protocols. A live team member will be with you shortly.",
  },
  fallback: "I understand. Could you tell me a bit more about what you need? I'm here to help with AC repair, furnace service, maintenance plans, or anything HVAC-related!"
}

const quickReplies = [
  { label: 'My AC stopped working', intent: 'ac_repair' },
  { label: 'Furnace issues', intent: 'furnace' },
  { label: 'Maintenance plans', intent: 'maintenance' },
  { label: 'I used you before', intent: 'reactivation' },
  { label: 'Pricing info', intent: 'pricing' },
  { label: 'Gas leak! 🚨', intent: 'emergency' },
]

export default function ChatDemo({ isOpen, onClose }) {
  const [messages, setMessages] = useState([
    { role: 'ai', text: aiResponses.greeting, timestamp: Date.now() },
  ])
  const [sessionId, setSessionId] = useState('')
  const [input, setInput] = useState('')

  const generateSessionId = () => {
    return 'sess_' + Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
  }

  useEffect(() => {
    setSessionId(generateSessionId())
  }, [])
  const [showQuickReplies, setShowQuickReplies] = useState(true)
  const [conversationState, setConversationState] = useState('greeting') // greeting, collecting_info, scheduling, confirmed
  const [isTyping, setIsTyping] = useState(false)
  const messagesEndRef = useRef(null)
  const inputRef = useRef(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  useEffect(() => {
    if (isOpen) {
      setTimeout(() => inputRef.current?.focus(), 300)
    }
  }, [isOpen])

  const addMessage = (role, text) => {
    setMessages(prev => [...prev, { role, text, timestamp: Date.now() }])
  }

  const simulateTyping = (text, delay = 800) => {
    setIsTyping(true)
    setShowQuickReplies(false)
    setTimeout(() => {
      addMessage('ai', text)
      setIsTyping(false)
      setTimeout(() => setShowQuickReplies(true), 500)
    }, delay)
  }

  const handleSend = (text) => {
    if (!text.trim() || isTyping) return
    addMessage('user', text)
    setInput('')
    setShowQuickReplies(false)
    handleAIResponse(text)
  }

  const handleQuickReply = (intent, label) => {
    addMessage('user', label)
    setShowQuickReplies(false)
    handleAIResponse(label)
  }

  const handleAIResponse = async (userText) => {
    setIsTyping(true)
    setShowQuickReplies(false)

    try {
      const isDev = window.location.port !== '3000' && window.location.hostname === 'localhost';
      const apiUrl = (isDev ? 'http://localhost:3000' : '') + '/api/chat';

      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          session_id: sessionId,
          message: userText
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      if (data.current_step) {
        setConversationState(data.current_step);
      }

      const responseText = data.response_message;
      const textLength = responseText.length;
      const typingDelay = Math.max(800, Math.min(2500, textLength * 12));

      setTimeout(() => {
        addMessage('ai', responseText);
        setIsTyping(false);
        setTimeout(() => setShowQuickReplies(true), 300);
      }, typingDelay);

    } catch (error) {
      console.error('Error fetching AI response:', error);
      setTimeout(() => {
        addMessage('ai', "I'm having a brief issue connecting with my server. Can you please try again?");
        setIsTyping(false);
        setTimeout(() => setShowQuickReplies(true), 300);
      }, 1000);
    }
  }

  const resetChat = () => {
    const newSessionId = 'sess_' + Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
    setSessionId(newSessionId)
    setMessages([{ role: 'ai', text: aiResponses.greeting, timestamp: Date.now() }])
    setConversationState('greeting')
    setShowQuickReplies(true)
    setIsTyping(false)
    setInput('')
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 z-50 flex items-end sm:items-end justify-end p-0 sm:p-6 pointer-events-none">
      {/* Backdrop */}
      <div className="absolute inset-0 bg-black/30 backdrop-blur-sm sm:bg-black/20 pointer-events-auto" onClick={onClose} />

      {/* Chat panel */}
      <div className="relative w-full sm:w-[420px] h-[100dvh] sm:h-[640px] bg-white sm:rounded-2xl shadow-2xl flex flex-col pointer-events-auto animate-fade-in-up sm:mb-4 border border-gray-200">
        {/* Header */}
        <div className="flex items-center justify-between px-4 py-3 bg-gradient-to-r from-hvac-blue-500 to-hvac-blue-700 text-white rounded-t-none sm:rounded-t-2xl">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 bg-white/20 rounded-full flex items-center justify-center">
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <div>
              <div className="font-semibold text-sm">HVAC AI Employee</div>
              <div className="flex items-center gap-1 text-xs text-blue-200">
                <span className="w-1.5 h-1.5 bg-green-400 rounded-full" />
                Online — Try me!
              </div>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <button onClick={resetChat} className="text-white/70 hover:text-white transition-colors p-1" title="Reset conversation" aria-label="Reset chat">
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
            </button>
            <button onClick={onClose} className="text-white/70 hover:text-white transition-colors p-1" aria-label="Close chat">
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto px-4 py-4 space-y-3 bg-gray-50">
          {messages.map((msg, i) => (
            <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'} animate-fade-in-up`}>
              <div
                className={`max-w-[85%] rounded-2xl px-4 py-2.5 text-sm leading-relaxed ${
                  msg.role === 'user'
                    ? 'bg-hvac-blue-500 text-white rounded-br-md'
                    : 'bg-white text-gray-800 shadow-sm border border-gray-100 rounded-bl-md'
                }`}
              >
                {msg.role === 'ai' ? (
                  <div className="whitespace-pre-line">{msg.text}</div>
                ) : (
                  msg.text
                )}
              </div>
            </div>
          ))}

          {/* Typing indicator */}
          {isTyping && (
            <div className="flex justify-start animate-fade-in-up">
              <div className="bg-white rounded-2xl rounded-bl-md px-4 py-3 border border-gray-100 shadow-sm">
                <div className="flex gap-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full typing-dot" />
                  <div className="w-2 h-2 bg-gray-400 rounded-full typing-dot" />
                  <div className="w-2 h-2 bg-gray-400 rounded-full typing-dot" />
                </div>
              </div>
            </div>
          )}

          {/* Quick replies */}
          {showQuickReplies && !isTyping && (
            <div className="flex flex-wrap gap-2 pt-2">
              {quickReplies.map((qr, i) => (
                <button
                  key={i}
                  onClick={() => handleQuickReply(qr.intent, qr.label)}
                  className="bg-white border border-gray-200 rounded-full px-3 py-1.5 text-xs font-medium text-gray-700 hover:bg-hvac-accent-50 hover:border-hvac-accent-300 hover:text-hvac-accent-700 transition-all shadow-sm"
                >
                  {qr.label}
                </button>
              ))}
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <div className="border-t border-gray-200 p-3 bg-white rounded-b-none sm:rounded-b-2xl">
          <form
            onSubmit={(e) => { e.preventDefault(); handleSend(input) }}
            className="flex items-center gap-2"
          >
            <input
              ref={inputRef}
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message..."
              disabled={isTyping}
              className="flex-1 px-4 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:border-hvac-accent-400 focus:ring-2 focus:ring-hvac-accent-100 transition-all disabled:opacity-50"
            />
            <button
              type="submit"
              disabled={!input.trim() || isTyping}
              className="w-10 h-10 bg-hvac-accent-500 disabled:bg-gray-200 text-white rounded-xl flex items-center justify-center hover:bg-hvac-accent-600 transition-colors disabled:cursor-not-allowed"
              aria-label="Send message"
            >
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19V5m0 0l-7 7m7-7l7 7" />
              </svg>
            </button>
          </form>
          <p className="text-[10px] text-gray-400 text-center mt-2">
            This is an interactive demo. Your conversations are not stored.
          </p>
        </div>
      </div>
    </div>
  )
}