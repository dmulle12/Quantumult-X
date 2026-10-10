# First-Party Remote Rule Sets

## What is active

The importable profile references three rule sources from this public repository in `[filter_remote]`. They are authored and maintained here; no third-party filter feed is loaded.

| Source | Forced policy | Scope |
|---|---|---|
| [`back-cn-media.list`](../rulesets/back-cn-media.list) | `BackCN` | A small set of official video, livestream, and music web endpoints; not all China domains or complete app/CDN allowlists. |
| [`proxy-services.list`](../rulesets/proxy-services.list) | `proxy` | Selected developer, AI, and global content-service domains. |
| [`direct-cn.list`](../rulesets/direct-cn.list) | `direct` | Existing selected mainland China service domains, followed by the China GeoIP fallback. |

Quantumult X's `force-policy` parameter makes each remote resource use its configured policy. The `[policy]` section defines `static = BackCN, direct, proxy`, with `direct` as its safe initial choice. The optional [`privacy-reject.optional.list`](../rulesets/privacy-reject.optional.list) is not loaded and has no effect unless you deliberately configure it.

## BackCN domain evidence and scope

The active BackCN rules are deliberately limited to first-party official service website hosts verified on the service pages below:

| Rule suffix | Service evidence |
|---|---|
| `www.bilibili.com` | [Bilibili official video site](https://www.bilibili.com/) |
| `live.bilibili.com` | [Bilibili official live site](https://live.bilibili.com/) |
| `live.douyin.com` | [Douyin official live site](https://live.douyin.com/) |
| `v.qq.com` | [Tencent Video official site](https://v.qq.com/) |
| `music.163.com` | [NetEase Cloud Music official site](https://music.163.com/) |
| `y.qq.com` | [QQ Music official site](https://y.qq.com/) |

The entries match only each named host and its subdomains. They do not match the registrable parent domain unless that parent is itself listed. Some app playback, API, or CDN traffic may use other domains; those are intentionally not guessed or included. Add further endpoints only when supported by reliable service-domain evidence and, ideally, confirmed in Quantumult X's activity log.

## Match order and priority

The active profile is arranged as follows:

1. `[filter_local]`: `geoip, lan, direct` for local-network traffic.
2. First `[filter_remote]` resource: the specific official media web endpoints above use `BackCN`.
3. Next remote resource: selected generic proxy-service suffixes use `proxy`.
4. Last remote resource: existing explicit China service suffixes use `direct`, then its final `geoip, cn, direct` rule handles remaining connections whose resolved IP is in China.
5. `final, proxy` handles traffic that matched none of the above.

Keep BackCN before the direct-China resource: the latter intentionally contains broad service suffixes such as `bilibili.com`, `douyin.com`, and `qq.com`. Thus `live.douyin.com`, `v.qq.com`, or `y.qq.com` can use the more specific BackCN route first, while other matching China-service subdomains remain on the existing direct policy. The GeoIP rule stays at the very end of the remote resources, rather than in `[filter_local]`, so it cannot shadow explicit host rules. The profile's generic proxy and direct rules otherwise remain separate from BackCN.

Financial, government, and work services are not added to the BackCN list. They continue to use existing explicit rules where present; connections to China-resolved IPs otherwise reach the GeoIP-direct fallback. Existing work or global services explicitly covered by `proxy-services.list` remain on the generic `proxy` policy. This is not a promise that every service is fully covered: review actual match logs for your apps and decide whether a separate explicit rule is needed.

A `host-suffix` entry matches the listed domain and its subdomains, not merely strings that happen to end with the same characters; for example, `github.com.attacker.invalid` is not a match for `github.com`.

## Configuring an actual mainland route

No subscription URL or user-specific mainland node was supplied, so this repository does not invent one. `BackCN` is a usable selector with built-in `direct` and `proxy` candidates, but it defaults to `direct` for safety. To actually return selected media traffic through mainland China, add the exact tag(s) of your own mainland-capable node(s) to the `BackCN` candidate list in `[policy]`, then select one in Quantumult X. The generic `proxy` policy is not guaranteed to exit in mainland China; the repository cannot verify your provider or node geography.

## Optional privacy blocks

The optional reject list includes ad and analytics domains that may also be used by site features, attribution, or embedded content. Blocking them can cause breakage. It is deliberately excluded from the profile. If you choose to use an entry, review it first and configure it as a separate remote resource or add selected entries to `[filter_local]`; rebuild and run the checks afterward.

## Change and test

1. Add or remove a three-column Quantumult X rule in the relevant `.list` file, following the existing `host-suffix, domain, policy` form. Keep `geoip, cn, direct` as the final active rule in `direct-cn.list`.
2. Keep BackCN-specific rules in the first remote set, selected generic proxy rules second, and direct-China rules with GeoIP fallback last. Avoid broad `host-keyword` matches and speculative domains.
3. Run `python3 tools/build_config.py` to update the generated remote-resource block in `Quantumult-X.conf`.
4. Run `python3 tools/build_config.py --check`, `python3 tools/validate_config.py`, and `python3 tools/test_rules.py`.
5. After publication, update remote resources in Quantumult X and confirm effective policies in its match/activity logs; local tests cannot test the provider's node geography or every app dependency.

The remote lists are served from `raw.githubusercontent.com`; Quantumult X needs network access to that host to download or update them. Regression cases in [`../tests/rule-cases.tsv`](../tests/rule-cases.tsv) cover BackCN-versus-direct precedence, suffix boundaries, the GeoIP-direct fallback for simulated China IPs, and the final proxy fallback. Do not add a provider subscription, private credentials, or MITM certificate material to this repository.

For resource syntax and parameters, see the official [Quantumult X sample configuration](https://github.com/crossutility/Quantumult-X/blob/master/sample.conf).
