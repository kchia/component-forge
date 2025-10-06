"use client";

import { useState, useCallback, useEffect } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import Link from "next/link";
import dynamic from "next/dynamic";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Alert } from "@/components/ui/alert";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { Upload, FileImage, CheckCircle2, ArrowRight, AlertTriangle } from "lucide-react";
import { useTokenExtraction } from "@/lib/query/hooks/useTokenExtraction";
import { useFigmaAuth } from "@/lib/query/hooks/useFigmaAuth";
import { useFigmaExtraction } from "@/lib/query/hooks/useFigmaExtraction";
import { useTokenStore } from "@/stores/useTokenStore";
import { useUIStore } from "@/stores/useUIStore";
import { useWorkflowStore } from "@/stores/useWorkflowStore";
import type { TokenData } from "@/components/tokens/TokenEditor";

// New components for EPIC 12
import { CompactTips } from "@/components/extract/CompactTips";
import { FigmaGuidance } from "@/components/extract/FigmaGuidance";

// Dynamic imports to avoid SSR issues with prismjs in CodeBlock
const TokenEditor = dynamic(
  () => import("@/components/tokens/TokenEditor").then(mod => ({ default: mod.TokenEditor })), 
  { 
    ssr: false,
    loading: () => <div className="p-4 text-sm text-muted-foreground">Loading editor...</div>
  }
);
const TokenExport = dynamic(
  () => import("@/components/tokens/TokenExport").then(mod => ({ default: mod.TokenExport })), 
  { 
    ssr: false,
    loading: () => <div className="p-4 text-sm text-muted-foreground">Loading export...</div>
  }
);

export default function TokenExtractionPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const tabParam = searchParams.get("tab");
  const [activeTab, setActiveTab] = useState(tabParam === "figma" ? "figma" : "screenshot");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [dragActive, setDragActive] = useState(false);
  const [validationWarnings, setValidationWarnings] = useState<string[]>([]);

  // Update active tab when URL param changes
  useEffect(() => {
    if (tabParam === "figma" || tabParam === "screenshot") {
      setActiveTab(tabParam);
    }
  }, [tabParam]);
  
  // Figma state
  const [figmaPat, setFigmaPat] = useState("");
  const [figmaUrl, setFigmaUrl] = useState("");
  const [isPatValid, setIsPatValid] = useState(false);
  
  const { mutate: extractTokens, isPending, isError, error } = useTokenExtraction();
  const { mutate: authFigma, isPending: isAuthPending } = useFigmaAuth();
  const { mutate: extractFromFigma, isPending: isFigmaPending } = useFigmaExtraction();
  const tokens = useTokenStore((state) => state.tokens);
  const metadata = useTokenStore((state) => state.metadata);
  const showAlert = useUIStore((state) => state.showAlert);
  const setUploadedFile = useWorkflowStore((state) => state.setUploadedFile);

  // Convert tokens to TokenEditor format with actual confidence scores from backend
  const getEditorTokens = (): TokenData | null => {
    if (!tokens) return null;

    return {
      colors: tokens.colors || {},
      typography: tokens.typography || {},
      spacing: tokens.spacing || {},
      borderRadius: tokens.borderRadius || {},
    };
  };

  // Check if tokens are actually empty (all categories are empty objects)
  const hasTokens = (): boolean => {
    if (!tokens) return false;
    const tokenCount =
      Object.keys(tokens.colors || {}).length +
      Object.keys(tokens.typography || {}).length +
      Object.keys(tokens.spacing || {}).length +
      Object.keys(tokens.borderRadius || {}).length;
    return tokenCount > 0;
  };

  // Get confidence scores from metadata
  const getConfidenceScores = (): Record<string, number> => {
    return (metadata as { confidence?: Record<string, number> })?.confidence || {};
  };

  // Image validation with dimension and quality checks
  interface ImageValidation {
    valid: boolean;
    errors: string[];
    warnings: string[];
  }

  const validateImageUpload = async (file: File): Promise<ImageValidation> => {
    const errors: string[] = [];
    const warnings: string[] = [];

    // Check file size (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
      errors.push("File size exceeds 10MB. Please compress your image.");
    }

    // Check file type
    const validTypes = ["image/png", "image/jpeg", "image/webp", "image/jpg"];
    if (!validTypes.includes(file.type)) {
      errors.push("Invalid file format. Please upload PNG, JPG, or WebP.");
    }

    // Check image dimensions
    return new Promise<ImageValidation>((resolve) => {
      const img = new Image();
      const objectUrl = URL.createObjectURL(file);

      img.onload = () => {
        URL.revokeObjectURL(objectUrl);

        // Check minimum width
        if (img.width < 1024) {
          warnings.push(
            `Image width is ${img.width}px. For best results, use images at least 1024px wide.`
          );
        }

        // Check if image is too small
        if (img.width < 512 || img.height < 512) {
          errors.push("Image is too small. Please upload a larger screenshot.");
        }

        // Check aspect ratio (very tall/wide images might be full app screenshots)
        const aspectRatio = img.width / img.height;
        if (aspectRatio > 3 || aspectRatio < 0.33) {
          warnings.push(
            "Unusual aspect ratio detected. Make sure your screenshot focuses on design tokens, not a full app layout."
          );
        }

        resolve({
          valid: errors.length === 0,
          errors,
          warnings
        });
      };

      img.onerror = () => {
        URL.revokeObjectURL(objectUrl);
        errors.push("Failed to load image. Please try a different file.");
        resolve({ valid: false, errors, warnings });
      };

      img.src = objectUrl;
    });
  };

  // Handle file selection with validation
  const handleFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setValidationWarnings([]);

      // Validate image
      const validation = await validateImageUpload(file);

      // Show errors
      if (!validation.valid) {
        showAlert('error', validation.errors.join(" "));
        return;
      }

      // Show warnings (but allow upload)
      if (validation.warnings.length > 0) {
        setValidationWarnings(validation.warnings);
      }

      setSelectedFile(file);

      // Create preview URL
      const previewUrl = URL.createObjectURL(file);
      setImagePreview(previewUrl);
    }
  };

  // Cleanup preview URL on unmount
  useEffect(() => {
    return () => {
      if (imagePreview) {
        URL.revokeObjectURL(imagePreview);
      }
    };
  }, [imagePreview]);

  // Handle drag and drop
  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback(async (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const file = e.dataTransfer.files?.[0];
    if (file) {
      setValidationWarnings([]);

      // Validate image
      const validation = await validateImageUpload(file);

      // Show errors
      if (!validation.valid) {
        showAlert('error', validation.errors.join(" "));
        return;
      }

      // Show warnings (but allow upload)
      if (validation.warnings.length > 0) {
        setValidationWarnings(validation.warnings);
      }

      setSelectedFile(file);

      // Create preview URL
      const previewUrl = URL.createObjectURL(file);
      setImagePreview(previewUrl);
    }
  }, [showAlert]);

  // Handle upload with success tracking
  const handleUpload = () => {
    if (selectedFile) {
      // Store file in workflow store for requirements page
      setUploadedFile(selectedFile);
      
      extractTokens(selectedFile, {
        onSuccess: () => {
          // Show success toast
          showAlert('success', '✓ Tokens extracted successfully! Scroll down to review and edit.');

          // Auto-scroll to TokenEditor after short delay
          setTimeout(() => {
            document.getElementById("token-editor")?.scrollIntoView({
              behavior: "smooth",
              block: "start"
            });
          }, 500);
        }
      });
    }
  };

  // Handle Figma PAT validation
  const handleValidatePat = () => {
    if (figmaPat.trim()) {
      authFigma(figmaPat, {
        onSuccess: (data) => {
          if (data.valid) {
            setIsPatValid(true);
          } else {
            showAlert('error', data.message);
          }
        },
      });
    }
  };

  // Handle Figma extraction
  const handleFigmaExtract = () => {
    if (figmaUrl.trim() && figmaPat.trim()) {
      extractFromFigma({
        figmaUrl,
        personalAccessToken: figmaPat,
      });
    }
  };

  // Handle tab change and update URL
  const handleTabChange = (value: string) => {
    setActiveTab(value);
    router.push(`/extract?tab=${value}`);
  };

  return (
    <main className="container mx-auto p-4 sm:p-8 space-y-6">
      {/* Page Header */}
      <div className="space-y-2">
        <h1 className="text-3xl font-bold tracking-tight">
          Extract Design Tokens
        </h1>
        <p className="text-muted-foreground">
          Upload a screenshot or connect to Figma to extract design tokens
        </p>
      </div>

      {/* Tabs for Screenshot vs Figma */}
      <Tabs value={activeTab} onValueChange={handleTabChange}>
        <TabsList className="grid w-full max-w-md grid-cols-2">
          <TabsTrigger value="screenshot">Screenshot</TabsTrigger>
          <TabsTrigger value="figma">Figma</TabsTrigger>
        </TabsList>

        {/* Screenshot Tab */}
        <TabsContent value="screenshot" className="space-y-4">
          {/* Compact Tips */}
          <CompactTips mode="screenshot" />

          <Card>
            <CardHeader>
              <CardTitle>Upload Screenshot</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Compact Upload Zone */}
              {!selectedFile && !tokens && (
                <div
                  className={`border-2 border-dashed rounded-lg p-6 text-center transition-colors ${
                    dragActive
                      ? "border-primary bg-primary/5"
                      : "border-muted-foreground/25"
                  }`}
                  onDragEnter={handleDrag}
                  onDragLeave={handleDrag}
                  onDragOver={handleDrag}
                  onDrop={handleDrop}
                >
                  <div className="flex flex-col items-center gap-3">
                    <Upload className="h-8 w-8 text-muted-foreground" />
                    <div className="space-y-2">
                      <p className="text-sm font-medium">
                        Drag and drop your screenshot here, or
                      </p>
                      <label htmlFor="file-upload">
                        <Button variant="outline" asChild>
                          <span>Browse Files</span>
                        </Button>
                        <input
                          id="file-upload"
                          type="file"
                          accept="image/png,image/jpeg,image/jpg"
                          onChange={handleFileChange}
                          className="hidden"
                        />
                      </label>
                    </div>
                    <p className="text-xs text-muted-foreground">
                      PNG or JPEG, max 10MB
                    </p>
                  </div>
                </div>
              )}

              {/* Selected File with Preview */}
              {selectedFile && !tokens && (
                <div className="space-y-4">
                  {/* Image Preview */}
                  {imagePreview && (
                    <div className="relative rounded-lg overflow-hidden border bg-gray-50">
                      <img
                        src={imagePreview}
                        alt="Screenshot preview"
                        className="w-full h-auto max-h-[500px] object-contain"
                      />
                    </div>
                  )}

                  {/* File Info and Actions */}
                  <div className="flex items-center justify-between gap-4">
                    <div className="flex items-center gap-3">
                      <FileImage className="h-5 w-5 text-muted-foreground" />
                      <div>
                        <p className="text-sm font-medium">
                          {selectedFile.name}
                        </p>
                        <p className="text-xs text-muted-foreground">
                          {(selectedFile.size / 1024).toFixed(0)} KB
                        </p>
                      </div>
                    </div>
                    <div className="flex gap-2">
                      <label htmlFor="file-upload-change">
                        <Button variant="outline" size="sm" asChild>
                          <span>Change</span>
                        </Button>
                        <input
                          id="file-upload-change"
                          type="file"
                          accept="image/png,image/jpeg,image/jpg"
                          onChange={handleFileChange}
                          className="hidden"
                        />
                      </label>
                      <Button onClick={handleUpload} disabled={isPending} size="sm">
                        {isPending ? "Extracting..." : "Extract Tokens"}
                      </Button>
                    </div>
                  </div>
                </div>
              )}

              {/* NEW: Validation Warnings */}
              {validationWarnings.length > 0 && (
                <Alert variant="warning">
                  <AlertTriangle className="h-4 w-4" />
                  <div className="ml-2">
                    <p className="font-medium text-sm">Quality Warnings</p>
                    <ul className="text-xs mt-1 space-y-1">
                      {validationWarnings.map((warning, i) => (
                        <li key={i}>• {warning}</li>
                      ))}
                    </ul>
                  </div>
                </Alert>
              )}

              {/* Progress */}
              {isPending && (
                <div className="space-y-2">
                  <Progress indeterminate className="h-2" />
                  <p className="text-sm text-muted-foreground text-center">
                    Analyzing screenshot with GPT-4V...
                  </p>
                </div>
              )}

              {/* Error */}
              {isError && (
                <Alert variant="error">
                  <p className="font-medium">Extraction Failed</p>
                  <p className="text-sm">{error?.message}</p>
                </Alert>
              )}

              {/* Extracted Tokens Preview */}
              {tokens && metadata && hasTokens() && (
                <div className="space-y-4">
                  <Alert variant="success">
                    <div className="flex items-start justify-between gap-4">
                      <div>
                        <p className="font-medium">✓ Tokens Extracted Successfully!</p>
                        <p className="text-sm mt-1">
                          From: {metadata.filename || 'Unknown file'}
                        </p>
                      </div>
                      {imagePreview && (
                        <div className="flex-shrink-0">
                          <img
                            src={imagePreview}
                            alt="Uploaded screenshot"
                            className="w-24 h-24 object-cover rounded border"
                          />
                        </div>
                      )}
                    </div>
                  </Alert>
                </div>
              )}

              {/* No tokens extracted warning */}
              {tokens && metadata && !hasTokens() && (
                <Alert variant="warning">
                  <AlertTriangle className="h-4 w-4" />
                  <div className="ml-2">
                    <p className="font-medium">No Design Tokens Extracted</p>
                    <p className="text-sm">
                      We couldn't identify any design tokens in this image. Try uploading a screenshot that clearly shows colors, typography, or spacing information.
                    </p>
                  </div>
                </Alert>
              )}
            </CardContent>
          </Card>

          {/* Token Editor */}
          {tokens && getEditorTokens() && hasTokens() && (
            <Card id="token-editor">
              <CardHeader>
                <CardTitle>Edit Tokens</CardTitle>
              </CardHeader>
              <CardContent>
                <TokenEditor
                  tokens={getEditorTokens()!}
                  confidence={getConfidenceScores()}
                />
              </CardContent>
            </Card>
          )}

          {/* Token Export */}
          {tokens && getEditorTokens() && hasTokens() && (
            <Card>
              <CardHeader>
                <CardTitle>Export Tokens</CardTitle>
              </CardHeader>
              <CardContent>
                <TokenExport
                  tokens={getEditorTokens()!}
                  metadata={{
                    method: "screenshot",
                    timestamp: new Date().toISOString(),
                  }}
                />
              </CardContent>
            </Card>
          )}

          {/* Navigation */}
          {tokens && hasTokens() && (
            <div className="flex justify-end">
              <Button asChild size="lg">
                <Link href="/requirements">
                  Continue to Requirements
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
              </Button>
            </div>
          )}
        </TabsContent>

        {/* Figma Tab */}
        <TabsContent value="figma" className="space-y-4">
          {/* Compact Tips */}
          <CompactTips mode="figma" />

          <Card>
            <CardHeader>
              <CardTitle>Figma Integration</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* PAT Input */}
              <div className="space-y-2">
                <label className="text-sm font-medium" htmlFor="figma-pat">
                  Figma Personal Access Token
                </label>
                <div className="flex gap-2">
                  <input
                    id="figma-pat"
                    type="password"
                    value={figmaPat}
                    onChange={(e) => {
                      setFigmaPat(e.target.value);
                      setIsPatValid(false);
                    }}
                    placeholder="figd_..."
                    className="flex-1 px-3 py-2 border rounded-md text-sm"
                    disabled={isPatValid}
                  />
                  {!isPatValid ? (
                    <Button
                      onClick={handleValidatePat}
                      disabled={!figmaPat.trim() || isAuthPending}
                    >
                      {isAuthPending ? "Validating..." : "Validate"}
                    </Button>
                  ) : (
                    <Button variant="outline" disabled>
                      <CheckCircle2 className="h-4 w-4 mr-2" />
                      Valid
                    </Button>
                  )}
                </div>
                <p className="text-xs text-muted-foreground">
                  Get your token from{" "}
                  <a
                    href="https://www.figma.com/developers/api#access-tokens"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="underline"
                  >
                    Figma Settings
                  </a>
                </p>
              </div>

              {/* Figma URL Input */}
              {isPatValid && (
                <div className="space-y-2">
                  <label className="text-sm font-medium" htmlFor="figma-url">
                    Figma File URL
                  </label>
                  <div className="flex gap-2">
                    <input
                      id="figma-url"
                      type="url"
                      value={figmaUrl}
                      onChange={(e) => setFigmaUrl(e.target.value)}
                      placeholder="https://www.figma.com/file/..."
                      className="flex-1 px-3 py-2 border rounded-md text-sm"
                    />
                    <Button
                      onClick={handleFigmaExtract}
                      disabled={!figmaUrl.trim() || isFigmaPending}
                    >
                      {isFigmaPending ? "Extracting..." : "Extract"}
                    </Button>
                  </div>
                  <p className="text-xs text-muted-foreground">
                    Paste the full URL of your Figma file
                  </p>
                </div>
              )}

              {/* Progress */}
              {isFigmaPending && (
                <div className="space-y-2">
                  <Progress indeterminate className="h-2" />
                  <p className="text-sm text-muted-foreground text-center">
                    Fetching file from Figma API...
                  </p>
                </div>
              )}

              {/* Cache Indicator */}
              {metadata?.cached && metadata?.extractionMethod === 'figma' && (
                <Alert>
                  <p className="text-sm">
                    ⚡ Results from cache (5 min TTL)
                  </p>
                </Alert>
              )}

              {/* Extracted Tokens Preview */}
              {tokens && metadata?.extractionMethod === 'figma' && hasTokens() && (
                <div className="space-y-4">
                  <Alert variant="success">
                    <p className="font-medium">Tokens Extracted Successfully!</p>
                    <p className="text-sm">
                      From: {metadata.filename || 'Figma file'}
                    </p>
                  </Alert>
                </div>
              )}

              {/* No tokens extracted warning for Figma */}
              {tokens && metadata?.extractionMethod === 'figma' && !hasTokens() && (
                <Alert variant="warning">
                  <AlertTriangle className="h-4 w-4" />
                  <div className="ml-2">
                    <p className="font-medium">No Design Tokens Extracted</p>
                    <p className="text-sm">
                      No published styles found in this Figma file. Make sure your design system has published color and text styles.
                    </p>
                  </div>
                </Alert>
              )}

              {/* Optional Detailed Guidance */}
              <Accordion type="single" collapsible className="mt-4">
                <AccordionItem value="figma-help">
                  <AccordionTrigger className="text-sm">
                    📚 Naming Conventions & Best Practices
                  </AccordionTrigger>
                  <AccordionContent>
                    <FigmaGuidance />
                  </AccordionContent>
                </AccordionItem>
              </Accordion>
            </CardContent>
          </Card>

          {/* Token Editor (shared for Figma) */}
          {tokens && metadata?.extractionMethod === 'figma' && getEditorTokens() && hasTokens() && (
            <Card>
              <CardHeader>
                <CardTitle>Edit Tokens</CardTitle>
              </CardHeader>
              <CardContent>
                <TokenEditor
                  tokens={getEditorTokens()!}
                  confidence={getConfidenceScores()}
                />
              </CardContent>
            </Card>
          )}

          {/* Token Export (shared for Figma) */}
          {tokens && metadata?.extractionMethod === 'figma' && getEditorTokens() && hasTokens() && (
            <Card>
              <CardHeader>
                <CardTitle>Export Tokens</CardTitle>
              </CardHeader>
              <CardContent>
                <TokenExport
                  tokens={getEditorTokens()!}
                  metadata={{
                    method: "figma",
                    timestamp: new Date().toISOString(),
                  }}
                />
              </CardContent>
            </Card>
          )}

          {/* Navigation (shared for Figma) */}
          {tokens && metadata?.extractionMethod === 'figma' && hasTokens() && (
            <div className="flex justify-end">
              <Button asChild size="lg">
                <Link href="/requirements">
                  Continue to Requirements
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
              </Button>
            </div>
          )}
        </TabsContent>
      </Tabs>
    </main>
  );
}
