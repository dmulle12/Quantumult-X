# App Rewrites and MitM

## Default State

`Quantumult-X.conf` lists three optional upstream resources, all set to `enabled=false`:

- Bilibili: Filters some ad endpoints and home-feed items, and modifies some profile and navigation responses.
- Weibo: Filters some ad responses and promoted items in the feed.
- FQ Reader: Blocks several advertising and analytics domains listed in the upstream rules.

Rules may change upstream. This document describes only the behavior reviewed at the time of writing and does not guarantee that future versions will behave the same way. Before enabling a resource, review the corresponding [upstream rule files](https://github.com/dmulle12/rules/tree/main/source) and build output.

## Before Enabling

1. Rewrites modify requests or responses for specific apps and may cause pages, search, sign-in, playback, or other features to malfunction. Disable the resource to roll back the changes.
2. Rewriting HTTPS content usually requires a Quantumult X MitM certificate. After installing and trusting the root certificate, the device can decrypt and inspect the relevant HTTPS traffic locally. Enable this only on devices you control and understand the implications.
3. Do not commit `[mitm]` `p12` or `passphrase` values, private keys, or personal certificates to the repository. The template contains none of these and does not configure MitM hostnames by default.
4. Enable only rules for apps you use and whose traffic you are willing to modify. Keep unused app rules disabled or remove their entries.

## Enablement Steps

1. Open `[rewrite_remote]` in `Quantumult-X.conf` and change `enabled=false` to `enabled=true` only for the resources you need.
2. Update the resources in Quantumult X. Review the `hostname` and rules in each resource's details to confirm their scope.
3. If the app indicates that MitM is required, first read the official Quantumult X documentation. Then enable MitM in the app, generate and install the certificate, and explicitly trust it in system settings. This template does not install certificates automatically.
4. Verify that the target app still works. If something goes wrong, disable the resource you just enabled and reconnect the tunnel.

## Local Syntax Example

[`../snippets/rewrite-examples.snippet`](../snippets/rewrite-examples.snippet) contains commented examples using only the reserved `example.invalid` domain; they do not intercept real app traffic.
