const problems = [
  {
    icon: (
      <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
      </svg>
    ),
    title: 'Missed Calls = Lost Revenue',
    description: 'HVAC businesses lose 30-50% of calls when they\'re out on jobs. Each missed call is a lost customer who calls your competitor instead.',
    stat: '$12K average monthly revenue lost to missed calls'
  },
  {
    icon: (
      <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
    ),
    title: 'Slow Response = Lower Conversion',
    description: 'Customers expect a response in minutes, not hours. Responding within 5 minutes increases conversion rates by 9x.',
    stat: '80% of customers choose the first company that responds'
  },
  {
    icon: (
      <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M16 4v12l-4-2-4 2V4M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
      </svg>
    ),
    title: 'Booking Abandonment',
    description: 'Over 60% of leads who start booking abandon the process. No follow-up means permanent loss of that revenue.',
    stat: '3 out of 5 booking attempts never complete'
  },
  {
    icon: (
      <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" />
      </svg>
    ),
    title: 'Customer Churn & Inactivity',
    description: '70% of past customers never come back without proactive outreach. Your database is a goldmine you\'re not mining.',
    stat: '85% of HVAC businesses don\'t reactivate past customers'
  }
]

export default function ProblemSolution() {
  return (
    <section className="py-16 md:py-24 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section header */}
        <div className="text-center mb-16">
          <h2 className="section-title">
            The problem isn't a lack of leads —<br />
            it's <span className="gradient-text">what happens after</span> they reach out
          </h2>
          <p className="section-subtitle">
            Every missed call, slow response, and abandoned booking is revenue your business earned but never collected.
          </p>
        </div>

        {/* Problem cards */}
        <div className="grid md:grid-cols-2 gap-6 mb-20">
          {problems.map((problem, i) => (
            <div key={i} className="group relative bg-white border border-gray-200 rounded-2xl p-6 hover:shadow-xl hover:border-hvac-blue-200 transition-all duration-300">
              <div className="flex items-start gap-4">
                <div className="flex-shrink-0 w-14 h-14 bg-red-50 rounded-xl flex items-center justify-center text-red-500 group-hover:scale-110 transition-transform">
                  {problem.icon}
                </div>
                <div>
                  <h3 className="text-lg font-bold text-gray-900 mb-2">{problem.title}</h3>
                  <p className="text-gray-600 mb-3">{problem.description}</p>
                  <div className="inline-flex items-center gap-1.5 bg-red-50 text-red-700 text-sm font-medium px-3 py-1 rounded-full">
                    <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" /></svg>
                    {problem.stat}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Solution callout */}
        <div className="bg-gradient-to-r from-hvac-blue-500 to-hvac-blue-700 rounded-3xl p-8 md:p-12 text-white text-center">
          <div className="max-w-3xl mx-auto">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-white/20 rounded-full mb-6">
              <svg className="w-8 h-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <h3 className="text-2xl md:text-3xl font-bold mb-4">
              Introducing HVAC AI Employee
            </h3>
            <p className="text-lg text-blue-100 mb-6 leading-relaxed">
              One AI that does the work of an entire office team. It answers every call instantly, recovers missed calls 
              within 60 seconds, nurtures undecided prospects, reactivates past customers, and sells maintenance 
              memberships automatically — all while you focus on the job site.
            </p>
            <div className="flex flex-wrap items-center justify-center gap-4">
              {['Responds in under 5 seconds', '24/7/365 coverage', 'Books appointments automatically', 'Recovers missed calls'].map(feature => (
                <span key={feature} className="inline-flex items-center gap-1.5 bg-white/10 backdrop-blur-sm rounded-full px-4 py-1.5 text-sm">
                  <svg className="w-4 h-4 text-green-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  {feature}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}