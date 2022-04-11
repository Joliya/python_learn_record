# -*- encoding: utf-8 -*-
"""
一个基因片段是A，G，T，C四种碱基构成的序列。疯狂科学家把霸王龙的基因序列和老虎的基因序列混合起来，制造了新的生物霸王虎。混合的时候轮流从
两个序列读一段随机长度的序列，放到新序列中，直到两个序列都读完。也就是说碱基的顺序不变，只是相互交织起来。现在警察要写一个函数，输入三个基因序列，
判断第三个序列是前两个序列混合而成以此证明杀人的霸王虎就是霸王龙和老虎混合成的。可以用递归，不用考虑性能。
例如:
序列1:“AGGGCT” 序列2:“CGGAT”
序列3:“ACGGGCGGATT” 输出:True
序列1:“AGCT”序列 2:“TCGA”
序列3:“AGTCTCGA” 输出: True
序列1:“AGCTT" 序列2:“CCCC”
序列3:“ACCCCGTTC” 输出:False
"""

from __future__ import absolute_import, unicode_literals


def new_tiger(gene_1, gene_2, new_gene):
    """
    todo: 有问题，解决不了用例第三条的问题
    判断新的基因序列是否是 前两个基因序列混合而成
    :param gene_1: 基因序列1
    :param gene_2: 基因序列1
    :param new_gene: 新的基因序列
    :return:
    """

    index = 0
    image_gene_1 = []
    image_gene_2 = []
    for i in gene_1:
        for j in range(index, len(new_gene)):
            if new_gene[j] == i:
                image_gene_1.append(new_gene[j])
                index = j + 1
                break
            else:
                image_gene_2.append(new_gene[j])

    for i in range(index, len(new_gene)):
        image_gene_2.append(new_gene[i])
    image_gene_1_str = "".join(image_gene_1)
    image_gene_2_str = "".join(image_gene_2)
    if image_gene_1_str == gene_1 and image_gene_2_str == gene_2:
        return True
    return False


def new_tiger2(gene_1, gene_2, new_gene):
    """
    判断新的基因序列是否是 前两个基因序列混合而成
    :param gene_1: 基因序列1
    :param gene_2: 基因序列1
    :param new_gene: 新的基因序列
    :return:
    """
    gene_1_len = len(gene_1)
    gene_2_len = len(gene_2)
    new_gene_len = len(new_gene)
    if gene_1_len + gene_2_len != new_gene_len:
        return False
    return help(gene_1, gene_1_len, 0, gene_2, gene_2_len, 0, new_gene, new_gene_len, 0)


def help(gene_1, gene_1_len, index_1, gene_2, gene_2_len, index_2, new_gene, new_gene_len, index):
    if gene_1_len == index_1 and gene_2_len == index_2 and new_gene_len == index:
        return True
    if gene_1_len > index_1 and gene_1[index_1] == new_gene[index]:
        result_1 = help(gene_1, gene_1_len, index_1 + 1, gene_2, gene_2_len, index_2, new_gene, new_gene_len, index + 1)
        if result_1:
            return result_1
    if gene_2_len > index_2 and gene_2[index_2] == new_gene[index]:
        result_2 = help(gene_1, gene_1_len, index_1, gene_2, gene_2_len, index_2 + 1, new_gene, new_gene_len, index + 1)
        if result_2:
            return result_2
    return False


if __name__ == '__main__':

    gene_1 = "AGGGCT"
    gene_2 = "CGGAT"
    new_gene = "ACGGGCGGATT"
    print(new_tiger2(gene_1, gene_2, new_gene))  # True

    gene_1 = "AGCT"
    gene_2 = "TCGA"
    new_gene = "AGTCTCGA"
    print(new_tiger2(gene_1, gene_2, new_gene))  # True

    gene_1 = "AGCTT"
    gene_2 = "CCCC"
    new_gene = "ACCCCGTTC"
    print(new_tiger2(gene_1, gene_2, new_gene))  # False

    gene_1 = "AAATATGC"
    gene_2 = "AAAGTAAC"
    new_gene = "AAAGAAATTAATAGCC"
    print(new_tiger2(gene_1, gene_2, new_gene))  # True

    gene_1 = "AACCTTGG"
    gene_2 = "AATCTGGC"
    new_gene = "AAAGAAATTAATAGCC"
    print(new_tiger2(gene_1, gene_2, new_gene))  # False

    gene_1 = "AGT"
    gene_2 = "ACT"
    new_gene = "AACGTT"
    print(new_tiger2(gene_1, gene_2, new_gene))  # True
