# Quantumult-X

A reviewable Quantumult X profile with **project-authored, first-party remote routing rules**, a configurable `BackCN` policy group, a deterministic configuration builder, an optional privacy blocklist, and safe rewrite examples. Active routing rules are served from this public repository rather than copied into the profile or fetched from a third-party rules provider.

> **Security defaults:** Back up your current profile before importing. No proxy subscription, credentials, MITM private key, or certificate is included. The profile's `BackCN` selector defaults to `direct`; actual return-to-China proxy routing requires you to add and select your own mainland-capable node tag.

## Repository layout

- [`Quantumult-X.conf`](./Quantumult-X.conf): Importable profile; references the project-owned remote rule sets in `[filter_remote]` and defines the configurable `BackCN` selector.
- [`rulesets/back-cn-media.list`](./rulesets/back-cn-media.list): Narrow official web endpoints for selected video, livestream, and music services.
- [`rulesets/proxy-services.list`](./rulesets/proxy-services.list): Curated proxy routes for selected developer, AI, and global content services.
- [`rulesets/direct-cn.list`](./rulesets/direct-cn.list): Curated direct routes for selected mainland China services, followed by the China GeoIP fallback.
- [`rulesets/privacy-reject.optional.list`](./rulesets/privacy-reject.optional.list): Optional ad/analytics blocks; intentionally not active in the default profile.
- [`docs/RULES.md`](./docs/RULES.md): Rule scope, source evidence, precedence, maintenance, and limitations.
- [`docs/REWRITES.md`](./docs/REWRITES.md): Rewrite/MitM safety notes and the limits of the supplied examples.
- [`snippets/rewrite-examples.snippet`](./snippets/rewrite-examples.snippet): Inactive syntax examples using the reserved `example.invalid` domain only.
- [`tools/build_config.py`](./tools/build_config.py): Validates source lists and generates the profile's remote-resource entries.
- [`tools/validate_config.py`](./tools/validate_config.py) and [`tools/test_rules.py`](./tools/test_rules.py): Structural/safety checks and routing regression tests.

## Quick start

1. Back up your current profile in Quantumult X and import `Quantumult-X.conf`.
2. Make sure Quantumult X can access `raw.githubusercontent.com` so it can download and periodically update the rules. If that host is unavailable on your network, the remote rules may not refresh.
3. Add a subscription from a proxy provider **you trust** in the app. No subscription URL or proxy nodes are supplied here.
4. The profile's `[policy]` section defines `static = BackCN, direct, proxy`. It safely selects `direct` by default. To use return-to-China routing, add your own mainland-capable node's exact policy tag to that candidate list and select it in Quantumult X. The generic `proxy` candidate is not guaranteed to exit in mainland China.
5. The profile uses built-in `proxy`, `direct`, and `reject` policies. Selected media website endpoints use `BackCN`; existing explicit China routes and the China GeoIP fallback remain `direct`; unmatched traffic uses `proxy`.
6. Keep MITM off unless you have reviewed a specific rewrite and understand the certificate's scope.

## Selected network, DNS, and helper resources

The profile keeps the selected return-to-China network settings in `[general]`: the connectivity check uses `http://wifi.vivo.com.cn/generate_204`, while the server check uses `http://cp.cloudflare.com/generate_204`. The location checker is configured with `http://ip-api.com/json/?fields=11024` and the specified `qx-loc.js` resource at `https://github.com/dmulle12/rules/raw/main/js/qx-loc.js`.

`resource_parser_url` points to the selected KOP-XIAO Quantumult X resource parser, served through jsDelivr at `https://cdn.jsdelivr.net/gh/KOP-XIAO/QuantumultX@master/Scripts/resource-parser.js`. The `qx-extract.js` parser line in the profile is commented out and is not active.

The `[dns]` section explicitly configures `no-system`, `no-ipv6`, Google DNS at `8.8.8.8` and `8.8.4.4`, plus `https://dns.google/dns-query`. `prefer-doh3` remains commented out. These are the profile's selected DNS and helper-resource settings; the documentation does not substitute different resolvers or parser/location services.

## Editing and verifying rules

Edit one of the source lists under `rulesets/`, then run:

```bash
python3 tools/build_config.py
python3 tools/build_config.py --check
python3 tools/validate_config.py
python3 tools/test_rules.py
```

The builder generates the `[filter_remote]` resource block; do not edit it by hand. Resources are loaded in this order: selected `BackCN` media endpoints, selected generic proxy services, then selected direct-China rules with `geoip, cn, direct` last. The local filter section retains only the LAN override and `final, proxy` fallback so it does not shadow those remote host rules.

## Scope and limitations

This is an intentionally small, human-reviewable editorial set—not a complete geographic firewall list, GFWList replacement, universal ad blocker, or exhaustive catalog of each service's API/CDN domains. The BackCN rules cover only the official web hostnames listed in [`docs/RULES.md`](./docs/RULES.md); some app media may use other CDN/API hosts and remain on the existing direct or GeoIP route. Add more only after checking reliable service-domain evidence and observed Quantumult X match logs.

The BackCN list is selective, **not a route for all China domains**. It does not add financial, government, or work services to BackCN. Existing direct service rules and `geoip, cn, direct` remain in effect; existing explicit proxy-service rules remain separate. The GeoIP fallback is based on the resolved IP, not the domain's perceived country, and a local test cannot establish a live service's complete dependency set.

No mainland nodes or user-specific subscription URLs were supplied. Until you add a mainland-capable candidate to `BackCN`, it remains safely set to `direct`; selecting the generic `proxy` candidate alone does not guarantee return-to-China routing.

The supported filter-resource syntax follows the official [Quantumult X sample configuration](https://github.com/crossutility/Quantumult-X/blob/master/sample.conf). The active lists are maintained in this repository and are not synchronized with third-party rules projects.
