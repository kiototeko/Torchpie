# TorchPie

## Install

```bash
pip install git+https://git.dev.tencent.com/SunDoge/torchpie.git
```

## Roadmap

- [ ] tests
- [ ] docs
- [ ] metrics
- [ ] ci

## Functions

- 自动保存实验代码和配置
- 主要关注DistributedDataParallel(apex)，不再支持cpu，DataParallel和DistributedDataParallel(torch)

## Startup Sequence

1. experiment: get experiment path, args
2. logging: log to experiment path
3. config: get config
4. your code
