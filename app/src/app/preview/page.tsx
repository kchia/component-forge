"use client";

import { useEffect, useState, useMemo } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { MetricCard } from "@/components/composite/MetricCard";
import { DynamicCodeBlock } from "@/components/ui/DynamicCodeBlock";
import { WorkflowBreadcrumb } from "@/components/composite/WorkflowBreadcrumb";
import { GenerationProgress } from "@/components/composite/GenerationProgress";
import { useWorkflowStore } from "@/stores/useWorkflowStore";
import { useTokenStore } from "@/stores/useTokenStore";
import { useGenerateComponent, useGenerationStatus } from "@/hooks/useGenerateComponent";
import { downloadGeneratedCode } from "@/lib/api";
import { 
  WorkflowStep,
  GenerationStage,
} from "@/types";
import { ArrowLeft, Download, CheckCircle2, Clock, AlertTriangle, RefreshCw } from "lucide-react";

export default function PreviewPage() {
  const router = useRouter();
  const [elapsedMs, setElapsedMs] = useState(0);
  const [startTime, setStartTime] = useState<number | null>(null);
  
  // Store state
  const completedSteps = useWorkflowStore((state) => state.completedSteps);
  const completeStep = useWorkflowStore((state) => state.completeStep);
  const componentType = useWorkflowStore((state) => state.componentType);
  const getApprovedProposals = useWorkflowStore((state) => state.getApprovedProposals);
  const tokens = useTokenStore((state) => state.tokens);

  // Generation mutation
  const generation = useGenerateComponent({
    onSuccess: () => {
      // Mark preview step as completed on successful generation
      completeStep(WorkflowStep.PREVIEW);
      // Stop timer
      setStartTime(null);
    },
    onError: (error) => {
      console.error('Generation failed:', error);
      // Stop timer
      setStartTime(null);
    },
  });

  const generationStatus = useGenerationStatus(generation);
  const isGenerating = generation.isPending;
  const isComplete = generation.isSuccess;
  const hasFailed = generation.isError;

  // Route guard: redirect if patterns not completed
  useEffect(() => {
    if (!completedSteps.includes(WorkflowStep.PATTERNS)) {
      router.push('/patterns');
    }
  }, [completedSteps, router]);

  // Trigger generation on page load (only once)
  useEffect(() => {
    // Only generate if we have required data and haven't generated yet
    if (
      componentType &&
      tokens &&
      !generation.data &&
      !isGenerating &&
      !hasFailed
    ) {
      const approvedRequirements = getApprovedProposals();
      const allRequirements = [
        ...approvedRequirements.props,
        ...approvedRequirements.events,
        ...approvedRequirements.states,
        ...approvedRequirements.accessibility,
      ];

      // Determine pattern_id based on component type
      // In a real implementation, this would come from pattern selection
      const patternId = componentType.toLowerCase() + '-001';

      // Start generation
      setStartTime(Date.now());
      generation.mutate({
        pattern_id: patternId,
        tokens,
        requirements: allRequirements,
      });
    }
  }, [componentType, tokens]); // Only depend on data, not mutation state

  // Update elapsed time while generating
  useEffect(() => {
    if (!startTime || !isGenerating) return;

    const interval = setInterval(() => {
      setElapsedMs(Date.now() - startTime);
    }, 100); // Update every 100ms for smooth counter

    return () => clearInterval(interval);
  }, [startTime, isGenerating]);

  // Determine current stage (mock for now, real backend will provide this)
  const currentStage = useMemo(() => {
    if (!isGenerating) {
      return isComplete ? GenerationStage.COMPLETE : GenerationStage.PARSING;
    }
    
    // Mock stage progression based on elapsed time
    if (elapsedMs < 10000) return GenerationStage.PARSING;
    if (elapsedMs < 25000) return GenerationStage.INJECTING;
    if (elapsedMs < 40000) return GenerationStage.GENERATING;
    if (elapsedMs < 50000) return GenerationStage.ASSEMBLING;
    return GenerationStage.FORMATTING;
  }, [isGenerating, isComplete, elapsedMs]);

  // Handle download action
  const handleDownload = () => {
    if (generation.data?.code) {
      const componentName = componentType || 'Component';
      downloadGeneratedCode(generation.data.code, componentName);
    }
  };

  // Handle retry action
  const handleRetry = () => {
    setElapsedMs(0);
    setStartTime(Date.now());
    generation.reset();
    
    // Retry generation
    const approvedRequirements = getApprovedProposals();
    const allRequirements = [
      ...approvedRequirements.props,
      ...approvedRequirements.events,
      ...approvedRequirements.states,
      ...approvedRequirements.accessibility,
    ];
    const patternId = (componentType?.toLowerCase() || 'button') + '-001';
    
    generation.mutate({
      pattern_id: patternId,
      tokens: tokens!,
      requirements: allRequirements,
    });
  };

  // Get generated code or placeholders
  const componentCode = generation.data?.code.component || '';
  const storiesCode = generation.data?.code.stories || '';
  const metadata = generation.data?.metadata;
  const timing = generation.data?.timing;

  return (
    <main className="container mx-auto p-4 sm:p-8 space-y-6">
      {/* Workflow Breadcrumb */}
      <WorkflowBreadcrumb />

      {/* Page Header */}
      <div className="space-y-2">
        <h1 className="text-3xl font-bold tracking-tight">
          Component Preview
        </h1>
        <p className="text-muted-foreground">
          {isGenerating && "Generating your component..."}
          {isComplete && "Review and download your generated component"}
          {hasFailed && "Generation failed - please try again"}
        </p>
      </div>

      {/* Generation Progress (show when generating) */}
      {isGenerating && (
        <GenerationProgress
          currentStage={currentStage}
          status={generationStatus}
          elapsedMs={elapsedMs}
        />
      )}

      {/* Error State */}
      {hasFailed && (
        <Card className="border-destructive">
          <CardContent className="pt-6">
            <div className="flex flex-col items-center text-center space-y-4">
              <AlertTriangle className="size-12 text-destructive" />
              <div>
                <h3 className="font-semibold text-lg">Generation Failed</h3>
                <p className="text-sm text-muted-foreground mt-2">
                  {generation.error?.message || "An error occurred during code generation."}
                </p>
              </div>
              <div className="flex gap-4">
                <Button onClick={handleRetry} variant="default">
                  <RefreshCw className="mr-2 h-4 w-4" />
                  Retry Generation
                </Button>
                <Button asChild variant="outline">
                  <Link href="/patterns">
                    <ArrowLeft className="mr-2 h-4 w-4" />
                    Back to Patterns
                  </Link>
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Quality Metrics (show when complete) */}
      {isComplete && metadata && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <MetricCard
            title="Accessibility"
            value={metadata.has_accessibility_warnings ? "Warnings" : "✓ Pass"}
            icon={metadata.has_accessibility_warnings ? AlertTriangle : CheckCircle2}
          />
          <MetricCard
            title="Type Safety"
            value={metadata.has_typescript_errors ? "Errors" : "✓ Pass"}
            icon={metadata.has_typescript_errors ? AlertTriangle : CheckCircle2}
          />
          <MetricCard
            title="Lines of Code"
            value={metadata.lines_of_code.toString()}
            icon={Clock}
          />
          <MetricCard
            title="Generation Time"
            value={timing ? `${(timing.total_ms / 1000).toFixed(1)}s` : "N/A"}
            icon={Clock}
          />
        </div>
      )}

      {/* Component Tabs (show when complete) */}
      {isComplete && componentCode && (
        <Tabs defaultValue="preview" className="space-y-4">
          <TabsList className="grid w-full max-w-2xl grid-cols-4">
            <TabsTrigger value="preview">Preview</TabsTrigger>
            <TabsTrigger value="code">Code</TabsTrigger>
            <TabsTrigger value="storybook">Storybook</TabsTrigger>
            <TabsTrigger value="quality">Quality</TabsTrigger>
          </TabsList>

          {/* Preview Tab */}
          <TabsContent value="preview">
            <Card>
              <CardHeader>
                <CardTitle>Component Preview</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="border rounded-lg p-8 bg-muted/20">
                  <p className="text-center text-muted-foreground">
                    Live preview will be available in a future update.
                  </p>
                  <p className="text-xs text-center text-muted-foreground mt-2">
                    For now, copy the code to test your component.
                  </p>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Code Tab */}
          <TabsContent value="code">
            <Card>
              <CardHeader>
                <CardTitle>Generated Code</CardTitle>
              </CardHeader>
              <CardContent>
                <DynamicCodeBlock language="tsx" code={componentCode} />
              </CardContent>
            </Card>
          </TabsContent>

          {/* Storybook Tab */}
          <TabsContent value="storybook">
            <Card>
              <CardHeader>
                <CardTitle>Storybook Stories</CardTitle>
              </CardHeader>
              <CardContent>
                {storiesCode ? (
                  <DynamicCodeBlock language="tsx" code={storiesCode} />
                ) : (
                  <p className="text-sm text-muted-foreground">
                    Storybook stories not available.
                  </p>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          {/* Quality Tab */}
          <TabsContent value="quality">
            <Card>
              <CardHeader>
                <CardTitle>Quality Report</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <h3 className="font-medium">Generation Metrics</h3>
                  <div className="text-sm space-y-1">
                    <p>
                      <span className="text-muted-foreground">Pattern used:</span>{" "}
                      {metadata?.pattern_used} v{metadata?.pattern_version}
                    </p>
                    <p>
                      <span className="text-muted-foreground">Tokens applied:</span>{" "}
                      {metadata?.tokens_applied}
                    </p>
                    <p>
                      <span className="text-muted-foreground">Requirements implemented:</span>{" "}
                      {metadata?.requirements_implemented}
                    </p>
                    <p>
                      <span className="text-muted-foreground">Imports:</span>{" "}
                      {metadata?.imports_count}
                    </p>
                  </div>
                </div>

                <div className="space-y-2">
                  <h3 className="font-medium">Code Quality</h3>
                  <div className="text-sm space-y-1">
                    <p className={metadata?.has_typescript_errors ? "text-destructive" : "text-success"}>
                      {metadata?.has_typescript_errors ? "✗" : "✓"} TypeScript compilation
                    </p>
                    <p className={metadata?.has_accessibility_warnings ? "text-warning" : "text-success"}>
                      {metadata?.has_accessibility_warnings ? "⚠" : "✓"} Accessibility
                    </p>
                  </div>
                </div>

                {timing && (
                  <div className="space-y-2">
                    <h3 className="font-medium">Performance</h3>
                    <div className="text-sm space-y-1">
                      <p>
                        <span className="text-muted-foreground">Total:</span>{" "}
                        {(timing.total_ms / 1000).toFixed(2)}s
                      </p>
                      <p className="text-xs text-muted-foreground">
                        Parsing: {(timing.parsing_ms / 1000).toFixed(2)}s •{" "}
                        Injection: {(timing.injection_ms / 1000).toFixed(2)}s •{" "}
                        Generation: {(timing.generation_ms / 1000).toFixed(2)}s •{" "}
                        Assembly: {(timing.assembly_ms / 1000).toFixed(2)}s
                      </p>
                    </div>
                  </div>
                )}

                <p className="text-sm text-muted-foreground">
                  <strong>Note:</strong> Full quality validation available with Epic 5.
                </p>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      )}

      {/* Loading placeholder */}
      {isGenerating && (
        <Card>
          <CardContent className="py-12">
            <p className="text-center text-muted-foreground">
              Generating your component... This typically takes less than 60 seconds.
            </p>
          </CardContent>
        </Card>
      )}

      {/* Actions */}
      <div className="flex flex-col sm:flex-row gap-4 justify-between">
        <Button asChild variant="outline">
          <Link href="/patterns">
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back to Patterns
          </Link>
        </Button>
        {isComplete && (
          <div className="flex gap-4">
            <Button variant="outline" onClick={handleDownload}>
              <Download className="mr-2 h-4 w-4" />
              Download Files
            </Button>
            <Button onClick={handleRetry}>
              <RefreshCw className="mr-2 h-4 w-4" />
              Regenerate
            </Button>
          </div>
        )}
      </div>
    </main>
  );
}
