export default function CTABanner({ onOpenChat }) {
  return (
    <section className="py-16 md:py-24 bg-gradient-to-br from-hvac-blue-500 to-hvac-blue-700 relative overflow-hidden">
      {/* Decorative elements */}
      <div className="absolute top-10 right-10 w-64 h-64 bg-white/5 rounded-full blur-3xl" />
      <div className="absolute bottom-10 left-10 w-48 h-48 bg-hvac-accent-300/10 rounded-full blur-3xl" />

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold text-white mb-6 leading-tight">
          Ready to never miss another call?
        </h2>
        <p className="text-lg md:text-xl text-blue-100 max-w-2xl mx-auto mb-10 leading-relaxed">
          Join 200+ HVAC companies already using HVAC AI Employee to capture every lead, 
          book more appointments, and grow revenue — without hiring more staff.
        </p>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <button onClick={onOpenChat} className="inline-flex items-center justify-center px-8 py-4 rounded-xl font-bold text-lg bg-white text-hvac-blue-600 hover:bg-blue-50 transition-all duration-200 shadow-xl hover:shadow-2xl w-full sm:w-auto">
            <svg className="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
            Talk to the AI — It's Free
          </button>
          <a href="mailto:sales@hvacaiemployee.com" className="inline-flex items-center justify-center px-8 py-4 rounded-xl font-bold text-lg border-2 border-white/30 text-white hover:bg-white/10 transition-all duration-200 w-full sm:w-auto">
            Talk to Sales
          </a>
        </div>

        <div className="mt-10 flex flex-wrap items-center justify-center gap-6 text-sm text-blue-200">
          <span className="inline-flex items-center gap-1.5">
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
            No credit card required
          </span>
          <span className="inline-flex items-center gap-1.5">
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
            30-day money-back guarantee
          </span>
          <span className="inline-flex items-center gap-1.5">
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
            Cancel anytime
          </span>
        </div>
      </div>
    </section>
  )
}