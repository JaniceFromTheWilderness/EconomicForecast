## 進出口預測
本範例所採用之主要預測模型呈現如下：

$$
y_{t+h} = f\left(\mathbf{F}_t;\boldsymbol{\beta}\right) + v_{t+h}, \quad t=1,\dots,T.
$$

此預測模型中，$y_{t+h}$ 代表進出口變數未來 $h$ 期的數值，而此變數可以被無法觀測到的總體因子 $\mathbf{F}_t$ 與對應之係數 $\boldsymbol{\beta}$ 解釋。$v_{t+h}$ 代表預測誤差。因為總體因子是無法觀測到的，為了能夠得到總體因子的估計，我們亦作出以下因子結構假設：

$$
\mathbf{x}_t = \boldsymbol{\Lambda} \mathbf{F}_t + \mathbf{e}_t,
$$

其中，$\mathbf{x}_t$ 代表一個高維度的資料集合，維度為 $N \times 1$；$\mathbf{F}_t = (\mathbf{f}_t^\top, \mathbf{g}_t^\top)^\top$ 且 $\mathbf{x}_t$ 可以被適當地分割為 $\mathbf{x}_{1t}$ 與 $\mathbf{x}_{2t}$，維度分別為 $N_1 \times 1$ 與 $N_2 \times 1$。因子 $\mathbf{f}_t$ 和 $\mathbf{g}_t$ 的維度分別為 $r_1$ 與 $r_2$。據此，我們可以將 $\boldsymbol{\Lambda}$ 得到下列改寫：

$$
\boldsymbol{\Lambda} =
\begin{bmatrix}
\mathbf{0} & \boldsymbol{\lambda}_{12} \\
\boldsymbol{\lambda}_{21} & \boldsymbol{\lambda}_{22}
\end{bmatrix}.
$$

上式假設 $\mathbf{g}_t$ 對於 $\mathbf{x}_{1t}$ 與 $\mathbf{x}_{2t}$ 都有影響，然而 $\mathbf{f}_t$ 則僅針對 $\mathbf{x}_{2t}$ 產生影響。換句話說，$\mathbf{x}_{1t}$ 對於協助預測 $y_{t+h}$ 理論上並沒有作用。為了達成合適的變數挑選，本範例考慮三種預測架構，詳列如下：

---

### Lasso-PCA

根據因子結構，本範例針對資料集 $\mathbf{X}$ 採用特徵分解 (eigen-decomposition) 進行因子估計。待得到 $\hat{\mathbf{F}}_t$ 後，由於模型假設 $y_{t+h}$ 只受到部分因子影響且假設函數 $f(\cdot)$ 為線性函數，因此接續採用 Lasso 型估計進行估計。具體而言，預測係數可透過以下步驟得知 ($\delta$ 為懲罰係數，可透過交叉驗證選取)：

$$
\hat{\boldsymbol{\beta}} = \arg\min_{\boldsymbol{\beta}} \left( \frac{1}{2} \left( \mathbf{y} - \hat{\mathbf{F}} \boldsymbol{\beta} \right)^\top \left( \mathbf{y} - \hat{\mathbf{F}} \boldsymbol{\beta} \right) + \delta \sum_{j=1}^{r} |\beta_j| \right).
$$

---

### Lasso-X

若研究者對於 $\mathbf{x}_{2t}$ 有事先資訊，預測模型亦可改寫為：

$$
y_{t+h} = f(\mathbf{x}_{2t}^\top; \boldsymbol{\gamma}) + v_t + o_p(1).
$$

一般而言，$\boldsymbol{\gamma}$ 為一非零矩陣且滿秩。當 $N_2$ 過大甚至大於 $T$，在假設函數 $f(\cdot)$ 為線性函數下，傳統統計方法無法提供良好的估計與預測。為了解決此問題，本範例亦考慮以下估計 ($\delta$ 為懲罰係數，可透過交叉驗證選取)：

$$
\hat{\boldsymbol{\gamma}} = \arg\min_{\boldsymbol{\gamma}} \left( \frac{1}{2} \left( \mathbf{y} - \mathbf{X} \boldsymbol{\gamma} \right)^\top \left( \mathbf{y} - \mathbf{X} \boldsymbol{\gamma} \right) + \delta \sum_{j=1}^{N} |\gamma_j| \right).
$$

---

### Ridge-PCA

本範例亦考慮 Ridge 型估計。具體而言，預測係數可透過以下步驟得知 ($\delta$ 為懲罰係數，可透過交叉驗證選取)：

$$
\hat{\boldsymbol{\beta}} = \arg\min_{\boldsymbol{\beta}} \left( \frac{1}{2} \left( \mathbf{y} - \hat{\mathbf{F}} \boldsymbol{\beta} \right)^\top \left( \mathbf{y} - \hat{\mathbf{F}} \boldsymbol{\beta} \right) + \delta \sum_{j=1}^{r} |\beta_j|^2 \right).
$$

---

### Boosting Regression

令 $\hat{f}(\mathbf{x}_t) = 0$，殘差 $r_t = y_t$。自 $b = 1,\dots,B$ 重複下列步驟：

1. 對樣本 $(r_t, \mathbf{x}_t)$ 進行迴歸樹分析；
2. 更新預測值 $\hat{f}(\mathbf{x}_t)$ ($\lambda$ 為學習參數)：
   $$
   \hat{f}(\mathbf{x}_t) = \hat{f}(\mathbf{x}_t) + \lambda \hat{f}(\mathbf{x}_t);
   $$
3. 更新殘差：
   $$
   r_t = r_t - \lambda \hat{f}(\mathbf{x}_t).
   $$

最終，我們可以得到：

$$
\hat{f}(\mathbf{x}_t) = \sum_{b=1}^B \lambda \hat{f}^b(\mathbf{x}_t).
$$
