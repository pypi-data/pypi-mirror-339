# 风险评估模型库

这是一个用于企业风险评估的Python库，提供了完整的风险评估功能，包括数据加载、风险计算、结果导出和可视化。

## 安装

```bash
pip install risk-assessment
```

## 功能特点

- 支持从Excel文件加载数据
- 计算多种风险类型（战略风险、财务风险、市场风险等）
- 生成详细的风险评估报告
- 可视化风险评分结果
- 支持自定义配置参数

## 使用示例

### 基本用法

```python
from risk_assessment_package import assess_risk

# 使用示例
excel_path = "test.xlsx"  # 替换为你的Excel文件路径
sheet_name = "Sheet3"     # 可选：指定工作表名称
    
try:
    # 执行风险评估
    result = assess_risk(excel_path, sheet_name=sheet_name)
    
    # 打印结果
    print("\n=== 风险评估结果 ===")
    for risk_result in result['results']:
        print(f"\n期间: {risk_result['period']}月")
        print(f"总风险评分: {risk_result['total_score']:.2f}")
        print(f"风险等级: {risk_result['risk_level']}")
        if risk_result.get('risk_basis') == 'threshold':
            print("【A类风险】触发原因：")
            for reason in risk_result['risk_reasons']:
                print(f"  - {reason}")
        
except Exception as e:
    print(f"错误: {e}")
```

### 使用自定义配置

```python
from risk_assessment_package import assess_risk

# 使用自定义配置文件执行风险评估
result = assess_risk(
    excel_path="test.xlsx", 
    sheet_name="Sheet3", 
    config_path="custom_config.yaml"
)
```

### 输出文件说明

使用`assess_risk`函数后会自动生成三个文件：
1. `your_data_results.xlsx` - 风险评估结果
2. `your_data_details.xlsx` - 详细计算过程
3. `your_data_chart.png` - 风险评分图表

返回值是一个字典，包含以下键：
- `results`: 风险评估结果的列表
- `results_path`: 结果Excel文件的路径
- `details_path`: 详细计算过程的Excel文件路径
- `chart_path`: 风险图表的图片路径

## 命令行使用

安装后，还可以通过命令行直接使用：

```bash
risk-assessment your_data.xlsx
```

## 数据格式要求

输入Excel文件需要满足以下要求：

1. 数据格式：
   - 第一列必须是指标名称
   - 后续列是各月份的数据
   - 第一行是列名（月份或其他时间标识）

2. 工作表选择：
   - 默认读取第一个工作表
   - 可以通过 `sheet_name` 参数指定工作表
   - 支持工作表名称或索引号

3. 必需的数据列：
   - 主营业务收入
   - 总营业务收入
   - 主营业务成本
   - 总业务成本
   - 主营业务费用
   - 研发费用
   - 负债总额
   - 资产总额
   - 带息负债总额
   - 经营现金流入
   - 经营现金流出
   - 经营净现金流
   - 投资分红等收益
   - 利息支出
   - 预付账款
   - 预收账款
   - 应收账款
   - 应付账款
   - 净资产
   - 应收账款总额
   - 坏账准备金额
   - 存货
   - 企业当年涉及司法诉讼案件的数量
   - 执行金额
   - 被执行金额
   - 已销号事件数
   - 年初事件数
   - 新增事件数
   - 已销号事件影响金额
   - 年初事件影响金额
   - 新增事件影响金额
   - 未销号事件兜底保障金额
   - 未销号事件追损挽损金额
   - 未销号事件累计计提减值金额
   - 未销号事件影响金额
   - 已处置金额
   - R1-R11（风险阈值参数）
   - n0（风险阈值参数）
   - m1-m3（信用风险参数）
   - x1-x5（社会责任风险参数）
   - y1-y4（社会责任风险参数）
   - z1-z3（社会责任风险参数）
   - 行业较差值
   - 货币资金
   - 财务费用中的利息费用

## 配置说明

可以通过YAML配置文件自定义以下参数：

- 各类风险的权重
- 风险阈值参数
- 计算参数

配置文件示例：

```yaml
weights:
  strategic: 0.25
  financial: 0.30
  market: 0.20
  legal_credit: 0.15
  event: 0.10
```

## 输出结果

风险评估结果包含：

1. 总体风险评分
2. 各项风险评分
3. 风险等级
4. 风险判断依据
5. 详细的计算过程

## 故障排除

如果遇到问题，可以检查：
- Excel文件格式是否正确
- 必要的依赖是否都已安装（pandas, numpy, matplotlib, openpyxl, PyYAML）
- 配置文件的格式是否正确

程序默认会在控制台输出日志信息，可以查看更多执行细节。

## 许可证

MIT License

## 贡献

欢迎提交问题和改进建议！ 