/**
 * API client for Pattern Retrieval endpoints (Epic 3)
 */

import { apiClient } from './client';
import type { RetrievalRequest, RetrievalResponse } from '@/types/retrieval';

export const retrievalApi = {
  /**
   * Search for patterns based on requirements
   * POST /api/v1/retrieval/search
   */
  async search(request: RetrievalRequest): Promise<RetrievalResponse> {
    const response = await apiClient.post<RetrievalResponse>(
      '/retrieval/search',
      request
    );
    return response.data;
  },
};
