/**
 * Requirement proposal API endpoints.
 */

import { apiClient, createLongTimeoutClient } from './client';
import {
  RequirementProposal,
  ComponentType,
  ComponentClassification,
} from '@/types/requirement.types';

/**
 * Requirement proposal request parameters.
 */
export interface RequirementProposalRequest {
  file: File;
  tokens?: Record<string, unknown>;
  figmaData?: Record<string, unknown>;
}

/**
 * Requirement proposal API response.
 */
export interface RequirementProposalResponse {
  componentType: ComponentType;
  componentConfidence: number;
  proposals: {
    props: RequirementProposal[];
    events: RequirementProposal[];
    states: RequirementProposal[];
    accessibility: RequirementProposal[];
  };
  metadata: {
    latencySeconds: number;
    timestamp: string;
    source: 'screenshot' | 'figma';
    totalProposals: number;
    targetLatencyP50: number;
    meetsLatencyTarget: boolean;
  };
}

/**
 * Propose functional requirements from screenshot/Figma frame.
 * 
 * Analyzes uploaded image to propose:
 * - Props (variant, size, disabled, etc.)
 * - Events (onClick, onChange, onHover, etc.)
 * - States (hover, focus, disabled, loading, etc.)
 * - Accessibility (aria-label, semantic HTML, keyboard nav, etc.)
 * 
 * Each proposal includes confidence score and rationale.
 * Target latency: p50 ≤15s
 * 
 * @param request - File and optional tokens/Figma data
 * @returns Promise with component type, proposals by category, metadata
 */
export async function proposeRequirements(
  request: RequirementProposalRequest
): Promise<RequirementProposalResponse> {
  try {
    // Create FormData for file upload
    const formData = new FormData();
    formData.append('file', request.file);
    
    // Add optional data as JSON if provided
    if (request.tokens) {
      formData.append('tokens', JSON.stringify(request.tokens));
    }
    if (request.figmaData) {
      formData.append('figma_data', JSON.stringify(request.figmaData));
    }

    // Use long timeout client for AI processing (up to 60s)
    const client = createLongTimeoutClient();
    
    const response = await client.post<RequirementProposalResponse>(
      '/requirements/propose',
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );

    return response.data;
  } catch (error) {
    // Error already transformed by interceptor
    throw error;
  }
}

/**
 * Get health status of requirements service.
 * 
 * @returns Service health status
 */
export async function getRequirementsHealth(): Promise<{
  status: string;
  service: string;
  version: string;
}> {
  try {
    const response = await apiClient.get('/requirements/health');
    return response.data;
  } catch (error) {
    throw error;
  }
}
