# Time Series Segmentation Benchmark

This repository contains notebook for conducting 10 experiments with diffrent datasets to compare performance of 4 algorithms: window, binary segmentation, bottomup and fluss.

The first 3 algorithms are supported with the number of change points to detect and cost function is seletcted to maximize results

Benchmark uses simple rank system based on F1 score (accuracy is useless metric here bcs of huge number of TN in this evalution method)
[All datasets come from here](https://www.timeseriesclassification.com/)

# Summary

Fluss is very efficient algorithm, however it assumes that the regime(segment) contains at least few pattern (patterns are of window size length), if the segemnts cotains less than 6\7 patterns it fails to properly segment time series due to using cac curve. Also its slower than classic change points detection algorithms due to complexity of calculating matrix profile but it can be easily fixed by simply chunking the data.

Classic change point algorithms are generally faster (cost function can increase its exectuion time), and they can be useful in certain data tyes: for example where there is no visible pattern or the segments contains very few of them. Altough when it comes to accuracy fluss seems to be way better, it outperformed these algorithms knowing only window_size. Propably using custom combined functions may enhance classic algorithms.
