# LightWave Ecosystem Schema Registry

> **Note**: This document serves as the single source of truth for data schemas across the LightWave ecosystem. These schemas define the structure and validation rules for data exchanged between services.

## Table of Contents

1. [Overview](#overview)
2. [Schema Standards](#schema-standards)
3. [Core Schemas](#core-schemas)
4. [User Schemas](#user-schemas)
5. [Project Schemas](#project-schemas)
6. [Media Schemas](#media-schemas)
7. [Integration Schemas](#integration-schemas)
8. [Versioning Strategy](#versioning-strategy)
9. [Implementation Guidelines](#implementation-guidelines)
10. [Related Documentation](#related-documentation)

## Overview

The LightWave ecosystem uses standardized JSON schemas to ensure data consistency, validation, and interoperability across services. This registry provides the authoritative definitions for all data structures used in the ecosystem.

All schemas follow JSON Schema draft-07 specifications and are available in machine-readable format for implementation in various languages and frameworks.

## Schema Standards

All schemas in the LightWave ecosystem adhere to these standards:

- JSON Schema draft-07 forma
- Camel case for property names (e.g., `firstName`)
- Required properties explicitly listed
- Clear descriptions for all properties
- Appropriate data types and formats specified
- Default values provided where applicable
- Validation constraints (min/max length, pattern, etc.) defined
- Nested objects handled via `$ref` references
- Enums used for fixed-value properties

## Core Schemas

### BaseEntity Schema

Base schema for all entities in the system.

#### Fields

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| id | string (uuid) | Unique identifier | Yes |
| createdAt | string (date-time) | Creation timestamp | Yes |
| updatedAt | string (date-time) | Last update timestamp | Yes |
| version | integer | Schema version number | Yes |

#### Examples

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "createdAt": "2023-11-25T12:34:56Z",
  "updatedAt": "2023-11-25T12:34:56Z",
  "version": 1
}
```

### Error Schema

Standard error response format.

#### Fields

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| code | string | Error code | Yes |
| message | string | Human-readable error message | Yes |
| details | object | Additional error details | No |
| requestId | string | Request identifier for tracing | No |

#### Examples

```json
{
  "code": "VALIDATION_ERROR",
  "message": "Invalid input data",
  "details": {
    "field": "email",
    "constraint": "format",
    "message": "Must be a valid email address"
  },
  "requestId": "req-123456-abcdef"
}
```

### Pagination Schema

Standard pagination response wrapper.

#### Fields

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| items | array | List of paginated items | Yes |
| total | integer | Total number of items | Yes |
| page | integer | Current page number | Yes |
| pageSize | integer | Number of items per page | Yes |
| totalPages | integer | Total number of pages | Yes |
| hasNext | boolean | Whether there are more pages | Yes |
| hasPrevious | boolean | Whether there are previous pages | Yes |

#### Examples

```json
{
  "items": [
    { "id": "item-1", "name": "First Item" },
    { "id": "item-2", "name": "Second Item" }
  ],
  "total": 10,
  "page": 1,
  "pageSize": 2,
  "totalPages": 5,
  "hasNext": true,
  "hasPrevious": false
}
```

## User Schemas

### User Schema

Represents a user in the system.

#### Fields

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| id | string (uuid) | User identifier | Yes |
| email | string (email) | Email address | Yes |
| firstName | string | First name | Yes |
| lastName | string | Last name | Yes |
| displayName | string | Display name | No |
| profilePicture | string (uri) | Profile picture URL | No |
| role | string (enum) | User role | Yes |
| status | string (enum) | Account status | Yes |
| createdAt | string (date-time) | Account creation date | Yes |
| updatedAt | string (date-time) | Last update date | Yes |
| lastLoginAt | string (date-time) | Last login date | No |
| preferences | object | User preferences | No |
| metadata | object | Additional metadata | No |

#### Examples

```json
{
  "id": "user-123456",
  "email": "john.doe@example.com",
  "firstName": "John",
  "lastName": "Doe",
  "displayName": "John Doe",
  "profilePicture": "https://assets.lightwave-media.site/users/user-123456/profile.jpg",
  "role": "ADMIN",
  "status": "ACTIVE",
  "createdAt": "2023-01-15T10:30:00Z",
  "updatedAt": "2023-11-20T14:25:10Z",
  "lastLoginAt": "2023-11-25T08:15:30Z",
  "preferences": {
    "theme": "dark",
    "notifications": {
      "email": true,
      "push": false
    }
  },
  "metadata": {
    "department": "Engineering",
    "location": "Remote"
  }
}
```

### UserProfile Schema

Public user profile information.

#### Fields

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| id | string (uuid) | User identifier | Yes |
| displayName | string | Display name | Yes |
| profilePicture | string (uri) | Profile picture URL | No |
| bio | string | User biography | No |
| website | string (uri) | Personal website | No |
| social | object | Social media links | No |
| joinedAt | string (date-time) | Join date | Yes |

#### Examples

```json
{
  "id": "user-123456",
  "displayName": "John Doe",
  "profilePicture": "https://assets.lightwave-media.site/users/user-123456/profile.jpg",
  "bio": "Senior Software Engineer with a passion for photography",
  "website": "https://johndoe.com",
  "social": {
    "twitter": "johndoe",
    "github": "johndoe",
    "linkedin": "john-doe-12345"
  },
  "joinedAt": "2023-01-15T10:30:00Z"
}
```

## Project Schemas

### Project Schema

Represents a project within the LightWave ecosystem.

#### Fields

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| id | string (uuid) | Project identifier | Yes |
| name | string | Project name | Yes |
| description | string | Project description | No |
| clientId | string (uuid) | Associated client identifier | Yes |
| status | string (enum) | Project status | Yes |
| type | string (enum) | Project type | Yes |
| startDate | string (date) | Project start date | Yes |
| endDate | string (date) | Project end date | No |
| budget | object | Budget information | No |
| team | array | Team members | No |
| createdAt | string (date-time) | Creation date | Yes |
| updatedAt | string (date-time) | Last update date | Yes |
| metadata | object | Additional metadata | No |

#### Examples

```json
{
  "id": "project-789012",
  "name": "Brand Photography Campaign",
  "description": "Corporate photography campaign for Q1 marketing materials",
  "clientId": "client-456789",
  "status": "IN_PROGRESS",
  "type": "PHOTOGRAPHY",
  "startDate": "2023-11-01",
  "endDate": "2023-12-15",
  "budget": {
    "amount": 15000,
    "currency": "USD",
    "type": "FIXED"
  },
  "team": [
    {
      "userId": "user-123456",
      "role": "PROJECT_MANAGER"
    },
    {
      "userId": "user-234567",
      "role": "PHOTOGRAPHER"
    }
  ],
  "createdAt": "2023-10-15T09:30:00Z",
  "updatedAt": "2023-11-20T14:15:00Z",
  "metadata": {
    "priority": "HIGH",
    "category": "Corporate"
  }
}
```

### Task Schema

Represents a task within a project.

#### Fields

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| id | string (uuid) | Task identifier | Yes |
| projectId | string (uuid) | Associated project identifier | Yes |
| title | string | Task title | Yes |
| description | string | Task description | No |
| assigneeId | string (uuid) | Assignee user identifier | No |
| status | string (enum) | Task status | Yes |
| priority | string (enum) | Task priority | Yes |
| dueDate | string (date) | Due date | No |
| estimatedHours | number | Estimated hours | No |
| actualHours | number | Actual hours spent | No |
| createdAt | string (date-time) | Creation date | Yes |
| updatedAt | string (date-time) | Last update date | Yes |
| completedAt | string (date-time) | Completion date | No |

#### Examples

```json
{
  "id": "task-345678",
  "projectId": "project-789012",
  "title": "Product Photography Session",
  "description": "Photograph new product line against white background",
  "assigneeId": "user-234567",
  "status": "IN_PROGRESS",
  "priority": "HIGH",
  "dueDate": "2023-11-30",
  "estimatedHours": 8,
  "actualHours": 4.5,
  "createdAt": "2023-11-20T09:00:00Z",
  "updatedAt": "2023-11-22T13:30:00Z",
  "completedAt": null
}
```

## Media Schemas

### Media Schema

Base schema for all media assets.

#### Fields

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| id | string (uuid) | Media identifier | Yes |
| type | string (enum) | Media type | Yes |
| name | string | File name | Yes |
| description | string | Media description | No |
| mimeType | string | MIME type | Yes |
| size | integer | File size in bytes | Yes |
| width | integer | Width in pixels (for images/videos) | No |
| height | integer | Height in pixels (for images/videos) | No |
| duration | number | Duration in seconds (for audio/video) | No |
| url | string (uri) | Access URL | Yes |
| thumbnailUrl | string (uri) | Thumbnail URL | No |
| ownerId | string (uuid) | Owner user identifier | Yes |
| access | string (enum) | Access level | Yes |
| metadata | object | Additional metadata | No |
| tags | array | Associated tags | No |
| createdAt | string (date-time) | Creation date | Yes |
| updatedAt | string (date-time) | Last update date | Yes |

#### Examples

```json
{
  "id": "media-901234",
  "type": "IMAGE",
  "name": "product-hero-shot.jpg",
  "description": "Main hero image for the new product line",
  "mimeType": "image/jpeg",
  "size": 2456789,
  "width": 4000,
  "height": 3000,
  "url": "https://assets.lightwave-media.site/projects/project-789012/product-hero-shot.jpg",
  "thumbnailUrl": "https://assets.lightwave-media.site/projects/project-789012/thumbnails/product-hero-shot.jpg",
  "ownerId": "user-234567",
  "access": "PROJECT",
  "metadata": {
    "camera": "Canon EOS R5",
    "lens": "RF 24-70mm F2.8 L IS USM",
    "iso": 100,
    "aperture": "f/8",
    "shutterSpeed": "1/125",
    "colorSpace": "sRGB"
  },
  "tags": ["product", "hero", "white-background"],
  "createdAt": "2023-11-22T10:15:00Z",
  "updatedAt": "2023-11-22T10:15:00Z"
}
```

### Collection Schema

Represents a collection of media assets.

#### Fields

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| id | string (uuid) | Collection identifier | Yes |
| name | string | Collection name | Yes |
| description | string | Collection description | No |
| type | string (enum) | Collection type | Yes |
| ownerId | string (uuid) | Owner user identifier | Yes |
| projectId | string (uuid) | Associated project identifier | No |
| mediaIds | array | List of media identifiers | Yes |
| coverMediaId | string (uuid) | Cover media identifier | No |
| access | string (enum) | Access level | Yes |
| shareUrl | string (uri) | Public share URL | No |
| password | string | Password protection | No |
| expiresAt | string (date-time) | Expiration date | No |
| createdAt | string (date-time) | Creation date | Yes |
| updatedAt | string (date-time) | Last update date | Yes |

#### Examples

```json
{
  "id": "collection-567890",
  "name": "Product Line Photos",
  "description": "Approved photos for the new product line",
  "type": "GALLERY",
  "ownerId": "user-234567",
  "projectId": "project-789012",
  "mediaIds": [
    "media-901234",
    "media-901235",
    "media-901236"
  ],
  "coverMediaId": "media-901234",
  "access": "CLIENT",
  "shareUrl": "https://share.lightwave-media.site/g/collection-567890",
  "password": "product2023",
  "expiresAt": "2024-01-31T23:59:59Z",
  "createdAt": "2023-11-23T15:30:00Z",
  "updatedAt": "2023-11-24T10:45:00Z"
}
```

## Integration Schemas

### Webhook Schema

Represents a webhook configuration.

#### Fields

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| id | string (uuid) | Webhook identifier | Yes |
| url | string (uri) | Webhook endpoint URL | Yes |
| events | array | Subscribed event types | Yes |
| active | boolean | Whether webhook is active | Yes |
| secret | string | Webhook secret | No |
| description | string | Webhook description | No |
| createdAt | string (date-time) | Creation date | Yes |
| updatedAt | string (date-time) | Last update date | Yes |
| lastTriggeredAt | string (date-time) | Last trigger date | No |
| failureCount | integer | Consecutive failure count | Yes |

#### Examples

```json
{
  "id": "webhook-123456",
  "url": "https://example.com/webhook",
  "events": ["media.created", "media.updated", "collection.shared"],
  "active": true,
  "secret": "whsec_abcdefghijklmnopqrstuvwxyz123456",
  "description": "Media updates notification endpoint",
  "createdAt": "2023-10-01T09:00:00Z",
  "updatedAt": "2023-10-01T09:00:00Z",
  "lastTriggeredAt": "2023-11-24T15:30:22Z",
  "failureCount": 0
}
```

### OAuth2Connection Schema

Represents an OAuth2 connection to an external service.

#### Fields

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| id | string (uuid) | Connection identifier | Yes |
| userId | string (uuid) | User identifier | Yes |
| provider | string (enum) | OAuth provider | Yes |
| accessToken | string | Access token | No |
| refreshToken | string | Refresh token | No |
| expiresAt | string (date-time) | Token expiration date | No |
| scope | string | OAuth scopes | Yes |
| providerUserId | string | User ID at provider | Yes |
| metadata | object | Additional metadata | No |
| createdAt | string (date-time) | Creation date | Yes |
| updatedAt | string (date-time) | Last update date | Yes |
| lastUsedAt | string (date-time) | Last usage date | No |

#### Examples

```json
{
  "id": "oauth-234567",
  "userId": "user-123456",
  "provider": "GOOGLE",
  "accessToken": "[REDACTED]",
  "refreshToken": "[REDACTED]",
  "expiresAt": "2023-12-25T10:30:00Z",
  "scope": "profile email drive.readonly",
  "providerUserId": "google-user-12345",
  "metadata": {
    "email": "john.doe@gmail.com",
    "displayName": "John Doe"
  },
  "createdAt": "2023-11-25T10:30:00Z",
  "updatedAt": "2023-11-25T10:30:00Z",
  "lastUsedAt": "2023-11-25T10:30:00Z"
}
```

## Versioning Strategy

The LightWave ecosystem follows these schema versioning principles:

- Schemas use explicit version fields to track schema versions
- Backward compatibility is maintained whenever possible
- New optional fields can be added without changing the version
- When breaking changes are needed, a new version is created
- Old versions remain supported for a deprecation period
- Deprecation notices are provided through API responses
- Migration guides are provided for all schema version changes
- Version history is documented for all schemas

## Implementation Guidelines

When implementing or consuming LightWave schemas:

- Always validate data against the appropriate schema
- Handle unknown properties gracefully (don't break on extra fields)
- Include schema versions in all data objects
- Use appropriate data formats (ISO dates, proper UUIDs, etc.)
- When upgrading, test against all schema versions still in use
- For critical data, maintain schema validation on both client and server
- Be aware of required vs. optional fields in your implementation
- Implement fallbacks for missing optional fields
- Use enums only for the specified values
- Maintain proper nesting structure for complex objects

## Related Documentation

- [API Design Principles](../lightwave-api-gateway/api-design-principles.md)
- [API Endpoints Index](api-endpoints-index.md)
- [Data Validation Guide](../lightwave-shared-core/data-validation.md)
- [Schema Versioning Policy](../lightwave-api-gateway/schema-versioning.md)