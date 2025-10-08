/**
 * Epic 5: Extended Quality Validation & Accessibility Testing
 * Validation service exports
 */

// Export all types
export type {
  ValidationResult,
  A11yViolation,
  KeyboardIssue,
  FocusIssue,
  ContrastViolation,
  TokenViolation,
  AutoFixResult,
  ValidationReport,
} from './types';

// Export WCAG utilities
export {
  parseColor,
  getRelativeLuminance,
  getContrastRatio,
  calculateContrastRatio,
  meetsWCAGAA,
  meetsWCAGAAA,
  calculateDeltaE,
  calculateDeltaEFromStrings,
  formatContrastRatio,
  rgbToHex,
  lightenColor,
  darkenColor,
  suggestAccessibleColors,
} from './utils';

export type { RGBColor } from './utils';

// Export validators (Tasks F2-F6)
export { A11yValidator } from './a11y-validator';
export { KeyboardValidator } from './keyboard-validator';
export { FocusValidator } from './focus-validator';
export { ContrastValidator } from './contrast-validator';
export { TokenValidator } from './token-validator';
