"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { useWorkflowStore } from "@/stores/useWorkflowStore";
import { useOnboardingStore } from "@/stores/useOnboardingStore";
import { Home, Upload, FileCheck, Layers, Eye, Menu, X, HelpCircle } from "lucide-react";
import { useState } from "react";

const navItems = [
  { href: "/", label: "Dashboard", icon: Home },
  { href: "/extract", label: "Extract", icon: Upload },
  { href: "/requirements", label: "Requirements", icon: FileCheck },
  { href: "/patterns", label: "Patterns", icon: Layers },
  { href: "/preview", label: "Preview", icon: Eye },
];

export function Navigation() {
  const pathname = usePathname();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const progress = useWorkflowStore((state) => state.progress);
  const { resetOnboarding } = useOnboardingStore();

  return (
    <nav className="border-b bg-background">
      <div className="container mx-auto px-4 sm:px-8">
        <div className="flex h-16 items-center justify-between">
          {/* Logo */}
          <Link href="/" className="flex items-center space-x-2">
            <div className="h-8 w-8 rounded-md bg-primary flex items-center justify-center">
              <span className="text-primary-foreground font-bold text-sm">CF</span>
            </div>
            <span className="font-bold text-lg hidden sm:inline">ComponentForge</span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = pathname === item.href;
              return (
                <Link key={item.href} href={item.href}>
                  <Button
                    variant={isActive ? "default" : "ghost"}
                    size="sm"
                    className={cn(
                      "gap-2",
                      isActive && "bg-primary text-primary-foreground"
                    )}
                  >
                    <Icon className="h-4 w-4" />
                    {item.label}
                  </Button>
                </Link>
              );
            })}
            
            {/* Help Button */}
            <Button
              variant="ghost"
              size="sm"
              onClick={() => resetOnboarding()}
              className="gap-2"
              aria-label="Show help and onboarding"
            >
              <HelpCircle className="h-4 w-4" />
              Help
            </Button>
          </div>

          {/* Mobile Menu Button */}
          <Button
            variant="ghost"
            size="sm"
            className="md:hidden"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          >
            {mobileMenuOpen ? (
              <X className="h-5 w-5" />
            ) : (
              <Menu className="h-5 w-5" />
            )}
          </Button>
        </div>

        {/* Workflow Progress */}
        {progress > 0 && (
          <div className="pb-2 px-4">
            <div className="flex items-center gap-2">
              <Progress value={progress} className="h-1" />
              <span className="text-xs text-muted-foreground min-w-[3ch]">
                {progress}%
              </span>
            </div>
          </div>
        )}
      </div>

      {/* Mobile Navigation */}
      {mobileMenuOpen && (
        <div className="md:hidden border-t bg-background">
          <div className="container mx-auto px-4 py-2 space-y-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = pathname === item.href;
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  onClick={() => setMobileMenuOpen(false)}
                >
                  <Button
                    variant={isActive ? "default" : "ghost"}
                    size="sm"
                    className={cn(
                      "w-full justify-start gap-2",
                      isActive && "bg-primary text-primary-foreground"
                    )}
                  >
                    <Icon className="h-4 w-4" />
                    {item.label}
                  </Button>
                </Link>
              );
            })}
            
            {/* Help Button in Mobile Menu */}
            <Button
              variant="ghost"
              size="sm"
              onClick={() => {
                resetOnboarding();
                setMobileMenuOpen(false);
              }}
              className="w-full justify-start gap-2"
              aria-label="Show help and onboarding"
            >
              <HelpCircle className="h-4 w-4" />
              Help
            </Button>
          </div>
        </div>
      )}
    </nav>
  );
}
