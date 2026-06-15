# SiteLens

> Lightweight, non-intrusive security scanner for small websites — built for people, not just security experts.

## What is this?

SiteLens scans a website for common, publicly-visible security issues —
expired SSL certificates, missing security headers, exposed sensitive files,
and weak email/DNS configuration — and explains findings in plain language
with actionable recommendations.

**This is a passive scanner.** It only checks publicly available information
(HTTP headers, DNS records, SSL certificates, accidentally-exposed files).
It does NOT perform attacks, exploits, or unauthorized access attempts.

## Who is this for?

- Small business owners who want to know if their website has basic issues
- Freelance developers doing a quick check before client handover
- Students learning security concepts hands-on
- Open source maintainers checking their project sites

## Installation

\`\`\`bash
pip install sitelens
\`\`\`

## Usage

\`\`\`bash
sitelens scan example.com
\`\`\`

## Status

🚧 Early development (v0.1.0) — core checks working, contributions welcome!

See [ROADMAP.md](Docs/ROADMAP.md) for what's coming next.

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) to get started.

## License

MIT — see [LICENSE](LICENSE)
