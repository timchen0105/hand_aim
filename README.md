# 手勢操控準星 hand_aim
hand aim for Aim Lab, just for fun :)<br>
本專案透過Python的opencv-python和mediapipe套件實現手勢辨識，然後再透過pyserial將食指座標傳輸給arduino，最後再透過arduino的Mouse.h函式庫移動滑鼠游標。<br>
arduino板選用leonardo是因為uno板操控游標要更新軔體比較麻煩，而且操控游標的時候無法接收序列埠傳輸的資訊。<br>
此外，因為想不出開槍的手勢，所以isFire只會一直是0，可以更改Aim Lab的射擊按鈕來開槍，未來想到手勢會在更新。<br>
