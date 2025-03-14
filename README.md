# Telegram 暗棋遊戲 Bot

## 📌 介紹
本專案旨在開發一個基於 Telegram 平台的暗棋遊戲 Bot，讓使用者能夠透過與 Bot 的互動，在 Telegram 上進行暗棋遊戲。電腦將作為對手，與玩家進行對弈。  
點此看[規格細節](https://hackmd.io/@vincentinttsh/BJg3g4w4p)。

## 🎯 功能特點
- **啟動新遊戲**：使用者可透過指令開始一場新的暗棋遊戲。
- **遵循暗棋規則**：遊戲嚴格按照標準暗棋規則進行，包括棋子佈局、移動方式、吃子規則等。
- **電腦對手**：電腦作為後手，具備基本的走棋和吃子策略。
- **非法操作提示**：當使用者進行非法操作時，Bot 會給予提示並阻止該行為。
- **遊戲結束判定**：能夠判斷遊戲結束條件，並宣布勝負結果。
- **重啟遊戲**：遊戲結束後，使用者可選擇重新開始一局。

## 🛠️ 使用方法
1. **添加 Bot**：
   - 在 Telegram 中搜尋並添加該暗棋遊戲 Bot。

2. **開始遊戲**：
   - 輸入 `/start` 指令以啟動新遊戲。

3. **遊戲操作**：
   - **翻棋**：點擊未翻開的棋子，將其翻為明棋。先行方第一次翻出的棋子顏色，該色成為他的棋子；反之為敵方。
   - **移動棋子**：選擇己方明棋，並點擊相鄰的空格以移動棋子。
   - **吃子**：選擇己方明棋，並點擊相鄰的敵方棋子以進行吃子操作。

4. **注意事項**：
   - 電腦作為後手，玩家需先行一步。
   - 若進行非法操作，Bot 會提示錯誤，並要求重新操作。

## ⚙️ 技術細節
- **開發語言**：Python
- **主要套件**：
  - `python-telegram-bot`：處理 Telegram Bot 的訊息接收與回應。
  - `numpy`：用於棋盤狀態的矩陣表示與操作。
- **遊戲邏輯**：
  - **棋盤表示**：使用 4x8 的矩陣表示棋盤，每個元素代表一個棋子或空格。
  - **棋子等級**：按照暗棋規則定義棋子等級，用於判斷吃子合法性。
  - **電腦策略**：電腦會根據當前棋局狀態，選擇翻棋、移動或吃子等操作。

## 🚀 未來改進
- **提升電腦算法**：引入更複雜的算法，提高電腦對手的競爭力。
- **圖形化介面**：在 Telegram 中展示更直觀的棋盤和棋子圖像。
