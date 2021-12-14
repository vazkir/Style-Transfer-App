import torch
from argparse import Namespace
from psp.models import pSp


def psp2onnx(_ckpt, _onnx):
    from argparse import Namespace
    from psp.models import pSp

    ckpt = torch.load(_ckpt,
                      map_location='cpu')

    img_tensor = torch.randn(1, 3, 256, 256)

    opts = Namespace(**ckpt['opts'])
    opts.checkpoint_path = "./cartoon_psp_mobile_256p.pt"
    opts.device = "cpu"

    net = pSp(opts)
    net.eval()

    dynamic_axes = {'input': {0: 'batch'}, 'output': {0: 'batch'}}
    torch.onnx.export(
        model=net,
        args=img_tensor,
        f=_onnx,
        verbose=False,
        do_constant_folding=True,
        input_names=['input'],
        output_names=['output'],
        opset_version=10
    )
