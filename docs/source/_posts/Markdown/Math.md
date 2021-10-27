---
title: Marldown之数学公式详解
tags: [Markdown, Math]
categories: [Markdown, Math]
# index_img: /image/page_image/git1.jpg
banner_img: /image/background/background11.jpg
date: 2020-11-10 08:00:00
hide: false
---

### 1. Math 引用

1. 行内式引用
   `\\(....\\)`
   `$..$`
2. 独立式引用
   `$$...$$`
   `\\[..\\]`
   `\begin{equation}...\end{equation}`

```
$ E = mc^2 $
$$ E = mc^2 $$
\[ \boxed{E = mc^2} \]
```

$ E = mc^2 $
$$ E = mc^2 $$
\[ \boxed{E = mc^2} \]

```math
E = mc^2
```

- 方程组

$$
\begin{cases}
a_1x+b_1y+c_1z=d_1\\
a_2x+b_2y+c_2z=d_2\\
a_3x+b_3y+c_3z=d_3\\
\end{cases}
$$

```
\begin{cases}
a_1x+b_1y+c_1z=d_1\\
a_2x+b_2y+c_2z=d_2\\
a_3x+b_3y+c_3z=d_3\\
\end{cases}
```

### 2. 基本元素

- 希腊字母

|  代码   |   符号    |  代码  |   符号   |  代码   |   符号    |  代码   |   符号    |   代码   |    符号    |    代码     |     符号      |
| :-----: | :-------: | :----: | :------: | :-----: | :-------: | :-----: | :-------: | :------: | :--------: | :---------: | :-----------: |
| \alpha  | $\alpha$  | \beta  | $\beta$  | \gamma  | $\gamma$  | \delta  | $\delta$  |   \mu    |   $\mu$    | \varepsilon | $\varepsilon$ |
|  \zeta  |  $\zeta$  |  \eta  |  $\eta$  | \Gamma  | $\Gamma$  | \Delta  | $\Delta$  |  \Theta  |  $\Theta$  |  \vartheta  |  $\vartheta$  |
| \theta  | $\theta$  | \iota  | $\iota$  | \kappa  | $\kappa$  | \lambda | $\lambda$ |   \phi   |   $\phi$   |  \epsilon   |  $\epsilon$   |
|   \nu   |   $\nu$   |  \xi   |  $\xi$   | \Lambda | $\Lambda$ |   \Xi   |   $\Xi$   |   \Pi    |   $\Pi$    |     \o      |      $o$      |
|   \pi   |   $\pi$   | \varpi | $\varpi$ |  \rho   |  $\rho$   | \varrho | $\varrho$ |  \sigma  |  $\sigma$  |  \varsigma  |  $\varsigma$  |
| \Sigma  | $\Sigma$  |  \Psi  |  $\Psi$  |  \Phi   |  $\Phi$   |  \tau   |  $\tau$   |  \Omega  |  $\Omega$  |  \upsilon   |  $\upsilon$   |
| \varphi | $\varphi$ |  \chi  |  $\chi$  |  \psi   |  $\psi$   | \omega  | $\omega$  | \Upsilon | $\Upsilon$ |             |      $ $      |

- 常用符号

| 代码  |      符号      |  代码  |      符号       |  代码  |      符号       |
| :---: | :------------: | :----: | :-------------: | :----: | :-------------: |
|   ^   |     $a^2$      |   \_   |      $a_2$      | \sqrt  |   $\sqrt{5}$    |
| \frac | $\frac {1}{2}$ | \dfrac | $\dfrac {1}{2}$ | \tfrac | $\tfrac {1}{2}$ |

- 特殊符号

|  代码   |   符号    | 代码  |  符号   |  代码  |   符号   |    代码     |     符号      |   代码    |    符号     |
| :-----: | :-------: | :---: | :-----: | :----: | :------: | :---------: | :-----------: | :-------: | :---------: |
| \infty  | $\infty$  | \cup  | $\cup$  |  \cap  |  $\cap$  |   \subset   |   $\subset$   | \subseteq | $\subseteq$ |
| \supset | $\supset$ |  \in  |  $\in$  | \notin | $\notin$ | \varnothing | $\varnothing$ |  \forall  |  $\forall$  |
| \exists | $\exists$ | \lnot | $\lnot$ | \nabla | $\nabla$ |  \partial   |  $\partial$   |

- 运算符

|      代码      |       符号       |      代码       |       符号        |        代码         |         符号          |        代码        |         符号         |      代码       |       符号        |
| :------------: | :--------------: | :-------------: | :---------------: | :-----------------: | :-------------------: | :----------------: | :------------------: | :-------------: | :---------------: | ------------------- | --------------------- |
|      \pm       |      $\pm$       |     \times      |     $\times$      |        \div         |        $\div$         |       \cdot        |       $\cdot$        |      \cap       |      $\cap$       |
|      \cup      |      $\cup$      |      \geq       |      $\geq$       |        \leq         |        $\leq$         |        \neq        |        $\neq$        |     \approx     |     $\approx$     |
|     \equiv     |     $\equiv$     |      \sum       |      $\sum$       |        \prod        |        $\prod$        |        \lim        |        $\lim$        |      \int       |      $\int$       |
|   \iint\quad   |     $\iint$      |     \iiint      |     $\iiint$      |     \leftarrow      |     $\leftarrow$      |    \rightarrow     |    $\rightarrow$     | \leftrightarrow | $\leftrightarrow$ |
|   \Leftarrow   |   $\Leftarrow$   |   \Rightarrow   |   $\Rightarrow$   |   \Leftrightarrow   |   $\Leftrightarrow$   |   \longleftarrow   |   $\longleftarrow$   | \longrightarrow | $\longrightarrow$ | \longleftrightarrow | $\longleftrightarrow$ |
| \Longleftarrow | $\Longleftarrow$ | \Longrightarrow | $\Longrightarrow$ | \Longleftrightarrow | $\Longleftrightarrow$ | \xleftarrow{x+y+z} | $\xleftarrow{x+y+z}$ |

- 样例

|         代码          |          符号          |             代码             |             符号              |              代码              |              符号               |
| :-------------------: | :--------------------: | :--------------------------: | :---------------------------: | :----------------------------: | :-----------------------------: |
|  \sum\_{i=1}^ni\quad  |  $\sum_{i=1}^ni\quad$  |  \sum\limits\_{i=1}^ni\quad  |  $\sum\limits_{i=1}^ni\quad$  |  \sum\nolimits\_{i=1}^ni\quad  |  $\sum\nolimits_{i=1}^ni\quad$  |
|  \prod\_{i=1}^n\quad  |  $\prod_{i=1}^n\quad$  |  \prod\limits\_{i=1}^n\quad  |  $\prod\limits_{i=1}^n\quad$  |  \prod\nolimits\_{i=1}^n\quad  |  $\prod\nolimits_{i=1}^n\quad$  |
| \lim\_{x\to0}x^2\quad | $\lim_{x\to0}x^2\quad$ | \lim\limits\_{x\to0}x^2\quad | $\lim\limits_{x\to0}x^2\quad$ | \lim\nolimits\_{x\to0}x^2\quad | $\lim\nolimits_{x\to0}x^2\quad$ |
|    \int_a\^bx\^2dx    |    $\int_a^bx^2dx$     |    \int\limits_a\^bx\^2dx    |    $\int\limits_a^bx^2dx$     |    \int\nolimits_a\^bx\^2dx    |    $\int\nolimits_a^bx^2dx$     |

\[ \int\int\quad \int\int\int\quad \int\int\int\int\quad \int\dots\int \]
`\[ \int\int\quad \int\int\int\quad \int\int\int\int\quad \int\dots\int \]`

- 注音和标注

$
\bar{x}     
\vec{x}
\hat{x}
\check{x}
\acute{x}
\grave{x}
\tilde{x}
\breve{x}
\mathring{x}
\dot{x}
\ddot{x}
$

```
\bar{x}
\vec{x}
\hat{x}
\check{x}
\acute{x}
\grave{x}
\tilde{x}
\breve{x}
\mathring{x}
\dot{x}
\ddot{x}
```

- 分隔符

$
\overline{xxx}
\underline{xxx}
\overleftarrow{xxx}
\underleftarrow{xxx}
\overrightarrow{xxx}
\underrightarrow{xxx}
\overleftrightarrow{xxx}
\underleftrightarrow{xxx}
\overbrace{xxx}             %brace 大括号
\underbrace{xxx}
\widehat{xxx}               %hat  帽
\widetilde{xxx}
$

```
\overline{xxx}
\underline{xxx}
\overleftarrow{xxx}
\underleftarrow{xxx}
\overrightarrow{xxx}
\underrightarrow{xxx}
\overleftrightarrow{xxx}
\underleftrightarrow{xxx}
\overbrace{xxx}             %brace 大括号
\underbrace{xxx}
\widehat{xxx}               %hat  帽
\widetilde{xxx}
```

\[
\Bigg(
\bigg(
\Big(
\big(
(x)
\big)
\Big)
\bigg)
\Bigg)\quad
\]

```
\[
    \Bigg(
        \bigg(
            \Big(
                \big(
                    (x)
                \big)
            \Big)
        \bigg)
    \Bigg)\quad
\]
```

\[
\Bigg[
\bigg[
\Big[
\big[
[x]
\big]
\Big]
\bigg]
\Bigg]\quad
\]

```
\[
    \Bigg[
        \bigg[
            \Big[
                \big[
                    [x]
                \big]
            \Big]
        \bigg]
    \Bigg]\quad
\]
```

\[
\Bigg\langle
\bigg\langle
\Big\langle
\big\langle
\langle x \rangle
\big\rangle
\Big\rangle
\bigg\rangle
\Bigg\rangle\quad
\]

```
\[
    \Bigg\langle
        \bigg\langle
            \Big\langle
                \big\langle
                    \langle x \rangle
                \big\rangle
            \Big\rangle
        \bigg\rangle
    \Bigg\rangle\quad
\]
```

\[
\Bigg\lvert
\bigg\lvert
\Big\lvert
\big\lvert
\lvert x \rvert
\big\rvert
\Big\rvert
\bigg\rvert
\Bigg\rvert\quad
\]

```
\[
    \Bigg\lvert
        \bigg\lvert
            \Big\lvert
                \big\lvert
                    \lvert x \rvert
                \big\rvert
            \Big\rvert
        \bigg\rvert
    \Bigg\rvert\quad
\]
```

\[
\Bigg\lVert
\bigg\lVert
\Big\lVert
\big\lVert
\lVert x \rVert
\big\rVert
\Big\rVert
\bigg\rVert
\Bigg\rVert
\]

```
\[
    \Bigg\lVert
        \bigg\lVert
            \Big\lVert
                \big\lVert
                    \lVert x \rVert
                \big\rVert
            \Big\rVert
        \bigg\rVert
    \Bigg\rVert
\]
```

- 省略号

\[ \dots , \cdots , \vdots ,\ddots \]

```
\[  \dots , \cdots , \vdots ,\ddots \]
```

- 空白间距

$
|\,| \\
|\:| \\
|\;| \\
|\quad| \\
|\qquad| \\
|\!|
$

```
|\,|
|\:|
|\;|
|\quad|
|\qquad|
|\!|
```

- 矩阵

> 居顶、居中(缺省) 、居底，分别用 t, c, b 来表示；  
> 列对齐也有三种方式：居左、居中、居右，分别用 l, c, r 表示。  
> \\\ 和& 用来分隔行和列。

\[
\begin{array}{ccc}
x_1 & x_2 & \dots \\\\
x_3 & x_4 & \dots \\\\
\vdots & \vdots & \ddots
\end{array}
\]

```
\[
    \begin{array}{ccc}
        x_1 & x_2 & \dots \\\\
        x_3 & x_4 & \dots \\\\
        \vdots & \vdots & \ddots
    \end{array}
\]
```

\[
\begin{pmatrix} a&b \\\\ c&d \end{pmatrix} \quad
\begin{bmatrix} a&b \\\\ c&d \end{bmatrix} \quad
\begin{Bmatrix} a&b \\\\ c&d \end{Bmatrix} \quad
\begin{vmatrix} a&b \\\\ c&d \end{vmatrix} \quad
\begin{Vmatrix} a&b \\\\ c&d \end{Vmatrix}
\]

```
\[
    \begin{pmatrix} a&b \\\\ c&d \end{pmatrix} \quad
    \begin{bmatrix} a&b \\\\ c&d \end{bmatrix} \quad
    \begin{Bmatrix} a&b \\\\ c&d \end{Bmatrix} \quad
    \begin{vmatrix} a&b \\\\ c&d \end{vmatrix} \quad
    \begin{Vmatrix} a&b \\\\ c&d \end{Vmatrix}
\]
```

Marry has a little matrix \( \begin{smallmatrix}
a&b\\\\c&d \end{smallmatrix} \) .

```
Marry has a little matrix \( \begin{smallmatrix}
a&b\\\\c&d \end{smallmatrix} \) .
```

- 多行公式
  -- 长公式
  $$
  x = a+b+c+ \\\\
  d+e+f+g
  $$

```
x = a+b+c+ \\\\
d+e+f+g
```

\[ \begin{split}
x =a+b+c+{} \\\\
d+e+f+g
\end{split} \]

```
\[ \begin{split}
x =a+b+c+{} \\\\
d+e+f+g
\end{split} \]
```

-- 公式组

$$
\begin{gather}
a = b+c+d \\\\
x = y+z
\end{gather} \\
\begin{align}
a &= b+c+d \\
x &= y+z
\end{align}
$$

```
\begin{gather}
a = b+c+d \\\\
x = y+z
\end{gather} \\
\begin{align}
a &= b+c+d \\
x &= y+z
\end{align}
```

- 数学字体
  \[
  \begin{equation}
  \mathrm{A}\quad
  \mathsf{A}\quad
  \mathtt{A}\quad
  \mathcal{A}\quad
  \mathbf{A}\quad
  \mathit{A}\quad
  \mathbb{A}\quad
  \mathfrak{A}\quad
  \mathscr{A}\quad
  \end{equation} \]

```
\[
\begin{equation}
\mathrm{A}\quad
\mathsf{A}\quad
\mathtt{A}\quad
\mathcal{A}\quad
\mathbf{A}\quad
\mathit{A}\quad
\mathbb{A}\quad
\mathfrak{A}\quad
\mathscr{A}\quad
\end{equation} \]
```
