import pandas as pd


def find_ids_sum_to_target(excel_path, target_amount):
    """
    从Excel文件中找出金额之和等于目标金额的ID组合
    
    参数:
    excel_path (str): Excel文件路径
    target_amount (float): 目标金额
    
    返回:
    list: 包含所有满足条件的ID组合列表
    """
    # 读取Excel文件的前两列数据
    df = pd.read_excel(excel_path, header=0, engine='openpyxl')
    
    id_amount_dict = {}
    for item in df.values:
        id_amount_dict[item[0]] = float(item[2])
    print(id_amount_dict)
    # 用于存储结果的列表
    result = []
    
    # 获取所有ID列表
    ids = list(id_amount_dict.keys())
    n = len(ids)
    
    # 使用递归函数来查找所有可能的组合
    def find_combinations(start, current_ids, current_sum):
        if current_sum == target_amount and current_ids:
            print(current_ids.copy())
            result.append(current_ids.copy())
            return
        
        if current_sum > target_amount or start >= n:
            return
        
        for i in range(start, n):
            current_id = ids[i]
            amount = id_amount_dict[current_id]
            
            # 尝试添加当前ID
            current_ids.append(current_id)
            find_combinations(i + 1, current_ids, current_sum + amount)
            current_ids.pop()  # 回溯
    
    # 开始查找组合
    find_combinations(0, [], 0)
    
    return result

# 示例使用
if __name__ == "__main__":
    excel_file = "/Users/zhangjinpeng/Documents/宝宝/计算和.xlsx"  # 替换为实际的Excel文件路径
    target = 24500  # 替换为目标金额
    
    result_combinations = find_ids_sum_to_target(excel_file, target)
    
    print(f"找到{len(result_combinations)}个组合，金额之和等于{target}:")
    for i, combo in enumerate(result_combinations, 1):
        print(f"组合{i}: {combo}")

