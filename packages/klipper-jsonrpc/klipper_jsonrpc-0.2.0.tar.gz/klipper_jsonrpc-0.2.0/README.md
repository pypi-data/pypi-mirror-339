# 🖨️ Klipper JSON-RPC クライアント

Klipper(Moonraker)と通信するためのPython WebSocket JSON-RPCクライアントライブラリです。

## ✨ 特徴

- 🔄 非同期・同期両方のAPIをサポート
- 🔌 WebSocketを使用した簡単なKlipper通信
- 🎯 カスタム通知ハンドラーのサポート
- 🔒 スレッドセーフな操作

## 🚀 インストール方法

## 📝 使用例

### 基本的な使い方

```python
from klipper_jsonrpc import KlipperClient

# クライアントのインスタンスを作成
client = KlipperClient()

# Klipper WebSocketに接続
client.run("ws://your-klipper-host/websocket")

# 同期的にリクエストを送信
response = client.sync_send_request("printer.info")
print(response)

# カスタム通知ハンドラーを追加
def on_status_update(data):
    print(f"ステータス更新: {data}")

client.add_method_process("notify_proc_stat_update", on_status_update)

# 接続を閉じる
client.sync_close()
```

### 非同期での使用例

```python
import asyncio
from klipper_jsonrpc import KlipperClient

async def main():
    client = KlipperClient()
    await client.connect("ws://your-klipper-host/websocket")
    
    response = await client.async_send_request("printer.info")
    print(response)
    
    await client.close()

asyncio.run(main())
```

## 💻 動作環境

- Python 3.7以上
- aiohttp 3.11.0以上

## 🔧 主な機能

- WebSocketを使用したKlipperとの双方向通信
- JSON-RPCプロトコルによるメッセージング
- カスタムイベントハンドラーの登録機能
- スレッドセーフな同期・非同期API

## 📚 API ドキュメント

### KlipperClient クラス

#### メソッド一覧

- `run(url)`: クライアントの接続を開始します
- `sync_send_request(method, params=None)`: 同期的にリクエストを送信します
- `async_send_request(method, params=None)`: 非同期でリクエストを送信します
- `add_method_process(method, func)`: カスタムメソッドハンドラーを追加します
- `sync_close()`: 接続を同期的に終了します
- `close()`: 接続を非同期で終了します

## 🤝 コントリビューション

バグ報告や機能要望は、GitHubのIssueにて受け付けています。
プルリクエストも大歓迎です！

## ⚖️ ライセンス


## 📞 サポート

ご不明な点がございましたら、GitHubのIssueにてお問い合わせください。
