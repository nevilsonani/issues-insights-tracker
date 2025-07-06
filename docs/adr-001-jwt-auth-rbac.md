# ADR-001: Use JWT-based OAuth2 for Authentication and Role-Based Access Control

**Status:** Accepted  
**Date:** 2024-06-09

## Context

The mini-saas-tracker application requires secure authentication and fine-grained role-based access control (RBAC) for three user roles: ADMIN, MAINTAINER, and REPORTER. The system must support both frontend (SvelteKit) and backend (FastAPI) components, and should be suitable for both web and API clients.

## Decision

We decided to use **JWT-based OAuth2 authentication** with FastAPI's OAuth2PasswordBearer flow. Each user receives a signed JWT token upon login, which is then sent in the `Authorization: Bearer <token>` header for all API requests. The backend decodes the JWT to identify the user and their role, and enforces RBAC in API endpoints using dependency injection.

- **RBAC** is enforced in the backend by checking the user's role in route dependencies.
- The **frontend** stores the JWT in localStorage and includes it in all API requests.
- The system does **not** use session cookies or OAuth2 PKCE, as the primary clients are SPAs and API consumers.

## Consequences

- **Pros:**
  - Stateless authentication: no server-side session storage required.
  - Easy integration with frontend frameworks and API clients.
  - Fine-grained RBAC is simple to enforce in FastAPI using dependencies.
  - JWTs can be extended to include more claims if needed.

- **Cons:**
  - JWTs must be securely stored in the frontend (localStorage is vulnerable to XSS).
  - No built-in support for token revocation or session expiration beyond token expiry.
  - PKCE or session cookies would be more secure for some use cases (e.g., public clients).

## Alternatives Considered

- **Session cookies:** More secure for traditional web apps, but less suitable for APIs and SPAs.
- **OAuth2 with PKCE:** More secure for public clients, but adds complexity and was not required for this use case.

## Related Decisions

- RBAC is also enforced in the frontend by conditionally rendering UI elements based on the user's role.
- All API endpoints requiring authentication use the same JWT-based dependency.

---

**Summary:**  
JWT-based OAuth2 was chosen for its simplicity, statelessness, and ease of integration with both frontend and backend, while providing robust RBAC enforcement. 