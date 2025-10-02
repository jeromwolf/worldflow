import { Link } from 'react-router-dom'
import { FiUpload, FiGlobe, FiEdit3, FiDownload } from 'react-icons/fi'

export default function Home() {
  return (
    <div className="bg-white">
      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center">
          <h1 className="text-5xl font-bold text-gray-900 mb-6">
            AI 기반 PDF 번역
            <br />
            <span className="text-primary-600">빠르고 정확하게</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            한국어 강의 자료를 해외 강사에게 전달하세요.
            PDF → Markdown → AI 번역 → 편집 → PDF 생성까지 한 번에.
          </p>
          <div className="flex justify-center space-x-4">
            <Link to="/upload" className="btn-primary text-lg px-8 py-3">
              지금 시작하기
            </Link>
            <Link to="/demo" className="btn-secondary text-lg px-8 py-3">
              데모 보기
            </Link>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="bg-gray-50 py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
            간단한 4단계 프로세스
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            {/* Step 1 */}
            <div className="text-center">
              <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <FiUpload className="w-8 h-8 text-primary-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                1. PDF 업로드
              </h3>
              <p className="text-gray-600">
                번역할 PDF 파일을 드래그 앤 드롭
              </p>
            </div>

            {/* Step 2 */}
            <div className="text-center">
              <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <FiGlobe className="w-8 h-8 text-primary-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                2. 언어 선택
              </h3>
              <p className="text-gray-600">
                원문 언어와 번역할 언어 선택
              </p>
            </div>

            {/* Step 3 */}
            <div className="text-center">
              <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <FiEdit3 className="w-8 h-8 text-primary-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                3. AI 번역 & 편집
              </h3>
              <p className="text-gray-600">
                GPT-4로 번역 후 Markdown 편집기로 수정
              </p>
            </div>

            {/* Step 4 */}
            <div className="text-center">
              <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <FiDownload className="w-8 h-8 text-primary-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                4. PDF 다운로드
              </h3>
              <p className="text-gray-600">
                번역된 PDF 파일 즉시 다운로드
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-primary-600 py-16">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold text-white mb-4">
            지금 바로 시작하세요
          </h2>
          <p className="text-primary-100 text-lg mb-8">
            무료 플랜으로 시작해보세요. 신용카드 필요 없습니다.
          </p>
          <Link to="/register" className="bg-white text-primary-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors inline-block">
            무료로 시작하기
          </Link>
        </div>
      </section>
    </div>
  )
}
