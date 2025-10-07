"use client"

import * as React from "react"
import { Progress } from "@/components/ui/progress"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { cn } from "@/lib/utils"
import {
  GenerationStage,
  GenerationStatus,
  getStageDisplayName,
  getStageProgress,
  formatTiming,
} from "@/types"
import { Clock, CheckCircle2, AlertCircle, Loader2 } from "lucide-react"

export interface GenerationProgressProps {
  /** Current generation stage */
  currentStage: GenerationStage
  /** Current generation status */
  status: GenerationStatus
  /** Elapsed time in milliseconds */
  elapsedMs?: number
  /** Error message if generation failed */
  error?: string
  /** Additional CSS classes */
  className?: string
}

/**
 * GenerationProgress - Shows real-time progress during code generation
 * 
 * Displays the current stage of the generation pipeline with:
 * - Progress bar showing completion percentage
 * - Stage-by-stage indicators (✓ completed, ⏳ pending, 🔄 current)
 * - Elapsed time counter
 * - Error message if generation fails
 * 
 * Stages:
 * 1. Parsing Pattern (20%)
 * 2. Injecting Tokens (40%)
 * 3. Generating Code (60%)
 * 4. Assembling Components (80%)
 * 5. Formatting Code (90%)
 * 6. Complete (100%)
 * 
 * @example
 * ```tsx
 * <GenerationProgress
 *   currentStage={GenerationStage.INJECTING}
 *   status={GenerationStatus.IN_PROGRESS}
 *   elapsedMs={15000}
 * />
 * ```
 */
export function GenerationProgress({
  currentStage,
  status,
  elapsedMs = 0,
  error,
  className,
}: GenerationProgressProps) {
  const progress = getStageProgress(currentStage)
  const isComplete = status === GenerationStatus.COMPLETED
  const isFailed = status === GenerationStatus.FAILED
  const isInProgress = status === GenerationStatus.IN_PROGRESS || status === GenerationStatus.PENDING

  // Get all stages in order
  const stages = [
    GenerationStage.PARSING,
    GenerationStage.INJECTING,
    GenerationStage.GENERATING,
    GenerationStage.ASSEMBLING,
    GenerationStage.FORMATTING,
  ]

  // Determine variant based on status
  const variant = isFailed ? "error" : isComplete ? "success" : "default"

  return (
    <Card className={cn(className)}>
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <span>
            {isComplete && "Generation Complete"}
            {isFailed && "Generation Failed"}
            {isInProgress && "Generating Component..."}
          </span>
          {elapsedMs > 0 && (
            <span className="text-sm font-normal text-muted-foreground flex items-center gap-1">
              <Clock className="size-4" />
              {formatTiming(elapsedMs)}
              {isInProgress && " / 60s target"}
            </span>
          )}
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Progress bar */}
        <Progress 
          value={isComplete ? 100 : progress} 
          variant={variant}
          aria-label={`Generation progress: ${progress}%`}
        />

        {/* Stage list */}
        <div className="space-y-2 text-sm" role="list" aria-label="Generation stages">
          {stages.map((stage) => {
            const stageProgress = getStageProgress(stage)
            const isStageComplete = progress > stageProgress || isComplete
            const isStageCurrent = stage === currentStage && isInProgress
            const isStagePending = progress < stageProgress && !isComplete

            return (
              <div 
                key={stage}
                className="flex items-center gap-2"
                role="listitem"
                aria-current={isStageCurrent ? "step" : undefined}
              >
                {/* Status icon */}
                {isStageComplete && (
                  <CheckCircle2 
                    className="size-4 text-success flex-shrink-0" 
                    aria-label="Completed"
                  />
                )}
                {isStageCurrent && (
                  <Loader2 
                    className="size-4 animate-spin flex-shrink-0" 
                    aria-label="In progress"
                  />
                )}
                {isStagePending && (
                  <Clock 
                    className="size-4 text-muted-foreground flex-shrink-0" 
                    aria-label="Pending"
                  />
                )}

                {/* Stage name */}
                <span 
                  className={cn(
                    "flex-1",
                    isStageComplete && "text-foreground",
                    isStageCurrent && "text-foreground font-medium",
                    isStagePending && "text-muted-foreground"
                  )}
                >
                  {getStageDisplayName(stage)}
                </span>

                {/* Progress percentage */}
                <span className="text-xs text-muted-foreground">
                  {stageProgress}%
                </span>
              </div>
            )
          })}
        </div>

        {/* Error message */}
        {isFailed && error && (
          <div className="flex items-start gap-2 p-3 bg-destructive/10 border border-destructive/20 rounded-md">
            <AlertCircle className="size-4 text-destructive flex-shrink-0 mt-0.5" />
            <div className="flex-1">
              <p className="text-sm font-medium text-destructive">
                Generation Error
              </p>
              <p className="text-sm text-muted-foreground mt-1">
                {error}
              </p>
            </div>
          </div>
        )}

        {/* Success message */}
        {isComplete && !error && (
          <div className="flex items-center gap-2 p-3 bg-success/10 border border-success/20 rounded-md">
            <CheckCircle2 className="size-4 text-success flex-shrink-0" />
            <p className="text-sm text-success font-medium">
              Component generated successfully in {formatTiming(elapsedMs)}
            </p>
          </div>
        )}

        {/* Performance note */}
        {isInProgress && elapsedMs > 60000 && (
          <p className="text-xs text-warning">
            Generation taking longer than expected (target: 60s)
          </p>
        )}
      </CardContent>
    </Card>
  )
}
