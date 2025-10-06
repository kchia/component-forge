"use client";

import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { MetricCard } from "@/components/composite/MetricCard";
import { useWorkflowStore } from "@/stores/useWorkflowStore";
import { WorkflowStep } from "@/types";
import { Sparkles, Palette, Component, RotateCcw } from "lucide-react";

export default function Dashboard() {
  const completedSteps = useWorkflowStore((state) => state.completedSteps);
  const resetWorkflow = useWorkflowStore((state) => state.resetWorkflow);
  const canAccessPatterns = completedSteps.includes(WorkflowStep.REQUIREMENTS);
  const hasProgress = completedSteps.length > 0;

  return (
    <main className="container mx-auto p-4 sm:p-8 space-y-8">
      {/* Header */}
      <div className="space-y-2">
        <h1 className="text-3xl sm:text-4xl font-bold tracking-tight">
          ComponentForge
        </h1>
        <p className="text-muted-foreground text-sm sm:text-base">
          AI-powered design token extraction and component generation
        </p>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <MetricCard
          title="Components Generated"
          value="0"
          icon={Component}
        />
        <MetricCard
          title="Success Rate"
          value="N/A"
          icon={Sparkles}
        />
        <MetricCard
          title="Avg Generation Time"
          value="N/A"
          icon={Palette}
        />
      </div>

      {/* Quick Actions Card */}
      <Card>
        <CardHeader>
          <CardTitle>Quick Actions</CardTitle>
        </CardHeader>
        <CardContent className="flex flex-col sm:flex-row gap-4">
          <Button asChild size="lg">
            <Link href="/extract">Extract Tokens</Link>
          </Button>
          {canAccessPatterns ? (
            <Button asChild variant="secondary" size="lg">
              <Link href="/patterns">View Patterns</Link>
            </Button>
          ) : (
            <Button variant="secondary" size="lg" disabled>
              View Patterns (Complete Requirements First)
            </Button>
          )}
          {hasProgress && (
            <Button 
              variant="outline" 
              size="lg"
              onClick={resetWorkflow}
              className="gap-2"
            >
              <RotateCcw className="h-4 w-4" />
              Reset Workflow
            </Button>
          )}
        </CardContent>
      </Card>

      {/* Recent Generations Card */}
      <Card>
        <CardHeader>
          <CardTitle>Recent Generations</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8 text-muted-foreground">
            <p>No components generated yet</p>
            <p className="text-sm mt-2">
              Start by extracting tokens from a screenshot or Figma file
            </p>
          </div>
        </CardContent>
      </Card>
    </main>
  );
}
