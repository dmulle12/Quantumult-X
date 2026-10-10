# Quantumult-X

一套可审阅、可调整的 Quantumult X 通用配置仓库：主配置、远程分流规则、可选应用重写说明，以及基础校验脚本。

> **安全默认值：** 仓库设计为私有；不包含节点订阅、账号凭据、MITM 私钥或证书。应用重写资源默认关闭。规则数据由一个公开的用户规则仓库提供。

## 文件

- [`Quantumult-X.conf`](./Quantumult-X.conf)：可导入的基础配置。
- [`docs/RULES.md`](./docs/RULES.md)：规则来源、匹配顺序与调整方法。
- [`docs/REWRITES.md`](./docs/REWRITES.md)：应用级重写范围、MITM 提示和启用步骤。
- [`snippets/rewrite-examples.snippet`](./snippets/rewrite-examples.snippet)：仅使用保留域名的重写语法示例，不会影响真实网站。
- [`tools/validate_config.py`](./tools/validate_config.py)：检查配置结构、URL 与默认关闭状态。

## 快速开始

1. 在 Quantumult X 中备份当前配置；从本仓库下载 `Quantumult-X.conf`，通过文件导入。
2. 在 `[server_remote]` 中填入你**自己信任的服务商**提供的 Quantumult X 订阅 URL；本仓库没有替你选择服务商，也没有伪造节点。
3. 检查服务商节点标签与 `[filter_local]` 的策略名称是否匹配。模板使用内置 `proxy`、`direct`、`reject` 策略。
4. 更新远程资源，检查 Quantumult X 的资源/活动日志。若网络环境无法访问 GitHub，可替换为你信任且可达的镜像源。
5. 应用重写保持关闭。只有明确需要某应用规则并审阅上游内容后，才启用对应行；HTTPS 重写还需要在应用中按官方流程启用 MitM 并安装/信任 Quantumult X 证书。

## 当前默认行为

- 广告与跟踪域名：`reject`。
- GFW 白名单例外、`loc-cn`：`direct`。
- GFW 规则：`proxy`。
- 局域网与中国大陆 IP：`direct`。
- 其余流量：`proxy`。

这是适合需要中国大陆直连与代理的通用起点，不保证适合所有地区、运营商、应用或法规环境。若你不需要中国大陆分流，可从 `[filter_remote]` 移除 `loc-cn`，并从 `[filter_local]` 移除 `geoip, cn, direct`。远程列表可能误拦截；排障时优先临时停用对应资源并检查命中记录。

## 上游与许可

远程规则和重写由 [`dmulle12/rules`](https://github.com/dmulle12/rules) 发布；其中广告规则由该项目转换自 Hagezi DNS Blocklists，具体来源、许可和更新策略请查阅上游说明。此仓库只引用远程资源，不复制其规则数据。Quantumult X 语法依据 [官方示例配置](https://github.com/crossutility/Quantumult-X/blob/master/sample.conf) 与 [官方 Rewrite 样例](https://github.com/crossutility/Quantumult-X/blob/master/rewrite.md)。

## 校验

```bash
python3 tools/validate_config.py
```

校验通过只代表配置结构与预期安全默认值符合仓库规则；最终能否导入、规则是否命中，应在 Quantumult X 中检查。
