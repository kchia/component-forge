# Wireframe: Upload Design

**Epic Reference**: Epic 1 - Design Token Extraction  
**User Story**: As a developer, I want to upload a design so that I can generate a component from it.

---

## Screen Layout

```
┌──────────────────────────────────────────────────────────────────────┐
│  ComponentForge                    [?] Help    [👤] Profile    [⚙️]  │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ← Back to Dashboard                                                │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐│
│  │                                                                ││
│  │  Step 1 of 6: Upload Design                                   ││
│  │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ││
│  │  [1] [2] [3] [4] [5] [6]                                      ││
│  │  Upload  Extract  Review  Select  Generate  Validate          ││
│  │                                                                ││
│  └────────────────────────────────────────────────────────────────┘│
│                                                                      │
│  Choose your design input method                                    │
│                                                                      │
│  ┌─────────────────────────┐  ┌─────────────────────────┐         │
│  │  📷 Upload Screenshot   │  │  🎨 Connect Figma       │         │
│  │                         │  │                         │         │
│  │  Drag & drop your       │  │  Use your Figma         │         │
│  │  design screenshot      │  │  Personal Access        │         │
│  │  here or browse         │  │  Token to extract       │         │
│  │                         │  │  from Figma files       │         │
│  │  ┌───────────────────┐ │  │                         │         │
│  │  │                   │ │  │  ┌──────────────────┐  │         │
│  │  │   Drop zone       │ │  │  │  Connect Figma   │  │         │
│  │  │   (dashed border) │ │  │  └──────────────────┘  │         │
│  │  │                   │ │  │                         │         │
│  │  └───────────────────┘ │  │  Requirements:          │         │
│  │                         │  │  • Figma account        │         │
│  │  Supported: PNG, JPG,  │  │  • Personal token       │         │
│  │  JPEG (Max 10MB)       │  │  • File access          │         │
│  │                         │  │                         │         │
│  │  [Browse Files...]     │  │                         │         │
│  │                         │  │                         │         │
│  └─────────────────────────┘  └─────────────────────────┘         │
│                                                                      │
│                                                                      │
│  💡 Tip: For best results, upload a clear screenshot showing the    │
│      component you want to generate. Figma integration provides     │
│      more accurate token extraction.                                │
│                                                                      │
│                                                  [Cancel] [Next →]  │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## After Screenshot Upload

```
┌──────────────────────────────────────────────────────────────────────┐
│  ComponentForge                    [?] Help    [👤] Profile    [⚙️]  │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ← Back to Dashboard                                                │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐│
│  │  Step 1 of 6: Upload Design                                   ││
│  │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ││
│  │  [✓] [2] [3] [4] [5] [6]                                      ││
│  └────────────────────────────────────────────────────────────────┘│
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐│
│  │  ✓ Screenshot uploaded successfully                           ││
│  │                                                                ││
│  │  ┌──────────────────┐                                         ││
│  │  │                  │  Filename: button-design.png            ││
│  │  │  [Thumbnail]     │  Size: 2.3 MB                           ││
│  │  │  Preview         │  Dimensions: 1200x800                   ││
│  │  │                  │                                          ││
│  │  └──────────────────┘  [Remove] [Replace]                     ││
│  │                                                                ││
│  └────────────────────────────────────────────────────────────────┘│
│                                                                      │
│  Component Type (Optional)                                          │
│  ┌────────────────────────────────────────────────────────────────┐│
│  │  [Auto-detect ▼]                                              ││
│  └────────────────────────────────────────────────────────────────┘│
│                                                                      │
│  Options: Auto-detect, Button, Card, Input, Select, Badge, Alert   │
│                                                                      │
│  💡 Leave as "Auto-detect" to let AI identify the component type   │
│                                                                      │
│                                           [← Back] [Next: Extract →]│
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Figma Connection Flow

```
┌──────────────────────────────────────────────────────────────────────┐
│  Connect Figma Account                                         [×]   │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  To extract design tokens directly from Figma, you'll need a        │
│  Personal Access Token.                                             │
│                                                                      │
│  📖 How to get your token:                                          │
│                                                                      │
│  1. Go to Figma Settings → Account → Personal Access Tokens        │
│  2. Click "Create new token"                                        │
│  3. Give it a name (e.g., "ComponentForge")                        │
│  4. Copy the token and paste it below                              │
│                                                                      │
│  Personal Access Token                                              │
│  ┌────────────────────────────────────────────────────────────────┐│
│  │ ••••••••••••••••••••••••••••••••••••••                        ││
│  └────────────────────────────────────────────────────────────────┘│
│                                                                      │
│  Figma File URL                                                     │
│  ┌────────────────────────────────────────────────────────────────┐│
│  │ https://figma.com/file/...                                    ││
│  └────────────────────────────────────────────────────────────────┘│
│                                                                      │
│  [×] Save token securely (encrypted storage)                        │
│                                                                      │
│                                           [Cancel] [Connect Figma]  │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Interactive Elements

### Upload Zone States

**Default State:**
```
┌───────────────────────────────────┐
│                                   │
│       📷                          │
│                                   │
│   Drop your screenshot here       │
│   or click to browse              │
│                                   │
│   PNG, JPG, JPEG (Max 10MB)      │
│                                   │
└───────────────────────────────────┘
```

**Hover State:**
```
┌───────────────────────────────────┐
│ ╔═════════════════════════════╗  │
│ ║         📷                  ║  │
│ ║                             ║  │
│ ║   Drop to upload            ║  │
│ ║                             ║  │
│ ╚═════════════════════════════╝  │
└───────────────────────────────────┘
```

**Uploading State:**
```
┌───────────────────────────────────┐
│                                   │
│       ⏳                          │
│                                   │
│   Uploading... 47%                │
│   ▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░          │
│                                   │
│   [Cancel Upload]                 │
│                                   │
└───────────────────────────────────┘
```

**Error State:**
```
┌───────────────────────────────────┐
│                                   │
│       ⚠️                          │
│                                   │
│   Upload failed                   │
│   File size exceeds 10MB          │
│                                   │
│   [Try Again]                     │
│                                   │
└───────────────────────────────────┘
```

---

## Component Details

### Layout Components
- **Container**: Max-width content area with padding
- **Card**: Bordered container for upload options
- **Modal**: Centered overlay for Figma connection

### UI Elements
- **Primary Button**: "Next →" (blue, filled)
- **Secondary Button**: "Cancel", "Browse Files" (gray, outline)
- **Destructive Button**: "Remove" (red, ghost)
- **Icon Buttons**: Help, Profile, Settings (ghost)

### Form Controls
- **File Input**: Hidden, triggered by drop zone or button
- **Select Dropdown**: Component type selection
- **Text Input**: Figma URL, token (password type)
- **Checkbox**: "Save token securely"

### Feedback Elements
- **Progress Bar**: Upload progress indicator
- **Toast Notification**: Success/error messages
- **Loading Spinner**: During upload/processing
- **Tooltip**: Contextual help on hover

---

## User Flows

### Screenshot Upload Flow
1. User lands on upload screen
2. User drags image or clicks "Browse Files"
3. File validation (type, size)
4. Upload progress indicator
5. Success state with thumbnail preview
6. Optional component type selection
7. Click "Next" to proceed

### Figma Connection Flow
1. User clicks "Connect Figma" card
2. Modal opens with instructions
3. User enters PAT and file URL
4. Validation of credentials
5. Success: Connection established
6. Figma file preview shown
7. Click "Next" to extract tokens

---

## Accessibility Features

### Keyboard Navigation
- **Tab**: Navigate through interactive elements
- **Enter/Space**: Activate buttons, open dropzone
- **Escape**: Close modal, cancel upload

### Screen Reader
- Upload zone: "File upload area for design screenshots"
- Progress: "Upload in progress, 47% complete"
- Success: "Screenshot uploaded successfully"
- Error: "Upload failed, file size exceeds limit"

### ARIA Labels
```html
<div role="button" aria-label="Upload screenshot drop zone" tabindex="0">
<input type="file" aria-label="Choose screenshot file" accept=".png,.jpg,.jpeg">
<progress aria-label="Upload progress" value="47" max="100">
```

---

## Responsive Behavior

### Desktop (≥1024px)
- Two-column layout for upload options
- Side-by-side cards
- Full-width preview thumbnails

### Tablet (768-1023px)
- Two-column layout maintained
- Slightly compressed cards
- Responsive thumbnail sizing

### Mobile (<768px)
- Single column stack
- Full-width cards
- Simplified upload zone
- Bottom sheet for Figma modal

---

## State Management

### Local State (Zustand)
```typescript
interface UploadState {
  selectedFile: File | null;
  uploadProgress: number;
  isUploading: boolean;
  uploadError: string | null;
  componentType: string;
  figmaConnected: boolean;
  figmaToken: string;
  figmaFileUrl: string;
}
```

### Server State (TanStack Query)
```typescript
// File upload mutation
useMutation({
  mutationFn: uploadScreenshot,
  onSuccess: (data) => navigate('/extract-tokens'),
  onError: (error) => toast.error(error.message)
})

// Figma connection mutation  
useMutation({
  mutationFn: connectFigma,
  onSuccess: () => toast.success('Figma connected'),
  onError: () => toast.error('Connection failed')
})
```

---

## Error Handling

### File Validation Errors
- **Invalid type**: "Please upload PNG, JPG, or JPEG only"
- **Too large**: "File exceeds 10MB limit (current: 12.3MB)"
- **Corrupted**: "Unable to read file. Please try another image"

### Upload Errors
- **Network error**: "Connection lost. Please check your network"
- **Server error**: "Upload failed. Please try again"
- **Timeout**: "Upload timed out. Please try a smaller file"

### Figma Errors
- **Invalid token**: "Token is invalid or expired"
- **Invalid URL**: "Please enter a valid Figma file URL"
- **No access**: "Unable to access this file. Check permissions"
- **Rate limit**: "Too many requests. Please wait and try again"

---

## Performance Considerations

### Optimizations
- Image preview thumbnail generation (max 400px width)
- Lazy loading for modals
- Debounced file validation
- Progressive upload with chunking for large files

### Loading States
- Skeleton screen during initial load
- Progress bar for uploads (0-100%)
- Spinner for Figma connection validation
- Optimistic UI for file selection

---

## Design Tokens

### Colors
- Primary action: `bg-blue-600 hover:bg-blue-700`
- Secondary action: `bg-gray-100 hover:bg-gray-200`
- Success: `bg-green-50 border-green-200`
- Error: `bg-red-50 border-red-200`
- Border: `border-gray-200`

### Spacing
- Card padding: `p-6`
- Section spacing: `space-y-6`
- Button spacing: `space-x-3`
- Form gap: `gap-4`

### Typography
- Heading: `text-2xl font-semibold`
- Body: `text-base text-gray-700`
- Label: `text-sm font-medium`
- Helper: `text-sm text-gray-500`

---

## Next Steps

After successful upload:
- → **02-token-extraction.md**: AI extracts design tokens from uploaded design
- User can also return to dashboard or cancel the process
