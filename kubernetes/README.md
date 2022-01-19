# Kubernetes 部署

这是用来快速部署本代理池的 Helm Charts。

首先需要有一个 Kubernetes 集群，其次需要安装 Helm，确保 helm 命令可以正常运行。

安装参考：

- Kubernetes：[https://setup.scrape.center/kubernetes](https://setup.scrape.center/kubernetes)。
- Helm: [https://setup.scrape.center/helm](https://setup.scrape.center/helm)。

## 安装

安装直接使用 helm 命令在本文件夹运行即可，使用 `-n` 可以制定 NameSpace。

```shell
helm install proxypool-app . -n scrape
```

其中 proxypool-app 就是应用的名字，可以任意取名，它会用作代理池 Deplyment 的名称。

如果需要覆盖变量，可以修改 values.yaml 文件，执行如下命令安装：

```shell
helm install proxypool-app . -f values.yaml -n scrape
```

## 更新

如果需要更新配置，可以修改 values.yaml 文件，执行如下命令更新版本：

```shell
helm upgrade proxypool-app . -f values.yaml -n scrape
```

## 卸载

如果不想使用了，可以只用 uninstall 命令卸载：

```shell
helm uninstall proxypool-app -n scrape
```
