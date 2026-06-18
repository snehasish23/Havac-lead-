export default function Hero({ onOpenChat }) {
  return (
    <section className="relative pt-24 lg:pt-28 pb-16 md:pb-24 overflow-hidden">
      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-hvac-blue-50 via-white to-hvac-accent-50 opacity-70" />
      
      {/* Decorative elements */}
      <div className="absolute top-20 right-0 w-96 h-96 bg-hvac-blue-100 rounded-full blur-3xl opacity-30" />
      <div className="absolute bottom-0 left-20 w-80 h-80 bg-hvac-accent-100 rounded-full blur-3xl opacity-30" />

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-12 md:pt-16">
        <div className="text-center max-w-4xl mx-auto">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 bg-hvac-blue-50 border border-hvac-blue-200 rounded-full px-4 py-1.5 mb-8">
            <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
            <span className="text-sm font-medium text-hvac-blue-700">Available 24/7 — Never miss another call</span>
          </div>

          <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-extrabold text-gray-900 leading-tight mb-6">
            The AI employee that{' '}
            <span className="gradient-text">never misses a call</span>
            , never forgets a customer, and{' '}
            <span className="gradient-text">never stops booking</span> appointments.
          </h1>

          <p className="text-lg md:text-xl text-gray-600 max-w-3xl mx-auto mb-10 leading-relaxed">
            An autonomous revenue layer for your HVAC business. Captures every lead, recovers missed calls, 
            reactivates past customers, and sells maintenance memberships — all without adding overhead.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-12">
            <button onClick={onOpenChat} className="btn-primary text-lg px-8 py-4 w-full sm:w-auto">
              <svg className="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
              Talk to the AI — Try It Free
            </button>
            <a href="#pricing" className="btn-secondary text-lg px-8 py-4 w-full sm:w-auto">
              See Plans & Pricing
            </a>
          </div>

          {/* Social proof */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-6 sm:gap-10 text-sm text-gray-500">
            <div className="flex items-center gap-2">
              <span className="flex -space-x-2">
                {[1,2,3,4].map(i => (
                  <div key={i} className="w-8 h-8 rounded-full bg-hvac-blue-100 border-2 border-white flex items-center justify-center text-xs font-semibold text-hvac-blue-600">
                    {String.fromCharCode(64 + i)}
                  </div>
                ))}
              </span>
              <span className="font-medium">Trusted by 200+ HVAC companies</span>
            </div>
            <div className="flex items-center gap-1">
              {[1,2,3,4,5].map(i => (
                <svg key={i} className="w-5 h-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                </svg>
              ))}
              <span className="font-medium ml-1">4.9/5 from HVAC owners</span>
            </div>
          </div>
        </div>

        {/* Dashboard preview */}
        <div className="mt-16 relative">
          <div className="absolute inset-0 bg-gradient-to-t from-white via-transparent to-transparent z-10 pointer-events-none" />
          <div className="relative bg-white rounded-2xl shadow-2xl border border-gray-200 overflow-hidden">
            <div className="bg-gray-50 px-6 py-3 border-b border-gray-200 flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-red-400" />
              <div className="w-3 h-3 rounded-full bg-yellow-400" />
              <div className="w-3 h-3 rounded-full bg-green-400" />
              <span className="ml-3 text-sm text-gray-500 font-medium">HVAC AI Employee — Dashboard</span>
            </div>
            <div className="p-6 grid grid-cols-2 md:grid-cols-4 gap-4">
              {[
                { label: 'Leads Captured', value: '1,247', change: '+28%', color: 'text-green-600' },
                { label: 'Appointments Booked', value: '843', change: '+34%', color: 'text-green-600' },
                { label: 'Missed Calls Recovered', value: '412', change: '+156%', color: 'text-green-600' },
                { label: 'Revenue Generated', value: '$184K', change: '+42%', color: 'text-green-600' },
              ].map(stat => (
                <div key={stat.label} className="bg-gray-50 rounded-lg p-4">
                  <div className="text-sm text-gray-500 mb-1">{stat.label}</div>
                  <div className="text-2xl font-bold text-gray-900">{stat.value}</div>
                  <div className={`text-sm font-medium ${stat.color}`}>{stat.change} this month</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}