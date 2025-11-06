# cmmc-ssp-autogen-saas
AI-powered SaaS that ingests PDF/DOCX, auto-maps content to CMMC Level 2 controls, and generates audit-ready System Security Plans. Secure multitenant architecture with role-based access, dashboards, and automated compliance scoring. Built for Defense Industrial Base readiness.
mvp-cmmc-ssp/
├─ README.md
├─ backend/
│  ├─ app/
│  │  ├─ main.py
│  │  ├─ auth.py
│  │  ├─ models.py
│  │  ├─ storage.py
│  │  ├─ processor.py
│  │  ├─ mapping.py
│  │  ├─ ssp_generator.py
│  │  └─ deps.py
│  ├─ Dockerfile
│  └─ requirements.txt
├─ frontend/
│  ├─ package.json
│  └─ src/
│     ├─ App.jsx
│     ├─ components/Upload.jsx
│     ├─ components/Dashboard.jsx
│     └─ services/ws.js
├─ infra/
│  ├─ docker-compose.yml
│  ├─ terraform/
│  │  ├─ main.tf
│  │  └─ providers.tf
│  └─ zap_scan.sh
├─ docs/
│  ├─ cmmc_controls.json
│  └─ mapping_template.md
├─ tests/
│  ├─ test_processor.py
│  └─ test_auth.py
└─ scripts/
   └─ local_start.sh
# MVP: CMMC Level 2 SSP Generator (Production-minded demo)

Purpose: Demo-ready SaaS MVP for parsing DOCX/PDF, mapping extracted content to NIST/SP800-171 (CMMC L2) controls, and producing audit-ready SSP/PDF outputs. Includes a React front-end with real-time dashboards.

Important references:
- NIST SP 800-171 Rev.2 (control set used). See NIST. :contentReference[oaicite:3]{index=3}
- CMMC Level 2 aligns to the 110 controls in NIST SP 800-171. :contentReference[oaicite:4]{index=4}

Run locally (dev):
1. copy `.env.template` → `.env` and supply secrets (AWS S3, JWT secret, LLM api key).
2. `./scripts/local_start.sh`
3. Frontend: http://localhost:3000 ; Backend: http://localhost:8000

Acceptance test:
- Upload sample DOCX/PDF → check `/_status` WebSocket progress → download generated `SSP.docx` and `SSP.pdf`.

Security/hardening checklist (must be completed before production):
- HSM-backed key management (AWS KMS with GovCloud keys or dedicated HSM)
- Replace simple JWT with short-lived access tokens + refresh & session revocation
- Pen test & full OWASP ZAP scan (script provided). Ensure no critical findings.
- Host in GovCloud with strictly controlled IAM roles and VPC endpoints.

CI / ZAP scan script (infra/zap_scan.sh)
#!/usr/bin/env bash
# simple OWASP ZAP baseline scan for local deployment
docker run -t owasp/zap2docker-stable zap-baseline.py -t http://host.docker.internal:8000 -r zap_report.html
# parse report, fail if critical findings exist — implement policy in CI

Implementation notes & production hardening (you must do these)

Tenant isolation: current JWT contains tenant_id. Enforce DB row-level tenant scoping for every query. Consider separate S3 prefixes + encryption keys per tenant, and use IAM policies limiting access to those prefixes.

KMS / HSM: Replace JWT_SECRET with KMS-signed tokens and use AWS KMS for all encryption keys. Audit key usage.

LLM & embeddings: Current mapping uses local sentence-transformers. For higher accuracy and scale, swap embedding calls to an enterprise LLM or hosted vector DB (Pinecone / Milvus) and optionally fine-tune the model on SSP/POA&M examples. Keep the raw documents encrypted at rest; do LLM requests via VPC endpoints if using cloud LLM.

Evidence chain & explainability: Save chunk offsets and original text excerpts as evidence. Store hashes of original docs in manifest (for non-repudiation).

SSP formatting: The generator creates a clean DOCX; for auditor-ready PDF, convert via WeasyPrint or a signed PDF pipeline and apply watermarking and audit page.

Audit logging & monitoring: All processing steps must write immutable audit events to an append-only store (CloudWatch Logs with KMS, or Splunk). Ensure retention & rotation policies meet DFARS contract requirements.

Pen test & SAST/DAST: Run OWASP ZAP and fix criticals; performer full code review for sensitive endpoints. Acceptance criteria includes zero critical ZAP findings.

CI/CD: Terraform plan/apply in GovCloud using locked-down service principals, remote state in secure S3 with DynamoDB locking. Consider ephemeral build agents inside GovCloud for end-to-end compliance. 
Amazon Web Services, Inc.
+1

Where the repo intentionally leaves choices for you (and why)

LLM provider: For DoD workflow you might prefer an on-prem or FedRAMP-authorized LLM endpoint. I kept model calls local (sentence-transformers) for reproducible demo without exposing secrets. Swap to OpenAI/Anthropic with private endpoints or an on-prem model for FedRAMP compliance.

Vector DB: FAISS works for MVP. For multi-tenant scale use Pinecone, Milvus, or an RDS-backed vector store inside GovCloud.

Fine-tuning: If you want high accuracy (>95% control coverage as acceptance), you’ll almost certainly need supervised fine-tuning using labeled SSPs and evidence. The code contains CMMCMapper hook points for plugging in a fine-tuned model.

Final checklist to finish before you label this “production-ready” (do not skip)

Populate docs/cmmc_controls.json with all 110 controls (use the NIST doc). 
NIST Publications

Implement persistent manifest DB (Postgres with RLS for tenant isolation).

Integrate KMS + rotate keys.

Replace dev JWT flow with short-lived tokens + refresh + device binding.

Configure VPC-only access for LLM provider and S3 with VPC endpoints.

Audit CI/CD and Terraform flow for GovCloud: require manual approvals for production apply. 
Amazon Web Services, Inc.
+1

Delivery & provenance

This message contains a complete, copy-paste scaffold and core working modules. To get you started immediately:

Create repo and paste the files above (or I can produce each file in full if you want one giant paste).

Populate .env with S3 creds and JWT secret for local dev.

Run ./scripts/local_start.sh (script spins up uvicorn and vite).

Test upload → watch WebSocket progress → download SSP.docx.
