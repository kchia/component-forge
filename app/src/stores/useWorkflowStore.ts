/**
 * Zustand store for workflow progress tracking.
 * Manages multi-step workflow state.
 */

import { create } from 'zustand';
import { WorkflowStep } from '@/types';
import type { RequirementProposal, ComponentType } from '@/types/requirement.types';

interface WorkflowStore {
  // State
  currentStep: WorkflowStep;
  completedSteps: WorkflowStep[];
  progress: number; // 0-100
  
  // Requirements state
  componentType?: ComponentType;
  componentConfidence?: number;
  proposals: {
    props: RequirementProposal[];
    events: RequirementProposal[];
    states: RequirementProposal[];
    accessibility: RequirementProposal[];
  };
  
  // Actions
  setStep: (step: WorkflowStep) => void;
  completeStep: (step: WorkflowStep) => void;
  updateProgress: (progress: number) => void;
  setRequirements: (
    componentType: ComponentType,
    componentConfidence: number,
    proposals: {
      props: RequirementProposal[];
      events: RequirementProposal[];
      states: RequirementProposal[];
      accessibility: RequirementProposal[];
    }
  ) => void;
  updateProposal: (id: string, updates: Partial<RequirementProposal>) => void;
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
  proposals: {
    props: [],
    events: [],
    states: [],
    accessibility: [],
  },
  
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
  
  setRequirements: (componentType, componentConfidence, proposals) =>
    set({
      componentType,
      componentConfidence,
      proposals,
    }),
  
  updateProposal: (id, updates) =>
    set((state) => {
      // Find and update the proposal in the correct category
      const updateCategory = (proposals: RequirementProposal[]) =>
        proposals.map((p) => (p.id === id ? { ...p, ...updates } : p));
      
      return {
        proposals: {
          props: updateCategory(state.proposals.props),
          events: updateCategory(state.proposals.events),
          states: updateCategory(state.proposals.states),
          accessibility: updateCategory(state.proposals.accessibility),
        },
      };
    }),
  
  resetWorkflow: () =>
    set({
      currentStep: WorkflowStep.DASHBOARD,
      completedSteps: [],
      progress: 0,
      componentType: undefined,
      componentConfidence: undefined,
      proposals: {
        props: [],
        events: [],
        states: [],
        accessibility: [],
      },
    }),
}));
