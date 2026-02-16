# 🔐 Security Policy

> SASDS — Security Considerations & Vulnerability Reporting

---

## Security Model

SASDS is designed for **local development and trusted environments**. The current architecture prioritizes developer productivity over hardened production security. When deploying to shared or public environments, additional security measures should be applied.

---

## Current Security Measures

### API Key Management

| Practice | Status |
|---|---|
| API keys stored in `.env` files | ✅ Implemented |
| `.env` excluded from version control via `.gitignore` | ✅ Implemented |
| Keys injected via environment variables in Docker | ✅ Implemented |
| Key rotation support | 🔜 Planned |

### Input Validation

| Practice | Status |
|---|---|
| Pydantic models for all API request/response schemas | ✅ Implemented |
| File path traversal protection (`secure_path()`) | ✅ Implemented |
| Empty input rejection | ✅ Implemented |

### Error Handling

| Practice | Status |
|---|---|
| Global exception handler (no stack trace leakage) | ✅ Implemented |
| Structured JSON error responses | ✅ Implemented |
| Request/response logging | ✅ Implemented |

### Infrastructure

| Practice | Status |
|---|---|
| CORS middleware (configurable origins) | ✅ Implemented |
| Docker containerization (process isolation) | ✅ Implemented |
| Generated projects isolated to `generated_projects/` | ✅ Implemented |

---

## Known Considerations

> [!IMPORTANT]
> The following items should be addressed before deploying SASDS in a production or multi-user environment.

### 1. CORS Configuration

**Current:** Open CORS (`allow_origins=["*"]`)
**Recommendation:** Restrict to specific frontend domain(s).

### 2. Authentication

**Current:** No authentication on API endpoints.
**Recommendation:** Add JWT-based authentication or API key validation.

### 3. Rate Limiting

**Current:** No rate limiting on AI-powered endpoints.
**Recommendation:** Add rate limiting (e.g., `slowapi`) to prevent API abuse.

### 4. File System Access

**Current:** Basic path traversal protection.
**Recommendation:** Implement proper sandboxing (e.g., chroot, containerized file I/O).

### 5. Terminal Access

**Current:** WebSocket terminal provides full shell access.
**Recommendation:** In multi-user environments, restrict shell access per user/session.

### 6. Data at Rest

**Current:** Generated code stored on local file system without encryption.
**Recommendation:** Encrypt sensitive data and implement access controls.

---

## Reporting Vulnerabilities

If you discover a security vulnerability, please report it responsibly:

1. **Do NOT** open a public GitHub issue
2. **Email** your findings to the project maintainer
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact assessment
   - Suggested fix (if any)
4. We will acknowledge receipt within **48 hours**
5. We will provide a fix timeline within **7 days**

---

## Security Roadmap

| Feature | Priority | Status |
|---|---|---|
| JWT Authentication | High | 🔜 Planned |
| API Rate Limiting | High | 🔜 Planned |
| CORS Lock-down (production config) | Medium | 🔜 Planned |
| Audit Logging | Medium | 🔜 Planned |
| File System Sandboxing | Medium | 🔜 Planned |
| Secret Rotation | Low | 🔜 Planned |
| RBAC (Role-Based Access Control) | Low | 🔜 Planned |
