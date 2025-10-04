"use client";

import * as React from "react";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue
} from "@/components/ui/select";
import { ConfidenceBadge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

// Standard font families (web-safe + popular)
const FONT_FAMILIES = [
  "Inter",
  "Roboto",
  "Open Sans",
  "Lato",
  "Montserrat",
  "Poppins",
  "Arial",
  "Helvetica",
  "Georgia",
  "Times New Roman",
  "Courier New",
  "Verdana"
] as const;

// Standard font sizes
const FONT_SIZES = [12, 14, 16, 18, 20, 24, 32, 40, 48, 56, 64] as const;

// Standard font weights
const FONT_WEIGHTS = [100, 200, 300, 400, 500, 600, 700, 800, 900] as const;

export interface TypographyEditorProps {
  /**
   * Current font family value
   */
  fontFamily?: string;

  /**
   * Font family confidence score
   */
  fontFamilyConfidence?: number;

  /**
   * Current font size value (with unit, e.g., "16px")
   */
  fontSize?: string;

  /**
   * Font size confidence score
   */
  fontSizeConfidence?: number;

  /**
   * Current font weight value
   */
  fontWeight?: string;

  /**
   * Font weight confidence score
   */
  fontWeightConfidence?: number;

  /**
   * Callback when font family changes
   */
  onFontFamilyChange?: (value: string) => void;

  /**
   * Callback when font size changes
   */
  onFontSizeChange?: (value: string) => void;

  /**
   * Callback when font weight changes
   */
  onFontWeightChange?: (value: string) => void;

  /**
   * Optional className
   */
  className?: string;
}

/**
 * TypographyEditor - Component for editing typography tokens
 *
 * @example
 * ```tsx
 * <TypographyEditor
 *   fontFamily="Inter"
 *   fontFamilyConfidence={0.75}
 *   fontSize="16px"
 *   fontSizeConfidence={0.90}
 *   fontWeight="500"
 *   fontWeightConfidence={0.85}
 * />
 * ```
 */
export function TypographyEditor({
  fontFamily = "Inter",
  fontFamilyConfidence = 1,
  fontSize = "16px",
  fontSizeConfidence = 1,
  fontWeight = "400",
  fontWeightConfidence = 1,
  onFontFamilyChange,
  onFontSizeChange,
  onFontWeightChange,
  className
}: TypographyEditorProps) {
  // Parse font size value (remove "px" if present)
  const parsedFontSize = parseInt(fontSize.replace("px", ""));
  const [customFontFamily, setCustomFontFamily] = React.useState("");
  const [showCustomFont, setShowCustomFont] = React.useState(
    !FONT_FAMILIES.includes(fontFamily as string)
  );

  return (
    <div className={cn("space-y-4", className)} data-testid="typography-editor">
      {/* Font Family */}
      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <Label htmlFor="font-family" className="text-sm font-medium">
            Font Family
          </Label>
          <ConfidenceBadge score={fontFamilyConfidence} />
        </div>

        {showCustomFont ? (
          <div className="space-y-2">
            <Input
              id="font-family"
              type="text"
              value={customFontFamily || fontFamily}
              onChange={(e) => {
                setCustomFontFamily(e.target.value);
                if (onFontFamilyChange) {
                  onFontFamilyChange(e.target.value);
                }
              }}
              placeholder="Enter custom font family"
            />
            <button
              type="button"
              onClick={() => setShowCustomFont(false)}
              className="text-sm text-blue-600 hover:text-blue-700"
              aria-label="Switch to font family presets"
            >
              Choose from presets
            </button>
          </div>
        ) : (
          <div className="space-y-2">
            <Select
              value={fontFamily}
              onValueChange={(value) => {
                if (value === "custom") {
                  setShowCustomFont(true);
                } else if (onFontFamilyChange) {
                  onFontFamilyChange(value);
                }
              }}
            >
              <SelectTrigger id="font-family">
                <SelectValue placeholder="Select font family" />
              </SelectTrigger>
              <SelectContent>
                {FONT_FAMILIES.map((font) => (
                  <SelectItem key={font} value={font}>
                    {font}
                  </SelectItem>
                ))}
                <SelectItem value="custom">Custom...</SelectItem>
              </SelectContent>
            </Select>
          </div>
        )}
      </div>

      {/* Font Size */}
      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <Label htmlFor="font-size" className="text-sm font-medium">
            Font Size
          </Label>
          <ConfidenceBadge score={fontSizeConfidence} />
        </div>

        <Select
          value={parsedFontSize.toString()}
          onValueChange={(value) => {
            if (onFontSizeChange) {
              onFontSizeChange(`${value}px`);
            }
          }}
        >
          <SelectTrigger id="font-size">
            <SelectValue placeholder="Select font size" />
          </SelectTrigger>
          <SelectContent>
            {FONT_SIZES.map((size) => (
              <SelectItem key={size} value={size.toString()}>
                {size}px
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      {/* Font Weight */}
      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <Label htmlFor="font-weight" className="text-sm font-medium">
            Font Weight
          </Label>
          <ConfidenceBadge score={fontWeightConfidence} />
        </div>

        <Select
          value={fontWeight}
          onValueChange={(value) => {
            if (onFontWeightChange) {
              onFontWeightChange(value);
            }
          }}
        >
          <SelectTrigger id="font-weight">
            <SelectValue placeholder="Select font weight" />
          </SelectTrigger>
          <SelectContent>
            {FONT_WEIGHTS.map((weight) => (
              <SelectItem key={weight} value={weight.toString()}>
                {weight} -{" "}
                {weight === 100
                  ? "Thin"
                  : weight === 200
                  ? "Extra Light"
                  : weight === 300
                  ? "Light"
                  : weight === 400
                  ? "Regular"
                  : weight === 500
                  ? "Medium"
                  : weight === 600
                  ? "Semi Bold"
                  : weight === 700
                  ? "Bold"
                  : weight === 800
                  ? "Extra Bold"
                  : "Black"}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>
    </div>
  );
}
