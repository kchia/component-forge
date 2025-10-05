"use client";

import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { CheckCircle2, XCircle } from "lucide-react";
import Image from "next/image";

interface Example {
  type: "good" | "bad";
  image: string;
  title: string;
  description: string;
  annotations: string[];
}

const examples: Example[] = [
  {
    type: "good",
    image: "/examples/good-color-palette.png",
    title: "Color Palette with Semantic Labels",
    description: "Clear color swatches with descriptive names",
    annotations: [
      "Colors are labeled with semantic names (Primary, Secondary, etc.)",
      "Hex values are visible",
      "High contrast, easy to read",
      "Organized in a grid layout"
    ]
  },
  {
    type: "good",
    image: "/examples/good-typography-scale.png",
    title: "Typography Scale",
    description: "Font sizes displayed with examples",
    annotations: [
      "Font sizes clearly labeled (XL, Large, Base, Small)",
      "Actual text examples shown at each size",
      "Font weights indicated",
      "Line heights visible"
    ]
  },
  {
    type: "good",
    image: "/examples/good-design-system.png",
    title: "Complete Design System Page",
    description: "Comprehensive design tokens in one view",
    annotations: [
      "All token categories visible (colors, typography, spacing)",
      "Well-organized sections",
      "Consistent labeling",
      "High resolution export"
    ]
  },
  {
    type: "bad",
    image: "/examples/bad-full-app.png",
    title: "Full Application Screenshot",
    description: "Too much visual complexity",
    annotations: [
      "Too many UI elements create visual noise",
      "Design tokens not clearly isolated",
      "Hard to distinguish semantic roles",
      "Low extraction confidence expected"
    ]
  },
  {
    type: "bad",
    image: "/examples/bad-low-res.png",
    title: "Low Resolution Image",
    description: "Blurry or pixelated screenshot",
    annotations: [
      "Text is hard to read",
      "Colors may not be accurate",
      "Details are lost",
      "May cause extraction errors"
    ]
  },
  {
    type: "bad",
    image: "/examples/bad-no-labels.png",
    title: "No Semantic Labels",
    description: "Colors without context",
    annotations: [
      "No indication of token purpose",
      "AI must guess semantic roles",
      "Lower confidence scores",
      "May require manual editing"
    ]
  }
];

export function ExampleComparison() {
  const goodExamples = examples.filter((ex) => ex.type === "good");
  const badExamples = examples.filter((ex) => ex.type === "bad");

  return (
    <div className="space-y-8">
      {/* Good Examples */}
      <div>
        <div className="flex items-center gap-2 mb-4">
          <CheckCircle2 className="h-6 w-6 text-success" />
          <h3 className="text-xl font-semibold">Good Examples</h3>
          <Badge variant="success">High Confidence Extraction</Badge>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {goodExamples.map((example, idx) => (
            <Card key={idx} className="overflow-hidden">
              <div className="aspect-video relative bg-muted">
                <Image
                  src={example.image}
                  alt={example.title}
                  fill
                  className="object-cover"
                />
              </div>
              <div className="p-4">
                <h4 className="font-semibold mb-1">{example.title}</h4>
                <p className="text-sm text-muted-foreground mb-3">
                  {example.description}
                </p>
                <ul className="space-y-1">
                  {example.annotations.map((annotation, i) => (
                    <li key={i} className="text-xs flex items-start gap-2">
                      <CheckCircle2 className="h-3 w-3 text-success mt-0.5 flex-shrink-0" />
                      <span>{annotation}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </Card>
          ))}
        </div>
      </div>

      {/* Bad Examples */}
      <div>
        <div className="flex items-center gap-2 mb-4">
          <XCircle className="h-6 w-6 text-destructive" />
          <h3 className="text-xl font-semibold">Avoid These</h3>
          <Badge variant="error">Poor Extraction Quality</Badge>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {badExamples.map((example, idx) => (
            <Card key={idx} className="overflow-hidden border-destructive/50">
              <div className="aspect-video relative bg-muted">
                <Image
                  src={example.image}
                  alt={example.title}
                  fill
                  className="object-cover opacity-60"
                />
              </div>
              <div className="p-4">
                <h4 className="font-semibold mb-1">{example.title}</h4>
                <p className="text-sm text-muted-foreground mb-3">
                  {example.description}
                </p>
                <ul className="space-y-1">
                  {example.annotations.map((annotation, i) => (
                    <li key={i} className="text-xs flex items-start gap-2">
                      <XCircle className="h-3 w-3 text-destructive mt-0.5 flex-shrink-0" />
                      <span>{annotation}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}
