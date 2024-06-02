import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.linear_model import RANSACRegressor, LinearRegression
from sklearn.preprocessing import StandardScaler
from scipy.spatial import Delaunay

import pickle

# 예제 데이터 생성 (실제 데이터로 대체하세요)
points = pickle.load(open('fault.pkl', 'rb'))


# 스케일링
scaler = StandardScaler()
points_scaled = scaler.fit_transform(points)


# 평면 찾기 함수 정의
def find_planes(points_scaled, num_planes=5, residual_threshold=0.05, max_trials=1000,
                                      min_slope=1.0):
    planes = []
    remaining_points = points_scaled.copy()

    for _ in range(num_planes):
        if len(remaining_points) < 3:
            break

        # RANSAC을 사용하여 평면 피팅
        ransac = RANSACRegressor(LinearRegression(), residual_threshold=residual_threshold, max_trials=max_trials)
        X = remaining_points[:, :2]  # x, y 좌표
        y = remaining_points[:, 2]  # z 좌표
        ransac.fit(X, y)

        # 내부점과 외부점 식별
        inlier_mask = ransac.inlier_mask_
        outlier_mask = np.logical_not(inlier_mask)

        # 평면의 계수 추출
        a, b = ransac.estimator_.coef_
        c = ransac.estimator_.intercept_

        # 특정 경사 조건 체크
        slope = np.sqrt(a ** 2 + b ** 2)
        if slope >= min_slope:
            planes.append((a, b, c, remaining_points[inlier_mask]))

        # 남은 점들로 갱신
        remaining_points = remaining_points[outlier_mask]

    return planes


# 평면 찾기 실행
planes = find_planes(points_scaled, num_planes=5, residual_threshold=0.1, max_trials=1000, min_slope=1.7)

# 시각화
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 모든 점 시각화
ax.scatter(points[:, 0], points[:, 1], points[:, 2], c='gray', marker='o', alpha=0.1, s=1)

# 각 평면의 점들을 시각화
colors = plt.cm.Spectral(np.linspace(0, 1, len(planes)))
print(len(planes))
for i, (a, b, c, plane_points) in enumerate(planes):
    # 원래 스케일로 되돌리기
    plane_points_original = scaler.inverse_transform(plane_points)
    ax.scatter(plane_points_original[:, 0], plane_points_original[:, 1], plane_points_original[:, 2], c=[colors[i]],
               marker='o', alpha=0.6, s=1)
    if len(plane_points_original) > 3:  # 최소 3개의 점이 있어야 삼각형 서피스를 만들 수 있음
            hull = Delaunay(plane_points_original[:, :2])
            ax.plot_trisurf(plane_points_original[:, 0], plane_points_original[:, 1], plane_points_original[:, 2], triangles=hull.simplices, color=colors[i], alpha=0.5)



ax.set_xlabel('X Axis')
ax.set_ylabel('Y Axis')
ax.set_zlabel('Z Axis')
plt.show()

pickle.dump(planes, open('faultplanes_iter.pkl', 'wb'))
