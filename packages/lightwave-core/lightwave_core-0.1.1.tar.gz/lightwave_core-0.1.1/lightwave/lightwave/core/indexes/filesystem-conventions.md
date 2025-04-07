# LightWave Ecosystem Filesystem Conventions

> **Note**: This document serves as the single source of truth for filesystem conventions and project structures across the LightWave ecosystem. These conventions ensure consistency, maintainability, and easier collaboration across projects.

## Table of Contents

1. [Overview](#overview)
2. [Common Project Structure](#common-project-structure)
3. [Repository Organization](#repository-organization)
4. [Django Application Structure](#django-application-structure)
5. [Frontend Application Structure](#frontend-application-structure)
6. [Documentation Organization](#documentation-organization)
7. [Infrastructure as Code Structure](#infrastructure-as-code-structure)
8. [Naming Conventions](#naming-conventions)
9. [Media and Static Asset Organization](#media-and-static-asset-organization)
10. [Implementation Guidelines](#implementation-guidelines)

## Overview

The LightWave ecosystem follows standardized filesystem conventions across all projects to ensure:

- Consistent project structure across repositories
- Intuitive location of components and files
- Clear separation of concerns
- Efficient collaboration across teams
- Streamlined onboarding for new developers
- Simplified maintenance and updates

## Common Project Structure

All LightWave repositories follow this high-level structure:

```tex
repository-name/
├── README.md               # Project overview and quickstar
├── CONTRIBUTING.md         # Contribution guidelines
├── LICENSE                 # Project license
├── CHANGELOG.md            # Version history and changes
├── .github/                # GitHub specific files
│   ├── workflows/          # GitHub Actions workflows
│   └── ISSUE_TEMPLATE/     # Issue templates
├── docs/                   # Documentation
├── src/                    # Source code
│   ├── backend/            # Backend code
│   └── frontend/           # Frontend code
├── tests/                  # Test files
├── scripts/                # Utility scripts
├── config/                 # Configuration files
└── .editorconfig           # Editor configuration
```

## Repository Organization

### Core Infrastructure Repositories

Repositories like `lightwave-infrastructure` and `lightwave-shared-core` follow this structure:

```tex
repository-name/
├── src/
│   ├── core/               # Core functionality
│   ├── utils/              # Utility functions
│   ├── services/           # Service implementations
│   ├── models/             # Data models
│   ├── config/             # Configuration managemen
│   └── integrations/       # External integrations
├── terraform/              # Infrastructure as Code
│   ├── modules/            # Reusable Terraform modules
│   └── environments/       # Environment-specific configurations
├── kubernetes/             # Kubernetes manifests
│   ├── base/               # Base configurations
│   └── overlays/           # Environment-specific overlays
└── scripts/
    ├── deployment/         # Deployment scripts
    ├── monitoring/         # Monitoring scripts
    └── maintenance/        # Maintenance scripts
```

### Application Repositories

Application repositories like `createos.io` and `cineos.io` follow this structure:

```tex
application-name/
├── src/
│   ├── backend/
│   │   ├── app/            # Main application code
│   │   ├── core/           # Core functionality
│   │   ├── api/            # API implementations
│   │   ├── auth/           # Authentication
│   │   ├── models/         # Data models
│   │   ├── services/       # Service implementations
│   │   ├── utils/          # Utility functions
│   │   └── tests/          # Unit tests
│   └── frontend/
│       ├── components/     # UI components
│       ├── pages/          # Page components
│       ├── styles/         # Styling
│       ├── hooks/          # React hooks
│       ├── utils/          # Utility functions
│       ├── services/       # Service clients
│       ├── assets/         # Static assets
│       └── tests/          # Frontend tests
├── docker/
│   ├── backend.Dockerfile  # Backend Docker configuration
│   └── frontend.Dockerfile # Frontend Docker configuration
└── deploy/
    ├── staging/            # Staging deployment files
    └── production/         # Production deployment files
```

### Development Tool Repositories

Development tool repositories like `lightwave-project-starter` follow this structure:

```tex
tool-name/
├── src/
│   ├── templates/          # Project templates
│   ├── generators/         # Code generators
│   ├── validators/         # Validation logic
│   └── utils/              # Utility functions
├── cli/                    # Command-line interface
├── samples/                # Sample projects/code
└── scripts/
    └── install/            # Installation scripts
```

### Documentation Repositories

Documentation repositories like `lightwave-eco-system-docs` follow this structure:

```tex
docs-repository/
├── index.md                # Main documentation entry poin
├── getting-started/        # Getting started guides
├── tutorials/              # Step-by-step tutorials
├── api-reference/          # API documentation
├── guides/                 # User guides
├── repositories/           # Repository-specific documentation
│   ├── repository-1/       # One folder per repository
│   └── repository-2/
├── architecture/           # Architecture documentation
├── decisions/              # Architecture Decision Records (ADRs)
├── assets/                 # Documentation assets
│   ├── images/             # Documentation images
│   └── diagrams/           # Architecture diagrams
└── glossary/               # Terminology definitions
```

## Django Application Structure

Django applications within the LightWave ecosystem follow this structure:

```tex
django-application/
├── src/backend/
│   ├── config/             # Project settings
│   │   ├── settings/       # Environment-specific settings
│   │   ├── urls.py         # URL routing
│   │   └── wsgi.py         # WSGI configuration
│   ├── apps/               # Django applications
│   │   ├── users/          # User management app
│   │   │   ├── __init__.py
│   │   │   ├── admin.py    # Admin interface
│   │   │   ├── apps.py     # App configuration
│   │   │   ├── models.py   # Data models
│   │   │   ├── serializers.py # API serializers
│   │   │   ├── services.py # Business logic
│   │   │   ├── urls.py     # URL patterns
│   │   │   └── views.py    # View controllers
│   │   └── # Other apps following the same structure
│   ├── core/               # Core functionality
│   │   ├── __init__.py
│   │   ├── middleware.py   # Custom middleware
│   │   ├── exceptions.py   # Custom exceptions
│   │   └── utils.py        # Utility functions
│   ├── templates/          # HTML templates
│   │   ├── base.html       # Base template
│   │   └── # App-specific templates
│   ├── static/             # Static files
│   │   ├── css/            # CSS files
│   │   ├── js/             # JavaScript files
│   │   └── images/         # Image files
│   └── manage.py           # Django management scrip
├── tests/                  # Test files
│   ├── conftest.py         # Test configuration
│   ├── factories.py        # Test factories
│   └── # Test modules
└── requirements/           # Dependency files
    ├── base.txt            # Base requirements
    ├── dev.txt             # Development requirements
    └── prod.txt            # Production requirements
```

## Frontend Application Structure

Frontend applications within the LightWave ecosystem follow this structure:

```tex
frontend-application/
├── src/frontend/
│   ├── public/             # Public assets
│   │   ├── index.html      # HTML entry poin
│   │   ├── favicon.ico     # Favicon
│   │   └── robots.txt      # Robots file
│   ├── src/                # Source code
│   │   ├── components/     # UI components
│   │   │   ├── common/     # Common components
│   │   │   │   ├── Button.tsx
│   │   │   │   ├── Card.tsx
│   │   │   │   └── # Other common components
│   │   │   └── # Feature-specific components
│   │   ├── pages/          # Page components
│   │   │   ├── Home.tsx    # Home page
│   │   │   ├── Dashboard.tsx # Dashboard page
│   │   │   └── # Other pages
│   │   ├── hooks/          # Custom hooks
│   │   ├── contexts/       # React contexts
│   │   ├── services/       # API services
│   │   │   ├── api.ts      # API clien
│   │   │   ├── auth.ts     # Authentication service
│   │   │   └── # Other services
│   │   ├── utils/          # Utility functions
│   │   ├── types/          # TypeScript type definitions
│   │   ├── assets/         # Static assets
│   │   │   ├── images/     # Image files
│   │   │   └── styles/     # Global styles
│   │   ├── App.tsx         # Main application componen
│   │   ├── index.tsx       # Application entry poin
│   │   └── routes.tsx      # Route definitions
│   ├── package.json        # Dependencies and scripts
│   ├── tsconfig.json       # TypeScript configuration
│   └── .eslintrc.js        # ESLint configuration
└── tests/                  # Test files
    ├── setupTests.ts       # Test setup
    └── # Test files
```

## Documentation Organization

All documentation within the LightWave ecosystem follows this structure:

```tex
docs/
├── index.md                # Documentation home page
├── getting-started/        # Getting started guides
│   ├── installation.md     # Installation guide
│   ├── quickstart.md       # Quickstart guide
│   └── configuration.md    # Configuration guide
├── tutorials/              # Step-by-step tutorials
│   ├── tutorial-1.md       # First tutorial
│   └── # Other tutorials
├── user-guides/            # User guides
│   ├── guide-1.md          # First guide
│   └── # Other guides
├── api-reference/          # API documentation
│   ├── overview.md         # API overview
│   ├── authentication.md   # Authentication
│   └── # Endpoint documentation
├── architecture/           # Architecture documentation
│   ├── overview.md         # Architecture overview
│   ├── components.md       # Component documentation
│   └── # Other architecture docs
└── contributing/           # Contribution guidelines
    ├── code-style.md       # Code style guide
    ├── pull-requests.md    # PR guidelines
    └── testing.md          # Testing guidelines
```

## Infrastructure as Code Structure

Infrastructure as Code (IaC) within the LightWave ecosystem follows this structure:

```tex
terraform/
├── modules/                # Reusable Terraform modules
│   ├── networking/         # Networking module
│   │   ├── main.tf         # Main configuration
│   │   ├── variables.tf    # Input variables
│   │   ├── outputs.tf      # Output values
│   │   └── README.md       # Module documentation
│   ├── database/           # Database module
│   │   └── # Similar structure
│   └── # Other modules
├── environments/           # Environment-specific configurations
│   ├── dev/                # Development environmen
│   │   ├── main.tf         # Main configuration
│   │   ├── variables.tf    # Environment variables
│   │   └── terraform.tfvars # Variable values
│   ├── staging/            # Staging environmen
│   │   └── # Similar structure
│   └── production/         # Production environmen
│       └── # Similar structure
└── scripts/                # Terraform scripts
    ├── init.sh             # Initialization scrip
    └── apply.sh            # Apply scrip
```

## Naming Conventions

### File and Directory Naming

- Use `kebab-case` for directory names: `user-management/`
- Use `snake_case` for Python files: `user_utils.py`
- Use `PascalCase` for React component files: `UserProfile.tsx`
- Use `camelCase` for JavaScript/TypeScript utility files: `dateUtils.ts`
- Use `UPPER_SNAKE_CASE` for constant files: `API_ENDPOINTS.ts`

### Code Naming

- Classes: `PascalCase` (e.g., `UserManager`)
- Functions/Methods: `snake_case` in Python, `camelCase` in JavaScript/TypeScrip
- Variables: `snake_case` in Python, `camelCase` in JavaScript/TypeScrip
- Constants: `UPPER_SNAKE_CASE` (e.g., `MAX_RETRY_COUNT`)
- Database Tables: `plural_snake_case` (e.g., `user_profiles`)
- CSS Classes: `kebab-case` (e.g., `user-avatar`)

### Branch Naming

- Feature branches: `feature/short-description`
- Bugfix branches: `bugfix/short-description`
- Hotfix branches: `hotfix/short-description`
- Release branches: `release/version`

## Media and Static Asset Organization

Media and static assets follow this organization:

```tex
static/
├── css/                    # CSS files
│   ├── vendor/             # Third-party CSS
│   └── app/                # Application CSS
├── js/                     # JavaScript files
│   ├── vendor/             # Third-party JS
│   └── app/                # Application JS
├── images/                 # Image files
│   ├── icons/              # Icon images
│   ├── logos/              # Logo images
│   └── backgrounds/        # Background images
└── fonts/                  # Font files

media/
├── uploads/                # User uploads
│   ├── profile-pictures/   # Profile pictures
│   └── documents/          # Document uploads
├── generated/              # Generated media
└── exports/                # Exported files
```

## Implementation Guidelines

### Project Setup Guidelines

1. **Create Standard Directory Structure**
   - Set up the project following the appropriate template for its type
   - Use the `lightwave-project-starter` tool to scaffold new projects
   - Include all standard files (README.md, LICENSE, etc.)

2. **Configuration Management**
   - Store environment-specific configurations in appropriate files
   - Use environment variables for sensitive information
   - Document all configuration options

3. **Documentation Requirements**
   - Every repository must include a README.md with:
     - Project description
     - Setup instructions
     - Usage examples
     - Link to full documentation
   - Include inline documentation for code
   - Maintain architecture documentation

### Directory Organization Best Practices

1. **Logical Grouping**
   - Group related files together
   - Separate by feature rather than file type when appropriate
   - Keep modules small and focused

2. **Dependency Management**
   - Clearly define module dependencies
   - Avoid circular dependencies
   - Use virtual environments for Python projects
   - Use package managers for JavaScript/TypeScript projects

3. **Testing Organization**
   - Mirror the source directory structure in test directories
   - Use appropriate naming: `test_*.py` for Python, `*.test.ts` for TypeScrip
   - Separate unit, integration, and end-to-end tests

### File Placement Rules

1. **Code Files**
   - Place application code in the `src/` directory
   - Place tests in the `tests/` directory
   - Keep utility scripts in the `scripts/` directory

2. **Configuration Files**
   - Place global configuration in the `config/` directory
   - Place environment-specific configuration in environment subdirectories
   - Store local development configurations in `.local` files

3. **Documentation Files**
   - Place all documentation in the `docs/` directory
   - Use Markdown format for documentation files
   - Include diagrams and images in the `docs/assets/` directory

### Version Control Guidelines

1. **Repository Structure**
   - Keep repositories focused on a single domain
   - Use monorepos only when components are tightly coupled
   - Include .gitignore file with appropriate patterns

2. **Commit Organization**
   - Make atomic, focused commits
   - Use conventional commit messages
   - Reference issue numbers in commit messages

## Related Documentation

- [Project Starter Guide](../lightwave-project-starter/project-starter-guide.md)
- [Code Style Guide](../lightwave-dev-tools/code-style-guide.md)
- [CI/CD Pipeline Documentation](../lightwave-ci-cd/pipeline-documentation.md)
- [Architecture Documentation](../architecture/overview.md)
- [Django Application Template](../lightwave-project-starter/templates/django-application.md)
- [React Application Template](../lightwave-project-starter/templates/react-application.md)