import fetch from '@/config/fetch'

/** 灰度反转 **/
export const grayscaleReversal = data => fetch('/grayscaleReversal', data, 'POST');
/** 直方图 **/
export const histogram = data => fetch('/histogram', data, 'POST');
/** 直方图均衡化 **/
export const histogramEqualization = data => fetch('/histogramEqualization', data, 'POST');
/** 分段线性变换 **/
export const segmentedLinearTransformation = data => fetch('/segmentedLinearTransformation', data, 'POST');
/** 对数变换 **/
export const logarithmicTransformation = data => fetch('/logarithmicTransformation', data, 'POST');
/** 伽马变换 **/
export const gammaTransformation = data => fetch('/gammaTransformation', data, 'POST');
