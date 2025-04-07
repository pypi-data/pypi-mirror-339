# LightWave Ecosystem URL Index

> **Note**: This document serves as the single source of truth for all URL structures and endpoints across the LightWave ecosystem. It defines the standard URL patterns, API endpoints, and routing conventions used across all applications.

## Table of Contents

1. [Production URLs](#production-urls)
2. [URL Structure](#url-structure)
3. [GitHub Repositories](#github-repositories)
4. [Implementation Guidelines](#implementation-guidelines)

## Production URLs

> **Important**: All production URLs follow the pattern `{subdomain}.{domain}.{tld}`. Each application maintains its own domain for complete isolation and security.

### Central Platform

- **CreateOS**: <https://createos.io>                   (Central business management platform)
  - **Admin**: <https://admin.createos.io>              (System administration and CMS)
  - **Auth**: <https://auth.createos.io>                (Centralized authentication service)
  - **API**: <https://api.createos.io>                  (Core API endpoints)
  - **App**: <https://app.createos.io>                  (Main web application)
  - **CDN**: <https://cdn.createos.io>                  (Cloudflare R2 CDN for assets)

### Professional Applications

- **CineOS**: <https://cineos.io>                       (Cinematography workflow platform)
  - **Admin**: <https://admin.cineos.io>                (System administration and CMS)
  - **Auth**: <https://auth.cineos.io>                  (Application-specific auth)
  - **API**: <https://api.cineos.io>                    (Application API endpoints)
  - **App**: <https://app.cineos.io>                    (Main web application)
  - **Mobile**: <https://mobile.cineos.io>              (Mobile app API)
  - **Desktop**: <https://desktop.cineos.io>            (Desktop app API)
  - **CDN**: <https://cdn.cineos.io>                    (Cloudflare R2 CDN for assets)

- **PhotographyOS**: <https://photographyos.io>         (Photography workflow platform)
  - **Admin**: <https://admin.photographyos.io>         (System administration and CMS)
  - **Auth**: <https://auth.photographyos.io>           (Application-specific auth)
  - **API**: <https://api.photographyos.io>             (Application API endpoints)
  - **App**: <https://app.photographyos.io>             (Main web application)
  - **Mobile**: <https://mobile.photographyos.io>       (Mobile app API)
  - **Desktop**: <https://desktop.photographyos.io>     (Desktop app API)
  - **CDN**: <https://cdn.photographyos.io>             (Cloudflare R2 CDN for assets)

- **Photo Workflows**: <https://photo-workflows.com>    (Photo processing automation)
  - **Admin**: <https://admin.photo-workflows.com>      (System administration and CMS)
  - **Auth**: <https://auth.photo-workflows.com>        (Application-specific auth)
  - **API**: <https://api.photo-workflows.com>          (Application API endpoints)
  - **App**: <https://app.photo-workflows.com>          (Main web application)
  - **Mobile**: <https://mobile.photo-workflows.com>    (Mobile app API)
  - **Desktop**: <https://desktop.photo-workflows.com>  (Desktop app API)
  - **CDN**: <https://cdn.photo-workflows.com>          (Cloudflare R2 CDN for assets)

### Marketing Sites

- **Portfolio**: <https://joelschaeffer.com>            (Portfolio, Blog & shop)
  - **Admin**: <https://admin.joelschaeffer.com>        (Content management)
  - **Auth**: <https://auth.joelschaeffer.com>          (Customer authentication)
  - **API**: <https://api.joelschaeffer.com>            (Shop and portfolio API)
  - **App**: <https://shop.joelschaeffer.com>           (E-commerce platform)
  - **Mobile**: <https://mobile.joelschaeffer.com>      (Mobile app API)
  - **Desktop**: <https://desktop.joelschaeffer.com>    (Desktop app API)
  - **CDN**: <https://cdn.joelschaeffer.com>            (Cloudflare R2 CDN for assets)

- **Corporate**: <https://lightwave-media.site>         (Company information)
  - **Admin**: <https://admin.lightwave-media.site>     (Content management)
  - **Auth**: <https://auth.lightwave-media.site>       (Staff authentication)
  - **CDN**: <https://cdn.lightwave-media.site>         (Cloudflare R2 CDN for assets)

## URL Structure

> **Note**: The URL structure follows RESTful conventions and hierarchical organization. All endpoints use versioning (v1) for future compatibility.

### Common URL Patterns

#### Marketing Pages (`www.domain.io` or `.com`)

> **Purpose**: Public-facing marketing and information pages for each application.

```markdown
# Core Pages
/                   # Home page (Landing page)
/about/            # About us/company information
/team/             # Team members and roles
/careers/          # Career opportunities
/contact/          # Contact information
  /sales/          # Sales team contac
  /support/        # Support team contac
  /partners/       # Partner inquiries

# Product Information
/products/         # Product listing
/products/_id/     # Product detail page
/pricing/          # Pricing plans
  /compare/        # Pricing comparison tool
/features/         # Feature overview
  /_id/            # Feature detail page
/integrations/     # Integration partners
  /_id/            # Integration detail
/releases/         # Release notes
  /_id/            # Release detail

# Customer Resources
/testimonials/     # Customer success stories
/reviews/          # Product reviews
/resources/        # Resource center
  /guides/         # User guides
  /tutorials/      # Video tutorials
  /documentation/  # Technical documentation
  /api/            # API documentation
  /faq/            # Frequently asked questions
  /blog/           # Blog posts
    /_id/          # Blog post detail

# Community & Suppor
/community/        # Community hub
/forum/           # Discussion forum
  /_id/           # Forum topic
/support/         # Support center
  /help/          # Help articles
    /_id/         # Help article detail
  /tickets/       # Support tickets
    /_id/         # Ticket detail
  /status/        # System status
  /maintenance/   # Maintenance schedule
  /feedback/      # Feedback form

# Legal & Compliance
/legal/           # Legal information
  /privacy/       # Privacy policy
  /terms/         # Terms of service
  /cookies/       # Cookie policy
  /gdpr/          # GDPR compliance
  /ccpa/          # CCPA compliance
  /accessibility/ # Accessibility statemen
  /sitemap/       # Site map
  /disclaimer/    # Legal disclaimer
  /licenses/      # Software licenses
  /trademarks/    # Trademark information
  /copyright/     # Copyright notice
  /compliance/    # Compliance information
  /security/      # Security policy
  /data/          # Data handling
  /transparency/  # Transparency repor

# International
/languages/       # Language selection
/regions/         # Regional information
  /_id/           # Region detail
/currency/        # Currency selection
/units/           # Unit system selection
/timezone/        # Timezone selection

# System Pages
/404/             # Not found page
/500/             # Server error page
/maintenance/     # Maintenance page
/coming-soon/     # Coming soon page
/thank-you/       # Thank you page
/confirmation/    # Confirmation page
/error/           # Error page
/offline/         # Offline page
/redirect/        # Redirect page
```

#### Main Application (`app.domain.com`)

> **Purpose**: Core application interface and functionality.

```markdown
# Global Navigation
/home/            # Home dashboard (app overview)
/notifications/   # Notifications center
/help/           # Help center
/settings/       # User settings
/profile/        # User profile

# Project Managemen
/projects/       # Project lis
/projects/_id/   # Project detail
  /overview/     # Project overview
  /dashboard/    # Project dashboard
  /files/        # Project files
  /team/         # Project team
  /settings/     # Project settings
  /activity/     # Project activity
  /analytics/    # Project analytics
  /timeline/     # Project timeline
  /budget/       # Project budge
  /documents/    # Project documents
  /notes/        # Project notes
  /tasks/        # Project tasks
  /calendar/     # Project calendar
  /reports/      # Project reports

# Resource Managemen
/resources/      # Resource lis
  /files/       # File library
  /templates/   # Template library
  /assets/      # Asset library
  /media/       # Media library
  /documents/   # Document library
  /archives/    # Archive library

# Team Collaboration
/team/          # Team overview
  /members/     # Team members
  /roles/       # Team roles
  /permissions/ # Team permissions
  /schedule/    # Team schedule
  /availability/# Team availability
  /chat/        # Team cha
  /meetings/    # Team meetings
  /announcements/# Team announcements

# Communication
/communication/ # Communication hub
  /messages/    # Direct messages
  /channels/    # Communication channels
  /threads/     # Message threads
  /announcements/# Announcements
  /notifications/# Notification settings
  /preferences/ # Communication preferences

# Analytics & Reporting
/analytics/    # Analytics dashboard
  /overview/   # Analytics overview
  /reports/    # Custom reports
  /metrics/    # Key metrics
  /insights/   # Data insights
  /exports/    # Data exports
  /schedules/  # Report schedules
  /templates/  # Report templates

# Settings & Configuration
/settings/     # Settings center
  /account/    # Account settings
  /preferences/# User preferences
  /notifications/# Notification settings
  /security/   # Security settings
  /integrations/# Integration settings
  /billing/    # Billing settings
  /api/        # API settings
  /webhooks/   # Webhook settings
  /backup/     # Backup settings
  /audit/      # Audit logs

# Help & Suppor
/help/         # Help center
  /guides/     # User guides
  /tutorials/  # Tutorials
  /faq/        # FAQ
  /support/    # Support tickets
  /feedback/   # Feedback
  /documentation/# Documentation

# User Profile
/profile/      # Profile overview
  /info/       # Profile information
  /activity/   # User activity
  /preferences/# User preferences
  /security/   # Security settings
  /devices/    # Connected devices
  /sessions/   # Active sessions
  /history/    # Activity history
  /notifications/# Notification preferences

# Search & Discovery
/search/       # Global search
  /advanced/   # Advanced search
  /filters/    # Search filters
  /saved/      # Saved searches
  /history/    # Search history
  /suggestions/# Search suggestions
```

#### Admin Subdomain (`admin.domain.com`)

> **Purpose**: System administration and management interface.

```markdown
/                   # Admin dashboard
/users/             # User managemen
/settings/          # System settings
/logs/              # System logs
/analytics/         # System analytics
/backups/           # Backup managemen
/security/          # Security settings
/audit/             # Audit logs
/roles/             # Role managemen
/permissions/       # Permission managemen
```

#### Auth Subdomain (`auth.domain.com`)

> **Purpose**: Centralized authentication and authorization service.

```markdown
/v1/
  /login/           # Login endpoin
  /logout/          # Logout endpoin
  /refresh/         # Token refresh
  /verify/          # Token verification
  /register/        # User registration
  /password/        # Password managemen
    /reset/         # Password reset reques
    /change/        # Password change
    /forgot/        # Forgot password
    /validate/      # Password validation
  /2fa/             # Two-factor authentication
    /enable/        # Enable 2FA
    /disable/       # Disable 2FA
    /verify/        # Verify 2FA code
    /backup/        # Backup codes
    /recovery/      # Recovery options
  /sessions/        # Session managemen
    /list/          # List active sessions
    /revoke/        # Revoke session
    /revoke-all/    # Revoke all sessions
    /info/          # Session information
  /oauth/           # OAuth endpoints
    /providers/     # List OAuth providers
    /_provider/     # Provider-specific endpoints
      /login/       # OAuth login
      /callback/    # OAuth callback
      /revoke/      # Revoke OAuth access
      /refresh/     # Refresh OAuth token
      /profile/     # OAuth profile data
  /sso/             # Single Sign-On
    /initiate/      # Initiate SSO
    /callback/      # SSO callback
    /metadata/      # SSO metadata
    /logout/        # SSO logou
```

#### API Subdomain (`api.domain.com`)

> **Purpose**: RESTful API endpoints for application functionality.

```markdown
/v1/
  /users/           # User managemen
    /me/            # Current user
    /_id/           # User details
      /profile/     # User profile
      /preferences/ # User preferences
      /activity/    # User activity
      /devices/     # User devices
  /clients/         # Client managemen
    /_id/           # Client details
      /projects/    # Client's projects
      /invoices/    # Client's invoices
      /documents/   # Client documents
      /history/     # Client history
  /projects/        # Project managemen
    /_id/           # Project details
      /tasks/       # Project tasks
      /files/       # Project files
      /team/        # Project team
      /timeline/    # Project timeline
      /budget/      # Project budge
  /analytics/       # Analytics data
    /revenue/       # Revenue metrics
    /performance/   # Performance metrics
    /usage/         # Usage statistics
    /audience/      # Audience analytics
    /engagement/    # Engagement metrics
  /integrations/    # Integration managemen
    /_provider/     # Provider-specific endpoints
      /connect/     # Connect integration
      /disconnect/  # Disconnect integration
      /sync/        # Sync data
      /webhook/     # Webhook endpoints
      /status/      # Integration status
  /media/           # Media managemen
    /upload/        # Media upload
    /download/      # Media download
    /process/       # Media processing
    /transform/     # Media transformation
    /optimize/      # Media optimization
  /notifications/   # Notification system
    /channels/      # Notification channels
    /templates/     # Notification templates
    /preferences/   # Notification preferences
    /history/       # Notification history
  /search/          # Search functionality
    /index/         # Search index
    /query/         # Search query
    /suggest/       # Search suggestions
    /filters/       # Search filters
  /reports/         # Reporting system
    /generate/      # Generate reports
    /templates/     # Report templates
    /schedule/      # Report scheduling
    /export/        # Report expor
```

## GitHub Repositories

> **Note**: Repository organization follows a modular approach with clear separation of concerns.

### Core Infrastructure

- **lightwave-infrastructure**: <https://github.com/lightwave-media/lightwave-infrastructure>
  - Infrastructure as Code (IaC)
  - Deployment configurations
  - Environment managemen
  - Monitoring setup

- **lightwave-shared-core**: <https://github.com/lightwave-media/lightwave-shared-core>
  - Shared libraries
  - Common utilities
  - Core functionality
  - Base components

- **lightwave-design-system**: <https://github.com/lightwave-media/lightwave-design-system>
  - UI components
  - Design tokens
  - Style guides
  - Theme system

### Applications

- **createos.io**: <https://github.com/lightwave-media/createos.io>
  - Central platform
  - Business managemen
  - Integration hub

- **cineos.io**: <https://github.com/lightwave-media/cineos.io>
  - Cinematography workflow
  - Production managemen
  - Asset handling

- **photographyos.io**: <https://github.com/lightwave-media/photographyos.io>
  - Photography workflow
  - Session managemen
  - Gallery system

- **photo-workflows**: <https://github.com/lightwave-media/photo-workflows>
  - Processing automation
  - Workflow engine
  - Output managemen

- **joelschaeffer.com**: <https://github.com/lightwave-media/joelschaeffer.com>
  - Portfolio site
  - E-commerce
  - Blog system

- **lightwave-media.site**: <https://github.com/lightwave-media/lightwave-media.site>
  - Corporate website
  - Company information
  - Marketing conten

### Development Tools

- **lightwave-project-starter**: <https://github.com/lightwave-media/lightwave-project-starter>
  - Project templates
  - Development setup
  - Best practices

- **lightwave-dev-tools**: <https://github.com/lightwave-media/lightwave-dev-tools>
  - Development utilities
  - Testing tools
  - Debugging tools

- **lightwave-ci-cd**: <https://github.com/lightwave-media/lightwave-ci-cd>
  - CI/CD pipelines
  - Deployment automation
  - Quality gates

### Documentation

- **lightwave-eco-system-docs**: <https://github.com/lightwave-media/lightwave-eco-system-docs>
  - System documentation
  - API references
  - User guides

## Implementation Guidelines

> **Important**: Follow these guidelines when implementing new endpoints or modifying existing ones.

### URL Structure Guidelines

1. **Consistency**
   - Use consistent URL patterns across all applications
   - Follow RESTful conventions
   - Maintain hierarchical organization

2. **Versioning**
   - All API endpoints must be versioned
   - Use semantic versioning for major changes
   - Maintain backward compatibility

3. **Security**
   - Implement proper authentication
   - Use HTTPS for all endpoints
   - Follow security best practices

4. **Performance**
   - Optimize for speed
   - Implement caching
   - Use compression

5. **Documentation**
   - Document all endpoints
   - Include examples
   - Maintain changelog

### Best Practices

1. **Naming Conventions**
   - Use lowercase for URLs
   - Use hyphens for word separation
   - Keep URLs concise and meaningful

2. **Resource Identification**
   - Use UUIDs for resource IDs
   - Implement proper error handling
   - Include resource metadata

3. **API Design**
   - Follow REST principles
   - Use proper HTTP methods
   - Implement proper status codes

4. **Error Handling**
   - Use consistent error formats
   - Provide meaningful error messages
   - Include error codes

5. **Rate Limiting**
   - Implement rate limiting
   - Use proper headers
   - Document limits

6. **Caching**
   - Use cache headers
   - Implement ETags
   - Consider CDN usage

7. **Monitoring**
   - Track endpoint usage
   - Monitor performance
   - Log errors

8. **Testing**
   - Write unit tests
   - Implement integration tests
   - Perform load testing

9. **Documentation**
   - Keep documentation updated
   - Include examples
   - Document changes

10. **Security**
    - Follow security guidelines
    - Implement proper authentication
    - Use secure protocols
