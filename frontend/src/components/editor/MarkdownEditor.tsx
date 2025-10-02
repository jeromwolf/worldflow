import { useRef, useEffect } from 'react'
import Editor, { Monaco } from '@monaco-editor/react'
import type { editor } from 'monaco-editor'

interface MarkdownEditorProps {
  value: string
  onChange: (value: string) => void
  readOnly?: boolean
  language?: string
  height?: string
}

export default function MarkdownEditor({
  value,
  onChange,
  readOnly = false,
  language = 'markdown',
  height = '600px'
}: MarkdownEditorProps) {
  const editorRef = useRef<editor.IStandaloneCodeEditor | null>(null)

  function handleEditorDidMount(editor: editor.IStandaloneCodeEditor, monaco: Monaco) {
    editorRef.current = editor

    // Configure Monaco for Markdown
    monaco.languages.setLanguageConfiguration('markdown', {
      wordPattern: /(-?\d*\.\d\w*)|([^\`\~\!\@\#\%\^\&\*\(\)\-\=\+\[\{\]\}\\\|\;\:\'\"\,\.\<\>\/\?\s]+)/g,
    })

    // Auto-save on change (debounced)
    let timeoutId: NodeJS.Timeout
    editor.onDidChangeModelContent(() => {
      clearTimeout(timeoutId)
      timeoutId = setTimeout(() => {
        const currentValue = editor.getValue()
        onChange(currentValue)
      }, 500) // 500ms debounce
    })
  }

  useEffect(() => {
    // Update editor value if changed externally
    if (editorRef.current && value !== editorRef.current.getValue()) {
      editorRef.current.setValue(value)
    }
  }, [value])

  return (
    <div className="border border-gray-300 rounded-lg overflow-hidden">
      <Editor
        height={height}
        defaultLanguage={language}
        value={value}
        onMount={handleEditorDidMount}
        options={{
          readOnly,
          minimap: { enabled: false },
          fontSize: 14,
          lineNumbers: 'on',
          wordWrap: 'on',
          scrollBeyondLastLine: false,
          automaticLayout: true,
          tabSize: 2,
          renderWhitespace: 'selection',
          folding: true,
          lineDecorationsWidth: 10,
          lineNumbersMinChars: 4,
          scrollbar: {
            vertical: 'visible',
            horizontal: 'visible',
            verticalScrollbarSize: 12,
            horizontalScrollbarSize: 12,
          },
        }}
        theme="vs-light"
      />
    </div>
  )
}
