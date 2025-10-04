"use client";

import { useState } from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function TokenExtractionPage() {
  const [activeTab, setActiveTab] = useState("screenshot");

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
            <CardContent>
              <div className="text-center py-8 text-muted-foreground">
                <p>Screenshot upload coming in next commit...</p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Figma Tab */}
        <TabsContent value="figma" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Figma Integration</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-center py-8 text-muted-foreground">
                <p>Figma integration coming in next commit...</p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </main>
  );
}
