# HTML/CSS/JS Replica Generation Prompt

You are an expert web developer tasked with creating **{{N}}** unique replicas of provided HTML/CSS/JS code. Each replica must maintain identical functionality while featuring distinct visual themes and contextual content.

## Input Placeholders:
```
ORIGINAL_HTML_CODE: {{original_html}}
ORIGINAL_CSS_CODE: {{original_css}}
ORIGINAL_JS_CODE: {{original_js}}
SHORT_TEXT: {{short_description}}
QUESTION_TEXT: {{problem_statement}}
TEST_CASES: {{test_scenarios}}
NUMBER_OF_REPLICAS: {{N}}
```

## Core Requirements:

### 🔧 Structural Preservation
- **Maintain identical layout structure** and DOM hierarchy
- **Preserve all JavaScript functionality** and event handlers
- **Keep responsive design** breakpoints and behavior
- **Maintain accessibility** features and ARIA attributes

### 🎨 Visual Transformation (Required Changes)
- **Color Schemes**: Primary/secondary colors, backgrounds, gradients
- **Typography**: Font families, sizes, weights, line heights
- **Visual Effects**: Shadows, borders, border-radius, opacity
- **Spacing**: Margins, padding, gaps (within 20% variance)
- **Animations**: Transition effects, durations, easing functions
- **UI Components**: Button styles, form elements, cards, icons

### 📝 Content Adaptation
- **Domain Context**: Transform theme (e.g., e-commerce → education → healthcare)
- **Terminology**: Update labels, headings, descriptions while preserving meaning
- **Placeholder Content**: Change examples, sample data, mock text
- **Maintain Logic**: New content must make semantic sense in context

### 🏷️ Technical Updates
- **HTML IDs**: Update to reflect new content context
- **CSS Classes**: Modify class names to match new theme
- **JavaScript Selectors**: Update all DOM selectors to match new IDs/classes
- **Variable Names**: Rename JavaScript variables for consistency
- **Comments**: Update code comments to reflect changes

## Quality Standards:

### ✅ Functional Requirements
- [ ] All original functionality preserved
- [ ] JavaScript works with updated selectors
- [ ] Form validations and interactions intact
- [ ] No console errors or broken references
- [ ] Responsive behavior maintained

### ✅ Visual Requirements
- [ ] Distinct visual identity (>70% styling difference)
- [ ] Professional, cohesive design
- [ ] Proper contrast ratios maintained
- [ ] Modern UI/UX principles applied
- [ ] Cross-browser compatibility preserved

### ✅ Content Requirements
- [ ] Contextually appropriate and coherent
- [ ] Professional language and tone
- [ ] Logical information hierarchy
- [ ] Meaningful placeholder data
- [ ] Updated test scenarios match new context

## Output Format:

For each of the **{N}** replicas, return exactly this structure:

```json
{
  "replica_1": {
    "short_text": "[Brief description of replica ]",
    "html_code": "",
    "css_code": "", 
    "js_code": "",
    "question_text": "[Modified problem statement for new context]",
    "test_cases": "[Updated test scenarios matching new functionality]",
    "html_solution": "[Complete HTML with new IDs and content]",
    "css_solution": "[Complete CSS with updated styling and selectors]",
    "js_solution": "[Complete JavaScript with updated selectors]",
    "subtopic": "",
    "course": "",
    "module": "",
    "unit": ""
  },
  "replica_2": {
    // Same structure for replica 2
  }
  // ... continue for all N replicas
}
```

## Transformation Examples:

| Original | Replica Example |
|----------|-----------------|
| **Theme**: Login Form (Blue) | **Theme**: Registration Form (Green) |
| **ID**: `login-form` | **ID**: `signup-form` |
| **Content**: "Enter Credentials" | **Content**: "Create Account" |
| **Button**: "Sign In" | **Button**: "Register" |
| **Colors**: `#007bff` (blue) | **Colors**: `#28a745` (green) |

## Domain Transformation Ideas:
- **E-commerce** → Booking System → Event Management
- **Finance** → Education → Healthcare
- **Social Media** → Business → Entertainment
- **Travel** → Real Estate → Food Services

## Advanced Styling Variations:
- **Modern Minimalist**: Clean lines, lots of whitespace, subtle shadows
- **Corporate Professional**: Conservative colors, structured layouts
- **Creative/Artistic**: Bold colors, unique typography, creative effects
- **Dark Theme**: Dark backgrounds, light text, neon accents
- **Material Design**: Elevated cards, ripple effects, consistent spacing

## Pre-Generation Checklist:
1. **Analyze** original code structure and functionality
2. **Plan** N distinct themes with different domains
3. **Map** ID/class transformations for each replica
4. **Verify** all JavaScript dependencies are updated
5. **Test** that each replica maintains core functionality
6. **Validate** visual distinctiveness between replicas

Generate exactly **{N}** replicas that are visually distinct, functionally identical, and professionally crafted.