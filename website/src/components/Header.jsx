import { useState } from 'react'

export default function Header() {
  const [mobileOpen, setMobileOpen] = useState(false)

  const navLinks = [
    { label: 'Modules', href: '#modules' },
    { label: 'Pricing', href: '#pricing' },
    { label: 'Try Demo', href: '#demo', primary: true },
  ]

  return (
    <header className="fixed w-full top-0 z-50 bg-white/95 backdrop-blur-sm border-b border-gray-100">
      <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16 lg:h-20">
          {/* Logo */}
          <a href="#" className="flex items-center gap-2">
            <div className="w-9 h-9 bg-gradient-to-br from-hvac-blue-500 to-hvac-accent-500 rounded-lg flex items-center justify-center">
              <svg className="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <span className="text-lg font-bold text-gray-900">HVAC <span className="gradient-text">AI Employee</span></span>
          </a>

          {/* Desktop nav */}
          <div className="hidden md:flex items-center gap-8">
            {navLinks.map(link => (
              link.primary ? (
                <a key={link.label} href={link.href} className="btn-primary text-sm px-5 py-2.5">
                  {link.label}
                </a>
              ) : (
                <a key={link.label} href={link.href} className="text-gray-600 hover:text-hvac-blue-500 font-medium transition-colors">
                  {link.label}
                </a>
              )
            ))}
          </div>

          {/* Mobile hamburger */}
          <button
            onClick={() => setMobileOpen(!mobileOpen)}
            className="md:hidden p-2 text-gray-600 hover:text-gray-900"
            aria-label="Toggle menu"
          >
            <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              {mobileOpen ? (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              ) : (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              )}
            </svg>
          </button>
        </div>

        {/* Mobile menu */}
        {mobileOpen && (
          <div className="md:hidden pb-4 border-t border-gray-100 pt-4">
            <div className="flex flex-col gap-3">
              {navLinks.map(link => (
                link.primary ? (
                  <a key={link.label} href={link.href} className="btn-primary text-sm text-center" onClick={() => setMobileOpen(false)}>
                    {link.label}
                  </a>
                ) : (
                  <a key={link.label} href={link.href} className="text-gray-600 hover:text-hvac-blue-500 font-medium py-2" onClick={() => setMobileOpen(false)}>
                    {link.label}
                  </a>
                )
              ))}
            </div>
          </div>
        )}
      </nav>
    </header>
  )
}