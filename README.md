# TorchPie

## Install

```bash
pip install git+https://git.dev.tencent.com/SunDoge/torchpie.git
```

## Usage

单机多卡分布式
```bash
python -m torchpie.distributed.launch --gpus 1,2,3,4 train.py -c config/default.conf -e exps/my-experiment
```

## Roadmap

- [ ] tests
- [ ] docs
- [ ] metrics
- [ ] ci

## Functions

- 自动保存实验代码和配置
- 主要关注DistributedDataParallel(apex)和DistributedDataParallel(torch)，不再支持cpu和DataParallel


