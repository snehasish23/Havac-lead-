const modules = [
  {
    icon: (
      <svg className="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M13 10V3L4 14h7v7l9-11h-7z" />
      </svg>
    ),
    title: 'Lead Capture & Instant Response',
    description: 'Captures every inbound lead from any channel — website, Google Business Profile, phone, SMS, ads, and organic traffic.',
    highlights: ['Responds in under 5 seconds', 'Works across all channels', '24/7/365 — never a missed opportunity'],
    color: 'bg-blue-50 text-blue-600',
  },
  {
    icon: (
      <svg className="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
    ),
    title: 'Lead Qualification Engine',
    description: 'Classifies service needs (AC repair, furnace, heat pump), scores urgency, verifies service areas, and qualifies budget — automatically.',
    highlights: ['Urgency scoring (Hot/Warm/Cold)', 'Service area & zip verification', 'Lead scoring 0-100'],
    color: 'bg-green-50 text-green-600',
  },
  {
    icon: (
      <svg className="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M17 8h2a2 2 0 012 2v6a2 2 0 01-2 2h-2v4l-4-4H9a1.994 1.994 0 01-1.414-.586m0 0L11 14h4a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2v4l.586-.586z" />
      </svg>
    ),
    title: 'AI Conversation Agent',
    description: 'Human-like, HVAC-fluent conversations. Safety-aware — escalates emergencies (gas leaks, CO, sparks) immediately.',
    highlights: ['Natural HVAC-specific dialog', 'Emergency detection & escalation', 'Never claims to be a technician'],
    color: 'bg-purple-50 text-purple-600',
  },
  {
    icon: (
      <svg className="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
      </svg>
    ),
    title: 'Missed Call Recovery',
    description: 'Detects missed calls the instant they happen and auto-callbacks within 60 seconds — never leave revenue on the table.',
    highlights: ['Auto-callback in under 1 minute', 'Qualifies & books live', 'No more "we\'ll call you back"'],
    color: 'bg-orange-50 text-orange-600',
  },
  {
    icon: (
      <svg className="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
    ),
    title: 'Booking Abandonment Recovery',
    description: 'SMS reminders, alternate time suggestions, objection handling — resumes bookings from the last step so no deal goes cold.',
    highlights: ['Auto-follow-up SMS sequences', 'Objection handling & rebuttals', 'Resume-from-last-step booking'],
    color: 'bg-rose-50 text-rose-600',
  },
  {
    icon: (
      <svg className="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" />
      </svg>
    ),
    title: 'Customer Reactivation Engine',
    description: 'Detects 12+ month inactive customers, expired plans, 10+ year old systems — sends personalized re-engagement messages.',
    highlights: ['Identifies dormant customers', 'Auto-reactivation sequences', 'Missed tune-up reminders'],
    color: 'bg-teal-50 text-teal-600',
  },
  {
    icon: (
      <svg className="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
      </svg>
    ),
    title: 'Maintenance Membership Engine',
    description: 'Auto-offers annual plans after completed jobs, schedules seasonal tune-ups, sends pre-summer/winter reminders.',
    highlights: ['Auto-enroll after service', 'Seasonal tune-up scheduling', 'Filter & IAQ program promotion'],
    color: 'bg-cyan-50 text-cyan-600',
  },
  {
    icon: (
      <svg className="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 17V7m0 10a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2h2a2 2 0 012 2m0 10a2 2 0 002 2h2a2 2 0 002-2M9 7a2 2 0 012-2h2a2 2 0 012 2m0 10V7m0 10a2 2 0 002 2h2a2 2 0 002-2V7a2 2 0 00-2-2h-2a2 2 0 00-2 2" />
      </svg>
    ),
    title: 'Human Escalation Engine',
    description: 'Seamlessly transfers to your team when needed — emergencies, commercial projects, or when confidence is low. Includes full conversation summary.',
    highlights: ['Emergency escalation (gas, CO, sparks)', 'Conversation summary for team', 'Transparent handoff process'],
    color: 'bg-amber-50 text-amber-600',
  },
  {
    icon: (
      <svg className="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4" />
      </svg>
    ),
    title: 'CRM & Scheduling Integrations',
    description: 'Works with ServiceTitan, Housecall Pro, Jobber, Google Calendar, and Outlook. Reads calendars, creates appointments, syncs data.',
    highlights: ['Seamless integration layer', 'Two-way calendar sync', 'Customer data enrichment'],
    color: 'bg-indigo-50 text-indigo-600',
  },
  {
    icon: (
      <svg className="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
      </svg>
    ),
    title: 'Analytics Dashboard',
    description: 'Real-time revenue attribution, lead & booking metrics, AI performance tracking, and speed-to-lead monitoring.',
    highlights: ['Revenue attribution per channel', 'AI performance metrics', 'Speed-to-lead tracking'],
    color: 'bg-violet-50 text-violet-600',
  },
]

export default function Modules() {
  return (
    <section id="modules" className="py-16 md:py-24 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="section-title">
            Everything you need to{' '}
            <span className="gradient-text">never lose a lead again</span>
          </h2>
          <p className="section-subtitle">
            10 core modules that work together as your autonomous revenue employee — from first touch to lifetime value.
          </p>
        </div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {modules.map((mod, i) => (
            <div key={i} className="bg-white rounded-2xl p-6 border border-gray-100 hover:shadow-lg hover:border-hvac-blue-200 transition-all duration-300 group">
              <div className={`w-12 h-12 rounded-xl ${mod.color} flex items-center justify-center mb-4 group-hover:scale-110 transition-transform`}>
                {mod.icon}
              </div>
              <h3 className="text-lg font-bold text-gray-900 mb-2">{mod.title}</h3>
              <p className="text-gray-600 text-sm mb-4 leading-relaxed">{mod.description}</p>
              <ul className="space-y-2">
                {mod.highlights.map((h, j) => (
                  <li key={j} className="flex items-start gap-2 text-sm text-gray-500">
                    <svg className="w-4 h-4 text-green-500 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    {h}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}