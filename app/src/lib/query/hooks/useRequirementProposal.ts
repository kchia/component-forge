/**
 * TanStack Query hook for requirement proposal from screenshots/Figma.
 */

import { useMutation } from '@tanstack/react-query';
import {
  proposeRequirements,
  RequirementProposalRequest,
  RequirementProposalResponse,
} from '@/lib/api/requirements.api';
import { useWorkflowStore } from '@/stores/useWorkflowStore';

/**
 * Hook for proposing requirements from uploaded image.
 * 
 * Calls POST /requirements/propose with file and optional tokens/Figma data.
 * Updates useWorkflowStore with component type and proposals on success.
 * 
 * Usage:
 * ```tsx
 * const { mutate, isPending, error } = useRequirementProposal();
 * 
 * mutate({
 *   file: imageFile,
 *   tokens: extractedTokens, // optional
 *   figmaData: figmaMetadata, // optional
 * });
 * ```
 * 
 * @returns TanStack Query mutation for requirement proposal
 */
export function useRequirementProposal() {
  const setRequirements = useWorkflowStore((state) => state.setRequirements);
  
  return useMutation<
    RequirementProposalResponse,
    Error,
    RequirementProposalRequest
  >({
    mutationFn: proposeRequirements,
    onSuccess: (data) => {
      // Update Zustand store with component type and proposals
      setRequirements(
        data.componentType,
        data.componentConfidence,
        data.proposals
      );
      
      // Log metadata in development
      if (process.env.NODE_ENV === 'development') {
        console.log('[useRequirementProposal] Success:', {
          componentType: data.componentType,
          confidence: data.componentConfidence,
          totalProposals: data.metadata.totalProposals,
          latency: `${data.metadata.latencySeconds}s`,
          meetsTarget: data.metadata.meetsLatencyTarget,
        });
      }
    },
    onError: (error) => {
      console.error('[useRequirementProposal] Error:', error.message);
    },
  });
}
