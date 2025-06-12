import pandas as pd


def find_ids_sum_to_target(excel_path, target_amount):
    """
    从Excel文件中找出金额之和最接近但不超过目标金额的ID组合
    
    参数:
    excel_path (str): Excel文件路径
    target_amount (float): 目标金额
    
    返回:
    list: 包含金额之和最接近目标金额的ID组合
    """
    # 读取Excel文件的前两列数据
    df = pd.read_excel(excel_path, header=0, engine='openpyxl')
    
    id_amount_dict = {}
    for item in df.values:
        id_amount_dict[item[0]] = float(item[2])
    print(id_amount_dict)
    
    # 用于存储结果的列表和当前最大和
    result = []
    max_sum = 0
    
    # 获取所有ID列表
    ids = list(id_amount_dict.keys())
    n = len(ids)
    
    # 使用递归函数来查找所有可能的组合
    def find_combinations(start, current_ids, current_sum):
        nonlocal result, max_sum
        
        # 如果当前和小于等于目标值且大于当前找到的最大和，更新结果
        if current_sum <= target_amount and current_sum > max_sum and current_ids:
            max_sum = current_sum
            result = [current_ids.copy()]
            print(f"找到更接近的组合: {current_ids.copy()}, 金额: {current_sum}")
        # 如果当前和等于当前找到的最大和，添加到结果列表
        elif current_sum == max_sum and current_ids:
            result.append(current_ids.copy())
            print(f"找到相同金额的组合: {current_ids.copy()}, 金额: {current_sum}")
        
        if current_sum >= target_amount or start >= n:
            return
        
        for i in range(start, n):
            current_id = ids[i]
            amount = id_amount_dict[current_id]
            
            # 如果添加当前ID后超过目标金额，跳过
            if current_sum + amount > target_amount:
                continue
                
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
    print(result_combinations)
    
    # if result_combinations:
    #     # 计算组合的总金额
    #     total_amount = 0
    #     if result_combinations[0]:
    #         for id in result_combinations[0]:
    #             total_amount += id_amount_dict.get(id, 0)
                
    #     print(f"找到{len(result_combinations)}个组合，金额之和为{total_amount}，最接近目标金额{target}:")
    #     for i, combo in enumerate(result_combinations, 1):
    #         print(f"组合{i}: {combo}")
    # else:
    #     print(f"未找到符合条件的组合")
