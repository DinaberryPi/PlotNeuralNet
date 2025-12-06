# 在 Overleaf 中使用双栏图片的说明

## 快速开始

1. **上传图片文件**
   - 在 Overleaf 项目中，点击 "Upload" 按钮
   - 上传 `electra_arch.png` 文件
   - 建议放在项目根目录或 `images/` 文件夹中

2. **在 LaTeX 文档中插入图片**

### 方法一：跨双栏图片（推荐）

使用 `figure*` 环境，图片会占满整个页面宽度（双栏宽度）：

```latex
\begin{figure*}[t]
    \centering
    \includegraphics[width=0.95\textwidth]{electra_arch.png}
    \caption{ELECTRA-small architecture for NLI. The model processes the concatenated premise and hypothesis through the ELECTRA-small backbone (12 transformer layers), extracts the \texttt{[CLS]} token representation, and applies a classification head to produce the final prediction.}
    \label{fig:electra_arch}
\end{figure*}
```

**注意**：
- `figure*` 中的星号表示跨双栏
- `[t]` 表示图片放在页面顶部
- `width=0.95\textwidth` 表示图片宽度为文本宽度的 95%（留出一些边距）

### 方法二：单栏图片

如果图片只需要占一栏宽度：

```latex
\begin{figure}[t]
    \centering
    \includegraphics[width=\columnwidth]{electra_arch.png}
    \caption{ELECTRA-small architecture for NLI.}
    \label{fig:electra_arch}
\end{figure}
```

## 重要提示

1. **文档格式**：确保你的文档使用了双栏格式：
   ```latex
   \documentclass[twocolumn]{article}
   % 或者
   \usepackage[twocolumn]{geometry}
   ```

2. **图片位置**：
   - `[t]` - 页面顶部
   - `[b]` - 页面底部
   - `[h]` - 当前位置（可能不适用于 figure*）
   - `[!t]` - 强制放在顶部

3. **图片引用**：在正文中引用图片：
   ```latex
   As shown in Figure~\ref{fig:electra_arch}, ...
   ```

4. **图片路径**：如果图片在子文件夹中，使用：
   ```latex
   \includegraphics[width=0.95\textwidth]{images/electra_arch.png}
   ```

## 常见问题

**Q: 图片显示不出来？**
- 检查文件路径是否正确
- 确保文件名大小写匹配
- 检查是否上传了 PNG 文件

**Q: 图片太大/太小？**
- 调整 `width` 参数：`0.8\textwidth`, `0.9\textwidth`, `1.0\textwidth`
- 或使用 `scale` 参数：`scale=0.8`

**Q: 图片位置不对？**
- `figure*` 环境中的图片会出现在下一页或当前页的顶部/底部
- 这是 LaTeX 的正常行为，用于优化页面布局

