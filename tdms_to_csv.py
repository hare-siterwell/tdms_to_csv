import os
import sys
import numpy as np
import pandas as pd
from nptdms import TdmsFile


# 在TDMS文件所在目录生成对应文件夹和CSV文件
def convert_tdms(file):
    if os.path.splitext(file)[-1] == '.tdms':
        with TdmsFile.open(file) as tdms_file:
            # 访问所有组
            for group in tdms_file.groups():
                df = pd.DataFrame()
                # 访问所有通道
                for channel in group.channels():
                    # 获取所有数据
                    num = np.array(tdms_file[group.name][channel.name][:])
                    df = pd.concat(
                        [df, pd.DataFrame(num, columns=[channel.name])],
                        axis=1)

                # 创建对应文件夹
                if not os.path.exists(os.path.splitext(file)[0]):
                    os.mkdir(os.path.splitext(file)[0])

                df[:][1:].to_csv(
                    os.path.splitext(file)[0] + '/' + group.name + '.csv')


# 遍历文件夹
def traversal_path(path):
    for item in os.scandir(path):
        if item.is_dir():
            traversal_path(item.path)
        elif item.is_file():
            convert_tdms(item.path)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        if os.path.isdir(sys.argv[1]):
            traversal_path(sys.argv[1])
        elif os.path.isfile(sys.argv[1]):
            convert_tdms(sys.argv[1])
