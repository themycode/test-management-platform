#!/usr/bin/env python
# -*- coding:utf-8 -*-


__author__ = '赖富玉'

'''
echarts图表数据生成器
'''

import logging

logger = logging.getLogger('mylogger')

class EchartsDataMaker:
    def __init__(self):
        pass

    @staticmethod
    def make_stacked_line_chart_data(source_data, x_axis_data, legend_data_list):
        '''
        组装、生成Stacked Line Chart图表数据（xAxis & series数据）
        source_data格式：
        {x_axis_item_name1: {legend_item_name1:legend_item_value1, legend_item_name2:legend_item_value2,...}, x_axis_item_name2: {legend_item_name1:legend_item_value1, legend_item_name2:legend_item_value2,...}}
        '''

        # 展示曲线图所需数据
        data_for_line = {
            'xAxisData': x_axis_data,
            'seriesData': []
        }


        try:
            legend_data_list.reverse()
            for legend_item in legend_data_list:
                temp_dict = {'name':'%s' % legend_item, 'type': 'line', 'data': []}
                data_for_line['seriesData'].append(temp_dict)
                for item in x_axis_data:
                    # 如果存在x坐标轴对应的数据
                    if item in source_data.keys():
                        if legend_item in source_data[item].keys():
                            temp_dict['data'].append(source_data[item][legend_item])
                        else:
                            temp_dict['data'].append(0)
                    else:
                        temp_dict['data'].append(0)
            return [True, data_for_line]
        except Exception as e:
            msg = '%s' % e
            return [False, msg]
