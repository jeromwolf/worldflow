import { useState } from 'react'
import MarkdownEditor from './MarkdownEditor'
import { FiEye, FiEdit3, FiCopy, FiCheck } from 'react-icons/fi'

interface SplitViewProps {
  originalMarkdown: string
  translatedMarkdown: string
  onTranslatedChange: (value: string) => void
  onSave: () => void
  isSaving?: boolean
}

export default function SplitView({
  originalMarkdown,
  translatedMarkdown,
  onTranslatedChange,
  onSave,
  isSaving = false
}: SplitViewProps) {
  const [viewMode, setViewMode] = useState<'split' | 'original' | 'translated'>('split')
  const [copied, setCopied] = useState(false)

  const handleCopyOriginal = () => {
    navigator.clipboard.writeText(originalMarkdown)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="flex flex-col h-full">
      {/* Toolbar */}
      <div className="bg-white border-b border-gray-200 px-4 py-3 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          {/* View Mode Selector */}
          <div className="inline-flex rounded-lg border border-gray-300">
            <button
              onClick={() => setViewMode('original')}
              className={`px-4 py-2 text-sm font-medium rounded-l-lg ${
                viewMode === 'original'
                  ? 'bg-primary-600 text-white'
                  : 'bg-white text-gray-700 hover:bg-gray-50'
              }`}
            >
              <FiEye className="inline mr-2" />
              원본
            </button>
            <button
              onClick={() => setViewMode('split')}
              className={`px-4 py-2 text-sm font-medium border-x border-gray-300 ${
                viewMode === 'split'
                  ? 'bg-primary-600 text-white'
                  : 'bg-white text-gray-700 hover:bg-gray-50'
              }`}
            >
              Split View
            </button>
            <button
              onClick={() => setViewMode('translated')}
              className={`px-4 py-2 text-sm font-medium rounded-r-lg ${
                viewMode === 'translated'
                  ? 'bg-primary-600 text-white'
                  : 'bg-white text-gray-700 hover:bg-gray-50'
              }`}
            >
              <FiEdit3 className="inline mr-2" />
              번역본
            </button>
          </div>

          {/* Copy Original */}
          <button
            onClick={handleCopyOriginal}
            className="px-3 py-2 text-sm text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50"
          >
            {copied ? (
              <>
                <FiCheck className="inline mr-2 text-green-600" />
                복사됨
              </>
            ) : (
              <>
                <FiCopy className="inline mr-2" />
                원본 복사
              </>
            )}
          </button>
        </div>

        {/* Save Button */}
        <button
          onClick={onSave}
          disabled={isSaving}
          className="btn-primary"
        >
          {isSaving ? '저장 중...' : '저장'}
        </button>
      </div>

      {/* Editor Area */}
      <div className="flex-1 overflow-hidden">
        {viewMode === 'split' && (
          <div className="grid grid-cols-2 gap-4 h-full p-4">
            {/* Original (Read-only) */}
            <div className="flex flex-col">
              <h3 className="text-sm font-semibold text-gray-700 mb-2">
                원본 (읽기 전용)
              </h3>
              <MarkdownEditor
                value={originalMarkdown}
                onChange={() => {}}
                readOnly={true}
                height="calc(100vh - 200px)"
              />
            </div>

            {/* Translated (Editable) */}
            <div className="flex flex-col">
              <h3 className="text-sm font-semibold text-gray-700 mb-2">
                번역본 (편집 가능)
              </h3>
              <MarkdownEditor
                value={translatedMarkdown}
                onChange={onTranslatedChange}
                readOnly={false}
                height="calc(100vh - 200px)"
              />
            </div>
          </div>
        )}

        {viewMode === 'original' && (
          <div className="h-full p-4">
            <h3 className="text-sm font-semibold text-gray-700 mb-2">
              원본 (읽기 전용)
            </h3>
            <MarkdownEditor
              value={originalMarkdown}
              onChange={() => {}}
              readOnly={true}
              height="calc(100vh - 200px)"
            />
          </div>
        )}

        {viewMode === 'translated' && (
          <div className="h-full p-4">
            <h3 className="text-sm font-semibold text-gray-700 mb-2">
              번역본 (편집 가능)
            </h3>
            <MarkdownEditor
              value={translatedMarkdown}
              onChange={onTranslatedChange}
              readOnly={false}
              height="calc(100vh - 200px)"
            />
          </div>
        )}
      </div>
    </div>
  )
}
