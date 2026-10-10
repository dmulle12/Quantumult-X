# App Rewrites and MitM

## Default state

`Quantumult-X.conf` has an empty `[rewrite_remote]` section and no active `[rewrite_local]` entries. This repository does not fetch third-party app rewrite feeds or claim to include working rewrites for specific live apps.

[`../snippets/rewrite-examples.snippet`](../snippets/rewrite-examples.snippet) contains commented syntax examples that use only the reserved `example.invalid` domain. They are inert examples; they do not intercept or modify real app traffic.

## Before writing or enabling a rewrite

1. A rewrite can change a request or response and may break sign-in, search, playback, payments, or other app behavior. Work only with an endpoint and app you control or are authorized to test.
2. HTTPS response rewrites typically require a Quantumult X MitM certificate. A trusted root certificate can allow the device to decrypt and inspect matching HTTPS traffic locally. Enable this only on devices you control and only for hostnames you deliberately selected.
3. Never commit `[mitm]` `p12` or `passphrase` values, private keys, or personal certificates.
4. Start with a narrow hostname and URL pattern; verify the request and response shape against the current app version. Disable the rewrite immediately if unrelated traffic is affected.

## Safe example workflow

The supplied snippet uses a reserved hostname and is not meant to work against a real service. To build a real rewrite, replace the placeholder only with a test endpoint you own, validate the syntax against the official [Quantumult X rewrite documentation](https://github.com/crossutility/Quantumult-X/blob/master/rewrite.md), and review the MITM scope in Quantumult X before importing or enabling it.
