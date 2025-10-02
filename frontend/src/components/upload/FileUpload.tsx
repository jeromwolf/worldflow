import { useCallback, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { FiUpload, FiFile, FiX, FiAlertCircle } from 'react-icons/fi'

interface FileUploadProps {
  onUpload: (file: File, sourceLang: string, targetLang: string) => Promise<void>
}

export default function FileUpload({ onUpload }: FileUploadProps) {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [sourceLang, setSourceLang] = useState('ko')
  const [targetLang, setTargetLang] = useState('en')
  const [isUploading, setIsUploading] = useState(false)
  const [error, setError] = useState('')

  const onDrop = useCallback((acceptedFiles: File[]) => {
    setError('')

    if (acceptedFiles.length === 0) {
      setError('PDF 파일만 업로드 가능합니다.')
      return
    }

    const file = acceptedFiles[0]

    // Validate file size (50MB)
    if (file.size > 50 * 1024 * 1024) {
      setError('파일 크기는 50MB를 초과할 수 없습니다.')
      return
    }

    setSelectedFile(file)
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf']
    },
    maxFiles: 1,
    multiple: false
  })

  const handleUpload = async () => {
    if (!selectedFile) return

    setIsUploading(true)
    setError('')

    try {
      await onUpload(selectedFile, sourceLang, targetLang)
      setSelectedFile(null)
    } catch (err: any) {
      setError(err.message || '업로드에 실패했습니다.')
    } finally {
      setIsUploading(false)
    }
  }

  const handleRemove = () => {
    setSelectedFile(null)
    setError('')
  }

  return (
    <div className="w-full max-w-2xl mx-auto">
      {/* Dropzone */}
      {!selectedFile && (
        <div
          {...getRootProps()}
          className={`border-2 border-dashed rounded-xl p-12 text-center cursor-pointer transition-colors ${
            isDragActive
              ? 'border-primary-600 bg-primary-50'
              : 'border-gray-300 hover:border-primary-400'
          }`}
        >
          <input {...getInputProps()} />

          <div className="flex flex-col items-center">
            <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mb-4">
              <FiUpload className="w-8 h-8 text-primary-600" />
            </div>

            {isDragActive ? (
              <p className="text-lg font-medium text-primary-600">
                여기에 파일을 놓으세요
              </p>
            ) : (
              <>
                <p className="text-lg font-medium text-gray-900 mb-2">
                  PDF 파일을 드래그하거나 클릭하세요
                </p>
                <p className="text-sm text-gray-500">
                  최대 50MB, 200페이지까지 지원
                </p>
              </>
            )}
          </div>
        </div>
      )}

      {/* Selected File */}
      {selectedFile && (
        <div className="bg-white border border-gray-200 rounded-xl p-6">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center space-x-3">
              <div className="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center">
                <FiFile className="w-6 h-6 text-red-600" />
              </div>
              <div>
                <p className="font-medium text-gray-900">{selectedFile.name}</p>
                <p className="text-sm text-gray-500">
                  {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                </p>
              </div>
            </div>
            <button
              onClick={handleRemove}
              className="text-gray-400 hover:text-gray-600"
              disabled={isUploading}
            >
              <FiX className="w-5 h-5" />
            </button>
          </div>

          {/* Language Selection */}
          <div className="grid grid-cols-2 gap-4 mb-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                원본 언어
              </label>
              <select
                value={sourceLang}
                onChange={(e) => setSourceLang(e.target.value)}
                className="input-field"
                disabled={isUploading}
              >
                <option value="ko">한국어</option>
                <option value="en">English</option>
                <option value="ja">日本語</option>
                <option value="zh">中文</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                번역 언어
              </label>
              <select
                value={targetLang}
                onChange={(e) => setTargetLang(e.target.value)}
                className="input-field"
                disabled={isUploading}
              >
                <option value="en">English</option>
                <option value="ko">한국어</option>
                <option value="ja">日本語</option>
                <option value="zh">中文</option>
              </select>
            </div>
          </div>

          {/* Upload Button */}
          <button
            onClick={handleUpload}
            disabled={isUploading || sourceLang === targetLang}
            className="btn-primary w-full"
          >
            {isUploading ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white inline-block mr-2"></div>
                업로드 중...
              </>
            ) : (
              '업로드 시작'
            )}
          </button>

          {sourceLang === targetLang && (
            <p className="text-sm text-amber-600 mt-2 text-center">
              원본 언어와 번역 언어가 같습니다
            </p>
          )}
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div className="mt-4 bg-red-50 border border-red-200 rounded-lg p-4 flex items-start">
          <FiAlertCircle className="text-red-600 mr-3 mt-0.5 flex-shrink-0" />
          <div>
            <p className="text-sm font-medium text-red-800">오류</p>
            <p className="text-sm text-red-700 mt-1">{error}</p>
          </div>
        </div>
      )}
    </div>
  )
}
