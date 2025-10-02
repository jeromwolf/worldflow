import { Link } from 'react-router-dom'

export default function Header() {
  return (
    <header className="bg-white border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-xl">A</span>
            </div>
            <span className="text-xl font-bold text-gray-900">
              All-Rounder Translation
            </span>
          </Link>

          {/* Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            <Link
              to="/pricing"
              className="text-gray-700 hover:text-primary-600 font-medium transition-colors"
            >
              가격
            </Link>
            <Link
              to="/docs"
              className="text-gray-700 hover:text-primary-600 font-medium transition-colors"
            >
              사용 가이드
            </Link>
            <Link
              to="/dashboard"
              className="text-gray-700 hover:text-primary-600 font-medium transition-colors"
            >
              대시보드
            </Link>
          </nav>

          {/* Auth Buttons */}
          <div className="flex items-center space-x-4">
            <Link to="/login" className="btn-secondary">
              로그인
            </Link>
            <Link to="/register" className="btn-primary">
              시작하기
            </Link>
          </div>
        </div>
      </div>
    </header>
  )
}
