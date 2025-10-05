/**
 * TypeScript interfaces matching backend Pydantic models
 * for API request/response contracts.
 */

// Image metadata returned from backend
export interface ImageMetadata {
  width: number;
  height: number;
  format: string;
  mode: string;
  size_bytes: number;
}

// Design tokens structure matching backend DesignTokens model
export interface DesignTokens {
  colors: Record<string, string>;
  typography: Record<string, any>;
  spacing: Record<string, any>;
}

// Token extraction response from POST /tokens/extract/screenshot
export interface TokenExtractionResponse {
  tokens: DesignTokens;
  metadata: {
    filename: string;
    image: ImageMetadata;
    extraction_method: string;
  };
  confidence?: Record<string, number>;
  fallbacks_used?: string[];
  review_needed?: string[];
}

// Figma authentication request for POST /tokens/figma/auth
export interface FigmaAuthRequest {
  personal_access_token: string;
}

// Figma authentication response
export interface FigmaAuthResponse {
  valid: boolean;
  user_email?: string;
  message: string;
}

// Figma extraction request for POST /extract/figma
export interface FigmaExtractRequest {
  figma_url: string;
  personal_access_token?: string;
}

// Figma extraction response
export interface FigmaExtractResponse {
  file_key: string;
  file_name: string;
  tokens: DesignTokens;
  cached: boolean;
}

// Error response structure from FastAPI
export interface APIErrorResponse {
  detail: string | Record<string, any>;
}
