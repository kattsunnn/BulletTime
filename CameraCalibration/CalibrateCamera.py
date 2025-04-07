import cv2
import numpy as np
import glob

# チェスボードの交点数（内側の交点）
chessboard_size = (10, 7)  # 例: 9x6の交点
square_size = 50.0  # 1マスのサイズ（mm単位）

# 3Dオブジェクトポイント（チェスボード平面上の実座標）
objp = np.zeros((chessboard_size[0]*chessboard_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)
objp *= square_size

objpoints = []  # 3Dポイント
imgpoints = []  # 2Dポイント（画像平面上）

# チェスボード画像のパス（例：calibフォルダの中）
images = glob.glob('calib/*.jpg')

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # チェスボードのコーナー検出
    ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)

    if ret:
        objpoints.append(objp)
        # コーナーをサブピクセル精度で補正
        corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1),
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001))
        imgpoints.append(corners2)

        # 検出確認
        cv2.drawChessboardCorners(img, chessboard_size, corners2, ret)
        cv2.imshow('Corners', img)
        cv2.waitKey(100)

cv2.destroyAllWindows()

# カメラキャリブレーション実行
ret, cameraMatrix, distCoeffs, rvecs, tvecs = cv2.calibrateCamera(
    objpoints, imgpoints, gray.shape[::-1], None, None)

# 結果の表示
print("\n== カメラ内部パラメータ ==")
print("カメラ行列（cameraMatrix）:")
print(cameraMatrix)

print("\n== 歪み係数（distCoeffs） ==")
print(distCoeffs.ravel())

print("\n== RMS再投影誤差 ==")
print("RMS Error:", ret)

# 結果を保存
np.savez("calibration_result.npz",
         cameraMatrix=cameraMatrix,
         distCoeffs=distCoeffs,
         rvecs=rvecs,
         tvecs=tvecs)