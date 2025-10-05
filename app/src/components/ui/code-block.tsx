"use client"

import { useState, useEffect } from "react"
import { Button } from "./button"
import { Copy, Check } from "lucide-react"
import "prismjs/themes/prism-tomorrow.css"

// Dynamically import Prism to avoid SSR issues
let Prism: any = null
let languagesLoaded = false

async function loadPrism() {
  if (typeof window === "undefined") return null
  if (Prism && languagesLoaded) return Prism

  try {
    Prism = (await import("prismjs")).default
    // Load languages in correct dependency order
    await import("prismjs/components/prism-javascript")
    await import("prismjs/components/prism-typescript")
    await import("prismjs/components/prism-json")
    await import("prismjs/components/prism-css")
    // TSX extends TypeScript, load it last
    await import("prismjs/components/prism-tsx")
    languagesLoaded = true
    return Prism
  } catch (error) {
    console.error("Failed to load Prism:", error)
    return null
  }
}

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
  const [highlightedCode, setHighlightedCode] = useState(code)

  useEffect(() => {
    // Load Prism and highlight code
    async function highlight() {
      try {
        const prism = await loadPrism()
        if (prism && prism.languages && prism.languages[language]) {
          const highlighted = prism.highlight(code, prism.languages[language], language)
          setHighlightedCode(highlighted)
        } else {
          // Fallback to plain text if Prism or language not available
          setHighlightedCode(code)
        }
      } catch (error) {
        // If highlighting fails, just show plain code
        console.warn(`Prism highlighting failed for language '${language}':`, error)
        setHighlightedCode(code)
      }
    }

    highlight()
  }, [code, language])

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(code)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (err) {
      console.error("Failed to copy code:", err)
    }
  }

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
        <pre className="p-4 text-sm font-mono leading-relaxed text-gray-100">
          {showLineNumbers ? (
            <code className="block">
              {lines.map((line, index) => {
                const lineNumber = index + 1
                const highlightedLines = highlightedCode.split("\n")
                const highlightedLine = highlightedLines[index] || line

                return (
                  <div key={index} className="table-row">
                    <span className="table-cell pr-4 text-gray-500 select-none text-right">
                      {lineNumber}
                    </span>
                    <span
                      className="table-cell text-gray-100"
                      dangerouslySetInnerHTML={{ __html: highlightedLine }}
                    />
                  </div>
                )
              })}
            </code>
          ) : (
            <code className="text-gray-100" dangerouslySetInnerHTML={{ __html: highlightedCode }} />
          )}
        </pre>
      </div>
    </div>
  )
}
