# 💱 Universal Currency Analyzer (通用汇率分析器)

A professional, data-driven currency exchange analysis tool built with Python and Streamlit. This application helps users make informed decisions on when to exchange currencies by analyzing historical trends, technical indicators, and moving averages.

---

## ✨ Features (功能特点)

- **Universal Currency Pairs:** Analyze any combination of major currencies (USD, CNY, CAD, EUR, GBP, JPY, etc.).
- **DXY Index Support:** Monitor the US Dollar Index (DXY) to understand global USD strength.
- **Technical Indicators:** Includes **RSI (Relative Strength Index)** and **Moving Averages (SMA 30/100)** for trend analysis.
- **Smart Decision Signals:** Automated "Good", "Caution", or "Wait" signals based on technical analysis.
- **Bidirectional Views:** Easily toggle between "1 Source = X Target" and "1 Target = X Source".
- **Interactive Charts:** High-quality, zoomable candlestick charts powered by Plotly.
- **Bilingual Support:** Fully localized in **English** and **简体中文**.
- **Quick Converter:** Built-in calculator to compare current rates against the 30-day average.

---

## 🚀 Getting Started (快速入门)

### Prerequisites (环境要求)
- Python 3.8+
- Git

### Installation (安装步骤)

1. **Clone the repository:**
   ```bash
   git clone git@github.com:oap/xe.git
   cd xe
   ```

2. **Set up virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the App (运行应用)

```bash
streamlit run app.py
```

---

## ☁️ Deployment (部署指南)

This project is configured with a **CI/CD pipeline** using GitHub Actions. It automatically builds a Docker container and publishes it to **GitHub Container Registry (ghcr.io)** whenever you push changes to the `main` branch.

### 1. Automated Build (自动构建)
Simply push your code changes to the `main` branch:
```bash
git add .
git commit -m "update app"
git push origin main
```
GitHub Actions will automatically build the Docker image. You can find your image at:
`ghcr.io/oap/xe:latest`

> **Note:** For the first deployment, go to your GitHub Repo -> **Packages** -> **Package Settings** and change the visibility to **Public** so Cloudflare can pull the image without authentication tokens.

### 2. Host on Cloudflare (Cloudflare 部署)
You can deploy this container directly using **Cloudflare Containers**:

1.  Log in to the **Cloudflare Dashboard**.
2.  Navigate to **Compute (Containers)**.
3.  Create a new deployment.
4.  **Image URL:** `ghcr.io/oap/xe:latest`
5.  **Port:** `8501` (Streamlit default).
6.  **Deploy!** Cloudflare will pull the latest image and host your app globally.

---

## 💡 How it Works (指标说明)

- **RSI < 30:** Oversold condition. The currency may be undervalued (Buying opportunity).
- **RSI > 70:** Overbought condition. The currency may be overvalued (Potential peak).
- **SMA 30 (Orange):** Represents the short-term trend. When the rate stays above SMA 30, it indicates an upward trend.
- **Decision Logic:** The app evaluates if the current rate is trending above its 30-day average while monitoring RSI to avoid "buying the top."

---

## 🛠 Tech Stack (技术栈)

- **Language:** Python
- **UI Framework:** [Streamlit](https://streamlit.io/)
- **Data Source:** [yfinance](https://github.com/ranaroussi/yfinance) (Yahoo Finance API)
- **Charts:** [Plotly](https://plotly.com/)
- **Data Processing:** Pandas, Numpy

---

## 📜 Disclaimer (免责声明)

*This application is for informational and educational purposes only. It does not constitute financial advice. Exchange rates and market data provided by Yahoo Finance may be delayed. Always consult with a professional financial advisor before making significant currency exchanges.*

*此应用仅供信息参考和教育用途，不构成任何理财建议。由 Yahoo Finance 提供的汇率和市场数据可能存在延迟。在进行重大货币兑换前，请务必咨询专业的理财顾问。*
