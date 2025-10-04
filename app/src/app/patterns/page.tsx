"use client";

import Link from "next/link";
import { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { PatternCard } from "@/components/composite/PatternCard";
import { ArrowRight, Search } from "lucide-react";

// Placeholder patterns (will be replaced with Epic 3 backend)
const placeholderPatterns = [
  {
    id: "1",
    name: "Primary Button",
    description: "Standard button component with variants",
    confidence: 0.95,
    preview: "Button",
  },
  {
    id: "2",
    name: "Input Field",
    description: "Form input with validation support",
    confidence: 0.88,
    preview: "Input",
  },
  {
    id: "3",
    name: "Card Container",
    description: "Flexible card layout component",
    confidence: 0.92,
    preview: "Card",
  },
  {
    id: "4",
    name: "Alert Banner",
    description: "Alert component with severity levels",
    confidence: 0.78,
    preview: "Alert",
  },
];

export default function PatternsPage() {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedPattern, setSelectedPattern] = useState<string | null>(null);

  const filteredPatterns = placeholderPatterns.filter((pattern) =>
    pattern.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    pattern.description.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <main className="container mx-auto p-4 sm:p-8 space-y-6">
      {/* Page Header */}
      <div className="space-y-2">
        <h1 className="text-3xl font-bold tracking-tight">
          Select Design Patterns
        </h1>
        <p className="text-muted-foreground">
          Choose from AI-matched design patterns for your component
        </p>
      </div>

      {/* Search */}
      <div className="relative max-w-md">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
        <Input
          placeholder="Search patterns..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="pl-10"
        />
      </div>

      {/* Patterns Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredPatterns.map((pattern) => (
          <PatternCard
            key={pattern.id}
            patternId={pattern.id}
            name={pattern.name}
            version="1.0.0"
            matchScore={pattern.confidence}
            metadata={{
              description: pattern.description,
            }}
            onSelect={() => setSelectedPattern(pattern.id)}
            onPreview={() => setSelectedPattern(pattern.id)}
          />
        ))}
      </div>

      {/* Placeholder Note */}
      <Card>
        <CardContent className="py-6">
          <p className="text-sm text-muted-foreground text-center">
            <strong>Note:</strong> These are placeholder patterns. Real patterns will be retrieved by Epic 3 backend.
          </p>
        </CardContent>
      </Card>

      {/* Navigation */}
      <div className="flex justify-between">
        <Button asChild variant="outline">
          <Link href="/requirements">← Back to Requirements</Link>
        </Button>
        <Button asChild size="lg">
          <Link href="/preview">
            Preview Component
            <ArrowRight className="ml-2 h-4 w-4" />
          </Link>
        </Button>
      </div>

      {/* Pattern Preview Dialog */}
      <Dialog open={!!selectedPattern} onOpenChange={() => setSelectedPattern(null)}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>
              {placeholderPatterns.find((p) => p.id === selectedPattern)?.name}
            </DialogTitle>
          </DialogHeader>
          <div className="py-4">
            <p className="text-sm text-muted-foreground">
              Pattern preview will be available with Epic 3 backend integration.
            </p>
          </div>
        </DialogContent>
      </Dialog>
    </main>
  );
}
