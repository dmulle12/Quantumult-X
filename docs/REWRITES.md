# Rewrite / MitM 说明

## 默认状态

`Quantumult-X.conf` 列出三项可选上游资源，但全部设为 `enabled=false`：

- Bilibili：过滤部分广告接口、首页信息流项目，并调整部分个人页/导航响应。
- Weibo：过滤部分广告响应及信息流推广项目。
- FQ Reader：拦截上游规则中列出的若干广告/统计域名。

规则会随上游变化；这里只描述目前审阅到的行为，不能保证未来版本行为不变。启用前请查看对应的 [上游规则文件](https://github.com/dmulle12/rules/tree/main/source) 与构建结果。

## 启用前须知

1. 重写会改变特定 App 的请求/响应，可能导致页面、搜索、登录、播放或其他功能异常；停用该资源可回滚。
2. HTTPS 内容重写通常需要 Quantumult X MitM 证书。安装并信任根证书后，相关 HTTPS 流量可被本机解密检查。只对自己控制的设备启用，并了解其影响。
3. 不要把 `[mitm]` 的 `p12`、`passphrase`、私钥或个人证书提交到仓库。模板不包含这些资料，也不默认配置 MitM 主机名。
4. 只启用你实际使用且愿意修改其流量的应用规则；不需要的应用可保持禁用或删除对应行。

## 启用步骤

1. 打开 `Quantumult-X.conf` 的 `[rewrite_remote]`，只将所需资源的 `enabled=false` 改为 `enabled=true`。
2. 在 Quantumult X 中更新资源，查看资源详情中的 `hostname` 与规则，确认范围。
3. 如应用提示需要 MitM，先阅读 Quantumult X 官方说明，再在应用内启用 MitM、生成并安装证书，并在系统设置中显式信任。证书安装操作不由此模板自动完成。
4. 验证目标 App 功能。异常时先禁用刚启用的资源并重连隧道。

## 本地语法示例

[`../snippets/rewrite-examples.snippet`](../snippets/rewrite-examples.snippet) 仅包含对 `example.invalid` 保留域名的注释样例，不会拦截真实 App 流量。
