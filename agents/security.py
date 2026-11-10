# Security Agent

Static code review of all new and modified code, dependency scanning from
pip/npm manifests, configuration file checks, and command execution audit.
Identifies CVEs, unsafe patterns, secret leaks, and permission issues.

Flags: CVE match, hardcoded secrets, dangerous system calls, unauthorized
access patterns, dependency vulnerabilities, privilege escalation risk.
Output is advisory only — does not block development, reports findings upward.
