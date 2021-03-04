# breakout
Breakout with python

![breakout_image2](https://user-images.githubusercontent.com/61465092/75839872-2c5b7b00-5e0d-11ea-837f-08e0997a4a20.png)


# 環境
* Python 3.8.1
* pygame 1.9.6


# スタート方法
* インストール
```
git clone https://github.com/Kazu-SK/breakout.git
```

* 実行
```
python breakout.py
```

* Ctrlキーを入力したらBGMと共にゲームがスタート。
* スタート時、ボールはオレンジ色の線の方向に進む。


  
# シールド(自機)
* ボールがシールドのどの部分に接触したかでその後のボールの飛ぶ方向が決まる。真ん中付近に当たった場合は真上に飛び、左側に当たった場合はボールも左側に飛ぶ。



# ブロック
* ブロックの色によって効果が異なる。

  - 緑色 : 普通のブロック
  - 水色 : シールドの横幅が最大になる。
  - 青色 : シールドの横幅が最小になる。
  - 白色 : 横幅がスタート時の大きさに戻る。
      


# ゲームオーバー
* 以下の場合、ゲームオーバーとなる。

  - シールドの赤い部分にボールが接触した場合
  - 一番下のオレンジの壁にボールが接触した場合


# スコア
* 画面の左上に表示している。
* ブロックひとつにつき10ポイントが与えられる。連続でブロックを破壊した場合、連続で破壊した個数×5ポイントがブロック破壊時に上乗せされる。
* ゲームをクリアした場合、クリアの早さに応じてボーナスポイントが与えられる。ただし、9分12秒以内(bgm2周分)にクリアしない場合、ボーナスポイントは0になる。
* ゲーム終了後、ポイントの合計がスコアとして出力される。


# 使用BGM,効果音のサイト
* ゲームクリア時のBGM
    <a href="https://pocket-se.info/">ポケットサウンド/効果音素材</a>

* その他の効果音、BGM
    <a href="https://maoudamashii.jokersounds.com/" title="フリー音楽素材/魔王魂" target="_blank">フリー音楽素材/魔王魂</a>
