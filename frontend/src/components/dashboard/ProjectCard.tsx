import { FiFile, FiClock, FiCheckCircle, FiAlertCircle, FiEdit3, FiTrash2 } from 'react-icons/fi'
import { useNavigate } from 'react-router-dom'

interface Project {
  id: string
  original_filename: string
  source_language: string
  target_language: string
  status: string
  progress_percent: number
  page_count: number
  created_at: string
}

interface ProjectCardProps {
  project: Project
  onDelete: (id: string) => void
}

export default function ProjectCard({ project, onDelete }: ProjectCardProps) {
  const navigate = useNavigate()

  const getStatusIcon = () => {
    switch (project.status) {
      case 'completed':
        return <FiCheckCircle className="text-green-600" />
      case 'failed':
        return <FiAlertCircle className="text-red-600" />
      case 'parsing':
      case 'translating':
        return (
          <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-primary-600"></div>
        )
      default:
        return <FiClock className="text-gray-400" />
    }
  }

  const getStatusText = () => {
    switch (project.status) {
      case 'uploading':
        return '업로드 중'
      case 'parsing':
        return 'PDF 파싱 중'
      case 'translating':
        return '번역 중'
      case 'completed':
        return '완료'
      case 'failed':
        return '실패'
      default:
        return project.status
    }
  }

  const getStatusColor = () => {
    switch (project.status) {
      case 'completed':
        return 'text-green-600'
      case 'failed':
        return 'text-red-600'
      case 'parsing':
      case 'translating':
        return 'text-primary-600'
      default:
        return 'text-gray-600'
    }
  }

  const handleEdit = () => {
    if (project.status === 'completed' || project.status === 'translating') {
      navigate(`/editor/${project.id}`)
    }
  }

  const handleDelete = () => {
    if (confirm(`"${project.original_filename}" 프로젝트를 삭제하시겠습니까?`)) {
      onDelete(project.id)
    }
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('ko-KR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  return (
    <div className="card hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-start space-x-3 flex-1 min-w-0">
          <div className="w-10 h-10 bg-red-100 rounded-lg flex items-center justify-center flex-shrink-0">
            <FiFile className="w-5 h-5 text-red-600" />
          </div>

          <div className="flex-1 min-w-0">
            <h3 className="font-semibold text-gray-900 truncate">
              {project.original_filename}
            </h3>
            <p className="text-sm text-gray-500 mt-1">
              {project.source_language.toUpperCase()} → {project.target_language.toUpperCase()}
              {project.page_count && ` • ${project.page_count} 페이지`}
            </p>
          </div>
        </div>

        {/* Actions - Always visible */}
        <div className="flex items-center space-x-2 flex-shrink-0 ml-2">
          {(project.status === 'completed' || project.status === 'translating') && (
            <button
              onClick={handleEdit}
              className="p-2 text-gray-600 hover:text-primary-600 hover:bg-primary-50 rounded-lg transition-colors"
              title="편집"
            >
              <FiEdit3 className="w-4 h-4" />
            </button>
          )}

          <button
            onClick={handleDelete}
            className="p-2 text-gray-600 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
            title="삭제"
          >
            <FiTrash2 className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Status */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          {getStatusIcon()}
          <span className={`text-sm font-medium ${getStatusColor()}`}>
            {getStatusText()}
          </span>
        </div>

        <span className="text-xs text-gray-500">
          {formatDate(project.created_at)}
        </span>
      </div>

      {/* Progress Bar */}
      {(project.status === 'parsing' || project.status === 'translating') && (
        <div className="mt-3">
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-primary-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${project.progress_percent}%` }}
            ></div>
          </div>
          <p className="text-xs text-gray-500 mt-1 text-right">
            {project.progress_percent}%
          </p>
        </div>
      )}
    </div>
  )
}
