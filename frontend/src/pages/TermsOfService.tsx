export default function TermsOfService() {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <a href="/" className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-gradient-to-br from-emerald-600 to-teal-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-sm">R</span>
              </div>
              <h1 className="text-xl font-bold bg-gradient-to-r from-emerald-600 to-teal-600 bg-clip-text text-transparent">
                Resumade
              </h1>
            </a>
          </div>
        </div>
      </header>

      {/* Content */}
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <h1 className="text-4xl font-bold text-gray-900 mb-8">Terms of Service</h1>
        <p className="text-sm text-gray-600 mb-8">Last updated: October 10, 2025</p>

        <div className="prose prose-lg max-w-none space-y-8">
          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">1. Acceptance of Terms</h2>
            <p className="text-gray-700">
              By accessing and using Resumade, you accept and agree to be bound by the terms and provisions of this agreement. If you do not agree to these terms, please do not use our service.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">2. Use of Service</h2>
            <p className="text-gray-700 mb-4">You agree to use Resumade only for lawful purposes. You must not:</p>
            <ul className="list-disc pl-6 text-gray-700 space-y-2">
              <li>Use the service to create fraudulent or misleading resumes</li>
              <li>Attempt to gain unauthorized access to our systems</li>
              <li>Upload malicious code or viruses</li>
              <li>Violate any applicable laws or regulations</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">3. User Accounts</h2>
            <p className="text-gray-700">
              You are responsible for maintaining the confidentiality of your account credentials and for all activities that occur under your account. You must notify us immediately of any unauthorized use of your account.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">4. Content Ownership</h2>
            <p className="text-gray-700">
              You retain all rights to the content you create using Resumade. We do not claim ownership of your resume content. However, you grant us a license to store and process your content to provide our services.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">5. Service Availability</h2>
            <p className="text-gray-700">
              We strive to provide reliable service but do not guarantee uninterrupted access. We may modify, suspend, or discontinue any part of the service at any time without notice.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">6. Limitation of Liability</h2>
            <p className="text-gray-700">
              Resumade is provided "as is" without warranties of any kind. We are not liable for any damages arising from your use of the service, including but not limited to lost opportunities or employment outcomes.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">7. Termination</h2>
            <p className="text-gray-700">
              We reserve the right to terminate or suspend your account at any time for violations of these terms. You may also terminate your account at any time by contacting us.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">8. Changes to Terms</h2>
            <p className="text-gray-700">
              We may update these terms from time to time. We will notify you of significant changes by email or through the service. Continued use of the service after changes constitutes acceptance of the new terms.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">9. Contact Information</h2>
            <p className="text-gray-700">
              For questions about these Terms of Service, please contact us at:{' '}
              <a href="mailto:legal@resumade.com" className="text-emerald-600 hover:text-emerald-700">
                legal@resumade.com
              </a>
            </p>
          </section>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center text-gray-600">
            <p>&copy; 2025 Resumade. All rights reserved.</p>
            <div className="mt-4 space-x-4">
              <a href="/privacy" className="text-emerald-600 hover:text-emerald-700">Privacy Policy</a>
              <a href="/terms" className="text-emerald-600 hover:text-emerald-700">Terms of Service</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
