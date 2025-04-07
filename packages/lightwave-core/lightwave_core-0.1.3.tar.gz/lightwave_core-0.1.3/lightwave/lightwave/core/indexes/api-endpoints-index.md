# LightWave Ecosystem API Endpoints Index

> **Note**: This document serves as the single source of truth for all API endpoints across the LightWave ecosystem. It provides a complete reference of all endpoints with authentication requirements and usage patterns.

## Table of Contents

1. [API Structure Overview](#api-structure-overview)
2. [Authentication Endpoints](#authentication-endpoints)
3. [Core Service Endpoints](#core-service-endpoints)
4. [Application-specific Endpoints](#application-specific-endpoints)
5. [Integration Endpoints](#integration-endpoints)
6. [Implementation Guidelines](#implementation-guidelines)

## API Structure Overview

All LightWave ecosystem APIs follow these conventions:

* **Base URL Pattern**: `https://api.{domain}.{tld}/v1/`
* **Authentication**: JWT tokens via Bearer authentication
* **Content Type**: JSON for request and response bodies
* **Versioning**: URL-based versioning with `v1`, `v2`, etc.
* **Error Format**: Standardized error responses with code, message, and details
* **Response Envelope**: All responses include status, data, and meta fields
* **Documentation**: OpenAPI/Swagger documentation available at `/docs`

## Authentication Endpoints

Authentication services are provided by each application's auth subdomain.

### Central Authentication (createos.io)

Base URL: `https://auth.createos.io/v1/`

| Method | Endpoint | Description | Authentication | Status |
|--------|----------|-------------|----------------|--------|
| POST | `/login/` | Authenticate user credentials | None | Live |
| POST | `/logout/` | Invalidate user session | Bearer Token | Live |
| POST | `/refresh/` | Refresh authentication token | Refresh Token | Live |
| GET | `/verify/` | Verify token validity | Bearer Token | Live |
| POST | `/register/` | Register new user | None | Live |
| POST | `/password/reset/` | Request password reset | None | Live |
| POST | `/password/change/` | Change password | Bearer Token | Live |
| POST | `/password/forgot/` | Forgot password flow | None | Live |
| POST | `/password/validate/` | Validate password strength | None | Live |
| GET | `/2fa/enable/` | Enable two-factor auth | Bearer Token | Live |
| GET | `/2fa/disable/` | Disable two-factor auth | Bearer Token | Live |
| POST | `/2fa/verify/` | Verify 2FA code | Bearer Token | Live |
| GET | `/2fa/backup/` | Generate backup codes | Bearer Token | Live |
| GET | `/2fa/recovery/` | Recovery options | Bearer Token | Live |
| GET | `/sessions/list/` | List active sessions | Bearer Token | Live |
| POST | `/sessions/revoke/` | Revoke specific session | Bearer Token | Live |
| POST | `/sessions/revoke-all/` | Revoke all sessions | Bearer Token | Live |
| GET | `/sessions/info/` | Get session information | Bearer Token | Live |
| GET | `/oauth/providers/` | List OAuth providers | None | Live |
| GET | `/oauth/{provider}/login/` | Initialize OAuth flow | None | Live |
| GET | `/oauth/{provider}/callback/` | OAuth callback | None | Live |
| POST | `/oauth/{provider}/revoke/` | Revoke OAuth access | Bearer Token | Live |
| POST | `/oauth/{provider}/refresh/` | Refresh OAuth token | Bearer Token | Live |
| GET | `/oauth/{provider}/profile/` | Get OAuth profile data | Bearer Token | Live |
| GET | `/sso/initiate/` | Initiate SSO flow | None | Live |
| GET | `/sso/callback/` | SSO callback | None | Live |
| GET | `/sso/metadata/` | SSO metadata | None | Live |
| POST | `/sso/logout/` | SSO logout | Bearer Token | Live |

### Photography OS Authentication

Base URL: `https://auth.photographyos.io/v1/`

Same endpoints as CreateOS authentication, with application-specific business logic.

### Cinematography OS Authentication

Base URL: `https://auth.cineos.io/v1/`

Same endpoints as CreateOS authentication, with application-specific business logic.

### Photo Workflows Authentication

Base URL: `https://auth.photo-workflows.com/v1/`

Same endpoints as CreateOS authentication, with application-specific business logic.

## Core Service Endpoints

### API Gateway

Base URL: `https://api.gateway.lightwave-media.site/v1/`

| Method | Endpoint | Description | Authentication | Status |
|--------|----------|-------------|----------------|--------|
| GET | `/status/` | Gateway status | None | Live |
| GET | `/routes/` | List available routes | Bearer Token | Live |
| GET | `/services/` | List running services | Bearer Token | Live |
| GET | `/metrics/` | Retrieve gateway metrics | Bearer Token | Live |
| POST | `/cache/flush/` | Flush gateway cache | Bearer Token | Live |
| GET | `/ratelimit/status/` | Rate limiting status | Bearer Token | Live |

### Monitoring Service

Base URL: `https://api.monitoring.lightwave-media.site/v1/`

| Method | Endpoint | Description | Authentication | Status |
|--------|----------|-------------|----------------|--------|
| GET | `/status/` | System status overview | Bearer Token | Live |
| GET | `/alerts/` | Active alerts | Bearer Token | Live |
| GET | `/metrics/` | System metrics | Bearer Token | Live |
| GET | `/logs/` | System logs | Bearer Token | Live |
| GET | `/services/` | Service health | Bearer Token | Live |
| GET | `/uptime/` | Service uptime | Bearer Token | Live |
| POST | `/alerts/acknowledge/` | Acknowledge alert | Bearer Token | Live |
| POST | `/alerts/resolve/` | Resolve alert | Bearer Token | Live |
| POST | `/alerts/silence/` | Silence alert | Bearer Token | Live |

### Shared Core Services

Base URL: `https://api.shared.lightwave-media.site/v1/`

| Method | Endpoint | Description | Authentication | Status |
|--------|----------|-------------|----------------|--------|
| GET | `/health/` | Health check | None | Live |
| GET | `/config/` | Shared configuration | Bearer Token | Live |
| GET | `/feature-flags/` | Feature flags | Bearer Token | Live |
| GET | `/countries/` | Countries list | None | Live |
| GET | `/currencies/` | Currencies list | None | Live |
| GET | `/timezones/` | Timezones list | None | Live |
| GET | `/languages/` | Languages list | None | Live |

### AI Services

Base URL: `https://api.ai.lightwave-media.site/v1/`

| Method | Endpoint | Description | Authentication | Status |
|--------|----------|-------------|----------------|--------|
| POST | `/text/generate/` | Generate text | Bearer Token | Live |
| POST | `/image/generate/` | Generate image | Bearer Token | Live |
| POST | `/image/edit/` | Edit image | Bearer Token | Live |
| POST | `/image/analyze/` | Analyze image | Bearer Token | Live |
| POST | `/video/analyze/` | Analyze video | Bearer Token | Live |
| POST | `/content/moderate/` | Content moderation | Bearer Token | Live |
| POST | `/speech/transcribe/` | Speech to text | Bearer Token | Live |
| POST | `/text/translate/` | Translate text | Bearer Token | Live |

## Application-specific Endpoints

### CreateOS.io

Base URL: `https://api.createos.io/v1/`

| Method | Endpoint | Description | Authentication | Status |
|--------|----------|-------------|----------------|--------|
| GET | `/users/me/` | Current user details | Bearer Token | Live |
| GET | `/users/{id}/` | User details | Bearer Token | Live |
| GET | `/users/{id}/profile/` | User profile | Bearer Token | Live |
| PATCH | `/users/{id}/profile/` | Update user profile | Bearer Token | Live |
| GET | `/users/{id}/preferences/` | User preferences | Bearer Token | Live |
| PATCH | `/users/{id}/preferences/` | Update preferences | Bearer Token | Live |
| GET | `/users/{id}/activity/` | User activity | Bearer Token | Live |
| GET | `/users/{id}/devices/` | User devices | Bearer Token | Live |
| POST | `/clients/` | Create client | Bearer Token | Live |
| GET | `/clients/` | List clients | Bearer Token | Live |
| GET | `/clients/{id}/` | Client details | Bearer Token | Live |
| PATCH | `/clients/{id}/` | Update client | Bearer Token | Live |
| DELETE | `/clients/{id}/` | Delete client | Bearer Token | Live |
| GET | `/clients/{id}/projects/` | Client's projects | Bearer Token | Live |
| GET | `/clients/{id}/invoices/` | Client's invoices | Bearer Token | Live |
| GET | `/clients/{id}/documents/` | Client documents | Bearer Token | Live |
| GET | `/clients/{id}/history/` | Client history | Bearer Token | Live |
| POST | `/projects/` | Create project | Bearer Token | Live |
| GET | `/projects/` | List projects | Bearer Token | Live |
| GET | `/projects/{id}/` | Project details | Bearer Token | Live |
| PATCH | `/projects/{id}/` | Update project | Bearer Token | Live |
| DELETE | `/projects/{id}/` | Delete project | Bearer Token | Live |
| GET | `/projects/{id}/tasks/` | Project tasks | Bearer Token | Live |
| POST | `/projects/{id}/tasks/` | Create task | Bearer Token | Live |
| GET | `/projects/{id}/files/` | Project files | Bearer Token | Live |
| POST | `/projects/{id}/files/` | Upload file | Bearer Token | Live |
| GET | `/projects/{id}/team/` | Project team | Bearer Token | Live |
| PATCH | `/projects/{id}/team/` | Update team | Bearer Token | Live |
| GET | `/projects/{id}/timeline/` | Project timeline | Bearer Token | Live |
| GET | `/projects/{id}/budget/` | Project budget | Bearer Token | Live |
| PATCH | `/projects/{id}/budget/` | Update budget | Bearer Token | Live |
| GET | `/analytics/revenue/` | Revenue metrics | Bearer Token | Live |
| GET | `/analytics/performance/` | Performance metrics | Bearer Token | Live |
| GET | `/analytics/usage/` | Usage statistics | Bearer Token | Live |
| GET | `/analytics/audience/` | Audience analytics | Bearer Token | Live |
| GET | `/analytics/engagement/` | Engagement metrics | Bearer Token | Live |
| GET | `/integrations/{provider}/connect/` | Connect integration | Bearer Token | Live |
| DELETE | `/integrations/{provider}/disconnect/` | Disconnect integration | Bearer Token | Live |
| POST | `/integrations/{provider}/sync/` | Sync data | Bearer Token | Live |
| POST | `/integrations/{provider}/webhook/` | Webhook endpoint | Webhook Secret | Live |
| GET | `/integrations/{provider}/status/` | Integration status | Bearer Token | Live |
| POST | `/media/upload/` | Media upload | Bearer Token | Live |
| GET | `/media/download/{id}/` | Media download | Bearer Token | Live |
| POST | `/media/process/{id}/` | Media processing | Bearer Token | Live |
| POST | `/media/transform/{id}/` | Media transformation | Bearer Token | Live |
| POST | `/media/optimize/{id}/` | Media optimization | Bearer Token | Live |
| GET | `/notifications/channels/` | Notification channels | Bearer Token | Live |
| GET | `/notifications/templates/` | Notification templates | Bearer Token | Live |
| GET | `/notifications/preferences/` | Notification preferences | Bearer Token | Live |
| PATCH | `/notifications/preferences/` | Update preferences | Bearer Token | Live |
| GET | `/notifications/history/` | Notification history | Bearer Token | Live |
| POST | `/search/index/` | Search index | Bearer Token | Live |
| GET | `/search/query/` | Search query | Bearer Token | Live |
| GET | `/search/suggest/` | Search suggestions | Bearer Token | Live |
| GET | `/search/filters/` | Search filters | Bearer Token | Live |
| POST | `/reports/generate/` | Generate reports | Bearer Token | Live |
| GET | `/reports/templates/` | Report templates | Bearer Token | Live |
| POST | `/reports/schedule/` | Report scheduling | Bearer Token | Live |
| GET | `/reports/export/{id}/` | Report export | Bearer Token | Live |

### PhotographyOS.io

Base URL: `https://api.photographyos.io/v1/`

| Method | Endpoint | Description | Authentication | Status |
|--------|----------|-------------|----------------|--------|
| POST | `/sessions/` | Create photo session | Bearer Token | Live |
| GET | `/sessions/` | List photo sessions | Bearer Token | Live |
| GET | `/sessions/{id}/` | Session details | Bearer Token | Live |
| PATCH | `/sessions/{id}/` | Update session | Bearer Token | Live |
| DELETE | `/sessions/{id}/` | Delete session | Bearer Token | Live |
| GET | `/sessions/{id}/photos/` | Session photos | Bearer Token | Live |
| POST | `/sessions/{id}/photos/` | Upload photos | Bearer Token | Live |
| POST | `/photos/` | Create photo | Bearer Token | Live |
| GET | `/photos/` | List photos | Bearer Token | Live |
| GET | `/photos/{id}/` | Photo details | Bearer Token | Live |
| PATCH | `/photos/{id}/` | Update photo | Bearer Token | Live |
| DELETE | `/photos/{id}/` | Delete photo | Bearer Token | Live |
| POST | `/photos/{id}/edit/` | Edit photo | Bearer Token | Live |
| POST | `/photos/{id}/tags/` | Add tags | Bearer Token | Live |
| DELETE | `/photos/{id}/tags/{tag_id}/` | Remove tag | Bearer Token | Live |
| POST | `/galleries/` | Create gallery | Bearer Token | Live |
| GET | `/galleries/` | List galleries | Bearer Token | Live |
| GET | `/galleries/{id}/` | Gallery details | Bearer Token | Live |
| PATCH | `/galleries/{id}/` | Update gallery | Bearer Token | Live |
| DELETE | `/galleries/{id}/` | Delete gallery | Bearer Token | Live |
| POST | `/galleries/{id}/photos/` | Add photos to gallery | Bearer Token | Live |
| DELETE | `/galleries/{id}/photos/{photo_id}/` | Remove photo from gallery | Bearer Token | Live |
| POST | `/albums/` | Create album | Bearer Token | Live |
| GET | `/albums/` | List albums | Bearer Token | Live |
| GET | `/albums/{id}/` | Album details | Bearer Token | Live |
| PATCH | `/albums/{id}/` | Update album | Bearer Token | Live |
| DELETE | `/albums/{id}/` | Delete album | Bearer Token | Live |
| POST | `/image-processing/resize/` | Resize image | Bearer Token | Live |
| POST | `/image-processing/crop/` | Crop image | Bearer Token | Live |
| POST | `/image-processing/filter/` | Apply filter | Bearer Token | Live |
| POST | `/image-processing/adjust/` | Adjust image | Bearer Token | Live |
| POST | `/image-processing/batch/` | Batch processing | Bearer Token | Live |
| GET | `/clients/{id}/galleries/` | Client galleries | Bearer Token | Live |
| POST | `/clients/{id}/galleries/` | Create client gallery | Bearer Token | Live |
| POST | `/invoices/` | Create invoice | Bearer Token | Live |
| GET | `/invoices/` | List invoices | Bearer Token | Live |
| GET | `/invoices/{id}/` | Invoice details | Bearer Token | Live |
| PATCH | `/invoices/{id}/` | Update invoice | Bearer Token | Live |
| DELETE | `/invoices/{id}/` | Delete invoice | Bearer Token | Live |
| POST | `/invoices/{id}/send/` | Send invoice | Bearer Token | Live |
| GET | `/contracts/` | List contracts | Bearer Token | Live |
| POST | `/contracts/` | Create contract | Bearer Token | Live |
| GET | `/contracts/{id}/` | Contract details | Bearer Token | Live |
| POST | `/contracts/{id}/send/` | Send contract | Bearer Token | Live |
| GET | `/analytics/sessions/` | Session analytics | Bearer Token | Live |
| GET | `/analytics/revenue/` | Revenue analytics | Bearer Token | Live |
| GET | `/analytics/photos/` | Photo analytics | Bearer Token | Live |

### CineOS.io

Base URL: `https://api.cineos.io/v1/`

| Method | Endpoint | Description | Authentication | Status |
|--------|----------|-------------|----------------|--------|
| POST | `/productions/` | Create production | Bearer Token | Live |
| GET | `/productions/` | List productions | Bearer Token | Live |
| GET | `/productions/{id}/` | Production details | Bearer Token | Live |
| PATCH | `/productions/{id}/` | Update production | Bearer Token | Live |
| DELETE | `/productions/{id}/` | Delete production | Bearer Token | Live |
| POST | `/shots/` | Create shot | Bearer Token | Live |
| GET | `/shots/` | List shots | Bearer Token | Live |
| GET | `/shots/{id}/` | Shot details | Bearer Token | Live |
| PATCH | `/shots/{id}/` | Update shot | Bearer Token | Live |
| DELETE | `/shots/{id}/` | Delete shot | Bearer Token | Live |
| POST | `/shots/{id}/metadata/` | Update shot metadata | Bearer Token | Live |
| POST | `/shots/{id}/upload/` | Upload shot file | Bearer Token | Live |
| POST | `/scenes/` | Create scene | Bearer Token | Live |
| GET | `/scenes/` | List scenes | Bearer Token | Live |
| GET | `/scenes/{id}/` | Scene details | Bearer Token | Live |
| PATCH | `/scenes/{id}/` | Update scene | Bearer Token | Live |
| DELETE | `/scenes/{id}/` | Delete scene | Bearer Token | Live |
| GET | `/scenes/{id}/shots/` | Scene shots | Bearer Token | Live |
| POST | `/equipment/` | Create equipment | Bearer Token | Live |
| GET | `/equipment/` | List equipment | Bearer Token | Live |
| GET | `/equipment/{id}/` | Equipment details | Bearer Token | Live |
| PATCH | `/equipment/{id}/` | Update equipment | Bearer Token | Live |
| DELETE | `/equipment/{id}/` | Delete equipment | Bearer Token | Live |
| POST | `/equipment/{id}/maintenance/` | Record maintenance | Bearer Token | Live |
| POST | `/call-sheets/` | Create call sheet | Bearer Token | Live |
| GET | `/call-sheets/` | List call sheets | Bearer Token | Live |
| GET | `/call-sheets/{id}/` | Call sheet details | Bearer Token | Live |
| PATCH | `/call-sheets/{id}/` | Update call sheet | Bearer Token | Live |
| DELETE | `/call-sheets/{id}/` | Delete call sheet | Bearer Token | Live |
| POST | `/call-sheets/{id}/send/` | Send call sheet | Bearer Token | Live |
| POST | `/shot-lists/` | Create shot list | Bearer Token | Live |
| GET | `/shot-lists/` | List shot lists | Bearer Token | Live |
| GET | `/shot-lists/{id}/` | Shot list details | Bearer Token | Live |
| PATCH | `/shot-lists/{id}/` | Update shot list | Bearer Token | Live |
| DELETE | `/shot-lists/{id}/` | Delete shot list | Bearer Token | Live |
| POST | `/budgets/` | Create budget | Bearer Token | Live |
| GET | `/budgets/` | List budgets | Bearer Token | Live |
| GET | `/budgets/{id}/` | Budget details | Bearer Token | Live |
| PATCH | `/budgets/{id}/` | Update budget | Bearer Token | Live |
| DELETE | `/budgets/{id}/` | Delete budget | Bearer Token | Live |
| GET | `/budgets/{id}/line-items/` | Budget line items | Bearer Token | Live |
| POST | `/budgets/{id}/line-items/` | Add line item | Bearer Token | Live |
| POST | `/storyboards/` | Create storyboard | Bearer Token | Live |
| GET | `/storyboards/` | List storyboards | Bearer Token | Live |
| GET | `/storyboards/{id}/` | Storyboard details | Bearer Token | Live |
| PATCH | `/storyboards/{id}/` | Update storyboard | Bearer Token | Live |
| DELETE | `/storyboards/{id}/` | Delete storyboard | Bearer Token | Live |
| POST | `/storyboards/{id}/frames/` | Add storyboard frame | Bearer Token | Live |
| GET | `/analytics/productions/` | Production analytics | Bearer Token | Live |
| GET | `/analytics/equipment/` | Equipment analytics | Bearer Token | Live |

### Photo Workflows

Base URL: `https://api.photo-workflows.com/v1/`

| Method | Endpoint | Description | Authentication | Status |
|--------|----------|-------------|----------------|--------|
| POST | `/workflows/` | Create workflow | Bearer Token | Live |
| GET | `/workflows/` | List workflows | Bearer Token | Live |
| GET | `/workflows/{id}/` | Workflow details | Bearer Token | Live |
| PATCH | `/workflows/{id}/` | Update workflow | Bearer Token | Live |
| DELETE | `/workflows/{id}/` | Delete workflow | Bearer Token | Live |
| POST | `/workflows/{id}/execute/` | Execute workflow | Bearer Token | Live |
| GET | `/workflows/{id}/executions/` | List executions | Bearer Token | Live |
| POST | `/workflows/{id}/duplicate/` | Duplicate workflow | Bearer Token | Live |
| POST | `/workflows/{id}/actions/` | Add workflow action | Bearer Token | Live |
| DELETE | `/workflows/{id}/actions/{action_id}/` | Remove workflow action | Bearer Token | Live |
| POST | `/actions/` | Create action | Bearer Token | Live |
| GET | `/actions/` | List actions | Bearer Token | Live |
| GET | `/actions/{id}/` | Action details | Bearer Token | Live |
| PATCH | `/actions/{id}/` | Update action | Bearer Token | Live |
| DELETE | `/actions/{id}/` | Delete action | Bearer Token | Live |
| POST | `/batches/` | Create batch | Bearer Token | Live |
| GET | `/batches/` | List batches | Bearer Token | Live |
| GET | `/batches/{id}/` | Batch details | Bearer Token | Live |
| PATCH | `/batches/{id}/` | Update batch | Bearer Token | Live |
| DELETE | `/batches/{id}/` | Delete batch | Bearer Token | Live |
| POST | `/batches/{id}/photos/` | Add photos to batch | Bearer Token | Live |
| DELETE | `/batches/{id}/photos/{photo_id}/` | Remove photo from batch | Bearer Token | Live |
| POST | `/batches/{id}/workflow/` | Assign workflow to batch | Bearer Token | Live |
| POST | `/batches/{id}/execute/` | Execute batch | Bearer Token | Live |
| GET | `/batches/{id}/status/` | Batch status | Bearer Token | Live |
| POST | `/presets/` | Create preset | Bearer Token | Live |
| GET | `/presets/` | List presets | Bearer Token | Live |
| GET | `/presets/{id}/` | Preset details | Bearer Token | Live |
| PATCH | `/presets/{id}/` | Update preset | Bearer Token | Live |
| DELETE | `/presets/{id}/` | Delete preset | Bearer Token | Live |
| POST | `/presets/{id}/duplicate/` | Duplicate preset | Bearer Token | Live |
| POST | `/imports/` | Create import | Bearer Token | Live |
| GET | `/imports/` | List imports | Bearer Token | Live |
| GET | `/imports/{id}/` | Import details | Bearer Token | Live |
| DELETE | `/imports/{id}/` | Delete import | Bearer Token | Live |
| GET | `/imports/{id}/status/` | Import status | Bearer Token | Live |
| POST | `/exports/` | Create export | Bearer Token | Live |
| GET | `/exports/` | List exports | Bearer Token | Live |
| GET | `/exports/{id}/` | Export details | Bearer Token | Live |
| DELETE | `/exports/{id}/` | Delete export | Bearer Token | Live |
| GET | `/exports/{id}/status/` | Export status | Bearer Token | Live |
| GET | `/analytics/workflows/` | Workflow analytics | Bearer Token | Live |
| GET | `/analytics/actions/` | Action analytics | Bearer Token | Live |
| GET | `/analytics/batches/` | Batch analytics | Bearer Token | Live |

## Integration Endpoints

### Payment Processing

Base URL: `https://api.payments.lightwave-media.site/v1/`

| Method | Endpoint | Description | Authentication | Status |
|--------|----------|-------------|----------------|--------|
| POST | `/payment-methods/` | Create payment method | Bearer Token | Live |
| GET | `/payment-methods/` | List payment methods | Bearer Token | Live |
| DELETE | `/payment-methods/{id}/` | Delete payment method | Bearer Token | Live |
| POST | `/charges/` | Create charge | Bearer Token | Live |
| GET | `/charges/{id}/` | Charge details | Bearer Token | Live |
| POST | `/refunds/` | Create refund | Bearer Token | Live |
| GET | `/refunds/{id}/` | Refund details | Bearer Token | Live |
| POST | `/subscriptions/` | Create subscription | Bearer Token | Live |
| GET | `/subscriptions/` | List subscriptions | Bearer Token | Live |
| GET | `/subscriptions/{id}/` | Subscription details | Bearer Token | Live |
| PATCH | `/subscriptions/{id}/` | Update subscription | Bearer Token | Live |
| DELETE | `/subscriptions/{id}/` | Cancel subscription | Bearer Token | Live |
| POST | `/webhooks/stripe/` | Stripe webhook | Webhook Secret | Live |
| POST | `/webhooks/paypal/` | PayPal webhook | Webhook Secret | Live |

### Email Service

Base URL: `https://api.email.lightwave-media.site/v1/`

| Method | Endpoint | Description | Authentication | Status |
|--------|----------|-------------|----------------|--------|
| POST | `/send/` | Send email | Bearer Token | Live |
| POST | `/send-template/` | Send template email | Bearer Token | Live |
| POST | `/templates/` | Create template | Bearer Token | Live |
| GET | `/templates/` | List templates | Bearer Token | Live |
| GET | `/templates/{id}/` | Template details | Bearer Token | Live |
| PATCH | `/templates/{id}/` | Update template | Bearer Token | Live |
| DELETE | `/templates/{id}/` | Delete template | Bearer Token | Live |
| GET | `/deliveries/` | Email delivery stats | Bearer Token | Live |
| GET | `/analytics/` | Email analytics | Bearer Token | Live |
| POST | `/webhooks/sendgrid/` | SendGrid webhook | Webhook Secret | Live |

### Storage Service

Base URL: `https://api.storage.lightwave-media.site/v1/`

| Method | Endpoint | Description | Authentication | Status |
|--------|----------|-------------|----------------|--------|
| POST | `/files/upload/` | Upload file | Bearer Token | Live |
| GET | `/files/` | List files | Bearer Token | Live |
| GET | `/files/{id}/` | File details | Bearer Token | Live |
| DELETE | `/files/{id}/` | Delete file | Bearer Token | Live |
| POST | `/files/{id}/copy/` | Copy file | Bearer Token | Live |
| POST | `/files/{id}/move/` | Move file | Bearer Token | Live |
| GET | `/files/{id}/download/` | Download file | Bearer Token | Live |
| POST | `/folders/` | Create folder | Bearer Token | Live |
| GET | `/folders/` | List folders | Bearer Token | Live |
| GET | `/folders/{id}/` | Folder details | Bearer Token | Live |
| PATCH | `/folders/{id}/` | Update folder | Bearer Token | Live |
| DELETE | `/folders/{id}/` | Delete folder | Bearer Token | Live |
| GET | `/folders/{id}/contents/` | Folder contents | Bearer Token | Live |
| POST | `/shares/` | Create share | Bearer Token | Live |
| GET | `/shares/` | List shares | Bearer Token | Live |
| GET | `/shares/{id}/` | Share details | Bearer Token | Live |
| PATCH | `/shares/{id}/` | Update share | Bearer Token | Live |
| DELETE | `/shares/{id}/` | Delete share | Bearer Token | Live |

## Implementation Guidelines

### API Endpoint Conventions

When implementing new API endpoints:

1. **Naming Conventions**
   * Use plural nouns for resource collections (`/users/` not `/user/`)
   * Use lowercase, hyphenated names for multi-word resources (`/payment-methods/`)
   * Prefer nested resources for relations (`/clients/{id}/projects/`)
   * Use verb-based endpoints sparingly and only for actions (`/workflows/{id}/execute/`)

2. **HTTP Methods**
   * `GET`: Retrieve resources, never modify data
   * `POST`: Create new resources or execute operations
   * `PATCH`: Partial update of existing resources
   * `PUT`: Complete replacement of resources (use sparingly)
   * `DELETE`: Remove resources

3. **Status Codes**
   * `200 OK`: Successful GET, PATCH, PUT requests
   * `201 Created`: Successful POST requests that create new resources
   * `204 No Content`: Successful DELETE requests
   * `400 Bad Request`: Invalid input, validation errors
   * `401 Unauthorized`: Missing or invalid authentication
   * `403 Forbidden`: Authentication successful but insufficient permissions
   * `404 Not Found`: Resource doesn't exis
   * `409 Conflict`: Request conflicts with current state
   * `422 Unprocessable Entity`: Validation error details
   * `429 Too Many Requests`: Rate limit exceeded
   * `500 Internal Server Error`: Server-side error
   * `503 Service Unavailable`: Service temporarily unavailable

### Authentication Requirements

1. **Public Endpoints**
   * Health checks (`/health/`)
   * Public information (countries, languages, etc.)
   * Documentation endpoints (`/docs/`)
   * Authentication endpoints (`/login/`, `/register/`)

2. **User Authentication**
   * Bearer Token required for all user-specific operations
   * Token obtained via successful login or refresh
   * Token expires after 1 hour by defaul
   * Refresh tokens valid for 30 days

3. **Service Authentication**
   * Service-to-service communication uses service tokens
   * Tokens generated from service credentials
   * Higher rate limits than user tokens
   * Configurable expiry based on security requirements

4. **Webhook Authentication**
   * Webhook endpoints secured with webhook secrets
   * Signature validation required for all webhook requests
   * X-Webhook-Signature header contains HMAC signature

### API Versioning Strategy

1. **URL-based Versioning**
   * Major versions in URL (`/v1/`, `/v2/`)
   * Appropriate for significant, breaking changes
   * Allows multiple versions to coexis

2. **Compatibility Guidelines**
   * New fields can be added without version change
   * Field removal requires new version
   * Endpoints can't be removed without new version
   * Response format changes require new version

3. **Deprecation Process**
   * Endpoints marked as deprecated with `Deprecation` header
   * Minimum 6-month deprecation period
   * Clear migration path documented in response
   * Metrics tracked for deprecated endpoint usage

### Rate Limiting

1. **Default Limits**
   * Authenticated requests: 1000 requests per hour
   * Unauthenticated requests: 60 requests per hour
   * Batch operations: 10 requests per minute

2. **Rate Limit Headers**
   * `X-RateLimit-Limit`: Total requests allowed
   * `X-RateLimit-Remaining`: Requests remaining
   * `X-RateLimit-Reset`: Time when limit resets (UTC timestamp)

3. **Custom Limits**
   * API Gateway configurable per service
   * Enterprise accounts have higher limits
   * Sensitive operations may have lower limits

## Related Documentation

* [API Design Principles](../lightwave-api-gateway/api-design-principles.md)
* [Authentication Guide](../lightwave-shared-core/authentication.md)
* [Error Handling Guide](../lightwave-api-gateway/error-handling.md)
* [Rate Limiting Strategy](../lightwave-api-gateway/rate-limiting.md)
* [API Versioning Guide](../lightwave-api-gateway/versioning.md)