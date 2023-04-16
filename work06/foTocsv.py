from __future__ import print_function
import six
import os  # needed navigate the system to get the input data
import numpy as np
import radiomics
import glob
import pandas as pd
import SimpleITK as sitk
from radiomics import featureextractor  # This module is used for interaction with pyradiomics
import argparse


def catch_features(imagePath, maskPath):
    if imagePath is None or maskPath is None:  # Something went wrong, in this case PyRadiomics will also log an error
        raise Exception(
            'Error getting testcase!')  # Raise exception to prevent cells below from running in case of "run all"
    settings = {}
    settings['binWidth'] = 25  # 5
    settings['sigma'] = [3, 5]
    settings['Interpolator'] = sitk.sitkBSpline
    settings['resampledPixelSpacing'] = [1, 1, 1]  # 3,3,3
    settings['voxelArrayShift'] = 1000  # 300
    settings['normalize'] = True
    settings['normalizeScale'] = 100
    extractor = featureextractor.RadiomicsFeatureExtractor(**settings)
    # extractor = featureextractor.RadiomicsFeatureExtractor()
    # print('Extraction parameters:\n\t', extractor.settings)

    extractor.enableImageTypeByName('LoG')
    extractor.enableImageTypeByName('Wavelet')
    extractor.enableAllFeatures()
    extractor.enableFeaturesByName(
        firstorder=['Energy', 'TotalEnergy', 'Entropy', 'Minimum', '10Percentile', '90Percentile', 'Maximum', 'Mean',
                    'Median', 'InterquartileRange', 'Range', 'MeanAbsoluteDeviation', 'RobustMeanAbsoluteDeviation',
                    'RootMeanSquared', 'StandardDeviation', 'Skewness', 'Kurtosis', 'Variance', 'Uniformity'])
    extractor.enableFeaturesByName(
        shape=['VoxelVolume', 'MeshVolume', 'SurfaceArea', 'SurfaceVolumeRatio', 'Compactness1', 'Compactness2',
               'Sphericity', 'SphericalDisproportion', 'Maximum3DDiameter', 'Maximum2DDiameterSlice',
               'Maximum2DDiameterColumn', 'Maximum2DDiameterRow', 'MajorAxisLength', 'MinorAxisLength',
               'LeastAxisLength', 'Elongation', 'Flatness'])
    # 上边两句我将一阶特征和形状特征中的默认禁用的特征都手动启用，为了之后特征筛选
    # print('Enabled filters:\n\t', extractor.enabledImagetypes)
    feature_cur = []
    feature_name = []
    result = extractor.execute(imagePath, maskPath)
    for key, value in six.iteritems(result):
        # print('\t', key, ':', value)
        feature_name.append(key)
        feature_cur.append(value)
    # print(len(feature_cur[37:]))
    name = feature_name[37:]
    name = np.array(name)
    '''
    flag=1
    if flag:
        name = np.array(feature_name)
        name_df = pd.DataFrame(name)
        writer = pd.ExcelWriter('key.xlsx')
        name_df.to_excel(writer)
        writer.save()
        flag = 0
    '''
    for i in range(len(feature_cur[37:])):
        # if type(feature_cur[i+22]) != type(feature_cur[30]):
        feature_cur[i + 37] = float(feature_cur[i + 37])
    return feature_cur[37:], name


basePath = "F:\\nodule_malignancy_db\\train_set\\malignant\\"  # 文件夹路径
file = glob.glob(os.path.join(basePath, '*raw.npy'))

features = np.empty(shape=[0, 1051])
lname = []
features_list = []

for raw in file:
    mask = raw.replace('raw', 'mask')
    raw_np = np.load(raw)
    mask_np = np.load(mask)
    raw_itk = sitk.GetImageFromArray(raw_np)
    mask_itk = sitk.GetImageFromArray(mask_np)
    save_curdata, name = catch_features(raw_itk, mask_itk)
    lname = name
    features_list.append(save_curdata)

features_array = np.array(features_list)
df = pd.DataFrame(features_array, columns=name)
df['malignant'] = 1  # 是否为恶性肿瘤 1为恶性 0为良性

# 保存为csv文件
df.to_csv('train_set_malignant.csv', index=False)
