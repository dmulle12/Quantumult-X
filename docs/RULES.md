# Rule Set Guide

## Currently Enabled Remote Resources

| Resource | Default Policy | Purpose |
|---|---|---|
| `reject.quanx` | `reject` | Blocks ads and tracking. Large rule sets may affect functionality on some sites. |
| `gfw-skip.quanx` | `direct` | Direct-routing exceptions to proxy rules. |
| `loc-cn.quanx` | `direct` | Direct routing for mainland China domains. |
| `gfw.quanx` | `proxy` | Proxy-domain rules converted from GFWList. |

Resource URLs come from [`dmulle12/rules`](https://github.com/dmulle12/rules), whose `rel` branch is updated automatically. The main profile in this repository lists resources from top to bottom. If rules conflict, check the match logs in Quantumult X and, if necessary, adjust the order or disable an individual resource.

## Local Rules

In `[filter_local]`, `geoip, lan, direct` and `geoip, cn, direct` route LAN and mainland China IP addresses directly; `final, proxy` is the fallback. If the policy names do not match your Quantumult X version or node setup, first verify the built-in policy names and imported nodes before making changes. Do not add unknown group names.

If you do not need direct routing for mainland China, remove `geoip, cn, direct` and disable `loc-cn.quanx`. To assign a policy to a specific service, add a precise `host-suffix` or `host` rule to `[filter_local]` before `final`. For example:

```ini
; host-suffix, example.com, direct
```

`example.com` is a placeholder domain; replace it with a domain you have verified. Avoid overly broad keywords or wildcard rules.

## Upstream Scope and Limitations

The upstream `reject` list aggregates ad and tracking rules. Its maintainers state that it cannot remove native in-feed ads served from the same domain as the content; do not block an entire content service domain just because one ad remains. The upstream project also notes that `loc-cn` is a rule classification and does not guarantee that every listed domain is served from mainland China. See the upstream README for sources, build details, and licenses.
