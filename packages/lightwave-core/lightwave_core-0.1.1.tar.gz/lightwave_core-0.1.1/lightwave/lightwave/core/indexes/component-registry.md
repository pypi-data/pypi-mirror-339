# LightWave Design System Component Registry

> **Note**: This document serves as the single source of truth for all UI components in the LightWave Design System. It provides a complete catalog of all micro-components (MCPs) with their properties, examples, and usage patterns.

## Table of Contents

1. [Component Hierarchy](#component-hierarchy)
2. [Core MCPs](#core-mcps)
3. [Form Components](#form-components)
4. [Layout Components](#layout-components)
5. [Navigation Components](#navigation-components)
6. [Data Display Components](#data-display-components)
7. [Feedback Components](#feedback-components)
8. [Media Components](#media-components)
9. [Composite Components](#composite-components)
10. [Implementation Guidelines](#implementation-guidelines)

## Component Hierarchy

The LightWave Design System follows a hierarchical component model:

1. **Design Tokens**: Fundamental visual properties (colors, typography, spacing, etc.)
2. **Micro-Components (MCPs)**: Atomic UI building blocks
3. **Composite Components**: Combinations of MCPs for specific use cases
4. **Patterns**: Standardized arrangements of components for common scenarios
5. **Templates**: Full page layouts composed of components and patterns

## Core MCPs

### Buttons

| Component ID | Description | Properties | Repository | Status |
|--------------|-------------|------------|------------|--------|
| `lwds-button-primary` | Primary action button | `text`, `icon`, `loading`, `disabled`, `size` | lightwave-design-system | Stable |
| `lwds-button-secondary` | Secondary action button | `text`, `icon`, `loading`, `disabled`, `size` | lightwave-design-system | Stable |
| `lwds-button-tertiary` | Tertiary action button | `text`, `icon`, `loading`, `disabled`, `size` | lightwave-design-system | Stable |
| `lwds-button-danger` | Danger/destructive action button | `text`, `icon`, `loading`, `disabled`, `size` | lightwave-design-system | Stable |
| `lwds-button-ghost` | Ghost/minimal button | `text`, `icon`, `loading`, `disabled`, `size` | lightwave-design-system | Stable |
| `lwds-button-icon` | Icon-only button | `icon`, `loading`, `disabled`, `size`, `label` | lightwave-design-system | Stable |

### Typography

| Component ID | Description | Properties | Repository | Status |
|--------------|-------------|------------|------------|--------|
| `lwds-heading` | Heading text | `level`, `weight`, `color`, `align`, `transform` | lightwave-design-system | Stable |
| `lwds-text` | Body text | `size`, `weight`, `color`, `align`, `italic`, `underline` | lightwave-design-system | Stable |
| `lwds-link` | Hyperlink text | `href`, `external`, `size`, `weight`, `color`, `underline` | lightwave-design-system | Stable |
| `lwds-code` | Code display text | `language`, `inline`, `theme` | lightwave-design-system | Stable |
| `lwds-label` | Text label for form elements | `required`, `optional`, `disabled`, `error` | lightwave-design-system | Stable |

### Icons

| Component ID | Description | Properties | Repository | Status |
|--------------|-------------|------------|------------|--------|
| `lwds-icon` | Vector icon | `name`, `size`, `color`, `label` | lightwave-design-system | Stable |

## Form Components

### Inputs

| Component ID | Description | Properties | Repository | Status |
|--------------|-------------|------------|------------|--------|
| `lwds-input-text` | Text input field | `label`, `placeholder`, `value`, `disabled`, `readonly`, `error`, `helper`, `required` | lightwave-design-system | Stable |
| `lwds-input-email` | Email input field | `label`, `placeholder`, `value`, `disabled`, `readonly`, `error`, `helper`, `required` | lightwave-design-system | Stable |
| `lwds-input-password` | Password input field | `label`, `placeholder`, `value`, `disabled`, `readonly`, `error`, `helper`, `required`, `show-toggle` | lightwave-design-system | Stable |
| `lwds-input-number` | Numeric input field | `label`, `placeholder`, `value`, `min`, `max`, `step`, `disabled`, `readonly`, `error`, `helper`, `required` | lightwave-design-system | Stable |
| `lwds-input-tel` | Telephone input field | `label`, `placeholder`, `value`, `disabled`, `readonly`, `error`, `helper`, `required` | lightwave-design-system | Stable |
| `lwds-input-url` | URL input field | `label`, `placeholder`, `value`, `disabled`, `readonly`, `error`, `helper`, `required` | lightwave-design-system | Stable |
| `lwds-textarea` | Multi-line text input | `label`, `placeholder`, `value`, `rows`, `disabled`, `readonly`, `error`, `helper`, `required`, `resize` | lightwave-design-system | Stable |

### Selects and Multi-selects

| Component ID | Description | Properties | Repository | Status |
|--------------|-------------|------------|------------|--------|
| `lwds-select` | Dropdown select | `label`, `options`, `value`, `disabled`, `readonly`, `error`, `helper`, `required`, `searchable` | lightwave-design-system | Stable |
| `lwds-multi-select` | Multi-option select | `label`, `options`, `value`, `disabled`, `readonly`, `error`, `helper`, `required`, `searchable`, `max-selections` | lightwave-design-system | Stable |
| `lwds-combobox` | Combo box with autocomplete | `label`, `options`, `value`, `disabled`, `readonly`, `error`, `helper`, `required`, `allow-custom` | lightwave-design-system | Stable |

### Toggles and Checkboxes

| Component ID | Description | Properties | Repository | Status |
|--------------|-------------|------------|------------|--------|
| `lwds-checkbox` | Single checkbox | `label`, `checked`, `disabled`, `error`, `helper`, `required`, `indeterminate` | lightwave-design-system | Stable |
| `lwds-checkbox-group` | Group of checkboxes | `label`, `options`, `value`, `disabled`, `error`, `helper`, `required`, `direction` | lightwave-design-system | Stable |
| `lwds-radio` | Single radio button | `label`, `checked`, `disabled`, `error`, `helper`, `required` | lightwave-design-system | Stable |
| `lwds-radio-group` | Group of radio buttons | `label`, `options`, `value`, `disabled`, `error`, `helper`, `required`, `direction` | lightwave-design-system | Stable |
| `lwds-toggle` | Toggle switch | `label`, `checked`, `disabled`, `error`, `helper`, `required`, `size` | lightwave-design-system | Stable |

### Date and Time

| Component ID | Description | Properties | Repository | Status |
|--------------|-------------|------------|------------|--------|
| `lwds-date-picker` | Date selection widget | `label`, `value`, `min`, `max`, `disabled`, `readonly`, `error`, `helper`, `required`, `format` | lightwave-design-system | Stable |
| `lwds-time-picker` | Time selection widget | `label`, `value`, `min`, `max`, `disabled`, `readonly`, `error`, `helper`, `required`, `format`, `step` | lightwave-design-system | Stable |
| `lwds-datetime-picker` | Combined date and time picker | `label`, `value`, `min`, `max`, `disabled`, `readonly`, `error`, `helper`, `required`, `format` | lightwave-design-system | Stable |
| `lwds-date-range-picker` | Date range selection | `label`, `start`, `end`, `min`, `max`, `disabled`, `readonly`, `error`, `helper`, `required`, `format` | lightwave-design-system | Stable |

### Form Layou

| Component ID | Description | Properties | Repository | Status |
|--------------|-------------|------------|------------|--------|
| `lwds-form` | Form container | `action`, `method`, `enctype`, `novalidate`, `loading` | lightwave-design-system | Stable |
| `lwds-form-group` | Group of related form elements | `label`, `helper`, `error`, `required` | lightwave-design-system | Stable |
| `lwds-form-section` | Logical section within a form | `title`, `description`, `collapsible`, `collapsed` | lightwave-design-system | Stable |
| `lwds-fieldset` | HTML fieldset with legend | `legend`, `disabled` | lightwave-design-system | Stable |

### File Inputs

| Component ID | Description | Properties | Repository | Status |
|--------------|-------------|------------|------------|--------|
| `lwds-file-input` | File upload input | `label`, `accept`, `multiple`, `disabled`, `error`, `helper`, `required`, `max-size`, `max-files` | lightwave-design-system | Stable |
| `lwds-file-drop-zone` | Drag and drop file upload area | `label`, `accept`, `multiple`, `disabled`, `error`, `helper`, `required`, `max-size`, `max-files` | lightwave-design-system | Stable |

## Layout Components

### Containers

| Component ID | Description | Properties | Repository | Status |
|--------------|-------------|------------|------------|--------|
| `lwds-container` | Content container with maximum width | `size`, `padding`, `center` | lightwave-design-system | Stable |
| `lwds-box` | Generic container box | `padding`, `border`, `radius`, `shadow`, `background` | lightwave-design-system | Stable |
| `lwds-card` | Content card with optional header/footer | `title`, `subtitle`, `actions`, `padding`, `border`, `shadow` | lightwave-design-system | Stable |
| `lwds-panel` | Panel with header and collapsible content | `title`, `subtitle`, `actions`, `collapsed`, `collapsible` | lightwave-design-system | Stable |

### Grid and Flexbox

| Component ID | Description | Properties | Repository | Status |
|--------------|-------------|------------|------------|--------|
| `lwds-grid` | CSS Grid container | `columns`, `gap`, `responsive` | lightwave-design-system | Stable |
| `lwds-grid-item` | Grid item | `span`, `start`, `end`, `responsive` | lightwave-design-system | Stable |
| `lwds-flex` | Flexbox container | `direction`, `wrap`, `justify`, `align`, `gap` | lightwave-design-system | Stable |
| `lwds-flex-item` | Flex item | `grow`, `shrink`, `basis`, `align` | lightwave-design-system | Stable |

### Dividers and Spacing

| Component ID | Description | Properties | Repository | Status |
|--------------|-------------|------------|------------|--------|
| `lwds-divider` | Horizontal or vertical separator | `orientation`, `color`, `thickness`, `spacing` | lightwave-design-system | Stable |
| `lwds-spacer` | Empty space element | `size`, `responsive` | lightwave-design-system | Stable |

## Navigation Components

### Menus and Dropdowns

| Component ID | Description | Properties | Repository | Status |
|--------------|-------------|------------|------------|--------|
| `lwds-menu` | Vertical navigation menu | `items`, `active`, `collapsible`, `icons` | lightwave-design-system | Stable |
| `lwds-dropdown` | Dropdown container | `trigger`, `placement`, `offset`, `arrow`, `close-on-click` | lightwave-design-system | Stable |
| `lwds-dropdown-item` | Dropdown menu item | `text`, `icon`, `href`, `disabled`, `active`, `divider` | lightwave-design-system | Stable |
| `lwds-context-menu` | Right-click context menu | `items`, `trigger` | lightwave-design-system | Stable |

### Tabs and Navigation

| Component ID | Description | Properties | Repository | Status |
|--------------|-------------|------------|------------|--------|
| `lwds-tabs` | Tab navigation container | `tabs`, `active`, `align`, `size`, `variant` | lightwave-design-system | Stable |
| `lwds-tab` | Individual tab | `label`, `icon`, `disabled`, `active`, `closable` | lightwave-design-system | Stable |
| `lwds-tab-panel` | Tab content panel | `active` | lightwave-design-system | Stable |
| `lwds-pagination` | Pagination control | `total`, `current`, `per-page`, `size`, `simple` | lightwave-design-system | Stable |
| `lwds-breadcrumb` | Breadcrumb navigation | `items`, `separator`, `max-items` | lightwave-design-system | Stable |

### App Shell Navigation

| Component ID | Description | Properties | Repository | Status |
|--------------|-------------|------------|------------|--------|
| `lwds-app-bar` | Top application bar | `title`, `actions`, `user`, `notifications`, `search` | lightwave-design-system | Stable |
| `lwds-sidebar` | Application sidebar | `items`, `collapsed`, `collapsible`, `width` | lightwave-design-system | Stable |
| `lwds-footer` | Application footer | `copyright`, `links`, `version` | lightwave-design-system | Stable |

## Data Display Components

### Tables and Data Grids

| Component ID | Description | Properties | Repository | Status |
|--------------|-------------|------------|------------|--------|
| `lwds-table` | Data table | `columns`, `data`, `sortable`, `selectable`, `loading`, `empty-state` | lightwave-design-system | Stable |
| `lwds-data-grid` | Advanced data grid with filtering, sorting, pagination | `columns`, `data`, `sortable`, `filterable`, `pageable`, `selectable`, `loading`, `empty-state` | lightwave-design-system | Stable |
| `lwds-list` | Simple data list | `items`, `selectable`, `interactive`, `loading`, `empty-state` | lightwave-design-system | Stable |

### Data Visualization

| Component ID | Description | Properties | Repository | Status |
|--------------|-------------|------------|------------|--------|
| `lwds-chart-bar` | Bar chart | `data`, `labels`, `title`, `horizontal`, `stacked`, `colors`, `legend` | lightwave-design-system | Stable |
| `lwds-chart-line` | Line chart | `data`, `labels`, `title`, `smooth`, `fill`, `colors`, `legend` | lightwave-design-system | Stable |
| `lwds-chart-pie` | Pie/donut chart | `data`, `labels`, `title`, `donut`, `colors`, `legend` | lightwave-design-system | Stable |
| `lwds-stat` | Single statistic display | `value`, `label`, `icon`, `change`, `direction` | lightwave-design-system | Stable |
| `lwds-progress` | Progress bar | `value`, `max`, `label`, `size`, `color`, `indeterminate` | lightwave-design-system | Stable |

### Information Display

| Component ID | Description | Properties | Repository | Status |
|--------------|-------------|------------|------------|--------|
| `lwds-badge` | Status badge | `text`, `color`, `size`, `icon`, `dot` | lightwave-design-system | Stable |
| `lwds-tag` | Tag label with optional remove button | `text`, `color`, `size`, `icon`, `removable`, `href` | lightwave-design-system | Stable |
| `lwds-avatar` | User avatar | `src`, `alt`, `initials`, `size`, `shape`, `status` | lightwave-design-system | Stable |
| `lwds-tooltip` | Contextual information tooltip | `content`, `placement`, `trigger`, `delay`, `max-width` | lightwave-design-system | Stable |

## Feedback Components

### Alerts and Notifications

| Component ID | Description | Properties | Repository | Status |
|--------------|-------------|------------|------------|--------|
| `lwds-alert` | Alert message | `type`, `title`, `content`, `icon`, `dismissible`, `actions` | lightwave-design-system | Stable |
| `lwds-toast` | Temporary toast notification | `type`, `title`, `content`, `icon`, `duration`, `actions` | lightwave-design-system | Stable |
| `lwds-banner` | Page-level banner notification | `type`, `content`, `icon`, `dismissible`, `actions` | lightwave-design-system | Stable |

### Dialogs and Modals

| Component ID | Description | Properties | Repository | Status |
|--------------|-------------|------------|------------|--------|
| `lwds-modal` | Modal dialog | `title`, `content`, `size`, `closable`, `footer`, `actions` | lightwave-design-system | Stable |
| `lwds-dialog` | Simplified dialog | `title`, `content`, `type`, `actions` | lightwave-design-system | Stable |
| `lwds-drawer` | Side drawer panel | `title`, `content`, `side`, `size`, `closable`, `footer`, `actions` | lightwave-design-system | Stable |
| `lwds-popover` | Contextual popover panel | `title`, `content`, `placement`, `trigger`, `closable` | lightwave-design-system | Stable |

### Loading States

| Component ID | Description | Properties | Repository | Status |
|--------------|-------------|------------|------------|--------|
| `lwds-spinner` | Loading spinner | `size`, `color`, `label` | lightwave-design-system | Stable |
| `lwds-skeleton` | Content skeleton loader | `variant`, `lines`, `width`, `height`, `animation` | lightwave-design-system | Stable |

## Media Components

### Images and Video

| Component ID | Description | Properties | Repository | Status |
|--------------|-------------|------------|------------|--------|
| `lwds-image` | Responsive image | `src`, `alt`, `width`, `height`, `fit`, `lazy`, `fallback` | lightwave-design-system | Stable |
| `lwds-gallery` | Image gallery | `images`, `thumbnails`, `lightbox`, `grid` | lightwave-design-system | Stable |
| `lwds-video` | Video player | `src`, `poster`, `autoplay`, `controls`, `loop`, `muted` | lightwave-design-system | Stable |
| `lwds-avatar-group` | Group of overlapping avatars | `avatars`, `max`, `size`, `overlap` | lightwave-design-system | Stable |

## Composite Components

### Dashboard Components

| Component ID | Description | Properties | Repository | Status |
|--------------|-------------|------------|------------|--------|
| `lwds-dashboard-card` | Dashboard metric card | `title`, `value`, `change`, `direction`, `icon`, `chart`, `period` | lightwave-design-system | Stable |
| `lwds-dashboard-grid` | Dashboard grid layout | `columns`, `items`, `gap` | lightwave-design-system | Stable |
| `lwds-activity-feed` | Activity timeline feed | `items`, `loading`, `empty-state` | lightwave-design-system | Stable |

### Project Managemen

| Component ID | Description | Properties | Repository | Status |
|--------------|-------------|------------|------------|--------|
| `lwds-task-card` | Task display card | `title`, `description`, `assignee`, `status`, `priority`, `due-date`, `actions` | lightwave-design-system | Stable |
| `lwds-kanban-board` | Kanban board view | `columns`, `items`, `draggable` | lightwave-design-system | Stable |
| `lwds-task-list` | Task list view | `tasks`, `grouping`, `sorting`, `filtering` | lightwave-design-system | Stable |
| `lwds-timeline` | Project timeline view | `events`, `scale`, `today`, `range` | lightwave-design-system | Stable |

### User Managemen

| Component ID | Description | Properties | Repository | Status |
|--------------|-------------|------------|------------|--------|
| `lwds-user-card` | User profile card | `user`, `stats`, `actions`, `editable` | lightwave-design-system | Stable |
| `lwds-team-viewer` | Team members display | `members`, `roles`, `layout`, `actions` | lightwave-design-system | Stable |
| `lwds-permission-matrix` | Role/permission matrix editor | `roles`, `permissions`, `editable` | lightwave-design-system | Stable |

### Domain-specific Components

| Component ID | Description | Properties | Repository | Status |
|--------------|-------------|------------|------------|--------|
| `lwds-photo-card` | Photography image card | `image`, `metadata`, `actions`, `selectable` | photographyos.io | Stable |
| `lwds-shot-card` | Cinematography shot card | `shot`, `metadata`, `thumbnail`, `actions` | cineos.io | Stable |
| `lwds-client-card` | Client information card | `client`, `stats`, `actions`, `events` | createos.io | Stable |

## Implementation Guidelines

### Component Integration

1. **Django Integration**
   - All components are available as django-components
   - Import patterns: `{% component 'lwds-button-primary' text='Submit' %}`
   - Template locations: `templates/components/lwds-*/`

2. **React Integration**
   - All components are available as React components
   - Import patterns: `import { Button } from '@lightwave/design-system'`
   - Property patterns: `<Button variant="primary">Submit</Button>`

3. **HTML/CSS Integration**
   - All components have standalone HTML/CSS implementations
   - CSS classes follow `lwds-component-variant` naming convention
   - JavaScript behaviors available through opt-in data attributes

### Usage Best Practices

1. **Component Selection**
   - Use the most specific component for your use case
   - Combine MCPs rather than creating custom elements
   - Follow application-specific patterns for consistency

2. **Customization**
   - Prefer configuration over modification
   - Use design tokens for visual customization
   - Extend components through composition

3. **Accessibility**
   - All components meet WCAG 2.1 AA standards
   - Maintain accessibility when integrating components
   - Test with screen readers and keyboard navigation

4. **Performance**
   - Components are tree-shakable in JavaScript frameworks
   - All components support lazy loading
   - Static rendering is supported for all components

### Component Registry Updates

To add new components to this registry:

1. Create a component specification following LightWave Design System guidelines
2. Implement the component in the design system repository
3. Document the component properties and variants
4. Update the component registry with the new component details
5. Create usage examples for all supported frameworks

## Related Documentation

- [LightWave Design System Overview](../lightwave-design-system/overview.md)
- [Design Tokens Reference](../lightwave-design-system/design-tokens.md)
- [Component Development Guide](../lightwave-design-system/component-development.md)
- [Accessibility Guidelines](../lightwave-design-system/accessibility.md)
- [Django Integration](../lightwave-design-system/django-integration.md)
- [React Integration](../lightwave-design-system/react-integration.md)