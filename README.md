# ptt-scrape

PTT 爬蟲

## 用例

想要在 PTT 特定版上有特定作者發文時，能夠在 Discord 上接到通知。

## 使用方式

1. 安裝 [uv](https://docs.astral.sh/uv/getting-started/installation/)。
2. Clone 或是下載這個專案。
3. 在專案資料夾中，執行 `uv sync`。
4. 執行 `uv run --author: <author> --url: <url> --webhook-url: <webhook-url>`。

### 參數

- author: 作者名稱
- url: 板的網址，例如 <https://www.ptt.cc/bbs/Soft_Job/index.html>
- webhook-url: Discord 的 webhook 網址
