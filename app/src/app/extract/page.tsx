"use client";

import { useState, useCallback } from "react";
import Link from "next/link";
import dynamic from "next/dynamic";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Alert } from "@/components/ui/alert";
import { Upload, FileImage, CheckCircle2, ArrowRight } from "lucide-react";
import { useTokenExtraction } from "@/lib/query/hooks/useTokenExtraction";
import { useFigmaAuth } from "@/lib/query/hooks/useFigmaAuth";
import { useFigmaExtraction } from "@/lib/query/hooks/useFigmaExtraction";
import { useTokenStore } from "@/stores/useTokenStore";
import { useUIStore } from "@/stores/useUIStore";
import type { TokenData } from "@/components/tokens/TokenEditor";

// Dynamic imports to avoid SSR issues with prismjs in CodeBlock
const TokenEditor = dynamic(() => import("@/components/tokens/TokenEditor").then(mod => ({ default: mod.TokenEditor })), { ssr: false });
const TokenExport = dynamic(() => import("@/components/tokens/TokenExport").then(mod => ({ default: mod.TokenExport })), { ssr: false });

export default function TokenExtractionPage() {
  const [activeTab, setActiveTab] = useState("screenshot");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [dragActive, setDragActive] = useState(false);
  
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

  // Get confidence scores from metadata
  const getConfidenceScores = (): Record<string, number> => {
    return (metadata as { confidence?: Record<string, number> })?.confidence || {};
  };

  // File validation
  const validateFile = (file: File): string | null => {
    const maxSize = 10 * 1024 * 1024; // 10MB
    const allowedTypes = ['image/png', 'image/jpeg', 'image/jpg'];

    if (!allowedTypes.includes(file.type)) {
      return 'Please upload a PNG or JPEG image';
    }

    if (file.size > maxSize) {
      return 'File size must be less than 10MB';
    }

    return null;
  };

  // Handle file selection
  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const validationError = validateFile(file);
      if (!validationError) {
        setSelectedFile(file);
      } else {
        showAlert('error', validationError);
      }
    }
  };

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

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const file = e.dataTransfer.files?.[0];
    if (file) {
      const validationError = validateFile(file);
      if (!validationError) {
        setSelectedFile(file);
      } else {
        showAlert('error', validationError);
      }
    }
  }, [showAlert]);

  // Handle upload
  const handleUpload = () => {
    if (selectedFile) {
      extractTokens(selectedFile);
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
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full max-w-md grid-cols-2">
          <TabsTrigger value="screenshot">Screenshot</TabsTrigger>
          <TabsTrigger value="figma">Figma</TabsTrigger>
        </TabsList>

        {/* Screenshot Tab */}
        <TabsContent value="screenshot" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Upload Screenshot</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Drag and Drop Zone */}
              <div
                className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
                  dragActive
                    ? "border-primary bg-primary/5"
                    : "border-muted-foreground/25"
                }`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
              >
                <div className="flex flex-col items-center gap-4">
                  <div className="rounded-full bg-muted p-4">
                    <Upload className="h-8 w-8 text-muted-foreground" />
                  </div>
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

              {/* Selected File */}
              {selectedFile && !tokens && (
                <div className="flex items-center gap-4 p-4 border rounded-lg">
                  <FileImage className="h-8 w-8 text-muted-foreground" />
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium truncate">
                      {selectedFile.name}
                    </p>
                    <p className="text-xs text-muted-foreground">
                      {(selectedFile.size / 1024).toFixed(0)} KB
                    </p>
                  </div>
                  <Button onClick={handleUpload} disabled={isPending}>
                    {isPending ? "Extracting..." : "Extract Tokens"}
                  </Button>
                </div>
              )}

              {/* Progress */}
              {isPending && (
                <div className="space-y-2">
                  <Progress value={66} className="h-2" />
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
              {tokens && metadata && (
                <div className="space-y-4">
                  <Alert variant="success">
                    <p className="font-medium">Tokens Extracted Successfully!</p>
                    <p className="text-sm">
                      From: {metadata.filename || 'Unknown file'}
                    </p>
                  </Alert>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Token Editor */}
          {tokens && getEditorTokens() && (
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

          {/* Token Export */}
          {tokens && getEditorTokens() && (
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
          {tokens && (
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
                  <Progress value={66} className="h-2" />
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
              {tokens && metadata?.extractionMethod === 'figma' && (
                <div className="space-y-4">
                  <Alert variant="success">
                    <p className="font-medium">Tokens Extracted Successfully!</p>
                    <p className="text-sm">
                      From: {metadata.filename || 'Figma file'}
                    </p>
                  </Alert>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Token Editor (shared for Figma) */}
          {tokens && metadata?.extractionMethod === 'figma' && getEditorTokens() && (
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
          {tokens && metadata?.extractionMethod === 'figma' && getEditorTokens() && (
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
          {tokens && metadata?.extractionMethod === 'figma' && (
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
