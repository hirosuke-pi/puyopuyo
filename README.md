# puyopuyo

CUI版とことんぷよやりたい人向け。
一応Linux/Windowsは動作確認済み。

## 動作環境

Python3が入っているPC。

## 実行方法

puyopuyo.pyをダブルクリックすると起動。

## 操作方法

A: 左に移動
S: 下に移動
D: 右に移動

L: 右回転
M: 左回転

Enter: 終了
Space: 画面初期化

## 注意事項

プレイ中にウィンドウ幅を変更すると画面が崩壊するので、崩壊した場合はスペースキーを押すと直ります。

## 開発

```sh
# pre-commit hooks インストール
uv run pre-commit install

# 仮想環境作成＆依存インストール
uv sync

# リント＆フォーマット
uv run task lint

# 仮想環境の中に入る
. .venv/bin/activate

# (仮想環境内) リント＆フォーマット
task lint

# (仮想環境内) `puyopuyo` コマンド実行
puyopuyo

# 仮想環境から出る
deactivate
```
