import torch


@torch.no_grad()
def accuracy(output, target, topk=(1,)):
    """Computes the accuracy over the k top predictions for the specified values of k"""

    maxk = max(topk)
    # batch_size = target.size(0)
    # Faster
    batch_size = target.shape[0]
    _, pred = output.topk(maxk, dim=1)
    pred_t = pred.t()
    # broadcast
    correct = pred_t.eq(target.view(1, -1))

    res = []
    for k in topk:
        correct_k = correct[:k].view(-1).float().sum(0, keepdim=True)
        res.append(correct_k.mul_(100.0 / batch_size))
    return res
