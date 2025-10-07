/**
 * TypeScript interfaces for code generation API contracts.
 * 
 * Epic 4: Code Generation & Adaptation
 * These types match the backend generation API endpoints.
 */

import { DesignTokens } from './api.types';
import { RequirementProposal } from './requirement.types';

// Generation pipeline stages
export enum GenerationStage {
  PARSING = 'parsing',
  INJECTING = 'injecting',
  GENERATING = 'generating',
  ASSEMBLING = 'assembling',
  FORMATTING = 'formatting',
  COMPLETE = 'complete',
}

// Generation status
export enum GenerationStatus {
  PENDING = 'pending',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed',
  FAILED = 'failed',
}

// Generation request payload for POST /api/v1/generation/generate
export interface GenerationRequest {
  pattern_id: string;
  tokens: DesignTokens;
  requirements: RequirementProposal[];
}

// Code output from generation
export interface GeneratedCode {
  component: string;        // Component.tsx content
  stories: string;         // Component.stories.tsx content
  tokens_json?: string;    // tokens.json content (optional)
  requirements_json?: string; // requirements.json content (optional)
}

// Generation metadata and metrics
export interface GenerationMetadata {
  pattern_used: string;
  pattern_version: string;
  tokens_applied: number;
  requirements_implemented: number;
  lines_of_code: number;
  imports_count: number;
  has_typescript_errors: boolean;
  has_accessibility_warnings: boolean;
}

// Generation timing breakdown
export interface GenerationTiming {
  total_ms: number;
  parsing_ms: number;
  injection_ms: number;
  generation_ms: number;
  assembly_ms: number;
  formatting_ms: number;
}

// Provenance information
export interface ProvenanceInfo {
  pattern_id: string;
  pattern_version: string;
  generated_at: string;      // ISO 8601 timestamp
  tokens_hash: string;       // SHA-256 hash for change detection
  requirements_hash: string; // SHA-256 hash for change detection
}

// Generation response from POST /api/v1/generation/generate
export interface GenerationResponse {
  code: GeneratedCode;
  metadata: GenerationMetadata;
  timing: GenerationTiming;
  provenance: ProvenanceInfo;
  status: GenerationStatus;
  error?: string;
}

// Generation progress update (for real-time tracking)
export interface GenerationProgress {
  stage: GenerationStage;
  status: GenerationStatus;
  message: string;
  elapsed_ms: number;
  progress_percentage: number; // 0-100
}

// Generation error details
export interface GenerationError {
  stage: GenerationStage;
  error_type: string;
  message: string;
  details?: Record<string, any>;
  recoverable: boolean;
}

// Quality validation results (preview of Epic 5)
export interface QualityMetrics {
  accessibility_score: number;    // 0-100
  type_safety_score: number;      // 0-100
  token_adherence_score: number;  // 0-100
  pattern_match_score: number;    // 0-100
  warnings: string[];
  errors: string[];
}

/**
 * Helper function to get stage display name.
 * 
 * @param stage - Generation stage enum
 * @returns Human-readable stage name
 */
export function getStageDisplayName(stage: GenerationStage): string {
  const displayNames: Record<GenerationStage, string> = {
    [GenerationStage.PARSING]: 'Parsing Pattern',
    [GenerationStage.INJECTING]: 'Injecting Tokens',
    [GenerationStage.GENERATING]: 'Generating Code',
    [GenerationStage.ASSEMBLING]: 'Assembling Components',
    [GenerationStage.FORMATTING]: 'Formatting Code',
    [GenerationStage.COMPLETE]: 'Complete',
  };
  return displayNames[stage];
}

/**
 * Helper function to get stage progress percentage.
 * 
 * @param stage - Generation stage enum
 * @returns Progress percentage (0-100)
 */
export function getStageProgress(stage: GenerationStage): number {
  const progressMap: Record<GenerationStage, number> = {
    [GenerationStage.PARSING]: 20,
    [GenerationStage.INJECTING]: 40,
    [GenerationStage.GENERATING]: 60,
    [GenerationStage.ASSEMBLING]: 80,
    [GenerationStage.FORMATTING]: 90,
    [GenerationStage.COMPLETE]: 100,
  };
  return progressMap[stage];
}

/**
 * Helper function to check if generation is complete.
 * 
 * @param status - Generation status enum
 * @returns True if generation is in a terminal state
 */
export function isGenerationComplete(status: GenerationStatus): boolean {
  return status === GenerationStatus.COMPLETED || status === GenerationStatus.FAILED;
}

/**
 * Helper function to format timing in human-readable format.
 * 
 * @param ms - Milliseconds
 * @returns Formatted time string (e.g., "1.5s", "250ms")
 */
export function formatTiming(ms: number): string {
  if (ms >= 1000) {
    return `${(ms / 1000).toFixed(1)}s`;
  }
  return `${Math.round(ms)}ms`;
}
