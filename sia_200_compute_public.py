# -*- coding: utf-8 -*-
"""insigoo SIA · 200 项目逻辑体检信度检验 · 公开版统计脚本

运行即复算报告第三章至第七章全部数字，与 data/sia_200_stats_public.json 一一对应。
数据来源：200 个公开募捐平台在募项目的快检符号（聚合统计，不含任何项目实名或编号）。
计分口径：✅=1 / ⚠️=0.5 / ❌=0，满分 10 分；分档 ≥6 / 3–5.5 / <3。
信度口径：200×10 = 2000 符号位，双人独立盲判逐符号一致率 84.15%，判定 REVIEW。
重要边界：本报告是方法学信度记录，publishable=false，不得排序或按"已达标"引用。
"""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(BASE, "data", "sia_200_stats_public.json")
D = json.load(open(P, encoding="utf-8"))

OV = D["overall"]
TD = D["tier_dist"]
CO = D["consistency"]
DP = D["deep"]


def pct(a, b):
    return 100.0 * a / b if b else 0.0


print("=" * 60)
print("insigoo SIA · 200 项目逻辑体检信度检验 · 数字复算")
print("=" * 60)

print("\n[一] 样本与总体")
print("  样本量 n            =", D["meta"]["n"])
print("  平均分              = %.2f / 10" % OV["mean"])
print("  中位数 / 标准差     = %.1f / %.2f" % (OV["median"], OV["sd"]))
print("  分数区间            = %.1f – %.1f" % (OV["min"], OV["max"]))

print("\n[二] 分档")
for k in ["优先推进", "补充复评", "暂不推荐"]:
    v = TD[k]
    print("  %-6s n=%3d  pct=%.1f%%" % (k, v["n"], v["pct"]))
print("  分档合计            =", sum(v["n"] for v in TD.values()))

print("\n[三] 十项逐题（均分 = (✅×1 + ⚠️×0.5) / n）")
n = D["meta"]["n"]
for q, v in D["by_item"].items():
    calc = (v["pass"] * 1.0 + v["warn"] * 0.5) / n
    print("  %-3s 均分=%.2f  报告=%.2f  ✅=%3d ⚠️=%3d ❌=%3d  校验=%s"
          % (q, calc, v["mean"], v["pass"], v["warn"], v["fail"],
             "OK" if abs(calc - v["mean"]) < 0.011 else "DIFF"))

print("\n[四] 披露充分度分层")
for k, v in sorted(D["by_strata"].items(), key=lambda x: str(x[0])):
    print("  命中%s项  n=%3d  占比=%.1f%%  层内均分=%.2f  优先推进占比=%.1f%%"
          % (k, v["n"], v["pct"], v["mean"], v["priority_pct"]))

print("\n[五] 公开披露缺口")
g = D["disclosure_gap"]
gap0 = g["total_candidates"] - g["total_qualified"]
print("  候选 %d / 合格 %d / 三项全空 %d (%.1f%%)"
      % (g["total_candidates"], g["total_qualified"], gap0, g["gap_pct"]))
for c, v in sorted(g["by_cate"].items()):
    print("    %-6s 候选=%3d 全空=%3d 缺口率=%.1f%%"
          % (c, v["candidates"], v["hits0"], v["gap_pct"]))

print("\n[六] 四模块深度评级（30 份 × 4 模块 = 120 评级）")
for m, v in DP["by_level"].items():
    print("  %-28s %s" % (m, v))
print("  档位总计:", DP["level_totals"])

print("\n[七] 信度")
print("  符号位 %d / 一致 %d / 一致率 %.2f%% / 判定 %s"
      % (CO["symbol_positions"], CO["same"], CO["agreement_pct"], CO["verdict"]))
print("  分歧 %d（计算一致率校验 %.2f%%）"
      % (CO["diff"], pct(CO["same"], CO["symbol_positions"])))

print("\n" + "=" * 60)
print("边界：一致率 84.15% 属 REVIEW，未达 90% PASS 门槛；")
print("      publishable=false，分数不得排序或对外按已达标引用。")
print("=" * 60)
