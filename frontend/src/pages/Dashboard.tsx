import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import FileUpload from '@/components/upload/FileUpload'
import ProjectCard from '@/components/dashboard/ProjectCard'
import { FiPlus, FiRefreshCw } from 'react-icons/fi'

export default function Dashboard() {
  const navigate = useNavigate()
  const [projects, setProjects] = useState<any[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [showUpload, setShowUpload] = useState(false)

  useEffect(() => {
    fetchProjects()
  }, [])

  const fetchProjects = async () => {
    setIsLoading(true)

    try {
      const response = await fetch('http://localhost:8000/api/projects/')

      if (!response.ok) {
        if (response.status === 401) {
          // 인증 필요 - 개발 중에는 빈 배열 반환
          setProjects([])
          return
        }
        throw new Error('Failed to fetch projects')
      }

      const data = await response.json()
      setProjects(data.projects || [])
    } catch (err) {
      console.error('Failed to fetch projects:', err)
      setProjects([])
    } finally {
      setIsLoading(false)
    }
  }

  const handleUpload = async (file: File, sourceLang: string, targetLang: string) => {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('source_language', sourceLang)
    formData.append('target_language', targetLang)

    const response = await fetch('http://localhost:8000/api/projects/upload', {
      method: 'POST',
      body: formData
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Upload failed')
    }

    const project = await response.json()

    // Add to projects list
    setProjects([project, ...projects])
    setShowUpload(false)

    // Start translation automatically
    await startTranslation(project.id)
  }

  const startTranslation = async (projectId: string) => {
    try {
      const response = await fetch(`http://localhost:8000/api/translation/projects/${projectId}/translate`, {
        method: 'POST'
      })

      if (response.ok) {
        // Refresh projects to show updated status
        fetchProjects()
      }
    } catch (err) {
      console.error('Failed to start translation:', err)
    }
  }

  const handleDelete = async (projectId: string) => {
    try {
      const response = await fetch(`http://localhost:8000/api/projects/${projectId}`, {
        method: 'DELETE'
      })

      if (response.ok) {
        setProjects(projects.filter(p => p.id !== projectId))
      }
    } catch (err) {
      console.error('Failed to delete project:', err)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">프로젝트</h1>
            <p className="text-gray-600 mt-1">
              PDF 번역 프로젝트를 관리하세요
            </p>
          </div>

          <div className="flex items-center space-x-3">
            <button
              onClick={fetchProjects}
              className="btn-secondary"
              disabled={isLoading}
            >
              <FiRefreshCw className={`inline mr-2 ${isLoading ? 'animate-spin' : ''}`} />
              새로고침
            </button>

            <button
              onClick={() => setShowUpload(!showUpload)}
              className="btn-primary"
            >
              <FiPlus className="inline mr-2" />
              새 프로젝트
            </button>
          </div>
        </div>

        {/* Upload Section */}
        {showUpload && (
          <div className="mb-8">
            <div className="card">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-semibold text-gray-900">
                  새 프로젝트 생성
                </h2>
                <button
                  onClick={() => setShowUpload(false)}
                  className="text-gray-500 hover:text-gray-700"
                >
                  취소
                </button>
              </div>

              <FileUpload onUpload={handleUpload} />
            </div>
          </div>
        )}

        {/* Projects List */}
        {isLoading ? (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
            <p className="text-gray-600">프로젝트 불러오는 중...</p>
          </div>
        ) : projects.length === 0 ? (
          <div className="card text-center py-12">
            <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <FiPlus className="w-8 h-8 text-gray-400" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              프로젝트가 없습니다
            </h3>
            <p className="text-gray-600 mb-6">
              첫 번째 PDF 번역 프로젝트를 시작해보세요
            </p>
            <button
              onClick={() => setShowUpload(true)}
              className="btn-primary"
            >
              <FiPlus className="inline mr-2" />
              새 프로젝트 시작
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {projects.map((project) => (
              <ProjectCard
                key={project.id}
                project={project}
                onDelete={handleDelete}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
