import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import SplitView from '@/components/editor/SplitView'
import { FiDownload, FiFileText, FiAlertCircle, FiHome } from 'react-icons/fi'

export default function Editor() {
  const { projectId } = useParams<{ projectId: string }>()
  const navigate = useNavigate()

  const [project, setProject] = useState<any>(null)
  const [translatedMarkdown, setTranslatedMarkdown] = useState('')
  const [isSaving, setIsSaving] = useState(false)
  const [isGenerating, setIsGenerating] = useState(false)
  const [error, setError] = useState('')

  // Fetch project data
  useEffect(() => {
    fetchProject()
  }, [projectId])

  const fetchProject = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/projects/${projectId}`)

      if (!response.ok) throw new Error('Failed to fetch project')

      const data = await response.json()
      setProject(data)
      setTranslatedMarkdown(data.markdown_translated || '')
    } catch (err) {
      setError('프로젝트를 불러올 수 없습니다.')
    }
  }

  const handleSave = async () => {
    if (!projectId) return

    setIsSaving(true)
    setError('')

    try {
      const response = await fetch(`http://localhost:8000/api/projects/${projectId}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          markdown_translated: translatedMarkdown
        })
      })

      if (!response.ok) throw new Error('Failed to save')

      // Success feedback
      alert('저장되었습니다!')
    } catch (err) {
      setError('저장에 실패했습니다.')
    } finally {
      setIsSaving(false)
    }
  }

  const handleGeneratePDF = async () => {
    if (!projectId) return

    setIsGenerating(true)
    setError('')

    try {
      // 1. Save markdown first
      const saveResponse = await fetch(`http://localhost:8000/api/projects/${projectId}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          markdown_translated: translatedMarkdown
        })
      })

      if (!saveResponse.ok) throw new Error('Failed to save before PDF generation')

      // 2. Generate PDF
      const response = await fetch(`http://localhost:8000/api/pdf/projects/${projectId}/generate`, {
        method: 'POST'
      })

      if (!response.ok) throw new Error('PDF generation failed')

      // 3. Refresh project data to get new pdf_translated_url
      await fetchProject()

      // 4. Success - open download
      window.open(`http://localhost:8000/api/pdf/projects/${projectId}/download`, '_blank')
    } catch (err) {
      setError('PDF 생성에 실패했습니다.')
    } finally {
      setIsGenerating(false)
    }
  }

  if (!project) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <p className="text-gray-600">프로젝트 불러오는 중...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="h-screen flex flex-col">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            {/* Dashboard Button */}
            <button
              onClick={() => navigate('/dashboard')}
              className="text-gray-600 hover:text-gray-900 p-2 rounded-lg hover:bg-gray-100"
              title="프로젝트 목록"
            >
              <FiHome className="text-xl" />
            </button>

            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                {project.original_filename}
              </h1>
              <p className="text-sm text-gray-600 mt-1">
                {project.source_language} → {project.target_language}
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-3">
            {/* Generate PDF Button */}
            <button
              onClick={handleGeneratePDF}
              disabled={isGenerating || !translatedMarkdown}
              className="btn-primary"
            >
              {isGenerating ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white inline-block mr-2"></div>
                  PDF 생성 중...
                </>
              ) : (
                <>
                  <FiFileText className="inline mr-2" />
                  PDF 생성
                </>
              )}
            </button>
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="mt-4 bg-red-50 border border-red-200 rounded-lg p-3 flex items-center">
            <FiAlertCircle className="text-red-600 mr-2" />
            <span className="text-red-700 text-sm">{error}</span>
          </div>
        )}
      </div>

      {/* Editor */}
      <div className="flex-1 overflow-hidden bg-gray-50">
        <SplitView
          originalMarkdown={project.markdown_original || ''}
          translatedMarkdown={translatedMarkdown}
          onTranslatedChange={setTranslatedMarkdown}
        />
      </div>
    </div>
  )
}
