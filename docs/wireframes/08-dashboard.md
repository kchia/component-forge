# Wireframe: Dashboard

**Epic Reference**: Epic 0 - Project Setup, Epic 7 - Developer Experience  
**User Story**: As a developer, I want a dashboard to view my generated components and start new generations.

---

## Main Dashboard

```
┌──────────────────────────────────────────────────────────────────────┐
│  ComponentForge                    [?] Help    [👤] Profile    [⚙️]  │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐│
│  │                                                                ││
│  │  👋 Welcome back, Developer!                                   ││
│  │                                                                ││
│  │  Transform designs into production-ready components            ││
│  │                                                                ││
│  │  [+ New Generation]  [📁 Browse Library]  [📚 Patterns]       ││
│  │                                                                ││
│  └────────────────────────────────────────────────────────────────┘│
│                                                                      │
│  ┌───────────────────────────────────┐  ┌────────────────────────┐ │
│  │  Quick Stats                      │  │  Activity               │ │
│  │                                   │  │                         │ │
│  │  📊 12 Components Generated       │  │  Today                  │ │
│  │  ⭐ 8 Pattern Matches Found       │  │  • Button variant       │ │
│  │  ✓ 95% Average Quality Score      │  │    generated            │ │
│  │  💰 $2.40 AI Credits Used         │  │                         │ │
│  │                                   │  │  Yesterday              │ │
│  │                                   │  │  • Card component       │ │
│  │                                   │  │    created              │ │
│  │                                   │  │  • Input field added    │ │
│  └───────────────────────────────────┘  └────────────────────────┘ │
│                                                                      │
│  Recent Generations                                 [View All →]    │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                                                              │  │
│  │  ┌─────────────┬─────────────┬─────────────┬─────────────┐ │  │
│  │  │  Thumbnail  │ Name        │ Type        │ Status      │ │  │
│  │  ├─────────────┼─────────────┼─────────────┼─────────────┤ │  │
│  │  │  [Preview]  │ PrimaryBtn  │ Button      │ ✓ Ready    │ │  │
│  │  │             │ 2 min ago   │             │ [Export]    │ │  │
│  │  ├─────────────┼─────────────┼─────────────┼─────────────┤ │  │
│  │  │  [Preview]  │ ProductCard │ Card        │ ⏳ Review  │ │  │
│  │  │             │ 1 hour ago  │             │ [Continue]  │ │  │
│  │  ├─────────────┼─────────────┼─────────────┼─────────────┤ │  │
│  │  │  [Preview]  │ SearchInput │ Input       │ ✓ Ready    │ │  │
│  │  │             │ 3 hours ago │             │ [Export]    │ │  │
│  │  └─────────────┴─────────────┴─────────────┴─────────────┘ │  │
│  │                                                              │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  Pattern Library                                    [Browse All →]  │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐            │  │
│  │  │ Button │  │  Card  │  │ Input  │  │ Badge  │    +12     │  │
│  │  │  [•]   │  │  [•]   │  │  [•]   │  │  [•]   │    more    │  │
│  │  └────────┘  └────────┘  └────────┘  └────────┘            │  │
│  │  shadcn/ui  shadcn/ui  shadcn/ui  shadcn/ui                │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Navigation Sidebar (Expanded)

```
┌──────────────────┐
│  ComponentForge  │
├──────────────────┤
│                  │
│  📊 Dashboard    │ ← Active
│  ━━━━━━━━━━━━━━│
│                  │
│  + New           │
│    Generation    │
│                  │
│  📁 Components   │
│    Library       │
│                  │
│  📚 Pattern      │
│    Library       │
│                  │
│  📊 Analytics    │
│                  │
│  ⚙️ Settings     │
│                  │
│  ━━━━━━━━━━━━━━│
│                  │
│  [?] Help        │
│  👤 Profile      │
│  [←] Collapse    │
│                  │
└──────────────────┘
```

---

## Component Library View

```
┌──────────────────────────────────────────────────────────────────────┐
│  ComponentForge                    [?] Help    [👤] Profile    [⚙️]  │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  📁 Component Library                                               │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐│
│  │  [🔍 Search components...]     [Filter ▼]  [Sort: Recent ▼]  ││
│  └────────────────────────────────────────────────────────────────┘│
│                                                                      │
│  ┌────────────────┬────────────────┬────────────────────────────────┐│
│  │                │                │                                ││
│  │  ┌──────────┐ │  ┌──────────┐ │  ┌──────────┐                 ││
│  │  │          │ │  │          │ │  │          │                 ││
│  │  │ Preview  │ │  │ Preview  │ │  │ Preview  │                 ││
│  │  │          │ │  │          │ │  │          │                 ││
│  │  └──────────┘ │  └──────────┘ │  └──────────┘                 ││
│  │  PrimaryBtn    │  ProductCard   │  SearchInput                 ││
│  │  Button        │  Card          │  Input                       ││
│  │  2 min ago     │  1 hour ago    │  3 hours ago                 ││
│  │  v1.0.0        │  v1.2.1        │  v2.0.0                      ││
│  │                │                │                                ││
│  │  [View] [Edit] │  [View] [Edit] │  [View] [Edit]              ││
│  │  [Export]      │  [Export]      │  [Export]                    ││
│  │                │                │                                ││
│  ├────────────────┼────────────────┼────────────────────────────────┤
│  │                │                │                                ││
│  │  ┌──────────┐ │  ┌──────────┐ │  ┌──────────┐                 ││
│  │  │          │ │  │          │ │  │          │                 ││
│  │  │ Preview  │ │  │ Preview  │ │  │ Preview  │                 ││
│  │  │          │ │  │          │ │  │          │                 ││
│  │  └──────────┘ │  └──────────┘ │  └──────────┘                 ││
│  │  AlertBanner   │  SelectMenu    │  StatusBadge                 ││
│  │  Alert         │  Select        │  Badge                       ││
│  │  1 day ago     │  2 days ago    │  3 days ago                  ││
│  │  v1.0.0        │  v1.1.0        │  v1.0.0                      ││
│  │                │                │                                ││
│  │  [View] [Edit] │  [View] [Edit] │  [View] [Edit]              ││
│  │  [Export]      │  [Export]      │  [Export]                    ││
│  │                │                │                                ││
│  └────────────────┴────────────────┴────────────────────────────────┘│
│                                                                      │
│  [Load More...]                                                     │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Component Detail View

```
┌──────────────────────────────────────────────────────────────────────┐
│  ComponentForge                    [?] Help    [👤] Profile    [⚙️]  │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ← Back to Library                                                  │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐│
│  │                                                                ││
│  │  PrimaryBtn Button Component                      [⋮ Actions] ││
│  │  Created 2 minutes ago • v1.0.0 • By You                      ││
│  │                                                                ││
│  │  [Preview] [Code] [Storybook] [Tokens] [History]              ││
│  │  ━━━━━━━━                                                     ││
│  │                                                                ││
│  │  ┌──────────────────────────────────────────────────────────┐││
│  │  │                                                          │││
│  │  │                    Component Preview                     │││
│  │  │                                                          │││
│  │  │  ┌──────────────────────────────────────────────────┐  │││
│  │  │  │                                                  │  │││
│  │  │  │      [Primary Button]                           │  │││
│  │  │  │                                                  │  │││
│  │  │  │      [Secondary Button]                         │  │││
│  │  │  │                                                  │  │││
│  │  │  │      [Outline Button]                           │  │││
│  │  │  │                                                  │  │││
│  │  │  │      [Ghost Button]                             │  │││
│  │  │  │                                                  │  │││
│  │  │  └──────────────────────────────────────────────────┘  │││
│  │  │                                                          │││
│  │  │  Variant Controls:                                       │││
│  │  │  ○ Primary  ○ Secondary  ○ Outline  ○ Ghost             │││
│  │  │                                                          │││
│  │  │  Size Controls:                                          │││
│  │  │  ○ Small  ● Medium  ○ Large                              │││
│  │  │                                                          │││
│  │  │  State Controls:                                         │││
│  │  │  [ ] Disabled  [ ] Loading                               │││
│  │  │                                                          │││
│  │  └──────────────────────────────────────────────────────────┘││
│  │                                                                ││
│  └────────────────────────────────────────────────────────────────┘│
│                                                                      │
│  Component Information                                              │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Component Type: Button                                      │  │
│  │  Source: Screenshot (button-design.png)                      │  │
│  │  Pattern: shadcn/ui Button v1.2.3                            │  │
│  │  Quality Score: 96/100 ✓                                     │  │
│  │  Generated: 2 minutes ago                                    │  │
│  │  AI Cost: $0.18                                              │  │
│  │                                                               │  │
│  │  Props: variant, size, disabled, fullWidth                   │  │
│  │  Events: onClick, onKeyDown                                  │  │
│  │  Accessibility: ✓ WCAG AA Compliant                          │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  Quick Actions                                                      │
│                                                                      │
│  [📥 Export Component]  [🔄 Regenerate]  [📋 Copy Code]           │
│  [🎨 Edit Tokens]  [📝 Edit Requirements]  [🗑️ Delete]             │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Settings Screen

```
┌──────────────────────────────────────────────────────────────────────┐
│  ComponentForge                    [?] Help    [👤] Profile    [⚙️]  │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ⚙️ Settings                                                        │
│                                                                      │
│  ┌─────────────────┬──────────────────────────────────────────────┐│
│  │  General        │  General Settings                            ││
│  │  ━━━━━━━━━━━━━│                                              ││
│  │                 │  Theme                                        ││
│  │  Integrations   │  ┌──────────────────────────────────────┐   ││
│  │                 │  │ [Light ▼]                            │   ││
│  │  API Keys       │  └──────────────────────────────────────┘   ││
│  │                 │  Options: Light, Dark, System                ││
│  │  Preferences    │                                              ││
│  │                 │  Default Component Type                      ││
│  │  Billing        │  ┌──────────────────────────────────────┐   ││
│  │                 │  │ [Auto-detect ▼]                      │   ││
│  │  Team           │  └──────────────────────────────────────┘   ││
│  │                 │                                              ││
│  │  Profile        │  AI Processing                               ││
│  │                 │  [✓] Auto-generate requirements              ││
│  │                 │  [✓] Enable pattern matching                 ││
│  │                 │  [ ] Skip manual review                      ││
│  │                 │                                              ││
│  │                 │  Quality Validation                          ││
│  │                 │  [✓] Run TypeScript compiler                 ││
│  │                 │  [✓] Run accessibility checks                ││
│  │                 │  [✓] Run ESLint validation                   ││
│  │                 │                                              ││
│  │                 │                                              ││
│  │                 │                       [Cancel] [Save]        ││
│  │                 │                                              ││
│  └─────────────────┴──────────────────────────────────────────────┘│
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Integrations Tab

```
│  General        │  Figma Integration                               │
│                 │                                                  │
│  Integrations   │  ┌────────────────────────────────────────────┐ │
│  ━━━━━━━━━━━━━│  │  🎨 Figma                                 │ │
│                 │  │                                            │ │
│  API Keys       │  │  Status: ✓ Connected                      │ │
│                 │  │  Account: designer@company.com            │ │
│  Preferences    │  │  Last synced: 5 minutes ago               │ │
│                 │  │                                            │ │
│  Billing        │  │  [Disconnect]  [Sync Now]                 │ │
│                 │  └────────────────────────────────────────────┘ │
│  Team           │                                                  │
│                 │  Personal Access Token                           │
│  Profile        │  ┌────────────────────────────────────────────┐ │
│                 │  │ figd_••••••••••••••••••••••••••           │ │
│                 │  │ [Change Token]                             │ │
│                 │  └────────────────────────────────────────────┘ │
│                 │                                                  │
│                 │  File Access                                     │
│                 │  [✓] Read file structure                         │
│                 │  [✓] Extract styles and components               │
│                 │  [✓] Access design tokens                        │
│                 │                                                  │
│                 │  ┌────────────────────────────────────────────┐ │
│                 │  │  OpenAI Integration                        │ │
│                 │  │                                            │ │
│                 │  │  Status: ✓ Connected                      │ │
│                 │  │  Model: gpt-4o                            │ │
│                 │  │  Usage: $2.40 / $50.00 (4.8%)            │ │
│                 │  │                                            │ │
│                 │  │  [Manage API Key]                          │ │
│                 │  └────────────────────────────────────────────┘ │
```

---

## Empty States

### No Components Yet

```
┌──────────────────────────────────────────────────────────────────────┐
│                                                                      │
│                        📁                                            │
│                                                                      │
│              No components yet                                       │
│                                                                      │
│        Start by generating your first component                     │
│        from a design screenshot or Figma file                       │
│                                                                      │
│              [+ Create Your First Component]                         │
│                                                                      │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### No Search Results

```
┌──────────────────────────────────────────────────────────────────────┐
│                                                                      │
│                        🔍                                            │
│                                                                      │
│              No results found for "Card"                             │
│                                                                      │
│        Try adjusting your search or browse all components           │
│                                                                      │
│              [Clear Search]  [Browse All]                            │
│                                                                      │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Responsive Behavior

### Mobile Dashboard (<768px)

```
┌──────────────────────────────┐
│  ComponentForge         [☰]  │
├──────────────────────────────┤
│                              │
│  👋 Welcome back!            │
│                              │
│  [+ New Generation]          │
│  [📁 Browse Library]         │
│                              │
│  ┌──────────────────────────┐│
│  │  Stats                   ││
│  │  📊 12 Components        ││
│  │  ⭐ 8 Matches Found      ││
│  │  ✓ 95% Quality          ││
│  └──────────────────────────┘│
│                              │
│  Recent Generations          │
│                              │
│  ┌──────────────────────────┐│
│  │  [Preview]               ││
│  │  PrimaryBtn              ││
│  │  Button • 2 min ago      ││
│  │  [Export]                ││
│  └──────────────────────────┘│
│                              │
│  ┌──────────────────────────┐│
│  │  [Preview]               ││
│  │  ProductCard             ││
│  │  Card • 1 hour ago       ││
│  │  [Continue]              ││
│  └──────────────────────────┘│
│                              │
└──────────────────────────────┘
```

---

## Next Steps

From dashboard, users can:
- → **01-upload-design.md**: Start new component generation
- → **Component Detail**: View/edit existing components
- → **Settings**: Configure integrations and preferences
- → **Pattern Library**: Browse available patterns
