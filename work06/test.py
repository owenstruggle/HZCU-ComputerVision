import joblib
import pandas as pd
from sklearn.metrics import precision_score, accuracy_score, recall_score, f1_score
from sklearn.model_selection import train_test_split


def set_data(benign_path, malignant_path):
    verify_benign = pd.read_csv(benign_path).iloc[:, 1:]
    verify_malignant = pd.read_csv(malignant_path).iloc[:, 1:]

    # 合并
    verify = pd.concat([verify_benign, verify_malignant])

    # shuffle
    verify = verify.sample(frac=1.0).reset_index(drop=True)
    return verify.iloc[:, :92].to_numpy(), verify.iloc[:, 92:].to_numpy()


if __name__ == '__main__':
    x_verify, y_verify = set_data("dataset/x_low_test_set_benign.csv", "dataset/x_low_test_set_malignant.csv")

    # 加载模型
    rf = joblib.load('result/rf_clf.model')
    predict = rf.predict(x_verify)
    print('验证集上 accuracy', accuracy_score(predict, y_verify))  # 0.8
    print('验证集上 precision', precision_score(predict, y_verify))  # 0.62
    print('验证集上 recall', recall_score(predict, y_verify))  # 0.96875
    print('验证集上 F1 score', f1_score(predict, y_verify))  # 0.7560975609756097
    pass
