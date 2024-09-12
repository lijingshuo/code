import pingouin as pg
import pandas as pd
from pandas.api.types import is_numeric_dtype
import numpy as np
import os
import re
import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QThread
from PyQt5.uic import loadUi
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class CommonHelper:
    def __init__(self):
        pass

    @staticmethod
    def readQss(style):
        with open(style, 'r') as f:
            return f.read()

class MainApp(QMainWindow):
    def __init__(self):  # 构造方法
        super().__init__()  # 运行父类的构造方法
        self.setupUi()  # 传递自己
        self.pushButton.clicked.connect(self.openfile1)  # 打开csv文件
        self.pushButton_2.clicked.connect(self.openfile2)
        self.pushButton_3.clicked.connect(self.culture)
        self.pushButton_4.clicked.connect(self.savecsv)
    def setupUi(self):
        loadUi('./ICC.ui', self)

    def printf(self, mes):  # 日志输出
        self.textBrowser.append(mes)  # 在指定的区域显示提示信息
        QtWidgets.QApplication.processEvents()

    def openfile1(self):
        global input_table1
        ###获取路径===================================================================
        openfile_name1 = QFileDialog.getOpenFileName(self, '选择文件', '', 'csv files(*.csv)')
        ###获取路径====================================================================
        if str(openfile_name1[0]) != '':
            path_openfile_name1 = openfile_name1[0]
            self.lineEdit.setText(openfile_name1[0])
            input_table1 = pd.read_csv(path_openfile_name1)
            self.printf(str(input_table1.shape))
            self.printf('载入数据完成1')
        else:
            return

    def openfile2(self):
        global input_table2
        ###获取路径===================================================================
        openfile_name2 = QFileDialog.getOpenFileName(self, '选择文件', '', 'csv files(*.csv)')
        ###获取路径====================================================================
        if not openfile_name2[0] is None:
            path_openfile_name2 = openfile_name2[0]
            self.lineEdit_2.setText(openfile_name2[0])
            input_table2 = pd.read_csv(path_openfile_name2)
            self.printf(str(input_table2.shape))
            self.printf('载入数据完成2')
        else:
            return

    def culture(self):
        input1 = input_table1
        input2 = input_table2
        global icc1, icc2, icc3, icc1k, icc2k, icc3k
        icc1 = icc2 = icc3 = icc1k = icc2k = icc3k = []
        icc_check = False
        try:
            if self.checkBox.isChecked():
                input1 = input1.drop(input1.columns[0], axis=1)
                input2 = input2.drop(input2.columns[0], axis=1)
            input1.insert(0, "reader", np.ones(input1.shape[0]))
            input2.insert(0, "reader", np.ones(input2.shape[0]) * 2)
            input1.insert(0, "target", range(input1.shape[0]))
            input2.insert(0, "target", range(input2.shape[0]))
            data = pd.concat([input1, input2])  # make a data frame like the test data
            self.printf('整理后的数据：' + str(data.shape))
            data_header = data.columns.values.tolist()
            self.progressBar.setMaximum(len(data_header)-2)  # 设置进度条的最大值
            for i in range(len(data_header)-2):
                items = ['target','reader']
                feature_name = data_header[i+2]
                self.printf(feature_name)
                items.append(feature_name)
                feature = data[items]
                icc_temp = pg.intraclass_corr(data=feature, targets='target', raters='reader', ratings=feature_name)
                icc_temp =pd.DataFrame(icc_temp)
                if icc_check == False:
                    icc1 = icc_temp.loc[0]
                    icc1 = pd.DataFrame(icc1).T
                    self.printf(str(icc1))
                    temp_ci =str(icc1['CI95%']).split("[")[1]
                    temp_ci_start = temp_ci.split(",")[0].strip()
                    temp_ci_end =temp_ci.split(",")[1].split("]")[0].strip()
                    icc1['CI95%_Start'] = temp_ci_start
                    icc1['CI95%_End'] = temp_ci_end
                    icc1.insert(loc=0, column='Feature', value=feature_name)
                    icc2 = icc_temp.loc[1]
                    icc2 = pd.DataFrame(icc2).T
                    temp_ci =str(icc2['CI95%']).split("[")[1]
                    temp_ci_start = temp_ci.split(",")[0].strip()
                    temp_ci_end =temp_ci.split(",")[1].split("]")[0].strip()
                    icc2['CI95%_Start'] = temp_ci_start
                    icc2['CI95%_End'] = temp_ci_end
                    icc2.insert(loc=0, column='Feature', value=feature_name)
                    icc3 = icc_temp.loc[2]
                    icc3 = pd.DataFrame(icc3).T
                    temp_ci =str(icc3['CI95%']).split("[")[1]
                    temp_ci_start = temp_ci.split(",")[0].strip()
                    temp_ci_end =temp_ci.split(",")[1].split("]")[0].strip()
                    icc3['CI95%_Start'] = temp_ci_start
                    icc3['CI95%_End'] = temp_ci_end
                    icc3.insert(loc=0, column='Feature', value=feature_name)
                    icc1k = icc_temp.loc[3]
                    icc1k = pd.DataFrame(icc1k).T
                    temp_ci =str(icc1k['CI95%']).split("[")[1]
                    temp_ci_start = temp_ci.split(",")[0].strip()
                    temp_ci_end =temp_ci.split(",")[1].split("]")[0].strip()
                    icc1k['CI95%_Start'] = temp_ci_start
                    icc1k['CI95%_End'] = temp_ci_end
                    icc1k.insert(loc=0, column='Feature', value=feature_name)
                    icc2k  = icc_temp.loc[4]
                    icc2k = pd.DataFrame(icc2k).T
                    temp_ci =str(icc2k['CI95%']).split("[")[1]
                    temp_ci_start = temp_ci.split(",")[0].strip()
                    temp_ci_end =temp_ci.split(",")[1].split("]")[0].strip()
                    icc2k['CI95%_Start'] = temp_ci_start
                    icc2k['CI95%_End'] = temp_ci_end
                    icc2k.insert(loc=0, column='Feature', value=feature_name)
                    icc3k = icc_temp.loc[5]
                    icc3k = pd.DataFrame(icc3k).T
                    temp_ci =str(icc3k['CI95%']).split("[")[1]
                    temp_ci_start = temp_ci.split(",")[0].strip()
                    temp_ci_end =temp_ci.split(",")[1].split("]")[0].strip()
                    icc3k['CI95%_Start'] = temp_ci_start
                    icc3k['CI95%_End'] = temp_ci_end
                    icc3k.insert(loc=0, column='Feature', value=feature_name)
                    icc_check = True
                else:
                    icc_ = icc_temp.loc[0]
                    icc_ = pd.DataFrame(icc_).T
                    temp_ci =str(icc_['CI95%']).split("[")[1]
                    temp_ci_start = temp_ci.split(",")[0].strip()
                    temp_ci_end =temp_ci.split(",")[1].split("]")[0].strip()
                    icc_['CI95%_Start'] = temp_ci_start
                    icc_['CI95%_End'] = temp_ci_end
                    icc_.insert(loc=0, column='Feature', value=feature_name)
                    icc1 = pd.concat([icc1,icc_],axis=0).reset_index(drop = True)
                    icc_ = icc_temp.loc[1]
                    icc_ = pd.DataFrame(icc_).T
                    temp_ci =str(icc_['CI95%']).split("[")[1]
                    temp_ci_start = temp_ci.split(",")[0].strip()
                    temp_ci_end =temp_ci.split(",")[1].split("]")[0].strip()
                    icc_['CI95%_Start'] = temp_ci_start
                    icc_['CI95%_End'] = temp_ci_end
                    icc_.insert(loc=0, column='Feature', value=feature_name)
                    icc2 = pd.concat([icc2,icc_],axis=0).reset_index(drop = True)
                    icc_ = icc_temp.loc[2]
                    icc_ = pd.DataFrame(icc_).T
                    temp_ci =str(icc_['CI95%']).split("[")[1]
                    temp_ci_start = temp_ci.split(",")[0].strip()
                    temp_ci_end =temp_ci.split(",")[1].split("]")[0].strip()
                    icc_['CI95%_Start'] = temp_ci_start
                    icc_['CI95%_End'] = temp_ci_end
                    icc_.insert(loc=0, column='Feature', value=feature_name)
                    icc3 = pd.concat([icc3,icc_],axis=0).reset_index(drop = True)
                    icc_ = icc_temp.loc[3]
                    icc_ = pd.DataFrame(icc_).T
                    temp_ci =str(icc_['CI95%']).split("[")[1]
                    temp_ci_start = temp_ci.split(",")[0].strip()
                    temp_ci_end =temp_ci.split(",")[1].split("]")[0].strip()
                    icc_['CI95%_Start'] = temp_ci_start
                    icc_['CI95%_End'] = temp_ci_end
                    icc_.insert(loc=0, column='Feature', value=feature_name)
                    icc1k = pd.concat([icc1k,icc_],axis=0).reset_index(drop = True)
                    icc_  = icc_temp.loc[4]
                    icc_ = pd.DataFrame(icc_).T
                    temp_ci =str(icc_['CI95%']).split("[")[1]
                    temp_ci_start = temp_ci.split(",")[0].strip()
                    temp_ci_end =temp_ci.split(",")[1].split("]")[0].strip()
                    icc_['CI95%_Start'] = temp_ci_start
                    icc_['CI95%_End'] = temp_ci_end
                    icc_.insert(loc=0, column='Feature', value=feature_name)
                    icc2k = pd.concat([icc2k,icc_],axis=0).reset_index(drop = True)
                    icc_ = icc_temp.loc[5]
                    icc_ = pd.DataFrame(icc_).T
                    temp_ci =str(icc_['CI95%']).split("[")[1]
                    temp_ci_start = temp_ci.split(",")[0].strip()
                    temp_ci_end =temp_ci.split(",")[1].split("]")[0].strip()
                    icc_['CI95%_Start'] = temp_ci_start
                    icc_['CI95%_End'] = temp_ci_end
                    icc_.insert(loc=0, column='Feature', value=feature_name)
                    icc3k = pd.concat([icc3k,icc_],axis=0).reset_index(drop = True)
                self.printf(str(icc_temp))
                self.progressBar.setValue(i + 1)
            QMessageBox.information(self, "提示", "ICC分析完成")  # 调用弹窗提示
            self.printf('ICC分析完成')
            self.printf(str(icc1))
            self.progressBar.setValue(0)
            icc_check = False
        except Exception as e:
            self.printf(str(e))
            icc_check = False
            pass

    def savecsv(self):
        global icc1, icc2, icc3, icc1k, icc2k, icc3k
        ic = False
        try:
            if self.checkBox_2.isChecked():
                icc_1 = icc_2 = icc_3 = icc_1k = icc_2k = icc_3k = []
                self.progressBar.setMaximum(icc1.shape[0]+icc2.shape[0]+icc3.shape[0]+icc1k.shape[0]+icc2k.shape[0]+icc3k.shape[0]-1)  # 设置进度条的最大值
                j=0
                for i in range(icc1.shape[0]):
                    j=i
                    icc_temp = pd.DataFrame(icc1.loc[i]).T.reset_index()
                    if ic == False:
                        if is_numeric_dtype(icc_temp.iloc[0].at['ICC']) and pd.isna(icc_temp.iloc[0].at['ICC'])==False:
                            icc_1 = icc_temp
                            self.progressBar.setValue(j+1)
                            ic = True
                    else:
                        if is_numeric_dtype(icc_temp.iloc[0].at['ICC']) and pd.isna(icc_temp.iloc[0].at['ICC'])==False:
                            icc_1 = pd.concat([icc_1, icc_temp], axis=0)
                            self.progressBar.setValue(j+1)
                j_ =j
                ic = False
                for i in range(icc2.shape[0]):
                    icc_temp = pd.DataFrame(icc2.loc[i]).T.reset_index()
                    j=j_+i
                    if ic == False:
                        if is_numeric_dtype(icc_temp.iloc[0].at['ICC']) and pd.isna(icc_temp.iloc[0].at['ICC'])==False:
                            icc_2 = icc_temp
                            self.progressBar.setValue(j+1)
                            ic = True
                    else:
                        if is_numeric_dtype(icc_temp.iloc[0].at['ICC']) and pd.isna(icc_temp.iloc[0].at['ICC'])==False:
                            icc_2 = pd.concat([icc_2, icc_temp], axis=0)
                            self.progressBar.setValue(j+1)
                j_ = j
                ic = False
                for i in range(icc3.shape[0]):
                    j = j_+i
                    icc_temp = pd.DataFrame(icc3.loc[i]).T.reset_index()
                    if ic == False:
                        if is_numeric_dtype(icc_temp.iloc[0].at['ICC']) and pd.isna(icc_temp.iloc[0].at['ICC'])==False:
                            icc_3 = icc_temp
                            self.progressBar.setValue(j+1)
                            ic = True
                    else:
                        if is_numeric_dtype(icc_temp.iloc[0].at['ICC']) and pd.isna(icc_temp.iloc[0].at['ICC'])==False:
                            icc_3 = pd.concat([icc_3, icc_temp], axis=0)
                            self.progressBar.setValue(j+1)
                j_ = j
                ic = False
                for i in range(icc1k.shape[0]):
                    icc_temp = pd.DataFrame(icc1k.loc[i]).T.reset_index()
                    j=j_+i
                    if ic == False:
                        if is_numeric_dtype(icc_temp.iloc[0].at['ICC']) and pd.isna(icc_temp.iloc[0].at['ICC'])==False:
                            icc_1k = icc_temp
                            self.progressBar.setValue(j+1)
                            ic = True
                    else:
                        if is_numeric_dtype(icc_temp.iloc[0].at['ICC']) and pd.isna(icc_temp.iloc[0].at['ICC'])==False:
                            icc_1k = pd.concat([icc_1k, icc_temp], axis=0)
                            self.progressBar.setValue(j+1)
                j_ = j
                ic = False
                for i in range(icc2k.shape[0]):
                    icc_temp = pd.DataFrame(icc2k.loc[i]).T.reset_index()
                    j = j_+i
                    if ic == False:
                        if is_numeric_dtype(icc_temp.iloc[0].at['ICC']) and pd.isna(icc_temp.iloc[0].at['ICC'])==False:
                            icc_2k = icc_temp
                            self.progressBar.setValue(j+1)
                            ic = True
                    else:
                        if is_numeric_dtype(icc_temp.iloc[0].at['ICC']) and pd.isna(icc_temp.iloc[0].at['ICC'])==False:
                            icc_2k = pd.concat([icc_2k, icc_temp], axis=0)
                            self.progressBar.setValue(j+1)
                j_ = j
                ic = False
                for i in range(icc3k.shape[0]):
                    icc_temp = pd.DataFrame(icc3k.loc[i]).T.reset_index()
                    j = j_+i
                    if ic == False:
                        if is_numeric_dtype(icc_temp.iloc[0].at['ICC']) and pd.isna(icc_temp.iloc[0].at['ICC'])==False:
                            icc_3k = icc_temp
                            self.progressBar.setValue(j+1)
                            ic = True
                    else:
                        if is_numeric_dtype(icc_temp.iloc[0].at['ICC']) and pd.isna(icc_temp.iloc[0].at['ICC'])==False:
                            icc_3k = pd.concat([icc_3k, icc_temp], axis=0)
                            self.progressBar.setValue(j+1)
                ic = False
                dir_choose = QFileDialog.getExistingDirectory(self, "选取文件夹")  # 起始路径
                icc_1.to_csv(dir_choose+'/icc1_d.csv')  # 保存
                icc_2.to_csv(dir_choose+'/icc2_d.csv')  # 保存
                icc_3.to_csv(dir_choose+'/icc3_d.csv')  # 保存
                icc_1k.to_csv(dir_choose+'/icc1k_d.csv')  # 保存
                icc_2k.to_csv(dir_choose+'/icc2k_d.csv')  # 保存
                icc_3k.to_csv(dir_choose+'/icc3k_d.csv')  # 保存
                QMessageBox.information(self, "提示", "保存成功。")  # 调用弹窗提示
                self.progressBar.setValue(0)
            else:
                dir_choose = QFileDialog.getExistingDirectory(self, "选取文件夹")  # 起始路径
                icc1.to_csv(dir_choose+'/icc1.csv')  # 保存
                icc2.to_csv(dir_choose+'/icc2.csv')  # 保存
                icc3.to_csv(dir_choose+'/icc3.csv')  # 保存
                icc1k.to_csv(dir_choose+'/icc1k.csv')  # 保存
                icc2k.to_csv(dir_choose+'/icc2k.csv')  # 保存
                icc3k.to_csv(dir_choose+'/icc3k.csv')  # 保存
                QMessageBox.information(self, "提示", "保存成功。")  # 调用弹窗提示
        except Exception as e:
            self.printf(str(e))
            pass

if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)  # 高清显示
    app = QApplication(sys.argv)  # 创建GUI
    ui = MainApp()  # 创建PyQt设计的窗体对象
    # qssStyle = CommonHelper.readQss('./style.qss')
    # ui.setStyleSheet(qssStyle)
    ui.show()  # 显示窗体
    sys.exit(app.exec_())  # 程序关闭时退出进程
