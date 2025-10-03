# Wireframe: Requirement Proposal & Review

**Epic Reference**: Epic 2 - Requirement Proposal & Review  
**User Story**: As a developer, I want to review AI-generated component requirements so that the generated code meets my needs.

---

## Screen Layout

```
┌──────────────────────────────────────────────────────────────────────┐
│  ComponentForge                    [?] Help    [👤] Profile    [⚙️]  │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ← Back to Tokens                                                   │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐│
│  │  Step 3 of 6: Review Requirements                             ││
│  │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ││
│  │  [✓] [✓] [3] [4] [5] [6]                                      ││
│  │  Upload  Extract  Review  Select  Generate  Validate          ││
│  └────────────────────────────────────────────────────────────────┘│
│                                                                      │
│  ┌──────────────────┬──────────────────────────────────────────────┐│
│  │                  │                                              ││
│  │  Component Info  │  AI-Generated Requirements                  ││
│  │                  │                                              ││
│  │  ┌────────────┐ │  ⏳ Analyzing component...                  ││
│  │  │            │ │                                              ││
│  │  │  [Image]   │ │  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░ 82%                 ││
│  │  │  Preview   │ │                                              ││
│  │  │            │ │  • Inferring component type                 ││
│  │  │            │ │  • Detecting props and variants             ││
│  │  └────────────┘ │  • Identifying events and states            ││
│  │                  │  • Checking accessibility needs             ││
│  │  Detected Type:  │                                              ││
│  │  🤔 Analyzing... │  Estimated time: ~12 seconds                ││
│  │                  │                                              ││
│  └──────────────────┴──────────────────────────────────────────────┘│
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## After Analysis

```
┌──────────────────────────────────────────────────────────────────────┐
│  ComponentForge                    [?] Help    [👤] Profile    [⚙️]  │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ← Back to Tokens                                                   │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐│
│  │  Step 3 of 6: Review Requirements                             ││
│  │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ││
│  │  [✓] [✓] [✓] [4] [5] [6]                                      ││
│  └────────────────────────────────────────────────────────────────┘│
│                                                                      │
│  ┌──────────────────┬──────────────────────────────────────────────┐│
│  │  Component Info  │  AI-Generated Requirements                  ││
│  │                  │                                              ││
│  │  ┌────────────┐ │  ✓ Analysis complete (11.8s)                ││
│  │  │            │ │                                              ││
│  │  │  [Image]   │ │  [Props] [Events] [States] [A11y]           ││
│  │  │  Preview   │ │  ━━━━━━━                                    ││
│  │  │            │ │                                              ││
│  │  │            │ │  Props (4 requirements)                     ││
│  │  └────────────┘ │                                              ││
│  │                  │  ┌──────────────────────────────────────┐  ││
│  │  Detected Type:  │  │ variant                              │  ││
│  │  🔘 Button       │  │ Type: enum                           │  ││
│  │  [Change]        │  │ Values: "primary" | "secondary" |    │  ││
│  │                  │  │         "outline" | "ghost"          │  ││
│  │  Properties:     │  │                                       │  ││
│  │  • Interactive   │  │ Rationale: Multiple button styles    │  ││
│  │  • Clickable     │  │ detected in design                   │  ││
│  │  • Has variants  │  │                                       │  ││
│  │                  │  │ Confidence: 95% ✓                    │  ││
│  │                  │  │                                       │  ││
│  │                  │  │ [✓ Accept] [Edit] [Remove]          │  ││
│  │                  │  └──────────────────────────────────────┘  ││
│  │                  │                                              ││
│  │                  │  ┌──────────────────────────────────────┐  ││
│  │                  │  │ size                                 │  ││
│  │                  │  │ Type: enum                           │  ││
│  │                  │  │ Values: "sm" | "md" | "lg"          │  ││
│  │                  │  │                                       │  ││
│  │                  │  │ Rationale: Standard size variants    │  ││
│  │                  │  │ for buttons                          │  ││
│  │                  │  │                                       │  ││
│  │                  │  │ Confidence: 88% ✓                    │  ││
│  │                  │  │                                       │  ││
│  │                  │  │ [✓ Accept] [Edit] [Remove]          │  ││
│  │                  │  └──────────────────────────────────────┘  ││
│  │                  │                                              ││
│  │                  │  ┌──────────────────────────────────────┐  ││
│  │                  │  │ disabled                             │  ││
│  │                  │  │ Type: boolean                        │  ││
│  │                  │  │ Default: false                       │  ││
│  │                  │  │                                       │  ││
│  │                  │  │ Rationale: Common interactive state  │  ││
│  │                  │  │                                       │  ││
│  │                  │  │ Confidence: 92% ✓                    │  ││
│  │                  │  │                                       │  ││
│  │                  │  │ [✓ Accept] [Edit] [Remove]          │  ││
│  │                  │  └──────────────────────────────────────┘  ││
│  │                  │                                              ││
│  │                  │  ┌──────────────────────────────────────┐  ││
│  │                  │  │ fullWidth                            │  ││
│  │                  │  │ Type: boolean                        │  ││
│  │                  │  │ Default: false                       │  ││
│  │                  │  │                                       │  ││
│  │                  │  │ Rationale: Layout flexibility        │  ││
│  │                  │  │                                       │  ││
│  │                  │  │ Confidence: 76% ⚠                    │  ││
│  │                  │  │                                       │  ││
│  │                  │  │ [○ Review] [Edit] [Remove]          │  ││
│  │                  │  └──────────────────────────────────────┘  ││
│  │                  │                                              ││
│  │                  │  [+ Add Prop]                               ││
│  │                  │                                              ││
│  └──────────────────┴──────────────────────────────────────────────┘│
│                                                                      │
│  Summary: 4 props, 2 events, 3 states, 5 a11y requirements         │
│  Low confidence items: 2 (review recommended)                       │
│                                                                      │
│                                    [← Back] [Next: Select Pattern →]│
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Events Tab

```
│  [Props] [Events] [States] [A11y]                                  │
│          ━━━━━━━━                                                  │
│                                                                      │
│  Events (2 requirements)                                            │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ onClick                                                      │  │
│  │ Type: (event: MouseEvent) => void                           │  │
│  │                                                               │  │
│  │ Rationale: Primary interaction for button component         │  │
│  │                                                               │  │
│  │ Confidence: 98% ✓                                            │  │
│  │                                                               │  │
│  │ [✓ Accept] [Edit] [Remove]                                  │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ onKeyDown                                                    │  │
│  │ Type: (event: KeyboardEvent) => void                        │  │
│  │                                                               │  │
│  │ Rationale: Keyboard accessibility (Enter, Space)            │  │
│  │                                                               │  │
│  │ Confidence: 89% ✓                                            │  │
│  │                                                               │  │
│  │ [✓ Accept] [Edit] [Remove]                                  │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  [+ Add Event]                                                      │
```

---

## States Tab

```
│  [Props] [Events] [States] [A11y]                                  │
│                   ━━━━━━━                                          │
│                                                                      │
│  States (3 requirements)                                            │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ :hover                                                       │  │
│  │ Description: Mouse over state                                │  │
│  │ Visual Changes:                                              │  │
│  │ • Background opacity change                                  │  │
│  │ • Cursor pointer                                             │  │
│  │                                                               │  │
│  │ Confidence: 94% ✓                                            │  │
│  │                                                               │  │
│  │ [✓ Accept] [Edit] [Remove]                                  │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ :focus                                                       │  │
│  │ Description: Keyboard focus state                            │  │
│  │ Visual Changes:                                              │  │
│  │ • Focus ring (2px outline)                                   │  │
│  │ • Contrast: 3:1 minimum                                      │  │
│  │                                                               │  │
│  │ Confidence: 96% ✓                                            │  │
│  │                                                               │  │
│  │ [✓ Accept] [Edit] [Remove]                                  │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ :active                                                      │  │
│  │ Description: Pressed/clicked state                           │  │
│  │ Visual Changes:                                              │  │
│  │ • Scale transform (0.95)                                     │  │
│  │ • Darker background                                          │  │
│  │                                                               │  │
│  │ Confidence: 82% ✓                                            │  │
│  │                                                               │  │
│  │ [✓ Accept] [Edit] [Remove]                                  │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  [+ Add State]                                                      │
```

---

## Accessibility Tab

```
│  [Props] [Events] [States] [A11y]                                  │
│                             ━━━━━                                  │
│                                                                      │
│  Accessibility (5 requirements)                                     │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ ARIA Role                                                    │  │
│  │ Value: button                                                │  │
│  │                                                               │  │
│  │ Rationale: Semantic HTML button element                      │  │
│  │                                                               │  │
│  │ Confidence: 99% ✓                                            │  │
│  │                                                               │  │
│  │ [✓ Accept] [Edit] [Remove]                                  │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ aria-disabled                                                │  │
│  │ Required: When disabled=true                                 │  │
│  │                                                               │  │
│  │ Rationale: Announce disabled state to screen readers        │  │
│  │                                                               │  │
│  │ Confidence: 94% ✓                                            │  │
│  │                                                               │  │
│  │ [✓ Accept] [Edit] [Remove]                                  │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ Keyboard Navigation                                          │  │
│  │ Keys: Tab, Enter, Space                                      │  │
│  │                                                               │  │
│  │ Rationale: Full keyboard accessibility required             │  │
│  │                                                               │  │
│  │ Confidence: 97% ✓                                            │  │
│  │                                                               │  │
│  │ [✓ Accept] [Edit] [Remove]                                  │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ Focus Indicator                                              │  │
│  │ Specification: 2px solid outline, 3:1 contrast              │  │
│  │                                                               │  │
│  │ Rationale: WCAG 2.1 Focus Visible requirement               │  │
│  │                                                               │  │
│  │ Confidence: 91% ✓                                            │  │
│  │                                                               │  │
│  │ [✓ Accept] [Edit] [Remove]                                  │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ Color Contrast                                               │  │
│  │ Minimum: 4.5:1 (text), 3:1 (UI components)                  │  │
│  │                                                               │  │
│  │ Rationale: WCAG AA compliance required                       │  │
│  │                                                               │  │
│  │ Confidence: 88% ✓                                            │  │
│  │                                                               │  │
│  │ [✓ Accept] [Edit] [Remove]                                  │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  [+ Add A11y Requirement]                                           │
```

---

## Bulk Actions Bar

```
┌──────────────────────────────────────────────────────────────────────┐
│  ✓ 12 of 14 requirements selected                                   │
│                                                                      │
│  [✓ Accept All Selected] [Edit Selected] [Remove Selected]         │
│                                              [Clear Selection]      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Component Type Change Modal

```
┌──────────────────────────────────────────────────────────────────────┐
│  Change Component Type                                         [×]   │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Current: Button (95% confidence)                                   │
│                                                                      │
│  Select new component type:                                          │
│                                                                      │
│  ○ Button       (95%)  ← Recommended                               │
│  ○ Card         (12%)                                               │
│  ○ Input        (8%)                                                │
│  ○ Select       (5%)                                                │
│  ○ Badge        (3%)                                                │
│  ○ Alert        (2%)                                                │
│  ○ Custom/Other                                                     │
│                                                                      │
│  ⚠️ Changing the component type will regenerate requirements        │
│     and may result in different props and behaviors.                │
│                                                                      │
│                                           [Cancel] [Change Type]    │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Edit Requirement Modal

```
┌──────────────────────────────────────────────────────────────────────┐
│  Edit Requirement: variant                                     [×]   │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Name                                                                │
│  ┌────────────────────────────────────────────────────────────────┐│
│  │ variant                                                        ││
│  └────────────────────────────────────────────────────────────────┘│
│                                                                      │
│  Type                                                                │
│  ┌────────────────────────────────────────────────────────────────┐│
│  │ [enum ▼]                                                       ││
│  └────────────────────────────────────────────────────────────────┘│
│  Options: string, number, boolean, enum, object, array              │
│                                                                      │
│  Values (for enum)                                                  │
│  ┌────────────────────────────────────────────────────────────────┐│
│  │ • "primary"                                        [Remove]    ││
│  │ • "secondary"                                      [Remove]    ││
│  │ • "outline"                                        [Remove]    ││
│  │ • "ghost"                                          [Remove]    ││
│  │ [+ Add Value]                                                  ││
│  └────────────────────────────────────────────────────────────────┘│
│                                                                      │
│  Default Value (Optional)                                           │
│  ┌────────────────────────────────────────────────────────────────┐│
│  │ "primary"                                                      ││
│  └────────────────────────────────────────────────────────────────┘│
│                                                                      │
│  Required                                                            │
│  [×] This prop is required                                          │
│                                                                      │
│  Description                                                         │
│  ┌────────────────────────────────────────────────────────────────┐│
│  │ Visual style variant of the button. Controls colors,          ││
│  │ background, and border styling.                                ││
│  └────────────────────────────────────────────────────────────────┘│
│                                                                      │
│  AI Rationale                                                        │
│  Multiple button styles detected in design                          │
│  Confidence: 95% ✓                                                 │
│                                                                      │
│                                                  [Cancel] [Save]    │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Export Requirements

```
┌──────────────────────────────────────────────────────────────────────┐
│  Export Requirements                                           [×]   │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Download your approved requirements as JSON for later use.         │
│                                                                      │
│  File Format                                                         │
│  ○ JSON (recommended)                                               │
│  ○ TypeScript Interface                                             │
│  ○ Markdown Documentation                                           │
│                                                                      │
│  Include                                                             │
│  [✓] Props                                                          │
│  [✓] Events                                                         │
│  [✓] States                                                         │
│  [✓] Accessibility Requirements                                     │
│  [✓] AI Confidence Scores                                           │
│  [ ] Rationales                                                     │
│                                                                      │
│  Preview:                                                            │
│  ┌────────────────────────────────────────────────────────────────┐│
│  │ {                                                              ││
│  │   "componentType": "Button",                                   ││
│  │   "props": [                                                   ││
│  │     {                                                          ││
│  │       "name": "variant",                                       ││
│  │       "type": "enum",                                          ││
│  │       "values": ["primary", "secondary", ...],                 ││
│  │       "confidence": 0.95                                       ││
│  │     },                                                         ││
│  │     ...                                                        ││
│  │   ]                                                            ││
│  │ }                                                              ││
│  └────────────────────────────────────────────────────────────────┘│
│                                                                      │
│                                      [Cancel] [Download JSON]       │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Accessibility Features

### Keyboard Navigation
- **Tab**: Navigate requirements
- **Space**: Toggle accept/reject
- **Enter**: Edit requirement
- **Delete**: Remove requirement
- **Ctrl/Cmd + A**: Select all

### Screen Reader Announcements
- "Button component detected with 95% confidence"
- "4 props, 2 events, 3 states, 5 accessibility requirements proposed"
- "variant prop: enum type with 95% confidence"
- "Low confidence requirement flagged for review"

---

## State Management

```typescript
interface RequirementState {
  componentType: string;
  componentConfidence: number;
  props: Requirement[];
  events: Requirement[];
  states: Requirement[];
  accessibility: Requirement[];
  selectedIds: Set<string>;
  activeTab: 'props' | 'events' | 'states' | 'a11y';
}

interface Requirement {
  id: string;
  name: string;
  type: string;
  values?: string[];
  description: string;
  rationale: string;
  confidence: number;
  status: 'pending' | 'accepted' | 'rejected' | 'edited';
}
```

---

## Next Steps

After requirement approval:
- → **04-pattern-selection.md**: AI retrieves matching shadcn/ui patterns
- User can export requirements or save draft
