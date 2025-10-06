"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { MetricCard } from "@/components/composite/MetricCard";
import { DynamicCodeBlock } from "@/components/ui/DynamicCodeBlock";
import { WorkflowBreadcrumb } from "@/components/composite/WorkflowBreadcrumb";
import { useWorkflowStore } from "@/stores/useWorkflowStore";
import { WorkflowStep } from "@/types";
import { ArrowLeft, Download, CheckCircle2, Clock, AlertTriangle } from "lucide-react";

// Placeholder code (will be replaced with Epic 4 backend)
const placeholderCode = `import * as React from "react"
import { cn } from "@/lib/utils"

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "ghost"
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "primary", ...props }, ref) => {
    return (
      <button
        className={cn(
          "inline-flex items-center justify-center rounded-md px-4 py-2 text-sm font-medium",
          {
            "bg-primary text-primary-foreground": variant === "primary",
            "bg-secondary text-secondary-foreground": variant === "secondary",
            "hover:bg-accent hover:text-accent-foreground": variant === "ghost",
          },
          className
        )}
        ref={ref}
        {...props}
      />
    )
  }
)

Button.displayName = "Button"

export { Button }`;

const placeholderStorybook = `import type { Meta, StoryObj } from '@storybook/react'
import { Button } from './Button'

const meta: Meta<typeof Button> = {
  title: 'Components/Button',
  component: Button,
  tags: ['autodocs'],
}

export default meta
type Story = StoryObj<typeof Button>

export const Primary: Story = {
  args: {
    children: 'Button',
    variant: 'primary',
  },
}

export const Secondary: Story = {
  args: {
    children: 'Button',
    variant: 'secondary',
  },
}`;

export default function PreviewPage() {
  const router = useRouter();
  const completedSteps = useWorkflowStore((state) => state.completedSteps);
  const completeStep = useWorkflowStore((state) => state.completeStep);

  // Route guard: redirect if patterns not completed
  useEffect(() => {
    if (!completedSteps.includes(WorkflowStep.PATTERNS)) {
      router.push('/patterns');
    }
  }, [completedSteps, router]);

  // Handle download action
  const handleDownload = () => {
    // Mark preview step as completed when user downloads
    completeStep(WorkflowStep.PREVIEW);
    
    // In a real implementation, this would download the generated code
    console.log('Downloading component files...');
  };

  // Handle save action
  const handleSave = () => {
    // Mark preview step as completed when user saves
    completeStep(WorkflowStep.PREVIEW);
    
    // In a real implementation, this would save to the project
    console.log('Saving component to project...');
  };

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
          Review and download your generated component
        </p>
      </div>

      {/* Quality Metrics */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard
          title="Accessibility"
          value="95%"
          icon={CheckCircle2}
        />
        <MetricCard
          title="Type Safety"
          value="100%"
          icon={CheckCircle2}
        />
        <MetricCard
          title="Test Coverage"
          value="N/A"
          icon={Clock}
        />
        <MetricCard
          title="Warnings"
          value="0"
          icon={AlertTriangle}
        />
      </div>

      {/* Component Tabs */}
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
                  Live preview will be available with Epic 4 backend integration.
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
              <DynamicCodeBlock language="tsx" code={placeholderCode} />
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
              <DynamicCodeBlock language="tsx" code={placeholderStorybook} />
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
                <h3 className="font-medium">Accessibility</h3>
                <p className="text-sm text-muted-foreground">
                  ✓ Keyboard navigation supported
                  <br />
                  ✓ ARIA attributes present
                  <br />
                  ✓ Color contrast meets WCAG AA
                </p>
              </div>
              <div className="space-y-2">
                <h3 className="font-medium">Type Safety</h3>
                <p className="text-sm text-muted-foreground">
                  ✓ Full TypeScript support
                  <br />
                  ✓ Strict mode compliant
                  <br />
                  ✓ Props properly typed
                </p>
              </div>
              <p className="text-sm text-muted-foreground">
                <strong>Note:</strong> Full quality validation available with Epic 5.
              </p>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Placeholder Note */}
      <Card>
        <CardContent className="py-6">
          <p className="text-sm text-muted-foreground text-center">
            <strong>Note:</strong> This is a placeholder component. Real components will be generated by Epic 4 backend.
          </p>
        </CardContent>
      </Card>

      {/* Actions */}
      <div className="flex flex-col sm:flex-row gap-4 justify-between">
        <Button asChild variant="outline">
          <Link href="/patterns">
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back to Patterns
          </Link>
        </Button>
        <div className="flex gap-4">
          <Button variant="outline" onClick={handleDownload}>
            <Download className="mr-2 h-4 w-4" />
            Download ZIP
          </Button>
          <Button onClick={handleSave}>
            Save to Project
          </Button>
        </div>
      </div>
    </main>
  );
}
