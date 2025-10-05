"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useWorkflowStore } from "@/stores/useWorkflowStore";
import { useTokenStore } from "@/stores/useTokenStore";
import { useRequirementProposal } from "@/lib/query/hooks/useRequirementProposal";
import { ApprovalPanelContainer } from "@/components/requirements/ApprovalPanelContainer";
import { Alert } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { ArrowRight } from "lucide-react";

export default function RequirementsPage() {
  const router = useRouter();
  const uploadedFile = useWorkflowStore((state) => state.uploadedFile);
  const tokens = useTokenStore((state) => state.tokens);
  const componentType = useWorkflowStore((state) => state.componentType);

  const { mutate: proposeRequirements, isPending, error } = useRequirementProposal();

  // Auto-trigger requirement proposal on mount if file exists
  useEffect(() => {
    if (uploadedFile && !componentType) {
      proposeRequirements({
        file: uploadedFile,
        tokens: tokens || undefined,
      });
    }
  }, [uploadedFile, componentType, tokens, proposeRequirements]);

  // If no file, redirect to extract
  if (!uploadedFile) {
    return (
      <main className="container mx-auto p-8">
        <Alert variant="warning">
          <p className="font-medium mb-2">No screenshot found</p>
          <p className="text-sm mb-4">Please upload a screenshot first to generate requirements.</p>
          <Button asChild variant="outline" className="mt-2">
            <Link href="/extract">← Back to Extraction</Link>
          </Button>
        </Alert>
      </main>
    );
  }

  return (
    <main className="container mx-auto p-4 sm:p-8 space-y-6">
      {/* Page Header */}
      <div className="space-y-2">
        <h1 className="text-3xl font-bold tracking-tight">
          Review Requirements
        </h1>
        <p className="text-muted-foreground">
          AI-generated component requirements based on your screenshot
        </p>
      </div>

      {/* Loading State */}
      {isPending && (
        <div className="space-y-4">
          <Alert variant="info">
            <p className="font-medium">🤖 Analyzing your component...</p>
            <p className="text-sm mt-1">This typically takes 10-15 seconds.</p>
          </Alert>
          <Progress value={66} className="h-2" />
        </div>
      )}

      {/* Error State */}
      {error && (
        <Alert variant="error">
          <p className="font-medium">Analysis Failed</p>
          <p className="text-sm mt-1">{error.message}</p>
          <Button 
            variant="outline" 
            className="mt-4"
            onClick={() => {
              if (uploadedFile) {
                proposeRequirements({
                  file: uploadedFile,
                  tokens: tokens || undefined,
                });
              }
            }}
          >
            Try Again
          </Button>
        </Alert>
      )}

      {/* Approval Panel (shown after analysis completes) */}
      {componentType && !isPending && (
        <>
          <ApprovalPanelContainer />

          {/* Navigation */}
          <div className="flex justify-between">
            <Button asChild variant="outline">
              <Link href="/extract">← Back to Extraction</Link>
            </Button>
            <Button asChild size="lg">
              <Link href="/patterns">
                Continue to Patterns
                <ArrowRight className="ml-2 h-4 w-4" />
              </Link>
            </Button>
          </div>
        </>
      )}
    </main>
  );
}
