import joblib
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import plot_roc_curve
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier


def set_data(benign_path, malignant_path):
    train_benign = pd.read_csv(benign_path)  # (1177, 94)
    train_malignant = pd.read_csv(malignant_path)  # (409, 94)

    # 去除 name 列
    train_benign = train_benign.iloc[:, 1:]
    train_malignant = train_malignant.iloc[:, 1:]

    # 合并
    train = pd.concat([train_benign, train_malignant])

    # 分割 dataset
    return train_test_split(train.iloc[:, :92].to_numpy(), train.iloc[:, 92:].to_numpy(), test_size=0.4,
                            random_state=2021)


if __name__ == '__main__':
    x_train, x_test, y_train, y_test = set_data("dataset/x_low_train_set_benign.csv",
                                                "dataset/x_low_train_set_malignant.csv")
    y_test = y_test.reshape(-1)
    y_train = y_train.reshape(-1)

    # 创建模型
    lr_clf = LogisticRegression(solver='saga', max_iter=10000)
    dt_clf = DecisionTreeClassifier()
    knn_clf = KNeighborsClassifier()
    rf_clf = RandomForestClassifier()

    # 训练模型
    lr_clf.fit(x_train, y_train)
    dt_clf.fit(x_train, y_train)
    knn_clf.fit(x_train, y_train)
    rf_clf.fit(x_train, y_train)

    # 保存模型
    joblib.dump(lr_clf, 'result/lr_clf.model')
    joblib.dump(dt_clf, 'result/dt_clf.model')
    joblib.dump(knn_clf, 'result/knn_clf.model')
    joblib.dump(rf_clf, 'result/rf_clf.model')

    # 创建画布
    fig, ax = plt.subplots(figsize=(12, 10))
    lr_roc = plot_roc_curve(estimator=lr_clf, X=x_test, y=y_test, ax=ax, linewidth=1)
    dt_roc = plot_roc_curve(estimator=dt_clf, X=x_test, y=y_test, ax=ax, linewidth=1)
    knn_roc = plot_roc_curve(estimator=knn_clf, X=x_test, y=y_test, ax=ax, linewidth=1)
    rf_roc = plot_roc_curve(estimator=rf_clf, X=x_test, y=y_test, ax=ax, linewidth=1)
    ax.legend(fontsize=12)  # 更改图例字体大小
    plt.savefig('result/roc.png')  # 保存图像
    plt.show()  # 显示绘制的ROC曲线
