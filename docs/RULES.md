# 规则集说明

## 当前启用的远程资源

| 资源 | 默认策略 | 用途 |
|---|---|---|
| `reject.quanx` | `reject` | 广告/追踪等拦截规则；大型规则集可能影响个别站点功能。 |
| `gfw-skip.quanx` | `direct` | 代理规则中的直连例外。 |
| `loc-cn.quanx` | `direct` | 中国大陆域名直连。 |
| `gfw.quanx` | `proxy` | GFWList 转换的代理域名规则。 |

资源 URL 来自 [`dmulle12/rules`](https://github.com/dmulle12/rules)，其 `rel` 分支会自动更新。此仓库的主配置按从上到下的顺序列出资源；出现冲突时可在 Quantumult X 命中记录中核对，必要时调整顺序或停用单条资源。

## 本地规则

`[filter_local]` 中的 `geoip, lan, direct` 与 `geoip, cn, direct` 处理局域网和中国大陆 IP；`final, proxy` 是兜底。若策略名称与你的 Quantumult X 版本/节点设置不符，先确认内置策略名与已导入的节点，再修改，不要直接添加未知组名。

若你不需要中国大陆直连，删除 `geoip, cn, direct` 并停用 `loc-cn.quanx`。如希望为特定服务指定策略，在 `[filter_local]` 中添加精确的 `host-suffix` / `host` 规则，并放在 `final` 前面。例如：

```ini
; host-suffix, example.com, direct
```

`example.com` 仅为示例域名，请替换为自己确认的域名。避免使用过宽的关键字或通配规则。

## 上游范围与限制

上游 `reject` 列表包含聚合广告/跟踪规则，维护者说明它不能移除与内容同域的原生信息流广告；不要因为单个漏网广告就屏蔽整个内容服务域名。上游亦说明 `loc-cn` 代表规则归类，不保证每个域名的服务器都位于中国大陆。来源、构建说明与许可证见上游 README。
