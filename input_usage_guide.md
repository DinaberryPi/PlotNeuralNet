# LaTeX \input 命令使用指南

## 常见错误和解决方法

### 错误 1: 文件路径不存在
```latex
\input{latex/input/model_architecture.tex}  % 如果文件不存在会报错
```

**解决方法**：
1. 检查文件是否真的存在于该路径
2. 检查路径是否正确（注意大小写）
3. 在 Overleaf 中，确保文件已上传到正确位置

### 错误 2: 路径分隔符问题
```latex
\input{latex\input\model_architecture.tex}  % Windows 路径，可能出错
```

**正确写法**：
```latex
\input{latex/input/model_architecture}  % 使用正斜杠，不需要 .tex 扩展名
```

### 错误 3: 扩展名问题
```latex
\input{latex/input/model_architecture.tex}  % 可以加扩展名，但通常不加
```

**推荐写法**：
```latex
\input{latex/input/model_architecture}  % 不加 .tex 扩展名（推荐）
```

## 正确的使用方法

### 方法 1: 相对路径（推荐）
```latex
% 如果文件在 latex/input/model_architecture.tex
\input{latex/input/model_architecture}

% 如果文件在项目根目录
\input{model_architecture}

% 如果文件在当前目录的子文件夹
\input{sections/model_architecture}
```

### 方法 2: 使用 subfiles 包（适合大型项目）
```latex
\usepackage{subfiles}

% 在主文件中
\subfile{latex/input/model_architecture}
```

### 方法 3: 使用 import 包（更灵活）
```latex
\usepackage{import}

% 从指定路径导入
\subimport{latex/input/}{model_architecture}
```

## 在 Overleaf 中的最佳实践

### 1. 检查文件结构
确保你的文件结构是这样的：
```
your-project/
├── main.tex
├── latex/
│   └── input/
│       └── model_architecture.tex
└── images/
    └── electra_arch.png
```

### 2. 使用正确的命令
```latex
% 在 main.tex 中
\documentclass{article}
\begin{document}

\section{Model Architecture}
\input{latex/input/model_architecture}

\end{document}
```

### 3. 如果文件在根目录
```latex
% 如果 model_architecture.tex 在项目根目录
\input{model_architecture}
```

## 调试技巧

### 1. 检查文件是否存在
在 Overleaf 中：
- 点击左侧文件树
- 确认文件路径是否正确
- 检查文件名大小写

### 2. 查看编译错误
Overleaf 会显示具体错误信息：
- `File not found` - 文件不存在
- `Missing \begin{document}` - 文件格式问题
- `Undefined control sequence` - 命令错误

### 3. 测试路径
先尝试简单的路径：
```latex
% 测试：如果文件在根目录
\input{model_architecture}

% 如果上面可以，再尝试子目录
\input{latex/input/model_architecture}
```

## 常见错误信息

1. **`File 'latex/input/model_architecture.tex' not found`**
   - 文件不存在或路径错误
   - 检查文件是否已上传
   - 检查路径大小写

2. **`Missing \begin{document}`**
   - 被输入的文件不应该有 `\documentclass` 和 `\begin{document}`
   - `\input` 的文件应该只包含内容，不是完整文档

3. **`Undefined control sequence`**
   - 被输入的文件中使用了未定义的命令
   - 确保在主文件中加载了必要的包

## 示例：正确的文件结构

### main.tex
```latex
\documentclass[twocolumn]{article}
\usepackage{graphicx}

\begin{document}

\section{Introduction}
Some text here.

\section{Model Architecture}
\input{latex/input/model_architecture}

\section{Experiments}
More text here.

\end{document}
```

### latex/input/model_architecture.tex
```latex
% 注意：这里不需要 \documentclass 和 \begin{document}

We use ELECTRA-small as our backbone model.

\begin{figure*}[t]
    \centering
    \includegraphics[width=0.95\textwidth]{images/electra_arch.png}
    \caption{Model architecture.}
    \label{fig:arch}
\end{figure*}

The model consists of 12 transformer layers...
```

