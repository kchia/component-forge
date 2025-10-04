"use client"

import * as React from "react"
import { Card, CardContent, CardHeader } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { ColorPicker } from "./ColorPicker"
import { TypographyEditor } from "./TypographyEditor"
import { SpacingEditor } from "./SpacingEditor"
import { cn } from "@/lib/utils"

export interface TokenData {
  colors?: {
    [key: string]: { value: string; confidence: number }
  }
  typography?: {
    fontFamily?: { value: string; confidence: number }
    fontSize?: { value: string; confidence: number }
    fontWeight?: { value: string; confidence: number }
  }
  spacing?: {
    [key: string]: { value: string; confidence: number }
  }
}

export interface TokenEditorProps {
  /**
   * Token data to edit
   */
  tokens: TokenData
  
  /**
   * Callback when tokens are saved
   */
  onSave?: (tokens: TokenData) => void
  
  /**
   * Callback when reset is requested
   */
  onReset?: () => void
  
  /**
   * Whether the editor is in a loading state
   */
  loading?: boolean
  
  /**
   * Optional className
   */
  className?: string
}

/**
 * TokenEditor - Main container for editing all design tokens
 * 
 * Composes ColorPicker, TypographyEditor, and SpacingEditor components.
 * 
 * @example
 * ```tsx
 * <TokenEditor
 *   tokens={{
 *     colors: {
 *       primary: { value: "#3B82F6", confidence: 0.92 },
 *       background: { value: "#FFFFFF", confidence: 0.88 }
 *     },
 *     typography: {
 *       fontFamily: { value: "Inter", confidence: 0.75 },
 *       fontSize: { value: "16px", confidence: 0.90 }
 *     },
 *     spacing: {
 *       padding: { value: "16px", confidence: 0.85 }
 *     }
 *   }}
 *   onSave={(tokens) => console.log('Saved:', tokens)}
 *   onReset={() => console.log('Reset clicked')}
 * />
 * ```
 */
export function TokenEditor({
  tokens,
  onSave,
  onReset,
  loading = false,
  className,
}: TokenEditorProps) {
  const [editedTokens, setEditedTokens] = React.useState<TokenData>(tokens)
  const [hasChanges, setHasChanges] = React.useState(false)

  // Sync with external tokens changes
  React.useEffect(() => {
    setEditedTokens(tokens)
    setHasChanges(false)
  }, [tokens])

  const handleColorChange = (key: string, value: string) => {
    setEditedTokens((prev) => ({
      ...prev,
      colors: {
        ...prev.colors,
        [key]: {
          value,
          confidence: prev.colors?.[key]?.confidence || 0,
        },
      },
    }))
    setHasChanges(true)
  }

  const handleTypographyChange = (field: 'fontFamily' | 'fontSize' | 'fontWeight', value: string) => {
    setEditedTokens((prev) => ({
      ...prev,
      typography: {
        ...prev.typography,
        [field]: {
          value,
          confidence: prev.typography?.[field]?.confidence || 0,
        },
      },
    }))
    setHasChanges(true)
  }

  const handleSpacingChange = (key: string, value: string) => {
    setEditedTokens((prev) => ({
      ...prev,
      spacing: {
        ...prev.spacing,
        [key]: {
          value,
          confidence: prev.spacing?.[key]?.confidence || 0,
        },
      },
    }))
    setHasChanges(true)
  }

  const handleSave = () => {
    if (onSave) {
      onSave(editedTokens)
    }
    setHasChanges(false)
  }

  const handleReset = () => {
    setEditedTokens(tokens)
    setHasChanges(false)
    if (onReset) {
      onReset()
    }
  }

  return (
    <div className={cn("space-y-6", className)} data-testid="token-editor">
      {/* Colors Section */}
      {editedTokens.colors && Object.keys(editedTokens.colors).length > 0 && (
        <Card variant="outlined">
          <CardHeader>
            <h3 className="text-lg font-semibold">
              Colors ({Object.keys(editedTokens.colors).length})
            </h3>
          </CardHeader>
          <CardContent className="space-y-4">
            {Object.entries(editedTokens.colors).map(([key, data]) => (
              <ColorPicker
                key={key}
                label={key.charAt(0).toUpperCase() + key.slice(1)}
                value={data.value}
                confidence={data.confidence}
                onChange={(value) => handleColorChange(key, value)}
              />
            ))}
          </CardContent>
        </Card>
      )}

      {/* Typography Section */}
      {editedTokens.typography && (
        <Card variant="outlined">
          <CardHeader>
            <h3 className="text-lg font-semibold">Typography</h3>
          </CardHeader>
          <CardContent>
            <TypographyEditor
              fontFamily={editedTokens.typography.fontFamily?.value}
              fontFamilyConfidence={editedTokens.typography.fontFamily?.confidence}
              fontSize={editedTokens.typography.fontSize?.value}
              fontSizeConfidence={editedTokens.typography.fontSize?.confidence}
              fontWeight={editedTokens.typography.fontWeight?.value}
              fontWeightConfidence={editedTokens.typography.fontWeight?.confidence}
              onFontFamilyChange={(value) => handleTypographyChange('fontFamily', value)}
              onFontSizeChange={(value) => handleTypographyChange('fontSize', value)}
              onFontWeightChange={(value) => handleTypographyChange('fontWeight', value)}
            />
          </CardContent>
        </Card>
      )}

      {/* Spacing Section */}
      {editedTokens.spacing && Object.keys(editedTokens.spacing).length > 0 && (
        <Card variant="outlined">
          <CardHeader>
            <h3 className="text-lg font-semibold">
              Spacing ({Object.keys(editedTokens.spacing).length})
            </h3>
          </CardHeader>
          <CardContent className="space-y-4">
            {Object.entries(editedTokens.spacing).map(([key, data]) => (
              <SpacingEditor
                key={key}
                label={key.charAt(0).toUpperCase() + key.slice(1)}
                value={data.value}
                confidence={data.confidence}
                onChange={(value) => handleSpacingChange(key, value)}
              />
            ))}
          </CardContent>
        </Card>
      )}

      {/* Action Buttons */}
      <div className="flex gap-3 justify-end">
        <Button
          variant="secondary"
          onClick={handleReset}
          disabled={!hasChanges || loading}
        >
          Reset
        </Button>
        <Button
          onClick={handleSave}
          disabled={!hasChanges || loading}
          aria-label="Save changes"
        >
          {loading ? "Saving..." : "Save Changes"}
        </Button>
      </div>
    </div>
  )
}
