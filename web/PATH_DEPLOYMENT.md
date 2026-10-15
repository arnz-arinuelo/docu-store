# Root and subpath deployments

Build the existing Dockerfile with `--build-arg NEXT_PUBLIC_BASE_PATH=/docustore`
for a `/docustore` deployment. Omit the argument for the existing root mode.
The prefix is compiled into the client and server and cannot be changed at
runtime; the Docker healthcheck uses the same build argument.

Keep the prefix when proxying to Next.js. Next Link/router destinations remain
application-relative. Raw browser requests use the build prefix explicitly.

For DEV, configure these non-secret runtime settings:

- `APP_URL=https://daikon-dev.gatesfoundation.org/docustore`
- `APP_API_URL=https://daikon-dev.gatesfoundation.org/docustore-api`
- `APP_DUAR_URL=https://daikon-dev.gatesfoundation.org/duar`
- `APP_ENTRA_ID_CLIENT_ID` and `APP_ENTRA_ID_TENANT_ID`: existing DEV identifiers.
- `APP_SELF_SERVE_ENABLED=false`

The Entra callback uses the current browser origin plus the build prefix:
`https://daikon-dev.gatesfoundation.org/docustore/auth/callback`. Register that
exact SPA redirect on the existing DEV application. The pinned DUAR SDK uses
its existing implicit ID-token flow and nonce checks; this is not a new PKCE
login implementation. Deployment requires identity-owner policy approval.

DUAR's existing `docu-store` ServiceApp must allow the origin
`https://daikon-dev.gatesfoundation.org` without a path, validate the existing
Entra audience, and authorize the tester's existing workspace membership.
Outer oauth2-proxy authentication does not replace DUAR authorization.

Workspace discovery runs from the browser against `APP_DUAR_URL`; for DEV the
tester's workspace is `TBDA-DEV`. Credential minting is server-side only: the
browser posts to `<prefix>/api/auth/mint`, which calls DUAR `/authz/resolve`
with the service key. If the pod cannot reach the public DUAR URL, set the
optional server-only `APP_DUAR_INTERNAL_URL` (for example the in-cluster DUAR
service); it is never returned by `/api/config`.

Health probes use `<prefix>/api/health` (`/docustore/api/health` in DEV).

Supply `APP_DUAR_SERVICE_KEY` only to the server through the dedicated existing
Secret. Never supply it as a build argument or browser configuration. Production
config-fetch failures are explicit errors, rather than fallback to localhost.
