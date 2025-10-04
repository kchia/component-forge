"use client"

import { useState } from "react"
import { Button } from "./button"
import { Copy, Check } from "lucide-react"

// NOTE: This component currently does not include Prism.js syntax highlighting
// To enable full syntax highlighting, install prismjs:
//   npm install prismjs
//   npm install --save-dev @types/prismjs
// Then uncomment the Prism imports and highlighted code section below

// import Prism from "prismjs"
// import "prismjs/themes/prism-tomorrow.css"
// import "prismjs/components/prism-typescript"
// import "prismjs/components/prism-tsx"
// import "prismjs/components/prism-json"
// import "prismjs/components/prism-javascript"
// import "prismjs/components/prism-css"

export interface CodeBlockProps {
  code: string
  language?: string
  showLineNumbers?: boolean
  maxHeight?: string
  className?: string
}

export function CodeBlock({
  code,
  language = "typescript",
  showLineNumbers = false,
  maxHeight = "400px",
  className = "",
}: CodeBlockProps) {
  const [copied, setCopied] = useState(false)

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(code)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (err) {
      console.error("Failed to copy code:", err)
    }
  }

  // When Prism.js is installed, uncomment this section:
  // const highlighted = Prism.languages[language]
  //   ? Prism.highlight(code, Prism.languages[language], language)
  //   : code

  const lines = code.split("\n")

  return (
    <div
      className={`relative rounded-lg border border-gray-200 dark:border-gray-700 bg-gray-900 overflow-hidden ${className}`}
    >
      {/* Header with language label and copy button */}
      <div className="flex items-center justify-between px-4 py-2 bg-gray-800 border-b border-gray-700">
        <span className="text-xs text-gray-400 font-mono uppercase">
          {language}
        </span>
        <Button
          size="sm"
          variant="ghost"
          onClick={handleCopy}
          className="text-gray-400 hover:text-white h-7 gap-1.5"
          aria-label={copied ? "Code copied" : "Copy code to clipboard"}
        >
          {copied ? (
            <>
              <Check className="size-3.5" />
              <span className="text-xs">Copied</span>
            </>
          ) : (
            <>
              <Copy className="size-3.5" />
              <span className="text-xs">Copy</span>
            </>
          )}
        </Button>
      </div>

      {/* Code content */}
      <div className="overflow-auto" style={{ maxHeight }}>
        <pre className="p-4 text-sm font-mono leading-relaxed">
          {showLineNumbers ? (
            <code className="block">
              {lines.map((line, index) => (
                <div key={index} className="table-row">
                  <span className="table-cell pr-4 text-gray-500 select-none text-right">
                    {index + 1}
                  </span>
                  <span className="table-cell text-gray-100">{line}</span>
                </div>
              ))}
            </code>
          ) : (
            <code className="text-gray-100">{code}</code>
          )}
        </pre>
      </div>
    </div>
  )
}
