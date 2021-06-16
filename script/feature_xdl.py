import sys
import os

def update_feature_slots_set():
    """
       更新特征列,指定特征列,进行特征和样本共现性评估
    """
    feature_slots_set = set() 
    with open(sys.argv[1]) as f:
        for line in f.readlines():
            line = line.strip()
            feature_slots_set.add(line)
    return feature_slots_set

def update_feature_info(features, label, feature_slots_set, feature_info_dict, feature_pv_sum_dict):
    """
       产出特征的pv统计词典和特征与各label取值的pv统计词典
    """
    for feature in features.split(";"): #解析样本格式,目前格式为xdl的样本格式,可自行适配自己的样本格式,slot 为特征列id 或特征组名,比如性别,年龄等,sign为特征签名或者特征值
        slot_sign = feature.split(":")[0]
        slot, sign = slot_sign.split("@")
        if slot not in feature_slots_set:
            continue
        if slot_sign not in feature_info_dict:
            feature_info_dict[slot_sign]  = {}
        if label not in feature_info_dict[slot_sign]:
            feature_info_dict[slot_sign][label] = 1
        else:
            feature_info_dict[slot_sign][label] += 1
        if slot_sign not in feature_pv_sum_dict:
            feature_pv_sum_dict[slot_sign] = 1
        else:
            feature_pv_sum_dict[slot_sign] += 1
    return feature_info_dict, feature_pv_sum_dict

def output_feature_info(feature_info_dict, feature_pv_sum_dict):
    """
        feature, label, pos_pv, pv_sum
    """
    for feature in feature_info_dict:
        for label in feature_info_dict[feature]:
            if feature not in feature_pv_sum_dict:
                continue
            print "\t".join([feature, label, str(feature_info_dict[feature][label]), str(feature_pv_sum_dict[feature])])

def main():
    feature_slots_set = update_feature_slots_set()
    feature_info_dict = {}
    feature_pv_sum_dict = {}
    for line in sys.stdin:
        line = line.strip().split("|")
        features = line[2]
        label = line[-2].split("#")[0].split(":")[0]
        update_feature_info(features, label, feature_slots_set, feature_info_dict, feature_pv_sum_dict)
    output_feature_info(feature_info_dict, feature_pv_sum_dict)

if __name__ == "__main__":
    main()
