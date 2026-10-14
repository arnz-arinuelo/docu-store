# Security backlog

Follow-ups from the 2026-10-13 security-ops pass. Each is its own change.

- **Frontend CSP.** `web/apps/portal/next.config.ts` sets only `frame-ancestors 'none'`. A full policy needs nonces for Next's inline scripts.
- **Frontend security lint.** `web/` has no ESLint (`pnpm lint` is `tsc --noEmit`). Adding a linter with security rules is a toolchain decision.
- **Lint the backend tests.** `make lint` and CI cover `application/ domain/ infrastructure/ interfaces/` only. Extend both to `services/tests/` with a per-file `S101` ignore once the other findings there are cleaned.
