# ComfyUI-Flowty-TripoSR-ZHO

## 我在原作者的基础上进行了修改，区别如下（已和原作者沟通，意见不同，所以作为独立分支）：

1.是否内含背景去除功能
- 原版：为了保证更快的生成速度，选择去掉了背景去除的步骤，仅保留了生成部分
- 改版：增加了背景去除的选项，可以选择使用，也可选择不使用，速度上略慢一点

2.对 RGBA 图像的支持不同
- 目前原版 RGBA 图像直接转为 RGB 后生成的模型会带有黑色背板的，算是一个 bug，估计作者还会继续优化
- 我的改版遵从原项目对 alpha 通道重新着色为灰色的操作，所以可以保证生成模型不会带有背景


## 两版节点对比示意图：


![TPSR](https://github.com/ZHO-ZHO-ZHO/ComfyUI-Flowty-TripoSR/assets/140084057/2feb13f8-3271-41cf-b2be-e937c4ba6209)


## 与原版区别示意视频：



https://github.com/ZHO-ZHO-ZHO/ComfyUI-Flowty-TripoSR/assets/140084057/f0e038c8-de7a-425c-ba02-0edc45617077



## 使用建议：

更加追求速度可直接选择原版，想要自带背景去除 + 更好的 RGBA 支持选择我的改版就好，两个版本之间没有好坏之分，大家根据自己的喜好选择就好！


## 工作流设计：

LayerDiffusion 和 TripoSR 简直绝配！所以设计了一版和 LayerDiffusion 衔接的工作流，由 LayerDiffusion 生成透明对象，然后直接通过 TripoSR 转为 3D 模型（用的是我这版节点）

[LayerDIffusion + TripoSR 【Zho】](https://github.com/ZHO-ZHO-ZHO/ComfyUI-Flowty-TripoSR/blob/master/TRIPOSR-ZHO%20WORKFLOWS/LayerDIffusion%20%2B%20TripoSR%E3%80%90Zho%E3%80%91.json)


![Dingtalk_20240305224540](https://github.com/ZHO-ZHO-ZHO/ComfyUI-Flowty-TripoSR/assets/140084057/fe05a7ef-6354-48e9-9b47-51207ac5814a)




## 下面是原作者的内容：

This is a custom node that lets you use TripoSR right from ComfyUI.

[TripoSR](https://github.com/VAST-AI-Research/TripoSR) is a state-of-the-art open-source model for fast feedforward 3D reconstruction from a single image, collaboratively developed by Tripo AI and Stability AI. (TL;DR it creates a 3d model from an image.)

![example](workflow-sample.png)

I've created this node for experimentation, feel free to submit PRs for performance improvements etc.

### Installation:
* Install ComfyUI
* Clone this repo into ```custom_nodes```:
  ```shell
  $ cd ComfyUI/custom_nodes
  $ git clone https://github.com/flowtyone/ComfyUI-Flowty-TripoSR.git
  ```
* Install dependencies:
  ```shell
  $ cd ComfyUI-Flowty-TripoSR
  $ pip install -r requirements.txt
  ```
* [Download TripoSR](https://huggingface.co/stabilityai/TripoSR/blob/main/model.ckpt) and place it in ```ComfyUI/models/checkpoints```
* Start ComfyUI (or restart)

Special thanks to MrForExample for creating [ComfyUI-3D-Pack](https://github.com/MrForExample/ComfyUI-3D-Pack). Code from that node pack was used to display 3d models in comfyui.

This is a community project from [flowt.ai](https://flowt.ai). If you like it, check us out!

<picture>
 <source media="(prefers-color-scheme: dark)" srcset="logo-dark.svg" height="50">
 <source media="(prefers-color-scheme: light)" srcset="logo.svg" height="50">
 <img alt="flowt.ai logo" src="flowt.png" height="50">
</picture>
