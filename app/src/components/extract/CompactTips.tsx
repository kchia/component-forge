"use client";

import { Info } from "lucide-react";
import { Button } from "@/components/ui/button";

interface CompactTipsProps {
  mode: "screenshot" | "figma";
}

export function CompactTips({ mode }: CompactTipsProps) {
  if (mode === "screenshot") {
    return (
      <div className="mb-4 p-4 bg-muted/30 rounded-lg border border-muted">
        <div className="flex items-start gap-3">
          <Info className="h-5 w-5 text-primary mt-0.5 flex-shrink-0" />
          <div className="flex-1 space-y-2">
            <p className="text-sm font-medium">Tips for best results:</p>
            <ul className="text-sm text-muted-foreground space-y-1">
              <li>• Upload high-resolution screenshots (min 1024px wide, PNG/JPG/WebP)</li>
              <li>• Focus on design system pages with clear color palettes and typography scales</li>
              <li>• Include semantic labels in your design (e.g., "Primary Color", "Heading XL")</li>
            </ul>
            <div className="flex gap-2 mt-3">
              <Button
                variant="link"
                size="sm"
                className="h-auto p-0 text-xs"
                onClick={() => {
                  // Scroll to examples or open modal in future
                  const accordion = document.querySelector('[data-state]');
                  if (accordion) {
                    (accordion as HTMLElement).click();
                  }
                }}
              >
                View Examples →
              </Button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (mode === "figma") {
    return (
      <div className="mb-4 p-4 bg-muted/30 rounded-lg border border-muted">
        <div className="flex items-start gap-3">
          <Info className="h-5 w-5 text-primary mt-0.5 flex-shrink-0" />
          <div className="flex-1 space-y-2">
            <p className="text-sm font-medium">Figma Requirements:</p>
            <ul className="text-sm text-muted-foreground space-y-1">
              <li>• File must have published local styles (colors and text)</li>
              <li>• Personal Access Token required with file read permissions</li>
              <li>• Use semantic names like "Primary/Blue" or "Heading/XL" for best results</li>
            </ul>
            <div className="flex gap-2 mt-3">
              <Button
                variant="link"
                size="sm"
                className="h-auto p-0 text-xs"
                asChild
              >
                <a
                  href="https://help.figma.com/hc/en-us/articles/8085703771159-Manage-personal-access-tokens"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Get Figma Token →
                </a>
              </Button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return null;
}
