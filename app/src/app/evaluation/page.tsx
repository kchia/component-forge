/**
 * Evaluation Metrics Dashboard
 *
 * Displays comprehensive metrics for the screenshot-to-code pipeline:
 * - Overall pipeline success rate
 * - Stage-by-stage performance (token extraction, retrieval, generation)
 * - Retrieval comparison (E2E vs retrieval-only)
 * - Per-screenshot results
 */

import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { MetricCard, ComparisonTable } from "@/components/evaluation";
import type { EvaluationMetrics } from "@/types/evaluation";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function getEvaluationMetrics(): Promise<EvaluationMetrics | null> {
  try {
    const res = await fetch(`${API_BASE_URL}/api/v1/evaluation/metrics`, {
      cache: "no-store", // Always fetch fresh data
    });

    if (!res.ok) {
      console.error("Failed to fetch evaluation metrics:", res.statusText);
      return null;
    }

    return res.json();
  } catch (error) {
    console.error("Error fetching evaluation metrics:", error);
    return null;
  }
}

export default async function EvaluationPage() {
  const metrics = await getEvaluationMetrics();

  if (!metrics) {
    return (
      <div className="container mx-auto py-8 px-4">
        <h1 className="text-3xl font-bold mb-6">Evaluation Metrics</h1>

        <Alert variant="destructive">
          <AlertDescription>
            Failed to load evaluation metrics. Please ensure:
            <ul className="list-disc list-inside mt-2">
              <li>The backend server is running</li>
              <li>OPENAI_API_KEY is configured</li>
              <li>The golden dataset exists</li>
            </ul>
          </AlertDescription>
        </Alert>
      </div>
    );
  }

  const { overall, per_screenshot, retrieval_only, dataset_size, timestamp } =
    metrics;

  return (
    <div className="container mx-auto py-8 px-4">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-3xl font-bold">Evaluation Metrics</h1>
          <p className="text-gray-600 dark:text-gray-400 mt-1">
            Last updated: {timestamp}
          </p>
        </div>
        <Button
          onClick={() => {
            const blob = new Blob([JSON.stringify(metrics, null, 2)], {
              type: "application/json",
            });
            const url = URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = `evaluation_metrics_${timestamp.replace(/[: ]/g, "_")}.json`;
            a.click();
            URL.revokeObjectURL(url);
          }}
        >
          Export JSON
        </Button>
      </div>

      {/* Overall Pipeline Metrics */}
      <section className="mb-8">
        <h2 className="text-2xl font-semibold mb-4">Overall Pipeline Metrics</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <MetricCard
            label="Pipeline Success Rate"
            value={overall.pipeline_success_rate}
            target={0.8}
            format="percentage"
            description="% of screenshots producing valid code end-to-end"
          />
          <MetricCard
            label="Average Latency"
            value={overall.avg_latency_ms / 1000}
            target={20}
            format="seconds"
            description="Time from screenshot to valid code"
            inverted
          />
          <MetricCard
            label="Dataset Size"
            value={dataset_size}
            format="number"
            description="Number of test screenshots"
          />
        </div>
      </section>

      {/* Stage-by-Stage Performance */}
      <section className="mb-8">
        <h2 className="text-2xl font-semibold mb-4">
          Stage-by-Stage Performance
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Token Extraction */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Token Extraction</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold mb-2">
                {(overall.token_extraction.avg_accuracy * 100).toFixed(1)}%
              </div>
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                Average accuracy
              </p>
              <Badge
                variant={
                  overall.token_extraction.avg_accuracy >= 0.85
                    ? "success"
                    : "warning"
                }
              >
                Target: ≥ 85%
              </Badge>
            </CardContent>
          </Card>

          {/* Pattern Retrieval */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Pattern Retrieval</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold mb-2">
                {(overall.retrieval.mrr * 100).toFixed(1)}%
              </div>
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                MRR (Context Precision)
              </p>
              <Badge
                variant={overall.retrieval.mrr >= 0.9 ? "success" : "warning"}
              >
                Target: ≥ 90%
              </Badge>
              <div className="mt-3 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-600 dark:text-gray-400">
                    Hit@3:
                  </span>
                  <span className="font-mono">
                    {(overall.retrieval.hit_at_3 * 100).toFixed(1)}%
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600 dark:text-gray-400">
                    Precision@1:
                  </span>
                  <span className="font-mono">
                    {(overall.retrieval.precision_at_1 * 100).toFixed(1)}%
                  </span>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Code Generation */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Code Generation</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold mb-2">
                {(overall.generation.compilation_rate * 100).toFixed(1)}%
              </div>
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                Compilation rate
              </p>
              <Badge
                variant={
                  overall.generation.compilation_rate >= 0.9
                    ? "success"
                    : "warning"
                }
              >
                Target: ≥ 90%
              </Badge>
              <div className="mt-3 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-600 dark:text-gray-400">
                    Quality Score:
                  </span>
                  <span className="font-mono">
                    {overall.generation.avg_quality_score.toFixed(2)}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600 dark:text-gray-400">
                    Success Rate:
                  </span>
                  <span className="font-mono">
                    {(overall.generation.success_rate * 100).toFixed(1)}%
                  </span>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Retrieval Comparison */}
      {retrieval_only && (
        <section className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">Retrieval Comparison</h2>
          <p className="text-gray-600 dark:text-gray-400 mb-4">
            Comparing retrieval performance in E2E pipeline vs isolated testing
            ({retrieval_only.test_queries} test queries)
          </p>
          <ComparisonTable
            e2eMetrics={overall.retrieval}
            retrievalOnlyMetrics={retrieval_only}
          />
        </section>
      )}

      {/* Stage Failures */}
      <section className="mb-8">
        <h2 className="text-2xl font-semibold mb-4">Failure Analysis</h2>
        <Card>
          <CardContent className="pt-6">
            {Object.values(overall.stage_failures).reduce((a, b) => a + b, 0) ===
            0 ? (
              <div className="text-center py-4">
                <Badge variant="success" className="text-lg">
                  ✓ No failures detected
                </Badge>
              </div>
            ) : (
              <div className="space-y-2">
                <div className="flex justify-between items-center">
                  <span className="font-medium">Token Extraction Failures:</span>
                  <Badge variant={overall.stage_failures.token_extraction === 0 ? "success" : "warning"}>
                    {overall.stage_failures.token_extraction}
                  </Badge>
                </div>
                <div className="flex justify-between items-center">
                  <span className="font-medium">Retrieval Failures:</span>
                  <Badge variant={overall.stage_failures.retrieval === 0 ? "success" : "warning"}>
                    {overall.stage_failures.retrieval}
                  </Badge>
                </div>
                <div className="flex justify-between items-center">
                  <span className="font-medium">Generation Failures:</span>
                  <Badge variant={overall.stage_failures.generation === 0 ? "success" : "warning"}>
                    {overall.stage_failures.generation}
                  </Badge>
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      </section>

      {/* Per-Screenshot Results */}
      <section className="mb-8">
        <h2 className="text-2xl font-semibold mb-4">Per-Screenshot Results</h2>
        <div className="space-y-4">
          {per_screenshot.map((result) => (
            <Card key={result.screenshot_id}>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle className="text-lg">
                    {result.screenshot_id}
                  </CardTitle>
                  <Badge
                    variant={result.pipeline_success ? "success" : "warning"}
                  >
                    {result.pipeline_success ? "✓ Success" : "✗ Failed"}
                  </Badge>
                </div>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-sm">
                  <div>
                    <span className="text-gray-600 dark:text-gray-400">
                      Token Accuracy:
                    </span>
                    <div className="font-mono font-medium">
                      {(result.token_extraction.accuracy * 100).toFixed(1)}%
                    </div>
                  </div>
                  <div>
                    <span className="text-gray-600 dark:text-gray-400">
                      Retrieval:
                    </span>
                    <div className="font-mono font-medium">
                      {result.retrieval.correct ? "✓" : "✗"}{" "}
                      {result.retrieval.retrieved || "N/A"}
                    </div>
                  </div>
                  <div>
                    <span className="text-gray-600 dark:text-gray-400">
                      Generation:
                    </span>
                    <div className="font-mono font-medium">
                      {result.generation.code_compiles ? "✓" : "✗"} Quality:{" "}
                      {result.generation.quality_score.toFixed(2)}
                    </div>
                  </div>
                  <div>
                    <span className="text-gray-600 dark:text-gray-400">
                      Latency:
                    </span>
                    <div className="font-mono font-medium">
                      {(result.total_latency_ms / 1000).toFixed(1)}s
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>
    </div>
  );
}
