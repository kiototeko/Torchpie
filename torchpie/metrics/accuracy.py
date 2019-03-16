import torch


def binary_accuracy(output, target):
    '''
    Make sure output and target has same type
    '''
    correct = output == target
    return correct


def multi_class_accuracy(output, target):
    # output: [batch_size, num_classes] -> pred: [batch_size]
    pred = output.argmax(dim=1)
    correct = pred == target
    return correct


def multi_label_accuracy(output, target):
    # [batch_size, num_classes, prob]
    num_classes = output.shape[1]
    last_dim = output.ndimension()
    output = output.transpose(1, last_dim - 1)


def multilabel_accuracy(output, target):
    pass


class Accuracy:
    pass
