import { Link } from 'react-router-dom'

export default function Footer() {
  return (
    <footer className="bg-gray-900 text-gray-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* About */}
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center space-x-2 mb-4">
              <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-xl">A</span>
              </div>
              <span className="text-xl font-bold text-white">
                All-Rounder Translation
              </span>
            </div>
            <p className="text-gray-400 max-w-md">
              AI 기반 PDF 번역 서비스로 한국어 강의 자료를
              해외 강사에게 완벽하게 전달하세요.
            </p>
          </div>

          {/* Links */}
          <div>
            <h3 className="text-white font-semibold mb-4">서비스</h3>
            <ul className="space-y-2">
              <li>
                <Link to="/pricing" className="hover:text-white transition-colors">
                  가격 안내
                </Link>
              </li>
              <li>
                <Link to="/docs" className="hover:text-white transition-colors">
                  사용 가이드
                </Link>
              </li>
              <li>
                <Link to="/api" className="hover:text-white transition-colors">
                  API 문서
                </Link>
              </li>
            </ul>
          </div>

          {/* Support */}
          <div>
            <h3 className="text-white font-semibold mb-4">지원</h3>
            <ul className="space-y-2">
              <li>
                <Link to="/contact" className="hover:text-white transition-colors">
                  문의하기
                </Link>
              </li>
              <li>
                <Link to="/faq" className="hover:text-white transition-colors">
                  FAQ
                </Link>
              </li>
              <li>
                <Link to="/privacy" className="hover:text-white transition-colors">
                  개인정보처리방침
                </Link>
              </li>
              <li>
                <Link to="/terms" className="hover:text-white transition-colors">
                  이용약관
                </Link>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
          <p>&copy; 2025 All-Rounder Translation. All rights reserved.</p>
        </div>
      </div>
    </footer>
  )
}
