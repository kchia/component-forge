/**
 * Zustand store for workflow progress tracking.
 * Manages multi-step workflow state.
 */

import { create } from 'zustand';
import { WorkflowStep } from '@/types';

interface WorkflowStore {
  // State
  currentStep: WorkflowStep;
  completedSteps: WorkflowStep[];
  progress: number; // 0-100
  
  // Actions
  setStep: (step: WorkflowStep) => void;
  completeStep: (step: WorkflowStep) => void;
  updateProgress: (progress: number) => void;
  resetWorkflow: () => void;
}

// Calculate progress percentage based on completed steps
function calculateProgress(completedSteps: WorkflowStep[]): number {
  const totalSteps = 5; // Dashboard, Extract, Requirements, Patterns, Preview
  const completed = completedSteps.length;
  return Math.round((completed / totalSteps) * 100);
}

export const useWorkflowStore = create<WorkflowStore>((set) => ({
  // Initial state
  currentStep: WorkflowStep.DASHBOARD,
  completedSteps: [],
  progress: 0,
  
  // Actions
  setStep: (step) =>
    set({
      currentStep: step,
    }),
  
  completeStep: (step) =>
    set((state) => {
      const completedSteps = state.completedSteps.includes(step)
        ? state.completedSteps
        : [...state.completedSteps, step];
      
      return {
        completedSteps,
        progress: calculateProgress(completedSteps),
      };
    }),
  
  updateProgress: (progress) =>
    set({
      progress: Math.min(Math.max(progress, 0), 100), // Clamp 0-100
    }),
  
  resetWorkflow: () =>
    set({
      currentStep: WorkflowStep.DASHBOARD,
      completedSteps: [],
      progress: 0,
    }),
}));
