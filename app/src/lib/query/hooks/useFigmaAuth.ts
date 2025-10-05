/**
 * TanStack Query hook for Figma PAT authentication.
 */

import { useMutation } from '@tanstack/react-query';
import { authenticateFigma } from '@/lib/api/figma.api';
import { FigmaAuthResponse } from '@/types';

export function useFigmaAuth() {
  return useMutation<FigmaAuthResponse, Error, string>({
    mutationFn: authenticateFigma,
    onSuccess: (data) => {
      if (data.valid) {
        console.log('[useFigmaAuth] Authentication successful:', data.user_email);
      } else {
        console.warn('[useFigmaAuth] Authentication failed:', data.message);
      }
    },
    onError: (error) => {
      console.error('[useFigmaAuth] Error:', error.message);
    },
  });
}
