import pandas as pd
import yaml
from typing import Dict, Optional, List
import logging
import matplotlib.pyplot as plt
import numpy as np

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RiskModel:
    """
    风险评估模型类
    
    这个类提供了完整的风险评估功能，包括数据加载、风险计算、结果导出和可视化。
    
    参数:
        config_path (str, optional): 配置文件路径，包含权重和计算参数。默认为None。
    
    属性:
        df (pandas.DataFrame): 存储输入数据的DataFrame
        weights (dict): 各类风险的权重配置
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初始化风险评估模型
        
        参数:
            config_path (str, optional): 配置文件路径，包含权重和计算参数。默认为None。
        
        示例:
            >>> model = RiskModel()  # 使用默认配置
            >>> model = RiskModel('config.yaml')  # 使用自定义配置
        """
        self.df = None
        self.weights = {
            'strategic': 0.25,
            'financial': 0.30,
            'market': 0.20,
            'legal_credit': 0.15,
            'event': 0.10
        }
        
        # 定义通用的分段函数模板
        self._segment_templates = {
            'standard': [
                (lambda x, **kwargs: x >= 0.5, lambda x, **kwargs: 0),
                (lambda x, **kwargs: (x >= 0.3) & (x < 0.5), lambda x, **kwargs: 1),
                (lambda x, **kwargs: (x >= 0.2) & (x < 0.3), lambda x, **kwargs: 2),
                (lambda x, **kwargs: x < 0.2, lambda x, **kwargs: 4)
            ],
            'disposal': [
                (lambda x, **kwargs: x >= 0.6, lambda x, **kwargs: 0),
                (lambda x, **kwargs: (x >= 0.4) & (x < 0.6), lambda x, **kwargs: 1),
                (lambda x, **kwargs: (x >= 0.2) & (x < 0.4), lambda x, **kwargs: 2),
                (lambda x, **kwargs: x < 0.2, lambda x, **kwargs: 4)
            ]
        }
        
        if config_path:
            self.load_config(config_path)
            
    def load_config(self, config_path: str) -> None:
        """
        从YAML文件加载配置
        Args:
            config_path: 配置文件路径
        """
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                self.weights = config.get('weights', self.weights)
        except Exception as e:
            logger.warning(f"加载配置文件失败: {e}，将使用默认配置")

    def load_data(self, file_path: str, sheet_name: Optional[str] = None) -> None:
        """
        加载Excel数据文件
        
        参数:
            file_path (str): Excel文件路径
            sheet_name (str, optional): 工作表名称，默认为None（读取第一个工作表）
        
        异常:
            FileNotFoundError: 当文件不存在时抛出
            ValueError: 当数据格式不正确时抛出
        
        示例:
            >>> model.load_data('data.xlsx')
            >>> model.load_data('data.xlsx', sheet_name='Sheet1')
        """
        try:
            # 读取原始数据
            raw_df = pd.read_excel(file_path, sheet_name=sheet_name)
            
            # 将第一列设置为索引
            self.df = raw_df.set_index(raw_df.columns[0])
            
            # 转置数据，使月份成为索引
            self.df = self.df.transpose()
            
            # 将所有数值列转换为float类型
            for column in self.df.columns:
                try:
                    self.df[column] = pd.to_numeric(self.df[column], errors='coerce')
                except Exception as e:
                    logger.warning(f"列 '{column}' 转换为数值类型时出错: {e}")
            
            # 验证数据完整性
            self._validate_data()
            logger.info(f"成功加载数据，共{len(self.df)}行")
        except Exception as e:
            logger.error(f"数据加载失败: {e}")
            raise

    def _validate_data(self) -> None:
        """验证数据完整性"""
        required_columns = [
            '主营业务收入', '总营业务收入', '主营业务成本', '总业务成本', '主营业务费用',
            '研发费用', '负债总额', '资产总额', '带息负债总额', '经营现金流入',
            '经营现金流出', '经营净现金流', '投资分红等收益', '利息支出', '预付账款',
            '预收账款', '应收账款', '应付账款', '净资产',  '应收账款总额',
            '坏账准备金额', '存货', '企业当年涉及司法诉讼案件的数量', '执行金额',
            '被执行金额', '已销号事件数', '年初事件数', '新增事件数',
            '已销号事件影响金额', '年初事件影响金额', '新增事件影响金额',
            '未销号事件兜底保障金额', '未销号事件追损挽损金额',
            '未销号事件累计计提减值金额', '未销号事件影响金额', '已处置金额',
            'R1','R2','R3','R4','R5','R6','R7','R8','R9','R10','R11','n0',
            'm1', 'm2', 'm3','x1','x2','x3','x4','y1','y2','y3','z1','z2',
            'x5','y4','z3','行业较差值','货币资金','财务费用中的利息费用'
        ]
        
        # 检查所有必需的指标是否都在数据中
        missing_columns = [col for col in required_columns if col not in self.df.columns]
        if missing_columns:
            raise ValueError(f"缺少必要的指标: {', '.join(missing_columns)}")
            
        # 检查是否有空值或非数值
        for col in required_columns:
            if col in self.df.columns:
                null_values = self.df[col].isnull().sum()
                if null_values > 0:
                    logger.warning(f"列 '{col}' 中存在 {null_values} 个空值")
                non_numeric = self.df[col].apply(lambda x: not pd.api.types.is_numeric_dtype(type(x))).sum()
                if non_numeric > 0:
                    logger.warning(f"列 '{col}' 中存在 {non_numeric} 个非数值类型的数据")

    def _safe_divide(self, numerator: float, denominator: float, default_value: float = 0.0) -> float:
        """
        安全除法，处理除以零的情况
        Args:
            numerator: 分子
            denominator: 分母
            default_value: 当分母为0时返回的默认值
        Returns:
            除法结果或默认值
        """
        try:
            if abs(denominator) < 1e-10:  # 处理接近0的情况
                return default_value
            return numerator / denominator
        except Exception:
            return default_value

    def piecewise_function(self, x, segments, **kwargs):
        """
        实现分段函数的求值
        Args:
            x: 自变量的值
            segments: 一个列表，每个元素是一个二元组 (condition, func)
            kwargs: 其他参数
        Returns:
            满足条件的那一段对应的函数计算结果
        """
        for cond, func in segments:
            if cond(x, **kwargs):
                return func(x, **kwargs)
        raise ValueError(f"没有找到满足 x = {x} 的条件。")

    def _get_monthly_value(self, column: str, row_idx: int) -> float:
        """
        获取指定列的月度值（如果是累计值则计算增量）
        Args:
            column: 列名
            row_idx: 行索引
        Returns:
            月度值
        """
        current_value = self.df[column].iloc[row_idx]
        if row_idx == 0:  # 第一个月直接返回当前值
            return current_value
        previous_value = self.df[column].iloc[row_idx - 1]
        return current_value - previous_value

    def _calculate_strategic_risk(self, row_idx: int) -> float:
        """计算战略风险分数"""
        monthly_main_revenue = self._get_monthly_value('主营业务收入', row_idx)
        monthly_total_revenue = self._get_monthly_value('总营业务收入', row_idx)
        monthly_rd_expense = self._get_monthly_value('研发费用', row_idx)
        
        # 战略风险
        concentration1 = self._safe_divide(
            monthly_main_revenue,
            monthly_total_revenue
        )

        # 定义分段函数
        segment1 = [
            (lambda x, **kwargs: x >= 0.85, lambda x, **kwargs: 0),
            (lambda x, **kwargs: x < 0.85, lambda x, **kwargs: min(10, 100 * (0.85-self.df['R1'].iloc[row_idx])))
        ]
        fa1 = self.piecewise_function(concentration1, segment1)


        concentration2 = self._safe_divide(
            monthly_main_revenue - self.df['主营业务成本'].iloc[row_idx],
            monthly_total_revenue - self.df['总业务成本'].iloc[row_idx]
        )
        segment2 = [
            (lambda x, **kwargs: x >= 0.85, lambda x, **kwargs: 0),
            (lambda x, **kwargs: x < 0.85, lambda x, **kwargs: min(10, 300 * (0.85-self.df['R1'].iloc[row_idx])))
        ]
        fa2 = self.piecewise_function(concentration2, segment2)


        gross_margin = self._safe_divide(
            monthly_main_revenue - self.df['主营业务成本'].iloc[row_idx],
            monthly_main_revenue
        )
        segment3 = [
            (lambda x, **kwargs: x >= self.df['R1'].iloc[row_idx], lambda x, **kwargs: 0),
            (lambda x, **kwargs: x < self.df['R1'].iloc[row_idx], lambda x, **kwargs: min(30, 500 * (0.85-self.df['R1'].iloc[row_idx])))
        ]
        fa3 = self.piecewise_function(gross_margin, segment3)


        r_and_d_intensity = self._safe_divide(
            monthly_rd_expense,
            monthly_total_revenue
        )
        segment4 = [
            (lambda x, **kwargs: x >= self.df['R2'].iloc[row_idx], lambda x, **kwargs: 0),
            (lambda x, **kwargs: x < self.df['R2'].iloc[row_idx], lambda x, **kwargs: min(10, 300 * (self.df['经营现金流入'].iloc[row_idx]-self.df['R1'].iloc[row_idx])))
        ]
        fa4 = self.piecewise_function(r_and_d_intensity, segment4)


        loss_amount = (monthly_main_revenue -
                    (self.df['主营业务成本'].iloc[row_idx] + self.df['主营业务费用'].iloc[row_idx]))
        segment5 = [
            (lambda x, **kwargs: x > 0, lambda x, **kwargs: 0),
            (lambda x, **kwargs: x == 0, lambda x, **kwargs: 3),
            (lambda x, **kwargs: x < 0, lambda x, **kwargs: min(40, 3 * abs(loss_amount)/5000))
        ]
        fa5 = self.piecewise_function(loss_amount, segment5)


        return (fa1 * 0.1 + fa2 * 0.1 + fa3 * 0.3 + fa4 * 0.1 + fa5 * 0.4)

    def _calculate_financial_risk(self, row_idx: int) -> float:
        """计算财务风险分数"""
        # 计算各项指标
        debt_ratio = self._safe_divide(
            self.df['负债总额'].iloc[row_idx],
            self.df['资产总额'].iloc[row_idx]
        )
        segment6 = [
            (lambda x, **kwargs: x <= self.df['R3'].iloc[row_idx], lambda x, **kwargs: 0),
            (lambda x, **kwargs: x > self.df['R3'].iloc[row_idx], lambda x, **kwargs: min(30, 500 * (x - self.df['R3'].iloc[row_idx])))
        ]
        fb1 = self.piecewise_function(debt_ratio, segment6)


        interest_bearing_debt_ratio = self._safe_divide(
            self.df['带息负债总额'].iloc[row_idx],
            self.df['负债总额'].iloc[row_idx]
        )
        segment7 = [
            (lambda x, **kwargs: x <= self.df['R4'].iloc[row_idx], lambda x, **kwargs: 0),
            (lambda x, **kwargs: x > self.df['R4'].iloc[row_idx], lambda x, **kwargs: min(20, 400 * (debt_ratio - self.df['R4'].iloc[row_idx])))
        ]
        fb2 = self.piecewise_function(interest_bearing_debt_ratio, segment7)

        
        operating_cash_flow = (self.df['经营现金流入'].iloc[row_idx] - self.df['经营现金流出'].iloc[row_idx])
        segment8 = [
            (lambda x, **kwargs: x > 0, lambda x, **kwargs: 0),
            (lambda x, **kwargs: x <= 0, lambda x, **kwargs: min(25, 500 * abs(operating_cash_flow)))
        ]
        fb3 = self.piecewise_function(operating_cash_flow, segment8)

        
        inventory_ratio = self._safe_divide(
            self.df['经营净现金流'].iloc[row_idx] + self.df['投资分红等收益'].iloc[row_idx],
            self.df['利息支出'].iloc[row_idx]
        )
        segment9 = [
            (lambda x, **kwargs: x >= 1, lambda x, **kwargs: 0),
            (lambda x, **kwargs: x < 1, lambda x, **kwargs: min(25, 700 * abs(inventory_ratio - 1)))
        ]
        fb4 = self.piecewise_function(inventory_ratio, segment9)

        
        # 计算加权总分
        return (fb1 * 0.3 + fb2 * 0.2 + fb3 * 0.25 + fb4 * 0.25)

    def _calculate_market_risk(self, row_idx: int) -> float:
        """计算市场风险分数"""
        # 市场风险C
        monthly_total_revenue = self._get_monthly_value('总营业务收入', row_idx)
        prepaid_ratio = self._safe_divide(
            self.df['预付账款'].iloc[row_idx],
            self.df['总营业务收入'].iloc[row_idx]
        )
        segment10 = [
            (lambda x, **kwargs: x <= self.df['R5'].iloc[row_idx], lambda x, **kwargs: 0),
            (lambda x, **kwargs: x > self.df['R5'].iloc[row_idx], lambda x, **kwargs: min(10, 300 * abs(x - self.df['R5'].iloc[row_idx])))
        ]
        fc1 = self.piecewise_function(prepaid_ratio, segment10)


        pre_received_ratio = self._safe_divide(
            self.df['预收账款'].iloc[row_idx],
            self.df['资产总额'].iloc[row_idx]
        )
        segment11 = [
            (lambda x, **kwargs: x <= self.df['R6'].iloc[row_idx], lambda x, **kwargs: 0),
            (lambda x, **kwargs: x > self.df['R6'].iloc[row_idx], lambda x, **kwargs: min(10, 200 * abs(x - self.df['R6'].iloc[row_idx])))
        ]
        fc2 = self.piecewise_function(pre_received_ratio, segment11)

        
        accounts_payable_ratio = self._safe_divide(
            self.df['应付账款'].iloc[row_idx],
            self.df['总营业务收入'].iloc[row_idx]
        )
        segment12 = [
            (lambda x, **kwargs: x <= self.df['R7'].iloc[row_idx], lambda x, **kwargs: 0),
            (lambda x, **kwargs: x > self.df['R7'].iloc[row_idx], lambda x, **kwargs: min(15, 200 * abs(x - self.df['R7'].iloc[row_idx])))
        ]
        fc3 = self.piecewise_function(accounts_payable_ratio, segment12)

        
        receivables_ratio = self._safe_divide(
            self.df['应收账款'].iloc[row_idx],
            self.df['净资产'].iloc[row_idx]
        )
        segment13 = [
            (lambda x, **kwargs: x <= self.df['R8'].iloc[row_idx], lambda x, **kwargs: 0),
            (lambda x, **kwargs: x > self.df['R8'].iloc[row_idx], lambda x, **kwargs: min(15, 200 * abs(x - self.df['R8'].iloc[row_idx])))
        ]
        fc4 = self.piecewise_function(receivables_ratio, segment13)

        
        receivables_bad_debt_ratio = self._safe_divide(
            self.df['坏账准备金额'].iloc[row_idx],
            self.df['应收账款总额'].iloc[row_idx]
        )
        segment14 = [
            (lambda x, **kwargs: x >= 0.5, lambda x, **kwargs: 0),
            (lambda x, **kwargs: x < 0.5, lambda x, **kwargs: min(10, 100 * abs(x - 0.5)))
        ]
        fc5 = self.piecewise_function(receivables_bad_debt_ratio, segment14)

        
        inventory_ratio = self._safe_divide(
            self.df['存货'].iloc[row_idx],
            self.df['净资产'].iloc[row_idx]
        )
        segment15 = [
            (lambda x, **kwargs: x <= self.df['R9'].iloc[row_idx], lambda x, **kwargs: 0),
            (lambda x, **kwargs: x > self.df['R9'].iloc[row_idx], lambda x, **kwargs: min(20, 200 * abs(x - self.df['R9'].iloc[row_idx])))
        ]
        fc6 = self.piecewise_function(inventory_ratio, segment15)

        
        margin_ratio = self._safe_divide(
            monthly_total_revenue - self.df['总业务成本'].iloc[row_idx],
            monthly_total_revenue
        )
        segment16 = [
            (lambda x, **kwargs: x <= self.df['R10'].iloc[row_idx], lambda x, **kwargs: 0),
            (lambda x, **kwargs: x > self.df['R10'].iloc[row_idx], lambda x, **kwargs: min(20, 500 * abs(x - self.df['R10'].iloc[row_idx])))
        ]
        fc7 = self.piecewise_function(margin_ratio, segment16)

        
        # 计算加权总分
        return (fc1 * 0.1 + fc2 * 0.1 + fc3 * 0.15 + fc4 * 0.15 + 
                fc5 * 0.1 + fc6 * 0.2 + fc7 * 0.2)

    def _calculate_legal_credit_risk(self, row_idx: int) -> float:
        """计算法律信用风险分数"""
        # 法律信用风险
        litigation_cases = self.df['企业当年涉及司法诉讼案件的数量'].iloc[row_idx]
        segment17 = [
            (lambda x, **kwargs: x <= self.df['n0'].iloc[row_idx], lambda x, **kwargs: 0),
            (lambda x, **kwargs: x > self.df['n0'].iloc[row_idx], lambda x, **kwargs: min(30, abs(x - self.df['n0'].iloc[row_idx])))
        ]
        fd1 = self.piecewise_function(litigation_cases, segment17)

        
        execution_amount_ratio = self._safe_divide(
            self.df['执行金额'].iloc[row_idx],
            self.df['净资产'].iloc[row_idx]
        )
        segment18 = [
            (lambda x, **kwargs: x <= self.df['R11'].iloc[row_idx], lambda x, **kwargs: 0),
            (lambda x, **kwargs: x > self.df['R11'].iloc[row_idx], lambda x, **kwargs: min(35, 100 * abs(x - self.df['R11'].iloc[row_idx])))
        ]
        fd2 = self.piecewise_function(execution_amount_ratio, segment18)

        
        executed_amount_ratio = self._safe_divide(
            self.df['被执行金额'].iloc[row_idx],
            self.df['净资产'].iloc[row_idx]
        )
        segment19 = [
            (lambda x, **kwargs: x <= 0, lambda x, **kwargs: 0),
            (lambda x, **kwargs: x > 0, lambda x, **kwargs: min(35, 100 * x))
        ]
        fd3 = self.piecewise_function(executed_amount_ratio, segment19)

        
        # 计算加权总分
        return (fd1 * 0.3 + fd2 * 0.35 + fd3 * 0.35)

    def _calculate_event_risk(self, row_idx: int) -> float:
        """计算事件风险分数"""
        # 事件风险
        cancellation_rate = self._safe_divide(
            self.df['已销号事件数'].iloc[row_idx],
            self.df['年初事件数'].iloc[row_idx] + self.df['新增事件数'].iloc[row_idx]
        )
        segment20 = [
            (lambda x, **kwargs: x >= 0.5, lambda x, **kwargs: 0),
            (lambda x, **kwargs: (x >= 0.3) & (x < 0.5), lambda x, **kwargs: 1),
            (lambda x, **kwargs: (x >= 0.2) & (x < 0.3), lambda x, **kwargs: 2),
            (lambda x, **kwargs: x < 0.2, lambda x, **kwargs: 4)
        ]
        fe1 = self.piecewise_function(cancellation_rate, segment20)

        
        reduction_rate = self._safe_divide(
            self.df['已销号事件影响金额'].iloc[row_idx],
            self.df['年初事件影响金额'].iloc[row_idx] + self.df['新增事件影响金额'].iloc[row_idx]
        )
        segment21 = [
            (lambda x, **kwargs: x >= 0.5, lambda x, **kwargs: 0),
            (lambda x, **kwargs: (x >= 0.3) & (x < 0.5), lambda x, **kwargs: 1),
            (lambda x, **kwargs: (x >= 0.2) & (x < 0.3), lambda x, **kwargs: 2),
            (lambda x, **kwargs: x < 0.2, lambda x, **kwargs: 4)
        ]
        fe2 = self.piecewise_function(reduction_rate, segment21)

        
        loss_rate = self._safe_divide(
            self.df['未销号事件兜底保障金额'].iloc[row_idx] + self.df['未销号事件追损挽损金额'].iloc[row_idx],
            self.df['未销号事件影响金额'].iloc[row_idx]
        )
        segment22 = [
            (lambda x, **kwargs: x >= 0.5, lambda x, **kwargs: 0),
            (lambda x, **kwargs: (x >= 0.3) & (x < 0.5), lambda x, **kwargs: 1),
            (lambda x, **kwargs: (x >= 0.2) & (x < 0.3), lambda x, **kwargs: 2),
            (lambda x, **kwargs: x < 0.2, lambda x, **kwargs: 4)
        ]
        fe3 = self.piecewise_function(loss_rate, segment22)

        
        disposal_resolution_rate = self._safe_divide(
            self.df['已销号事件数'].iloc[row_idx],
            self.df['年初事件影响金额'].iloc[row_idx] + self.df['新增事件影响金额'].iloc[row_idx]
        )
        segment23 = [
            (lambda x, **kwargs: x >= 0.5, lambda x, **kwargs: 0),
            (lambda x, **kwargs: (x >= 0.3) & (x < 0.5), lambda x, **kwargs: 1),
            (lambda x, **kwargs: (x >= 0.2) & (x < 0.3), lambda x, **kwargs: 2),
            (lambda x, **kwargs: x < 0.2, lambda x, **kwargs: 4)
        ]
        fe4 = self.piecewise_function(disposal_resolution_rate, segment23)

        
        provision_coverage_rate = self._safe_divide(
            self.df['未销号事件累计计提减值金额'].iloc[row_idx],
            self.df['未销号事件影响金额'].iloc[row_idx] - 
            self.df['未销号事件兜底保障金额'].iloc[row_idx] - 
            self.df['未销号事件追损挽损金额'].iloc[row_idx]
        )
        segment24 = [
            (lambda x, **kwargs: x >= 0.5, lambda x, **kwargs: 0),
            (lambda x, **kwargs: (x >= 0.3) & (x < 0.5), lambda x, **kwargs: 1),
            (lambda x, **kwargs: (x >= 0.2) & (x < 0.3), lambda x, **kwargs: 2),
            (lambda x, **kwargs: x < 0.2, lambda x, **kwargs: 4)
        ]
        fe5 = self.piecewise_function(provision_coverage_rate, segment24)

        
        # 计算加权总分
        return (0.2 * fe1 + 0.2 * fe2 + 0.2 * fe3 + 0.2 * fe4 + 0.2 * fe5)

    def _calculate_risk_score(self, row_idx: int) -> Dict[str, float]:
        """
        计算信用风险和社会责任风险分数
        Args:
            row_idx: 行索引
        Returns:
            包含信用风险和社会责任风险的字典
        """
        # 计算信用风险（M1）
        credit_risk = 5*(self.df['m1'].iloc[row_idx] + self.df['m2'].iloc[row_idx] + self.df['m3'].iloc[row_idx])
        
        # 计算社会责任风险（G）
        X1 = 10 * self.df['x1'].iloc[row_idx] + 6 * self.df['x2'].iloc[row_idx] \
             + 3 * self.df['x3'].iloc[row_idx] + 1 * self.df['x4'].iloc[row_idx]
        Y1 = 10 * self.df['y1'].iloc[row_idx] + 5 * self.df['y2'].iloc[row_idx] \
             + 2 * self.df['y3'].iloc[row_idx]
        Z1 = 10 * self.df['z1'].iloc[row_idx] + 5 * self.df['z2'].iloc[row_idx]
        social_risk = X1 + Y1 + Z1
        
        print(f"第{row_idx}行数据的信用风险评分为：{credit_risk}")
        print(f"第{row_idx}行数据的社会责任风险评分为：{social_risk}")
        
        return {
            'credit_risk': credit_risk,
            'social_risk': social_risk
        }

    @staticmethod
    def _get_risk_level(score: float) -> Dict[str, str]:
        """
        根据分数确定风险等级
        Args:
            score: 风险评分
        Returns:
            包含风险等级和判断依据的字典
        """
        if score >= 90:
            return {"level": "高风险", "basis": "score"}
        elif score >= 70:
            return {"level": "中高风险", "basis": "score"}
        elif score >= 60:
            return {"level": "中低风险", "basis": "score"}
        else:
            return {"level": "低风险", "basis": "score"}

    def _check_threshold_risk(self, row_idx: int) -> Dict[str, any]:
        """
        检查是否触发阈值风险（第一层风险判断）
        Args:
            row_idx: 行索引
        Returns:
            包含是否高风险及原因的字典
        """
        monthly_main_revenue = self._get_monthly_value('主营业务收入', row_idx)
        # 定义阈值风险判断条件
        threshold_conditions = {
            '主业亏损金额': {
                'value': (monthly_main_revenue -
                    (self.df['主营业务成本'].iloc[row_idx] + self.df['主营业务费用'].iloc[row_idx])
                ),
                'threshold': 200000000,
                'condition': lambda x, t: x > t
            },
            '资产负债率': {
                'value': self._safe_divide(
                    self.df['负债总额'].iloc[row_idx],
                    self.df['资产总额'].iloc[row_idx]
                ),
                'threshold': 0.9,
                'condition': lambda x, t: x > t
            },
            '带息负债率': {
                'value': self._safe_divide(
                    self.df['带息负债总额'].iloc[row_idx],
                    self.df['负债总额'].iloc[row_idx]
                ),
                'threshold':  self.df['行业较差值'].iloc[row_idx],
                'condition': lambda x, t: x > t
            },
            '高危企业发生特别重大生产安全事故': {
                'value': self.df['x5'].iloc[row_idx],
                'threshold': 0,
                'condition': lambda x, t: x > t
            },
            '非高危企业发生特别重大生产安全事故': {
                'value': self.df['y4'].iloc[row_idx],
                'threshold': 0,
                'condition': lambda x, t: x > t
            },
            '企业发生重大及以上生态环境事件': {
                'value': self.df['z3'].iloc[row_idx],
                'threshold': 0,
                'condition': lambda x, t: x > t
            },
            '经营现金流量比率': {
                'value': self._safe_divide(
                    self.df['经营净现金流'].iloc[row_idx],
                    self.df['货币资金'].iloc[row_idx]
                ),
                'threshold': 0.3,
                'condition': lambda x, t: x > t
            }
        }

        # 检查是否触发任何阈值条件
        triggered_conditions = []
        for indicator, config in threshold_conditions.items():
            if config['condition'](config['value'], config['threshold']):
                triggered_conditions.append(f"{indicator}={config['value']:.2f}")

        if triggered_conditions:
            return {
                "is_high_risk": True,
                "level": "高风险",
                "basis": "threshold",
                "reasons": triggered_conditions
            }
        
        return {"is_high_risk": False}

    def _calculate_risk_for_row(self, row_idx: int) -> Dict[str, float]:
        """
        计算单行数据的风险评分
        Args:
            row_idx: 行索引
        Returns:
            包含各项风险分数的字典
        """
        try:
            # 计算基础风险分数
            risk_scores = {
                'strategic': self._calculate_strategic_risk(row_idx),
                'financial': self._calculate_financial_risk(row_idx),
                'market': self._calculate_market_risk(row_idx),
                'legal_credit': self._calculate_legal_credit_risk(row_idx),
                'event': self._calculate_event_risk(row_idx)
            }
            
            return risk_scores
            
        except Exception as e:
            logger.error(f"计算第{row_idx}行风险评分时出错: {e}")
            raise

    def calculate_total_risk(self) -> List[Dict]:
        """
        计算所有行的风险评分
        
        返回:
            List[Dict]: 包含每行风险评分的列表，每个字典包含：
                - period: 期间（如月份）
                - total_score: 总风险评分
                - risk_scores: 各项风险评分
                - risk_level: 风险等级
                - risk_basis: 风险判断依据
        
        异常:
            ValueError: 当数据未加载时抛出
        
        示例:
            >>> results = model.calculate_total_risk()
            >>> for result in results:
            ...     print(f"期间: {result['period']}, 总评分: {result['total_score']}")
        """
        if self.df is None:
            raise ValueError("请先加载数据")

        results = []
        for idx in range(len(self.df)):
            try:
                # 获取当前行的索引值（可能是日期或其他标识）
                row_index = self.df.index[idx]
                
                # 首先检查是否触发阈值风险（第一层判断）
                threshold_risk = self._check_threshold_risk(idx)
                
                # 计算当前行的风险评分
                risk_scores = self._calculate_risk_for_row(idx)
                
                # 计算信用风险和社会责任风险
                additional_risks = self._calculate_risk_score(idx)
                
                # 计算总分（包含所有风险）
                total_score = sum(score * self.weights[risk_type] 
                                for risk_type, score in risk_scores.items()) + \
                             additional_risks['social_risk']
                
                # 确定风险等级（优先使用阈值判断结果）
                if threshold_risk["is_high_risk"]:
                    risk_level = threshold_risk
                else:
                    risk_level = self._get_risk_level(total_score)
                
                # 组织结果
                result = {
                    'period': row_index,  # 期间（如月份）
                    'total_score': total_score,
                    'risk_scores': risk_scores,
                    'credit_risk': additional_risks['credit_risk'],
                    'social_risk': additional_risks['social_risk'],
                    'risk_level': risk_level["level"],
                    'risk_basis': risk_level["basis"]
                }
                
                # 如果是阈值触发的高风险，添加具体原因
                if threshold_risk["is_high_risk"]:
                    result['risk_reasons'] = threshold_risk["reasons"]
                
                results.append(result)
                
            except Exception as e:
                logger.error(f"处理第{idx}行数据时出错: {e}")
                continue
        
        return results

    def plot_risk_scores(self, results: List[Dict], save_path: Optional[str] = None) -> None:
        """
        绘制风险评分柱状图
        
        参数:
            results (List[Dict]): 风险评分结果列表
            save_path (str, optional): 图表保存路径，如果为None则显示图表
        
        示例:
            >>> model.plot_risk_scores(results)  # 显示图表
            >>> model.plot_risk_scores(results, 'risk_chart.png')  # 保存图表
        """
        try:
            # 准备数据
            periods = [str(result['period']) for result in results]
            
            # 按权重排序的风险类型
            sorted_risk_types = sorted(
                self.weights.items(), 
                key=lambda x: x[1], 
                reverse=True
            )
            
            risk_types = {
                'total': '总体风险',
                'credit_risk': '信用风险',
                'social_risk': '社会责任风险',
                **{k: {
                    'strategic': '战略风险',
                    'financial': '财务风险',
                    'market': '市场风险',
                    'legal_credit': '法律信用风险',
                    'event': '事件风险'
                }[k] for k, _ in sorted_risk_types}
            }

            # 设置中文字体
            plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
            plt.rcParams['axes.unicode_minus'] = False    # 用来正常显示负号

            # 创建图表
            fig, ax = plt.subplots(figsize=(15, 8))
            
            # 准备数据
            total_scores = [result['total_score'] for result in results]
            credit_risks = [result['credit_risk'] for result in results]
            social_risks = [result['social_risk'] for result in results]
            risk_scores = {
                risk_type: [result['risk_scores'][risk_type] for result in results]
                for risk_type, _ in sorted_risk_types
            }

            # 设置柱状图宽度和位置
            bar_width = 0.08  # 减小柱子宽度
            spacing = 0.02   # 添加间距
            index = np.arange(len(periods))
            
            # 设置颜色（按风险类型分组设置颜色）
            risk_colors = {
                'financial': '#FF0000',    # 财务风险-红色（权重0.30）
                'strategic': '#FFA500',    # 战略风险-橙色（权重0.25）
                'market': '#FFD700',       # 市场风险-金色（权重0.20）
                'legal_credit': '#006400', # 法律信用风险-深绿色（权重0.15）
                'event': '#7CFC00',        # 事件风险-草绿色（权重0.10）
                'credit_risk': '#FF69B4',  # 信用风险-粉色
                'social_risk': '#9370DB'   # 社会责任风险-紫色
            }
            
            # 计算总体风险柱状图的位置
            total_pos = index - 2 * (bar_width + spacing)
            
            # 绘制总分柱状图（深蓝色）
            bars_total = ax.bar(total_pos, total_scores, 
                              bar_width, label=risk_types['total'], 
                              color='#1976D2', alpha=0.9)
            
            # 在总分柱子上方添加风险等级标签
            for bar, result in zip(bars_total, results):
                height = bar.get_height()
                label_text = f'{height:.1f}\n{result["risk_level"]}'
                if "risk_reasons" in result:
                    label_text += "\n(阈值触发)"
                ax.text(bar.get_x() + bar_width/2., height,
                       label_text,
                       ha='center', va='bottom', fontsize=8)

            # 绘制信用风险柱状图（粉色）
            credit_pos = index - 1 * (bar_width + spacing)
            bars_credit = ax.bar(credit_pos, credit_risks,
                               bar_width, label=risk_types['credit_risk'],
                               color=risk_colors['credit_risk'], alpha=0.9)
            
            # 在信用风险柱子上方添加数值标签
            for bar in bars_credit:
                height = bar.get_height()
                ax.text(bar.get_x() + bar_width/2., height,
                       f'{height:.1f}', ha='center', va='bottom', fontsize=8)

            # 绘制社会责任风险柱状图（紫色）
            social_pos = index
            bars_social = ax.bar(social_pos, social_risks,
                               bar_width, label=risk_types['social_risk'],
                               color=risk_colors['social_risk'], alpha=0.9)
            
            # 在社会责任风险柱子上方添加数值标签
            for bar in bars_social:
                height = bar.get_height()
                ax.text(bar.get_x() + bar_width/2., height,
                       f'{height:.1f}', ha='center', va='bottom', fontsize=8)

            # 绘制分项风险评分柱状图
            for i, (risk_type, weight) in enumerate(sorted_risk_types):
                scores = risk_scores[risk_type]
                pos = index + (i + 1) * (bar_width + spacing)
                bars = ax.bar(pos, scores, bar_width, 
                            label=f'{risk_types[risk_type]}\n(权重:{weight:.2f})', 
                            color=risk_colors[risk_type], alpha=0.9)
                
                # 在柱子上方添加数值标签
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar_width/2., height,
                           f'{height:.1f}', ha='center', va='bottom', fontsize=8)

            # 设置图表属性
            ax.set_title('风险评分分析', fontsize=14, pad=15)
            ax.set_xlabel('月份', fontsize=12)
            ax.set_ylabel('风险评分', fontsize=12)
            ax.set_xticks(index)
            ax.set_xticklabels(periods)
            
            # 添加图例
            ax.legend(loc='upper right', bbox_to_anchor=(1.15, 1))
            
            # 添加网格线
            ax.grid(True, linestyle='--', alpha=0.3)

            # 调整布局
            plt.tight_layout()
            
            # 保存或显示图表
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                logger.info(f"图表已保存至: {save_path}")
            else:
                plt.show()
                
            # 关闭图表
            plt.close()

        except Exception as e:
            logger.error(f"绘制风险评分图表时出错: {e}")
            raise

    def export_calculation_details(self, results: List[Dict], save_path: str) -> None:
        """
        将计算过程中的中间结果导出到Excel文件
        
        参数:
            results (List[Dict]): 风险评分结果列表
            save_path (str): Excel文件保存路径
        
        异常:
            ValueError: 当保存路径无效时抛出
        
        示例:
            >>> model.export_calculation_details(results, 'risk_details.xlsx')
        """
        try:
            # 创建一个Excel写入器
            with pd.ExcelWriter(save_path, engine='openpyxl') as writer:
                # 1. 导出总体结果
                df_results = pd.DataFrame([
                    {
                        '月份': result['period'],
                        '总风险评分': result['total_score'],
                        '风险等级': result['risk_level'],
                        '风险判断依据': result['risk_basis'],
                        '战略风险': result['risk_scores']['strategic'],
                        '财务风险': result['risk_scores']['financial'],
                        '市场风险': result['risk_scores']['market'],
                        '法律信用风险': result['risk_scores']['legal_credit'],
                        '事件风险': result['risk_scores']['event'],
                        '信用风险': result['credit_risk'],
                        '社会责任风险': result['social_risk']
                    }
                    for result in results
                ])
                df_results.to_excel(writer, sheet_name='总体结果', index=False)

                # 2. 导出战略风险计算详情
                strategic_details = []
                for idx, result in enumerate(results):
                    row_idx = idx
                    monthly_main_revenue = self._get_monthly_value('主营业务收入', row_idx)
                    monthly_total_revenue = self._get_monthly_value('总营业务收入', row_idx)
                    monthly_rd_expense = self._get_monthly_value('研发费用', row_idx)
                    
                    concentration1 = self._safe_divide(monthly_main_revenue, monthly_total_revenue)
                    concentration2 = self._safe_divide(
                        monthly_main_revenue - self.df['主营业务成本'].iloc[row_idx],
                        monthly_total_revenue - self.df['总业务成本'].iloc[row_idx]
                    )
                    gross_margin = self._safe_divide(
                        monthly_main_revenue - self.df['主营业务成本'].iloc[row_idx],
                        monthly_main_revenue
                    )
                    r_and_d_intensity = self._safe_divide(monthly_rd_expense, monthly_total_revenue)
                    loss_amount = (monthly_main_revenue -
                                (self.df['主营业务成本'].iloc[row_idx] + self.df['主营业务费用'].iloc[row_idx]))
                    
                    # 计算战略风险各项得分
                    segment1 = [
                        (lambda x, **kwargs: x >= 0.85, lambda x, **kwargs: 0),
                        (lambda x, **kwargs: x < 0.85, lambda x, **kwargs: min(10, 100 * (0.85-self.df['R1'].iloc[row_idx])))
                    ]
                    fa1 = self.piecewise_function(concentration1, segment1)
                    
                    segment2 = [
                        (lambda x, **kwargs: x >= 0.85, lambda x, **kwargs: 0),
                        (lambda x, **kwargs: x < 0.85, lambda x, **kwargs: min(10, 300 * (0.85-self.df['R1'].iloc[row_idx])))
                    ]
                    fa2 = self.piecewise_function(concentration2, segment2)
                    
                    segment3 = [
                        (lambda x, **kwargs: x >= self.df['R1'].iloc[row_idx], lambda x, **kwargs: 0),
                        (lambda x, **kwargs: x < self.df['R1'].iloc[row_idx], lambda x, **kwargs: min(30, 500 * (0.85-self.df['R1'].iloc[row_idx])))
                    ]
                    fa3 = self.piecewise_function(gross_margin, segment3)
                    
                    segment4 = [
                        (lambda x, **kwargs: x >= self.df['R2'].iloc[row_idx], lambda x, **kwargs: 0),
                        (lambda x, **kwargs: x < self.df['R2'].iloc[row_idx], lambda x, **kwargs: min(10, 300 * (self.df['经营现金流入'].iloc[row_idx]-self.df['R1'].iloc[row_idx])))
                    ]
                    fa4 = self.piecewise_function(r_and_d_intensity, segment4)
                    
                    segment5 = [
                        (lambda x, **kwargs: x > 0, lambda x, **kwargs: 0),
                        (lambda x, **kwargs: x == 0, lambda x, **kwargs: 3),
                        (lambda x, **kwargs: x < 0, lambda x, **kwargs: min(40, 3 * abs(loss_amount)/5000))
                    ]
                    fa5 = self.piecewise_function(loss_amount, segment5)
                    
                    strategic_details.append({
                        '月份': result['period'],
                        '主营业务收入': monthly_main_revenue,
                        '总营业务收入': monthly_total_revenue,
                        '研发费用': monthly_rd_expense,
                        '主营业务成本': self.df['主营业务成本'].iloc[row_idx],
                        '主营业务费用': self.df['主营业务费用'].iloc[row_idx],
                        '业务集中度1': concentration1,
                        '业务集中度2': concentration2,
                        '毛利率': gross_margin,
                        '研发强度': r_and_d_intensity,
                        '亏损金额': loss_amount,
                        'R1值': self.df['R1'].iloc[row_idx],
                        'R2值': self.df['R2'].iloc[row_idx],
                        '经营现金流入': self.df['经营现金流入'].iloc[row_idx],
                        'fa1得分': fa1,
                        'fa2得分': fa2,
                        'fa3得分': fa3,
                        'fa4得分': fa4,
                        'fa5得分': fa5,
                        '战略风险总分': result['risk_scores']['strategic']
                    })
                pd.DataFrame(strategic_details).to_excel(writer, sheet_name='战略风险计算', index=False)

                # 3. 导出财务风险计算详情
                financial_details = []
                for idx, result in enumerate(results):
                    row_idx = idx
                    debt_ratio = self._safe_divide(
                        self.df['负债总额'].iloc[row_idx],
                        self.df['资产总额'].iloc[row_idx]
                    )
                    interest_bearing_debt_ratio = self._safe_divide(
                        self.df['带息负债总额'].iloc[row_idx],
                        self.df['负债总额'].iloc[row_idx]
                    )
                    operating_cash_flow = (self.df['经营现金流入'].iloc[row_idx] - 
                                         self.df['经营现金流出'].iloc[row_idx])
                    inventory_ratio = self._safe_divide(
                        self.df['经营净现金流'].iloc[row_idx] + self.df['投资分红等收益'].iloc[row_idx],
                        self.df['利息支出'].iloc[row_idx]
                    )
                    
                    # 计算财务风险各项得分
                    segment6 = [
                        (lambda x, **kwargs: x <= self.df['R3'].iloc[row_idx], lambda x, **kwargs: 0),
                        (lambda x, **kwargs: x > self.df['R3'].iloc[row_idx], lambda x, **kwargs: min(30, 500 * (x - self.df['R3'].iloc[row_idx])))
                    ]
                    fb1 = self.piecewise_function(debt_ratio, segment6)
                    
                    segment7 = [
                        (lambda x, **kwargs: x <= self.df['R4'].iloc[row_idx], lambda x, **kwargs: 0),
                        (lambda x, **kwargs: x > self.df['R4'].iloc[row_idx], lambda x, **kwargs: min(20, 400 * (debt_ratio - self.df['R4'].iloc[row_idx])))
                    ]
                    fb2 = self.piecewise_function(interest_bearing_debt_ratio, segment7)
                    
                    segment8 = [
                        (lambda x, **kwargs: x > 0, lambda x, **kwargs: 0),
                        (lambda x, **kwargs: x <= 0, lambda x, **kwargs: min(25, 500 * abs(operating_cash_flow)))
                    ]
                    fb3 = self.piecewise_function(operating_cash_flow, segment8)
                    
                    segment9 = [
                        (lambda x, **kwargs: x >= 1, lambda x, **kwargs: 0),
                        (lambda x, **kwargs: x < 1, lambda x, **kwargs: min(25, 700 * abs(inventory_ratio - 1)))
                    ]
                    fb4 = self.piecewise_function(inventory_ratio, segment9)
                    
                    financial_details.append({
                        '月份': result['period'],
                        '负债总额': self.df['负债总额'].iloc[row_idx],
                        '资产总额': self.df['资产总额'].iloc[row_idx],
                        '带息负债总额': self.df['带息负债总额'].iloc[row_idx],
                        '经营现金流入': self.df['经营现金流入'].iloc[row_idx],
                        '经营现金流出': self.df['经营现金流出'].iloc[row_idx],
                        '经营净现金流': self.df['经营净现金流'].iloc[row_idx],
                        '投资分红等收益': self.df['投资分红等收益'].iloc[row_idx],
                        '利息支出': self.df['利息支出'].iloc[row_idx],
                        '资产负债率': debt_ratio,
                        '带息负债率': interest_bearing_debt_ratio,
                        '经营现金流量': operating_cash_flow,
                        '利息保障倍数': inventory_ratio,
                        'R3值': self.df['R3'].iloc[row_idx],
                        'R4值': self.df['R4'].iloc[row_idx],
                        'fb1得分': fb1,
                        'fb2得分': fb2,
                        'fb3得分': fb3,
                        'fb4得分': fb4,
                        '财务风险总分': result['risk_scores']['financial']
                    })
                pd.DataFrame(financial_details).to_excel(writer, sheet_name='财务风险计算', index=False)

                # 4. 导出市场风险计算详情
                market_details = []
                for idx, result in enumerate(results):
                    row_idx = idx
                    monthly_total_revenue = self._get_monthly_value('总营业务收入', row_idx)
                    
                    prepaid_ratio = self._safe_divide(
                        self.df['预付账款'].iloc[row_idx],
                        self.df['总营业务收入'].iloc[row_idx]
                    )
                    pre_received_ratio = self._safe_divide(
                        self.df['预收账款'].iloc[row_idx],
                        self.df['资产总额'].iloc[row_idx]
                    )
                    accounts_payable_ratio = self._safe_divide(
                        self.df['应付账款'].iloc[row_idx],
                        self.df['总营业务收入'].iloc[row_idx]
                    )
                    receivables_ratio = self._safe_divide(
                        self.df['应收账款'].iloc[row_idx],
                        self.df['净资产'].iloc[row_idx]
                    )
                    receivables_bad_debt_ratio = self._safe_divide(
                        self.df['坏账准备金额'].iloc[row_idx],
                        self.df['应收账款总额'].iloc[row_idx]
                    )
                    inventory_ratio = self._safe_divide(
                        self.df['存货'].iloc[row_idx],
                        self.df['净资产'].iloc[row_idx]
                    )
                    margin_ratio = self._safe_divide(
                        monthly_total_revenue - self.df['总业务成本'].iloc[row_idx],
                        monthly_total_revenue
                    )
                    
                    # 计算市场风险各项得分
                    segment10 = [
                        (lambda x, **kwargs: x <= self.df['R5'].iloc[row_idx], lambda x, **kwargs: 0),
                        (lambda x, **kwargs: x > self.df['R5'].iloc[row_idx], lambda x, **kwargs: min(10, 300 * abs(x - self.df['R5'].iloc[row_idx])))
                    ]
                    fc1 = self.piecewise_function(prepaid_ratio, segment10)
                    
                    segment11 = [
                        (lambda x, **kwargs: x <= self.df['R6'].iloc[row_idx], lambda x, **kwargs: 0),
                        (lambda x, **kwargs: x > self.df['R6'].iloc[row_idx], lambda x, **kwargs: min(10, 200 * abs(x - self.df['R6'].iloc[row_idx])))
                    ]
                    fc2 = self.piecewise_function(pre_received_ratio, segment11)
                    
                    segment12 = [
                        (lambda x, **kwargs: x <= self.df['R7'].iloc[row_idx], lambda x, **kwargs: 0),
                        (lambda x, **kwargs: x > self.df['R7'].iloc[row_idx], lambda x, **kwargs: min(15, 200 * abs(x - self.df['R7'].iloc[row_idx])))
                    ]
                    fc3 = self.piecewise_function(accounts_payable_ratio, segment12)
                    
                    segment13 = [
                        (lambda x, **kwargs: x <= self.df['R8'].iloc[row_idx], lambda x, **kwargs: 0),
                        (lambda x, **kwargs: x > self.df['R8'].iloc[row_idx], lambda x, **kwargs: min(15, 200 * abs(x - self.df['R8'].iloc[row_idx])))
                    ]
                    fc4 = self.piecewise_function(receivables_ratio, segment13)
                    
                    segment14 = [
                        (lambda x, **kwargs: x >= 0.5, lambda x, **kwargs: 0),
                        (lambda x, **kwargs: x < 0.5, lambda x, **kwargs: min(10, 100 * abs(x - 0.5)))
                    ]
                    fc5 = self.piecewise_function(receivables_bad_debt_ratio, segment14)
                    
                    segment15 = [
                        (lambda x, **kwargs: x <= self.df['R9'].iloc[row_idx], lambda x, **kwargs: 0),
                        (lambda x, **kwargs: x > self.df['R9'].iloc[row_idx], lambda x, **kwargs: min(20, 200 * abs(x - self.df['R9'].iloc[row_idx])))
                    ]
                    fc6 = self.piecewise_function(inventory_ratio, segment15)
                    
                    segment16 = [
                        (lambda x, **kwargs: x <= self.df['R10'].iloc[row_idx], lambda x, **kwargs: 0),
                        (lambda x, **kwargs: x > self.df['R10'].iloc[row_idx], lambda x, **kwargs: min(20, 500 * abs(x - self.df['R10'].iloc[row_idx])))
                    ]
                    fc7 = self.piecewise_function(margin_ratio, segment16)
                    
                    market_details.append({
                        '月份': result['period'],
                        '预付账款比率': prepaid_ratio,
                        '预收账款比率': pre_received_ratio,
                        '应付账款比率': accounts_payable_ratio,
                        '应收账款比率': receivables_ratio,
                        '坏账准备比率': receivables_bad_debt_ratio,
                        '存货比率': inventory_ratio,
                        '毛利率': margin_ratio,
                        'R5值': self.df['R5'].iloc[row_idx],
                        'R6值': self.df['R6'].iloc[row_idx],
                        'R7值': self.df['R7'].iloc[row_idx],
                        'R8值': self.df['R8'].iloc[row_idx],
                        'R9值': self.df['R9'].iloc[row_idx],
                        'R10值': self.df['R10'].iloc[row_idx],
                        'fc1得分': fc1,
                        'fc2得分': fc2,
                        'fc3得分': fc3,
                        'fc4得分': fc4,
                        'fc5得分': fc5,
                        'fc6得分': fc6,
                        'fc7得分': fc7,
                        '市场风险总分': result['risk_scores']['market']
                    })
                pd.DataFrame(market_details).to_excel(writer, sheet_name='市场风险计算', index=False)

                # 5. 导出法律信用风险计算详情
                legal_details = []
                for idx, result in enumerate(results):
                    row_idx = idx
                    litigation_cases = self.df['企业当年涉及司法诉讼案件的数量'].iloc[row_idx]
                    execution_amount_ratio = self._safe_divide(
                        self.df['执行金额'].iloc[row_idx],
                        self.df['净资产'].iloc[row_idx]
                    )
                    executed_amount_ratio = self._safe_divide(
                        self.df['被执行金额'].iloc[row_idx],
                        self.df['净资产'].iloc[row_idx]
                    )
                    
                    # 计算法律信用风险各项得分
                    segment17 = [
                        (lambda x, **kwargs: x <= self.df['n0'].iloc[row_idx], lambda x, **kwargs: 0),
                        (lambda x, **kwargs: x > self.df['n0'].iloc[row_idx], lambda x, **kwargs: min(30, abs(x - self.df['n0'].iloc[row_idx])))
                    ]
                    fd1 = self.piecewise_function(litigation_cases, segment17)
                    
                    segment18 = [
                        (lambda x, **kwargs: x <= self.df['R11'].iloc[row_idx], lambda x, **kwargs: 0),
                        (lambda x, **kwargs: x > self.df['R11'].iloc[row_idx], lambda x, **kwargs: min(35, 100 * abs(x - self.df['R11'].iloc[row_idx])))
                    ]
                    fd2 = self.piecewise_function(execution_amount_ratio, segment18)
                    
                    segment19 = [
                        (lambda x, **kwargs: x <= 0, lambda x, **kwargs: 0),
                        (lambda x, **kwargs: x > 0, lambda x, **kwargs: min(35, 100 * x))
                    ]
                    fd3 = self.piecewise_function(executed_amount_ratio, segment19)
                    
                    legal_details.append({
                        '月份': result['period'],
                        '诉讼案件数量': litigation_cases,
                        '执行金额比率': execution_amount_ratio,
                        '被执行金额比率': executed_amount_ratio,
                        'n0值': self.df['n0'].iloc[row_idx],
                        'R11值': self.df['R11'].iloc[row_idx],
                        'fd1得分': fd1,
                        'fd2得分': fd2,
                        'fd3得分': fd3,
                        '法律信用风险总分': result['risk_scores']['legal_credit']
                    })
                pd.DataFrame(legal_details).to_excel(writer, sheet_name='法律信用风险计算', index=False)

                # 6. 导出事件风险计算详情
                event_details = []
                for idx, result in enumerate(results):
                    row_idx = idx
                    cancellation_rate = self._safe_divide(
                        self.df['已销号事件数'].iloc[row_idx],
                        self.df['年初事件数'].iloc[row_idx] + self.df['新增事件数'].iloc[row_idx]
                    )
                    reduction_rate = self._safe_divide(
                        self.df['已销号事件影响金额'].iloc[row_idx],
                        self.df['年初事件影响金额'].iloc[row_idx] + self.df['新增事件影响金额'].iloc[row_idx]
                    )
                    loss_rate = self._safe_divide(
                        self.df['未销号事件兜底保障金额'].iloc[row_idx] + self.df['未销号事件追损挽损金额'].iloc[row_idx],
                        self.df['未销号事件影响金额'].iloc[row_idx]
                    )
                    disposal_resolution_rate = self._safe_divide(
                        self.df['已销号事件数'].iloc[row_idx],
                        self.df['年初事件影响金额'].iloc[row_idx] + self.df['新增事件影响金额'].iloc[row_idx]
                    )
                    provision_coverage_rate = self._safe_divide(
                        self.df['未销号事件累计计提减值金额'].iloc[row_idx],
                        self.df['未销号事件影响金额'].iloc[row_idx] - 
                        self.df['未销号事件兜底保障金额'].iloc[row_idx] - 
                        self.df['未销号事件追损挽损金额'].iloc[row_idx]
                    )
                    
                    # 计算事件风险各项得分
                    segment20 = [
                        (lambda x, **kwargs: x >= 0.5, lambda x, **kwargs: 0),
                        (lambda x, **kwargs: (x >= 0.3) & (x < 0.5), lambda x, **kwargs: 1),
                        (lambda x, **kwargs: (x >= 0.2) & (x < 0.3), lambda x, **kwargs: 2),
                        (lambda x, **kwargs: x < 0.2, lambda x, **kwargs: 4)
                    ]
                    fe1 = self.piecewise_function(cancellation_rate, segment20)
                    
                    segment21 = [
                        (lambda x, **kwargs: x >= 0.5, lambda x, **kwargs: 0),
                        (lambda x, **kwargs: (x >= 0.3) & (x < 0.5), lambda x, **kwargs: 1),
                        (lambda x, **kwargs: (x >= 0.2) & (x < 0.3), lambda x, **kwargs: 2),
                        (lambda x, **kwargs: x < 0.2, lambda x, **kwargs: 4)
                    ]
                    fe2 = self.piecewise_function(reduction_rate, segment21)
                    
                    segment22 = [
                        (lambda x, **kwargs: x >= 0.5, lambda x, **kwargs: 0),
                        (lambda x, **kwargs: (x >= 0.3) & (x < 0.5), lambda x, **kwargs: 1),
                        (lambda x, **kwargs: (x >= 0.2) & (x < 0.3), lambda x, **kwargs: 2),
                        (lambda x, **kwargs: x < 0.2, lambda x, **kwargs: 4)
                    ]
                    fe3 = self.piecewise_function(loss_rate, segment22)
                    
                    segment23 = [
                        (lambda x, **kwargs: x >= 0.5, lambda x, **kwargs: 0),
                        (lambda x, **kwargs: (x >= 0.3) & (x < 0.5), lambda x, **kwargs: 1),
                        (lambda x, **kwargs: (x >= 0.2) & (x < 0.3), lambda x, **kwargs: 2),
                        (lambda x, **kwargs: x < 0.2, lambda x, **kwargs: 4)
                    ]
                    fe4 = self.piecewise_function(disposal_resolution_rate, segment23)
                    
                    segment24 = [
                        (lambda x, **kwargs: x >= 0.5, lambda x, **kwargs: 0),
                        (lambda x, **kwargs: (x >= 0.3) & (x < 0.5), lambda x, **kwargs: 1),
                        (lambda x, **kwargs: (x >= 0.2) & (x < 0.3), lambda x, **kwargs: 2),
                        (lambda x, **kwargs: x < 0.2, lambda x, **kwargs: 4)
                    ]
                    fe5 = self.piecewise_function(provision_coverage_rate, segment24)
                    
                    event_details.append({
                        '月份': result['period'],
                        '销号率': cancellation_rate,
                        '影响金额减少率': reduction_rate,
                        '损失率': loss_rate,
                        '处置解决率': disposal_resolution_rate,
                        '减值准备覆盖率': provision_coverage_rate,
                        '已销号事件数': self.df['已销号事件数'].iloc[row_idx],
                        '年初事件数': self.df['年初事件数'].iloc[row_idx],
                        '新增事件数': self.df['新增事件数'].iloc[row_idx],
                        '已销号事件影响金额': self.df['已销号事件影响金额'].iloc[row_idx],
                        '年初事件影响金额': self.df['年初事件影响金额'].iloc[row_idx],
                        '新增事件影响金额': self.df['新增事件影响金额'].iloc[row_idx],
                        '未销号事件兜底保障金额': self.df['未销号事件兜底保障金额'].iloc[row_idx],
                        '未销号事件追损挽损金额': self.df['未销号事件追损挽损金额'].iloc[row_idx],
                        '未销号事件影响金额': self.df['未销号事件影响金额'].iloc[row_idx],
                        '未销号事件累计计提减值金额': self.df['未销号事件累计计提减值金额'].iloc[row_idx],
                        'fe1得分': fe1,
                        'fe2得分': fe2,
                        'fe3得分': fe3,
                        'fe4得分': fe4,
                        'fe5得分': fe5,
                        '事件风险总分': result['risk_scores']['event']
                    })
                pd.DataFrame(event_details).to_excel(writer, sheet_name='事件风险计算', index=False)

                # 7. 导出信用风险和社会责任风险计算详情
                additional_risk_details = []
                for idx, result in enumerate(results):
                    row_idx = idx
                    # 计算信用风险（M1）
                    credit_risk = 5*(self.df['m1'].iloc[row_idx] + self.df['m2'].iloc[row_idx] + self.df['m3'].iloc[row_idx])
                    
                    # 计算社会责任风险（G）
                    X1 = 10 * self.df['x1'].iloc[row_idx] + 6 * self.df['x2'].iloc[row_idx] \
                         + 3 * self.df['x3'].iloc[row_idx] + 1 * self.df['x4'].iloc[row_idx]
                    Y1 = 10 * self.df['y1'].iloc[row_idx] + 5 * self.df['y2'].iloc[row_idx] \
                         + 2 * self.df['y3'].iloc[row_idx]
                    Z1 = 10 * self.df['z1'].iloc[row_idx] + 5 * self.df['z2'].iloc[row_idx]
                    social_risk = X1 + Y1 + Z1
                    
                    additional_risk_details.append({
                        '月份': result['period'],
                        'm1值': self.df['m1'].iloc[row_idx],
                        'm2值': self.df['m2'].iloc[row_idx],
                        'm3值': self.df['m3'].iloc[row_idx],
                        '信用风险总分': credit_risk,
                        'x1值': self.df['x1'].iloc[row_idx],
                        'x2值': self.df['x2'].iloc[row_idx],
                        'x3值': self.df['x3'].iloc[row_idx],
                        'x4值': self.df['x4'].iloc[row_idx],
                        'y1值': self.df['y1'].iloc[row_idx],
                        'y2值': self.df['y2'].iloc[row_idx],
                        'y3值': self.df['y3'].iloc[row_idx],
                        'z1值': self.df['z1'].iloc[row_idx],
                        'z2值': self.df['z2'].iloc[row_idx],
                        'X1得分': X1,
                        'Y1得分': Y1,
                        'Z1得分': Z1,
                        '社会责任风险总分': social_risk
                    })
                pd.DataFrame(additional_risk_details).to_excel(writer, sheet_name='信用和社会责任风险计算', index=False)

            logger.info(f"计算详情已保存至: {save_path}")
            
        except Exception as e:
            logger.error(f"导出计算详情时出错: {e}")
            raise
