import os
import PySimpleGUI as sg
import numpy as np
import pandas as pd
# from radiomics import featureextractor as fee
import radiomics
import radiomics.featureextractor


def main():
    gui()


def gui():
    sg.theme('TanBlue')
    tab1_layout = [[sg.Text()],
                   [sg.Text('配置文件名：', font=('黑体', 10), key='yamlname')],
                   [sg.InputText(key='-IN1-', size=(60, 1), readonly=True),
                    sg.FileBrowse('配置文件载入', key='-FL3-', file_types=(("Yaml Files", "*.yaml"),))],
                   [sg.Text('', size=(30, 1))],
                   [sg.Text('', size=(30, 1))],
                   [sg.Text('', size=(30, 1)), sg.Button('开始提取', size=(10, 2), key='autostart')]]
    tab2_layout = [[sg.Frame('图像类型:', layout=[
        [sg.CBox('Orginal', tooltip='表示对原始图像操作', key='cb1', default=True),
         sg.CBox('Wavelet', tooltip='小波变换', key='cb2'),
         sg.CBox('LoG', tooltip='表示的是拉普拉斯变换,选择此项后要设置Log_sigma的值', key='cb3'),
         sg.CBox('Square', tooltip='表示对图像进行平方操作再提取特征', key='cb4'),
         sg.CBox('SquareRoot', tooltip='表示对图像进行平方根操作之后再提取特征', key='cb5'),
         sg.CBox('Logarithm', tooltip='表示对图像进行log变换后再提取特征', key='cb6'),
         sg.CBox('Exponetial', tooltip='表示对图像进行指数变换后再提取特征', key='cb7')],
        [sg.Text('LoG_sigma:'),
         sg.InputText('Default', size=(20, 1),
                      tooltip='输入格式为1.0,2.0......数值需大于0，其中,为英文的逗号，如果值超过5.0要修改padDistance的大小',
                      key='-IN9-'),
         sg.Text('padDistance:', tooltip='设置在裁剪肿瘤体时的体素补充数量'),
         sg.Spin([i for i in range(0, 60)], size=(5, 1), initial_value=5, key='spin3')],
        [sg.Text('wavelet基函数类型:'), sg.OptionMenu((
            'Default', '1.1', '1.3', '1.5', '2.2', '2.4', '2.6', '2.8', '3.1',
            '3.3', '3.5', '3.7', '3.9', '4.4', '5.5', '6.8'),
            key='optionmenu3', default_value='Default')]])],
                   [sg.Frame('特征类型:', layout=[
                       [sg.CBox('firstorder', key='cb8', default=True),
                        sg.CBox('glcm', key='cb9', default=True),
                        sg.CBox('gldm', key='cb10', default=True),
                        sg.CBox('glrlm', key='cb11', default=True),
                        sg.CBox('glszm', key='cb12', default=True),
                        sg.CBox('ngtdm', key='cb13', default=True),
                        sg.CBox('shape2D+3D', key='cb14',
                                tooltip='提取2D和3D特征，当force2D为True时，此项不选，否则无法提取，', default=True)],
                       [sg.CBox('将一阶特征和形状特征中默认禁用的特征开启', key='cb19', default=False)]])],
                   [sg.Frame('设置:', layout=[
                       [sg.Text('Image_discretization  '), sg.Text('binWidth:', tooltip='灰度直方图的宽度'),
                        sg.Slider(range=(1, 100), orientation='h', size=(34, 20), key='slide1', default_value=25)],
                       [sg.Text('Force_2D_extraction  '), sg.Text('force2D:', tooltip='强制按2D层面提取特征'),
                        sg.OptionMenu(('False', 'True'), key='optionforce2D', default_value='False'),
                        sg.Text('force2Ddimension:',
                                tooltip='按2D哪个方向的层面提取特征，1代表横断图像的冠状位图像，2代表横断图像的矢状位图像'),
                        sg.OptionMenu(('0', '1', '2'), key='optionforce2Ddimension', default_value='0')],
                       [sg.Text('Texture_matrix_weighting  '),
                        sg.CBox('weightingNorm:', tooltip='特征纹理权重', key='cb19'),
                        sg.OptionMenu(('no_weighting', 'manhattan', 'euclidean', 'infinity'),
                                      key='optionweightingnorm', default_value='no_weighting')],
                       [sg.Text('Distance_to_neighbour  '), sg.Text('distances:', ),
                        sg.Spin([i for i in range(0, 60)], size=(5, 1), initial_value=1, key='spin2')],
                       [sg.Text('label:', tooltip='图像标注的标签值'),
                        sg.Spin([i for i in range(0, 60)], size=(5, 1), initial_value=1, key='spin1'),
                        sg.Text('[0-60]')],
                       [sg.Text('interpolator:', tooltip='None是不采用插值'), sg.OptionMenu(('None',
                                                                                             'sitkNearestNeighbor',
                                                                                             'sitkLinear',
                                                                                             'sitkBSpline',
                                                                                             'sitkGaussian',
                                                                                             'sitkLabelGaussian',
                                                                                             'sitkHammingWindwosedSinc',
                                                                                             'sitkCosineWindowedSinc',
                                                                                             'sitkWelchWindowedSinc',
                                                                                             'sitkLanczosWindowedSinc',
                                                                                             'sitkBlackmanWindowedSinc'),
                                                                                            key='optioninterpolator',
                                                                                            default_value='sitkBSpline')],
                       [sg.CBox('重采样', key='cb16'), sg.Text('resamplePixelSpacing:[X'),
                        sg.InputText(key='x', size=(5, 1)), sg.Text('Y'), sg.InputText(key='y', size=(5, 1)),
                        sg.Text('Z'), sg.InputText(key='z', size=(5, 1)), sg.Text(']'), ],
                       [sg.Text('normalize:',
                                tooltip='是否归一化，慎用，对一个序列的部分数据采用可能导致与整体数据得出的结果不同'),
                        sg.OptionMenu(('False', 'True'), key='optionnormalize', default_value='False'),
                        sg.Text('normalizeScale:'),
                        sg.Spin([i for i in range(0, 60)], size=(5, 1), initial_value=1, key='spin3')],
                       [sg.CBox('是否去掉提取特征中的无关信息，比如库的版本等', key='cb17', default=False)]])],
                   [sg.Text('', size=(30, 1)), sg.Button('开始提取', size=(10, 2), key='manualstart')]]
    left = [[sg.Frame('文件载入', layout=[[sg.Radio('文件', "filefolder", key='rad1', default=True)],
                                          [sg.Text('图像文件：'), sg.InputText(key='-IN3-', readonly=True),
                                           sg.FileBrowse(key='-FL1-',
                                                         file_types=(("Image", "*.nrrd"), ("Image", "*.nii")))],
                                          [sg.Text('标注文件：'), sg.InputText(key='-IN4-', readonly=True),
                                           sg.FileBrowse(key='-FL2-',
                                                         file_types=(("Image", "*.nrrd"), ("Image", "*.nii")))],
                                          [sg.Radio('文件夹', "filefolder", key='rad2')],
                                          [sg.Text('图像文件夹：'), sg.InputText(key='-IN5-', readonly=True),
                                           sg.FolderBrowse(key='-FD1-'), sg.Text('', size=(24, 1))],
                                          [sg.Text('标注文件夹：'), sg.InputText(key='-IN6-', readonly=True),
                                           sg.FolderBrowse(key='-FD2-')]])],
            [sg.Frame('特征文件存储', layout=[
                [sg.CBox('双盲', tooltip='采用双盲后，会在特征信息里添加一列存有文件名的单元', key='cb18'),
                 sg.Text('   特征名前加前缀:'), sg.InputText(key='-IN10-', size=(10, 1)), sg.Text('', size=(48, 1))],
                [sg.Text('特征文件命名：'), sg.InputText(key='-IN7-', size=(20, 1), default_text='Default'),
                 sg.Text('.CSV'), sg.Radio('输出按行排列', "filecsv", key='rad3', default=True),
                 sg.Radio('输出按列排列', "filecsv", key='rad4')],
                [sg.Text('文件保存在：'), sg.InputText(key='-IN8-', readonly=True), sg.FolderBrowse(key='-FD3-'),
                 sg.Text('', size=(24, 1))]])],
            [sg.TabGroup([[sg.Tab('自动参数配置', tab1_layout), sg.Tab('手动参数配置', tab2_layout)]])]]
    multil = sg.Multiline(size=(60, 1), font='Courier 8', expand_x=True, expand_y=True, write_only=True,
                          reroute_stdout=True, reroute_stderr=True, echo_stdout_stderr=True, autoscroll=True,
                          auto_refresh=True)
    layout = [[sg.Column(left), multil]]

    window = sg.Window('Uscube影像组学特征提取（基于Pyradiomics开源模块的插件）', layout, font=('宋体', 10),
                       default_element_size=(40, 1),
                       resizable=True, use_default_focus=False)


    # 获取配置文件的名称
    def getyamlname(listin1):
        if listin1 == '':
            return ''
        else:
            print(listin1)
            temp1 = listin1.rsplit('/', 1)
            print(temp1)
            temp1 = temp1[1].split('.', 1)[0]
            return temp1

    # 获取文件的名称
    def getfilename(listin2):
        if listin2 == '':
            return ''
        else:
            temp1 = listin2.rsplit('/', 1)
            temp1 = temp1[1].split('.', 1)[0]
            return temp1

    # 载入配置文件
    def getyaml(filepath):
        extractor = radiomics.featureextractor.RadiomicsFeatureExtractor(filepath)
        print(getyamlname(values['-IN1-']) + '配置参数：')
        print("Extraction parameters:\n\t", extractor.settings)
        print("Enabled filters:\n\t", extractor.enabledImagetypes)
        print("Enabled features:\n\t", extractor.enabledFeatures)
        return extractor

    # 根据配置文件自动提取特征
    def getfeature(extractor, imgname, maskname):
        texture = pd.DataFrame()
        try:
            featurevector = extractor.execute(imgname, maskname)
            texture = pd.DataFrame([featurevector])
            if values['-IN10-'] != '':
                for colname in list(texture):
                    texture.rename(columns={colname: values['-IN10-'] + colname}, inplace=True)
            if window['cb18'].get():
                texture.insert(0, 'filename', getfilename(imgname), allow_duplicates=False)
            print(texture)
            print('特征提取成功')
        except Exception:
            print('特征提取失败')
        return texture

    # 设置手动参数
    def manualconfig():
        # 设置settings
        settings = {'binWidth': values['slide1']}
        if values['optionforce2D'] == 'False':
            settings['force2D'] = False
        else:
            settings['force2D'] = True
        if settings['force2D']:
            settings['force2Ddimension'] = int(values['optionforce2Ddimension'])
        if window['cb19'].get():
            settings['weightingNorm'] = values['optionweightingnorm']
        settings['distances'] = [values['spin2']]
        if window['cb3'].get():
            if values['-IN9-'] != 'Default':
                my_list = values['-IN9-'].split(',')
                my_list = list(map(float, my_list))
                settings['sigma'] = my_list
            settings['padDistance'] = values['spin3']
        if window['cb2'].get() and values['optionmenu3'] != 'Default':
            settings['rbio'] = float(values['optionmenu3'])
        settings['label'] = values['spin1']
        settings['interpolator'] = values['optioninterpolator']
        if values['optionnormalize'] == 'False':
            settings['normalize'] = False
        else:
            settings['normalize'] = True
        if settings['normalize']:
            settings['normalizeScale'] = int(values['spin3'])
        if window['cb16'].get():
            if window['x'].get() == '' or window['y'].get() == '' or window['z'].get() == '':
                settings['resampledPixelSpacing'] = []
            else:
                settings['resampledPixelSpacing'] = [int(window['x'].get()), int(window['y'].get()),
                                                     int(window['z'].get())]
        extractor = radiomics.featureextractor.RadiomicsFeatureExtractor(**settings)

        # 设置extractor
        extractor.disableAllImageTypes()
        if values['cb1'] and values['cb2'] and values['cb3'] and values['cb4'] and values['cb5'] and values['cb6'] and \
                values['cb7']:
            extractor.enableAllImageTypes()
        else:
            if window['cb1'].get():
                extractor.enableImageTypeByName('Original')
            if window['cb2'].get():
                extractor.enableImageTypeByName('Wavelet')
            if window['cb3'].get():
                extractor.enableImageTypeByName('LoG')
            if window['cb4'].get():
                extractor.enableImageTypeByName('Square')
            if window['cb5'].get():
                extractor.enableImageTypeByName('SquareRoot')
            if window['cb6'].get():
                extractor.enableImageTypeByName('Logarithm')
            if window['cb7'].get():
                extractor.enableImageTypeByName('Exponetial')
        if window['cb8'].get() and window['cb9'].get() and window['cb10'].get() and window['cb11'].get() and window[
            'cb12'].get() and window['cb13'].get() and window['cb14'].get():
            extractor.enableAllFeatures()
            if window['cb8'].get() and window['cb19'].get():
                extractor.enableFeaturesByName(
                    firstorder=['Energy', 'TotalEnergy', 'Entropy', 'Minimum', '10Percentile', '90Percentile',
                                'Maximum', 'Mean', 'Median', 'InterquartileRange', 'Range', 'MeanAbsoluteDeviation',
                                'RobustMeanAbsoluteDeviation', 'RootMeanSquared', 'StandardDeviation', 'Skewness',
                                'Kurtosis', 'Variance', 'Uniformity'])
            if window['cb14'].get() and window['cb19'].get():
                extractor.enableFeaturesByName(
                    shape=['VoxelVolume', 'MeshVolume', 'SurfaceArea', 'SurfaceVolumeRatio', 'Compactness1',
                           'Compactness2', 'Sphericity', 'SphericalDisproportion', 'Maximum3DDiameter',
                           'Maximum2DDiameterSlice', 'Maximum2DDiameterColumn', 'Maximum2DDiameterRow',
                           'MajorAxisLength', 'MinorAxisLength', 'LeastAxisLength', 'Elongation', 'Flatness'])
        else:
            extractor.disableAllFeatures()
            if window['cb8'].get():
                extractor.enableFeatureClassByName('firstorder')
                if window['cb8'].get() and window['cb19'].get():
                    extractor.enableFeaturesByName(
                        firstorder=['Energy', 'TotalEnergy', 'Entropy', 'Minimum', '10Percentile', '90Percentile',
                                    'Maximum', 'Mean', 'Median', 'InterquartileRange', 'Range', 'MeanAbsoluteDeviation',
                                    'RobustMeanAbsoluteDeviation', 'RootMeanSquared', 'StandardDeviation', 'Skewness',
                                    'Kurtosis', 'Variance', 'Uniformity'])
            if window['cb9'].get():
                extractor.enableFeatureClassByName('glcm')
            if window['cb10'].get():
                extractor.enableFeatureClassByName('gldm')
            if window['cb11'].get():
                extractor.enableFeatureClassByName('glrlm')
            if window['cb12'].get():
                extractor.enableFeatureClassByName('glszm')
            if window['cb13'].get():
                extractor.enableFeatureClassByName('ngtdm')
            if window['cb14'].get():
                extractor.enableFeatureClassByName('shape')
                if window['cb14'].get() and window['cb19'].get():
                    extractor.enableFeaturesByName(
                        shape=['VoxelVolume', 'MeshVolume', 'SurfaceArea', 'SurfaceVolumeRatio', 'Compactness1',
                               'Compactness2', 'Sphericity', 'SphericalDisproportion', 'Maximum3DDiameter',
                               'Maximum2DDiameterSlice', 'Maximum2DDiameterColumn', 'Maximum2DDiameterRow',
                               'MajorAxisLength', 'MinorAxisLength', 'LeastAxisLength', 'Elongation', 'Flatness'])
        print("Extraction parameters:\n\t", extractor.settings)
        print("Enabled filters:\n\t", extractor.enabledImagetypes)
        print("Enabled features:\n\t", extractor.enabledFeatures)
        return extractor

    # 根据手动配置文件提取特征
    def getfeaturemanual(extractor, imgname, maskname):
        texture = pd.DataFrame()
        try:
            featurevector = extractor.execute(imgname, maskname)
            texture = pd.DataFrame([featurevector])
            if values['-IN10-'] != '':
                for colname in list(texture):
                    texture.rename(columns={colname: values['-IN10-'] + colname}, inplace=True)
            if window['cb18'].get():
                texture.insert(0, 'filename', getfilename(imgname), allow_duplicates=False)
            print(texture)
            print('特征提取成功')
        except Exception:
            print('特征提取失败')
        return texture

    # 保存为csv文件
    def saveascsv(filepath, filename, texture):
        if window['cb17'].get():
            temp = pd.DataFrame()
            for col in texture.columns:
                try:
                    df = texture[col].astype(np.float64)  # 如果能转换成数字格式的列保留
                    temp = pd.concat([temp, df], axis=1)  # 转换后的数据添加到空表里，axis=1代表按列添加
                except Exception:
                    pass
            texture = temp
            print(texture)
            print('非数字型数据清除成功')
        if os.path.exists(filepath + '\\' + filename):
            result = sg.popup_ok_cancel('是否将特征追加到已存在的文件中？')
            if result == 'OK':
                if window['rad3'].get():
                    try:
                        texture.to_csv(filepath + '\\' + filename, mode='a', header=False)  # 追加csv文件
                        print('特征文件追加完成')
                    except Exception:
                        print('特征文件追加失败')
                else:
                    try:
                        datafeaturetemp = pd.read_csv(filepath + '\\' + filename, index_col=0)
                        datafeaturetemp = pd.DataFrame(datafeaturetemp)
                        datafeaturetemp = datafeaturetemp.T
                        datafeaturetemp = pd.concat([datafeaturetemp, texture], axis=0)
                        datafeaturetemp = datafeaturetemp.T
                        datafeaturetemp.to_csv(filepath + '\\' + filename, mode='w')  # 追加csv文件
                        print('特征文件追加完成')
                    except Exception:
                        print('特征文件追加失败：存储过程失败')
            else:
                print('特征文件保存失败：该文件已存在')
                return
        else:
            if window['rad3'].get():
                try:
                    texture.to_csv(filepath + '\\' + filename, mode='w')  # 保存为csv文件
                except Exception:
                    print('特征文件保存失败：存储过程失败')
            else:
                datafeaturetemp = texture.T
                try:
                    datafeaturetemp.to_csv(filepath + '\\' + filename, mode='w')  # 保存为csv文件
                except Exception:
                    print('特征文件保存失败：存储过程失败')
            print('特征文件保存完成')

    while True:
        event, values = window.read(timeout=100)
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        elif event == 'autostart':
            if window['rad1'].get():
                if window['-IN3-'].get() == '' or window['-IN4-'].get() == '':
                    print('请先选择图像及标注文件')
                    continue
                elif window['-IN8-'].get() == '':
                    print('未设置特征文件保存文件夹')
                    continue
                elif window['-IN1-'].get() == '':
                    print('未载入特征配置文件')
                    continue
                else:
                    if os.path.isfile(window['-IN1-'].get()):
                        extractor1 = getyaml(window['-IN1-'].get())
                        datafeature = getfeature(extractor1, window['-IN3-'].get(), window['-IN4-'].get())
                        if not datafeature.empty:
                            saveascsv(window['-IN8-'].get(), window['-IN7-'].get() + '.csv', datafeature)
            elif window['rad2'].get():
                if window['-IN5-'].get() == '' or window['-IN6-'].get() == '':
                    continue
                else:
                    datatemp = pd.DataFrame()
                    extractor1 = getyaml(window['-IN1-'].get())
                    for filetemp_im in os.listdir(window['-IN5-'].get()):
                        filetemp1 = filetemp_im.split('.', 1)[0]
                        filetemp2 = filetemp_im.split('.', 1)[1]
                        filetemp1 = filetemp1.split('_', 1)[0]
                        print(filetemp_im)
                        for filetemp_lb in os.listdir(window['-IN6-'].get()):
                            if filetemp_lb == filetemp1 + '_label.' + filetemp2:
                                datafeature = getfeature(extractor1, window['-IN5-'].get() + '/' + filetemp_im,
                                                         window['-IN6-'].get() + '/' + filetemp_lb)
                                datatemp = pd.concat([datatemp, datafeature])
                    saveascsv(window['-IN8-'].get(), window['-IN7-'].get() + '.csv', datatemp)
        elif event == 'manualstart':
            if window['rad1'].get():
                if window['-IN3-'].get() == '' or window['-IN4-'].get() == '':
                    print('请先选择图像及标注文件')
                    continue
                elif window['-IN8-'].get() == '':
                    print('未设置特征文件保存文件夹')
                    continue
                else:
                    extractor1 = manualconfig()
                    datafeature = getfeaturemanual(extractor1, window['-IN3-'].get(), window['-IN4-'].get())
                    if not datafeature.empty:
                        saveascsv(window['-IN8-'].get(), window['-IN7-'].get() + '.csv', datafeature)
            elif window['rad2'].get():
                if window['-IN5-'].get() == '' or window['-IN6-'].get() == '':
                    continue
                else:
                    datatemp = pd.DataFrame()
                    extractor1 = manualconfig()
                    for filetemp_im in os.listdir(window['-IN5-'].get()):
                        filetemp1 = filetemp_im.split('.', 1)[0]
                        filetemp2 = filetemp_im.split('.', 1)[1]
                        filetemp1 = filetemp1.split('_', 1)[0]
                        print(filetemp_im)
                        for filetemp_lb in os.listdir(window['-IN6-'].get()):
                            if filetemp_lb == filetemp1 + '_label.' + filetemp2:
                                datafeature = getfeaturemanual(extractor1, window['-IN5-'].get() + '/' + filetemp_im,
                                                               window['-IN6-'].get() + '/' + filetemp_lb)
                                datatemp = pd.concat([datatemp, datafeature])
                    saveascsv(window['-IN8-'].get(), window['-IN7-'].get() + '.csv', datatemp)
    window.close()


if __name__ == '__main__':
    main()
