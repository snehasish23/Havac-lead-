const plans = [
  {
    name: 'Starter',
    price: '$299',
    period: '/month',
    description: 'Perfect for small operations looking to capture every lead.',
    features: [
      'Lead Capture & Instant Response',
      'Basic Lead Qualification',
      'Speed to Lead: Under 5 seconds',
      '24/7 Availability',
      'Website & Phone Integration',
      'Basic Analytics',
    ],
    cta: 'Start Free Trial',
    popular: false,
  },
  {
    name: 'Growth',
    price: '$599',
    period: '/month',
    description: 'The complete revenue capture solution for growing businesses.',
    features: [
      'Everything in Starter',
      'Missed Call Recovery (auto-callback)',
      'Booking Abandonment Recovery',
      'AI Nurturing Sequences',
      'CRM Integrations (ServiceTitan, Housecall Pro, Jobber)',
      'Calendar Sync (Google, Outlook)',
      'Advanced Analytics Dashboard',
    ],
    cta: 'Start Free Trial',
    popular: true,
  },
  {
    name: 'Scale',
    price: '$999',
    period: '/month',
    description: 'Maximum revenue optimization for established HVAC companies.',
    features: [
      'Everything in Growth',
      'Customer Reactivation Engine',
      'Maintenance Membership Engine',
      'Human Escalation Engine',
      'White-labeling',
      'Dedicated Account Manager',
      'Revenue Attribution Reports',
      'Priority Support',
    ],
    cta: 'Contact Sales',
    popular: false,
  },
]

export default function Pricing() {
  return (
    <section id="pricing" className="py-16 md:py-24 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="section-title">
            Simple pricing.{' '}
            <span className="gradient-text">Massive ROI.</span>
          </h2>
          <p className="section-subtitle">
            Most customers see a full ROI within the first 30 days. No hidden fees, no long-term contracts.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-6 lg:gap-8 max-w-5xl mx-auto">
          {plans.map((plan, i) => (
            <div
              key={i}
              className={`relative rounded-2xl p-6 lg:p-8 border-2 transition-all duration-300 ${
                plan.popular
                  ? 'border-hvac-accent-400 bg-white shadow-xl scale-105 lg:scale-105'
                  : 'border-gray-200 bg-white hover:shadow-lg hover:border-hvac-blue-300'
              }`}
            >
              {plan.popular && (
                <div className="absolute -top-3.5 left-1/2 -translate-x-1/2 bg-hvac-accent-500 text-white text-xs font-bold px-4 py-1 rounded-full">
                  Most Popular
                </div>
              )}

              <div className="text-center mb-6">
                <h3 className="text-xl font-bold text-gray-900 mb-1">{plan.name}</h3>
                <p className="text-gray-500 text-sm mb-4">{plan.description}</p>
                <div className="flex items-baseline justify-center gap-0.5">
                  <span className="text-4xl font-extrabold text-gray-900">{plan.price}</span>
                  <span className="text-gray-500">{plan.period}</span>
                </div>
              </div>

              <ul className="space-y-3 mb-8">
                {plan.features.map((feat, j) => (
                  <li key={j} className="flex items-start gap-3 text-sm">
                    <svg className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    <span className="text-gray-600">{feat}</span>
                  </li>
                ))}
              </ul>

              <button
                className={`w-full py-3 rounded-xl font-semibold text-sm transition-all duration-200 ${
                  plan.popular
                    ? 'bg-hvac-accent-500 text-white hover:bg-hvac-accent-600 shadow-lg hover:shadow-xl'
                    : 'bg-gray-900 text-white hover:bg-gray-800'
                }`}
              >
                {plan.cta}
              </button>
            </div>
          ))}
        </div>

        {/* Guarantee */}
        <div className="mt-12 text-center">
          <div className="inline-flex items-center gap-2 bg-green-50 border border-green-200 rounded-full px-6 py-3">
            <svg className="w-5 h-5 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            </svg>
            <span className="text-sm font-medium text-green-800">
              30-day money-back guarantee. If you don't see results, you don't pay.
            </span>
          </div>
        </div>
      </div>
    </section>
  )
}