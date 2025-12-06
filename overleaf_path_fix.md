# Overleaf 路径修复指南

## 你的文件结构
```
your-project/
├── latex/
│   ├── acl_latex.tex          ← 主文件（你当前编辑的文件）
│   ├── acl_lualatex.tex
│   ├── acl.sty
│   └── input/
│       ├── model_architecture.tex  ← 要输入的文件
│       └── electra_arch.png
└── figures/
```

## 问题分析

如果你在 `latex/acl_latex.tex` 中使用：
```latex
\input{latex/input/model_architecture.tex}  ❌ 错误！
```

**为什么会错？**
- `\input` 使用**相对路径**，相对于当前文件所在目录
- 当前文件在 `latex/` 目录
- 所以路径应该从 `latex/` 开始，而不是从根目录

## 正确的写法

### 在 `latex/acl_latex.tex` 中：

```latex
% ✅ 正确：相对路径从 latex/ 目录开始
\input{input/model_architecture}

% 或者（如果一定要加扩展名）
\input{input/model_architecture.tex}
```

### 如果图片也在 `latex/input/` 目录：

```latex
% 在 model_architecture.tex 中引用图片
\includegraphics[width=0.95\textwidth]{input/electra_arch.png}

% 或者设置图片路径
\graphicspath{{input/}{./}}
\includegraphics[width=0.95\textwidth]{electra_arch.png}
```

## 完整示例

### `latex/acl_latex.tex` 文件：

```latex
\documentclass[11pt,a4paper,twocolumn]{article}
\usepackage{graphicx}

% 设置图片路径
\graphicspath{{input/}{./}}

\begin{document}

\section{Model Architecture}

% ✅ 正确的输入方式
\input{input/model_architecture}

\section{Experiments}
...

\end{document}
```

### `latex/input/model_architecture.tex` 文件：

```latex
% 注意：这里不需要 \documentclass 和 \begin{document}

We use ELECTRA-small as our backbone model.

\begin{figure*}[t]
    \centering
    % 图片路径：因为设置了 \graphicspath，可以直接用文件名
    \includegraphics[width=0.95\textwidth]{electra_arch.png}
    \caption{ELECTRA-small architecture for NLI.}
    \label{fig:electra_arch}
\end{figure*}

The model consists of 12 transformer layers...
```

## 路径规则总结

| 当前文件位置 | 目标文件位置 | 正确的 \input 路径 |
|------------|------------|------------------|
| `latex/acl_latex.tex` | `latex/input/model_architecture.tex` | `input/model_architecture` |
| 根目录的 `main.tex` | `latex/input/model_architecture.tex` | `latex/input/model_architecture` |
| `latex/acl_latex.tex` | `latex/sections/intro.tex` | `sections/intro` |

## 快速修复步骤

1. **打开 `latex/acl_latex.tex`**
2. **找到错误的 `\input` 命令**
3. **修改为**：
   ```latex
   \input{input/model_architecture}
   ```
4. **重新编译**

## 调试技巧

如果还是出错，尝试：

1. **检查文件名大小写**：`model_architecture.tex` vs `Model_Architecture.tex`
2. **检查扩展名**：可以加 `.tex`，也可以不加
3. **使用绝对路径测试**（不推荐，但可以验证）：
   ```latex
   \input{./input/model_architecture}
   ```

