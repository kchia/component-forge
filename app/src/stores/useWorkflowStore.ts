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

  // Screenshot file state
  uploadedFile: File | null;

  // Requirements state
  componentType?: ComponentType;
  componentConfidence?: number;
  proposals: {
    props: RequirementProposal[];
    events: RequirementProposal[];
    states: RequirementProposal[];
    accessibility: RequirementProposal[];
  };

  // Export state
  exportId?: string;
  exportedAt?: string;

  // Actions
  setStep: (step: WorkflowStep) => void;
  completeStep: (step: WorkflowStep) => void;
  updateProgress: (progress: number) => void;
  setUploadedFile: (file: File) => void;
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
  removeProposal: (id: string) => void;
  addProposal: (proposal: RequirementProposal) => void;
  acceptAllProposals: () => void;
  setExportInfo: (exportId: string, exportedAt: string) => void;
  getApprovedProposals: () => {
    props: RequirementProposal[];
    events: RequirementProposal[];
    states: RequirementProposal[];
    accessibility: RequirementProposal[];
  };
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
  uploadedFile: null,
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
  
  setUploadedFile: (file) =>
    set({
      uploadedFile: file,
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

  removeProposal: (id) =>
    set((state) => {
      // Remove the proposal from the correct category
      const removeFromCategory = (proposals: RequirementProposal[]) =>
        proposals.filter((p) => p.id !== id);

      return {
        proposals: {
          props: removeFromCategory(state.proposals.props),
          events: removeFromCategory(state.proposals.events),
          states: removeFromCategory(state.proposals.states),
          accessibility: removeFromCategory(state.proposals.accessibility),
        },
      };
    }),

  addProposal: (proposal) =>
    set((state) => {
      // Add the proposal to the correct category
      const category = proposal.category;
      return {
        proposals: {
          ...state.proposals,
          [category]: [...state.proposals[category], proposal],
        },
      };
    }),

  acceptAllProposals: () =>
    set((state) => {
      // Mark all proposals as approved
      const acceptCategory = (proposals: RequirementProposal[]) =>
        proposals.map((p) => ({ ...p, approved: true }));

      return {
        proposals: {
          props: acceptCategory(state.proposals.props),
          events: acceptCategory(state.proposals.events),
          states: acceptCategory(state.proposals.states),
          accessibility: acceptCategory(state.proposals.accessibility),
        },
      };
    }),

  setExportInfo: (exportId, exportedAt) =>
    set({
      exportId,
      exportedAt,
    }),

  getApprovedProposals: () => {
    const state = useWorkflowStore.getState();
    const filterApproved = (proposals: RequirementProposal[]) =>
      proposals.filter((p) => p.approved);

    return {
      props: filterApproved(state.proposals.props),
      events: filterApproved(state.proposals.events),
      states: filterApproved(state.proposals.states),
      accessibility: filterApproved(state.proposals.accessibility),
    };
  },

  resetWorkflow: () =>
    set({
      currentStep: WorkflowStep.DASHBOARD,
      completedSteps: [],
      progress: 0,
      uploadedFile: null,
      componentType: undefined,
      componentConfidence: undefined,
      proposals: {
        props: [],
        events: [],
        states: [],
        accessibility: [],
      },
      exportId: undefined,
      exportedAt: undefined,
    }),
}));
