# Quantumult-X

A reviewable, customizable general-purpose Quantumult X configuration repository containing a main profile, remote routing rules, optional app rewrite guidance, and a basic validation script.

> **Security defaults:** This repository is intended to be private. It contains no server subscriptions, account credentials, MITM private keys, or certificates. App rewrite resources are disabled by default. Rule data is provided by a public, user-maintained rules repository.

## Files

- [`Quantumult-X.conf`](./Quantumult-X.conf): An importable base configuration.
- [`docs/RULES.md`](./docs/RULES.md): Rule sources, matching order, and customization guidance.
- [`docs/REWRITES.md`](./docs/REWRITES.md): App rewrite scope, MITM considerations, and enablement steps.
- [`snippets/rewrite-examples.snippet`](./snippets/rewrite-examples.snippet): Rewrite syntax examples using only reserved domains; they do not affect real websites.
- [`tools/validate_config.py`](./tools/validate_config.py): Checks the configuration structure, URLs, and disabled-by-default settings.

## Quick Start

1. Back up your current configuration in Quantumult X. Download `Quantumult-X.conf` from this repository and import it as a file.
2. Add a Quantumult X subscription URL provided by a provider **you trust** to `[server_remote]`. This repository does not select a provider or include fabricated nodes.
3. Check that your provider's node tags match the policy names in `[filter_local]`. The template uses the built-in `proxy`, `direct`, and `reject` policies.
4. Update the remote resources and inspect the resource and activity logs in Quantumult X. If your network cannot access GitHub, you can replace the URLs with a mirror that you trust and can reach.
5. Keep app rewrites disabled. Enable a resource only when you specifically need its app rules and have reviewed the upstream content. HTTPS rewrites also require enabling MitM in the app according to its official procedure and installing and trusting the Quantumult X certificate.

## Default Behavior

- Ad and tracking domains: `reject`.
- GFW whitelist exceptions and `loc-cn`: `direct`.
- GFW rules: `proxy`.
- LAN and mainland China IP addresses: `direct`.
- All other traffic: `proxy`.

This is a general starting point for users who need direct routing and proxy routing for mainland China. It is not guaranteed to suit every region, carrier, app, or regulatory environment. If you do not need mainland-China routing, remove `loc-cn` from `[filter_remote]` and `geoip, cn, direct` from `[filter_local]`. Remote lists may block traffic incorrectly; when troubleshooting, first disable the relevant resource temporarily and inspect the match logs.

## Upstream Sources and Licenses

Remote rules and rewrites are published by [`dmulle12/rules`](https://github.com/dmulle12/rules). The advertising rules in that project are converted from Hagezi DNS Blocklists; see the upstream documentation for specific sources, licenses, and update policies. This repository references remote resources without copying their rule data. Quantumult X syntax is based on the [official sample configuration](https://github.com/crossutility/Quantumult-X/blob/master/sample.conf) and the [official Rewrite examples](https://github.com/crossutility/Quantumult-X/blob/master/rewrite.md).

## Validation

```bash
python3 tools/validate_config.py
```

Passing validation means only that the configuration structure and expected security defaults meet this repository's checks. Verify importability and rule matching in Quantumult X.
