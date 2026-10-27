"""
Build complete Power BI Report Layout with fully bound visuals, queries, and data transforms.
Ensures every visual renders immediately on the Power BI Desktop canvas without user dragging!
"""

import os
import json
import uuid

BASE_DIR = r"D:\Admin\Documents\mutual_fund_analysis"
REPORT_DIR = os.path.join(BASE_DIR, "bluestock_mf_dashboard.Report")
os.makedirs(REPORT_DIR, exist_ok=True)

def make_card(entity, prop, func=0, display_name=None, x=10, y=10, w=280, h=110, z=0):
    vc_name = uuid.uuid4().hex[:20]
    agg_name = f"Agg_{prop}"
    from_name = entity[:1].lower()
    disp = display_name or prop
    
    config = {
        "name": vc_name,
        "layouts": [{"id": 0, "position": {"x": x, "y": y, "z": z, "width": w, "height": h, "tabOrder": z}}],
        "singleVisual": {
            "visualType": "cardVisual",
            "projections": {"Data": [{"queryRef": agg_name}]},
            "prototypeQuery": {
                "Version": 2,
                "From": [{"Name": from_name, "Entity": entity, "Type": 0}],
                "Select": [{
                    "Aggregation": {
                        "Expression": {"Column": {"Expression": {"SourceRef": {"Source": from_name}}, "Property": prop}},
                        "Function": func
                    },
                    "Name": agg_name,
                    "NativeReferenceName": disp
                }]
            }
        }
    }
    
    query = {
        "Commands": [{
            "SemanticQueryDataShapeCommand": {
                "Query": {
                    "Version": 2,
                    "From": [{"Name": from_name, "Entity": entity, "Type": 0}],
                    "Select": [{
                        "Aggregation": {
                            "Expression": {"Column": {"Expression": {"SourceRef": {"Source": from_name}}, "Property": prop}},
                            "Function": func
                        },
                        "Name": agg_name,
                        "NativeReferenceName": disp
                    }]
                },
                "Binding": {"Primary": {"Groupings": [{"Projections": [0]}]}, "Version": 1},
                "ExecutionMetricsKind": 1
            }
        }]
    }
    
    data_transforms = {
        "projectionOrdering": {"Data": [0]},
        "queryMetadata": {"Select": [{"Restatement": disp, "Name": agg_name, "Type": 1}]},
        "visualElements": [{"DataRoles": [{"Name": "Data", "Projection": 0, "isActive": False}]}],
        "selects": [{
            "displayName": disp,
            "queryName": agg_name,
            "roles": {"Data": True},
            "type": {"category": None, "underlyingType": 259},
            "expr": {
                "Aggregation": {
                    "Expression": {"Column": {"Expression": {"SourceRef": {"Entity": entity}}, "Property": prop}},
                    "Function": func
                }
            }
        }]
    }
    
    return {
        "x": x, "y": y, "width": w, "height": h, "z": z,
        "config": json.dumps(config),
        "query": json.dumps(query),
        "dataTransforms": json.dumps(data_transforms)
    }

def make_bar_chart(entity, cat_prop, val_prop, func=0, visual_type="clusteredBarChart", x=10, y=10, w=500, h=400, z=0):
    vc_name = uuid.uuid4().hex[:20]
    from_name = entity[:1].lower()
    cat_query_name = f"{entity}.{cat_prop}"
    val_query_name = f"Sum({entity}.{val_prop})"
    
    config = {
        "name": vc_name,
        "layouts": [{"id": 0, "position": {"x": x, "y": y, "z": z, "width": w, "height": h, "tabOrder": z}}],
        "singleVisual": {
            "visualType": visual_type,
            "projections": {
                "Category": [{"queryRef": cat_query_name, "active": True}],
                "Y": [{"queryRef": val_query_name}]
            },
            "prototypeQuery": {
                "Version": 2,
                "From": [{"Name": from_name, "Entity": entity, "Type": 0}],
                "Select": [
                    {
                        "Column": {"Expression": {"SourceRef": {"Source": from_name}}, "Property": cat_prop},
                        "Name": cat_query_name,
                        "NativeReferenceName": cat_prop
                    },
                    {
                        "Aggregation": {
                            "Expression": {"Column": {"Expression": {"SourceRef": {"Source": from_name}}, "Property": val_prop}},
                            "Function": func
                        },
                        "Name": val_query_name,
                        "NativeReferenceName": f"Sum of {val_prop}"
                    }
                ],
                "OrderBy": [{
                    "Direction": 2,
                    "Expression": {
                        "Aggregation": {
                            "Expression": {"Column": {"Expression": {"SourceRef": {"Source": from_name}}, "Property": val_prop}},
                            "Function": func
                        }
                    }
                }]
            }
        }
    }
    
    query = {
        "Commands": [{
            "SemanticQueryDataShapeCommand": {
                "Query": {
                    "Version": 2,
                    "From": [{"Name": from_name, "Entity": entity, "Type": 0}],
                    "Select": [
                        {
                            "Column": {"Expression": {"SourceRef": {"Source": from_name}}, "Property": cat_prop},
                            "Name": cat_query_name,
                            "NativeReferenceName": cat_prop
                        },
                        {
                            "Aggregation": {
                                "Expression": {"Column": {"Expression": {"SourceRef": {"Source": from_name}}, "Property": val_prop}},
                                "Function": func
                            },
                            "Name": val_query_name,
                            "NativeReferenceName": f"Sum of {val_prop}"
                        }
                    ],
                    "OrderBy": [{
                        "Direction": 2,
                        "Expression": {
                            "Aggregation": {
                                "Expression": {"Column": {"Expression": {"SourceRef": {"Source": from_name}}, "Property": val_prop}},
                                "Function": func
                            }
                        }
                    }]
                },
                "Binding": {"Primary": {"Groupings": [{"Projections": [0, 1]}]}, "Version": 1},
                "ExecutionMetricsKind": 1
            }
        }]
    }
    
    data_transforms = {
        "projectionOrdering": {"Category": [0], "Y": [1]},
        "projectionActiveItems": {"Category": [{"queryRef": cat_query_name, "suppressConcat": False}]},
        "queryMetadata": {
            "Select": [
                {"Restatement": cat_prop, "Name": cat_query_name, "Type": 2048},
                {"Restatement": f"Sum of {val_prop}", "Name": val_query_name, "Type": 1}
            ]
        },
        "visualElements": [{"DataRoles": [{"Name": "Category", "Projection": 0, "isActive": True}, {"Name": "Y", "Projection": 1, "isActive": False}]}],
        "selects": [
            {
                "displayName": cat_prop,
                "queryName": cat_query_name,
                "roles": {"Category": True},
                "type": {"category": None, "underlyingType": 1},
                "expr": {"Column": {"Expression": {"SourceRef": {"Entity": entity}}, "Property": cat_prop}}
            },
            {
                "displayName": f"Sum of {val_prop}",
                "queryName": val_query_name,
                "roles": {"Y": True},
                "sort": 2,
                "sortOrder": 0,
                "type": {"category": None, "underlyingType": 259},
                "expr": {
                    "Aggregation": {
                        "Expression": {"Column": {"Expression": {"SourceRef": {"Entity": entity}}, "Property": val_prop}},
                        "Function": func
                    }
                }
            }
        ]
    }
    
    return {
        "x": x, "y": y, "width": w, "height": h, "z": z,
        "config": json.dumps(config),
        "query": json.dumps(query),
        "dataTransforms": json.dumps(data_transforms)
    }

def make_donut(entity, cat_prop, val_prop, func=0, x=10, y=10, w=350, h=300, z=0):
    res = make_bar_chart(entity, cat_prop, val_prop, func, visual_type="donutChart", x=x, y=y, w=w, h=h, z=z)
    return res

def make_slicer(entity, prop, x=10, y=10, w=200, h=80, z=0):
    vc_name = uuid.uuid4().hex[:20]
    from_name = entity[:1].lower()
    q_name = f"{entity}.{prop}"
    
    config = {
        "name": vc_name,
        "layouts": [{"id": 0, "position": {"x": x, "y": y, "z": z, "width": w, "height": h, "tabOrder": z}}],
        "singleVisual": {
            "visualType": "slicer",
            "projections": {"Values": [{"queryRef": q_name, "active": True}]},
            "prototypeQuery": {
                "Version": 2,
                "From": [{"Name": from_name, "Entity": entity, "Type": 0}],
                "Select": [{
                    "Column": {"Expression": {"SourceRef": {"Source": from_name}}, "Property": prop},
                    "Name": q_name,
                    "NativeReferenceName": prop
                }]
            }
        }
    }
    
    query = {
        "Commands": [{
            "SemanticQueryDataShapeCommand": {
                "Query": {
                    "Version": 2,
                    "From": [{"Name": from_name, "Entity": entity, "Type": 0}],
                    "Select": [{
                        "Column": {"Expression": {"SourceRef": {"Source": from_name}}, "Property": prop},
                        "Name": q_name,
                        "NativeReferenceName": prop
                    }]
                },
                "Binding": {"Primary": {"Groupings": [{"Projections": [0]}]}, "Version": 1},
                "ExecutionMetricsKind": 1
            }
        }]
    }
    
    data_transforms = {
        "objects": {"data": [{"properties": {"mode": {"expr": {"Literal": {"Value": "'Basic'"}}}}}]},
        "projectionOrdering": {"Values": [0]},
        "projectionActiveItems": {"Values": [{"queryRef": q_name, "suppressConcat": False}]},
        "queryMetadata": {"Select": [{"Restatement": prop, "Name": q_name, "Type": 2048}]},
        "visualElements": [{"DataRoles": [{"Name": "Values", "Projection": 0, "isActive": True}]}],
        "selects": [{
            "displayName": prop,
            "queryName": q_name,
            "roles": {"Values": True},
            "type": {"category": None, "underlyingType": 1},
            "expr": {"Column": {"Expression": {"SourceRef": {"Entity": entity}}, "Property": prop}}
        }]
    }
    
    return {
        "x": x, "y": y, "width": w, "height": h, "z": z,
        "config": json.dumps(config),
        "query": json.dumps(query),
        "dataTransforms": json.dumps(data_transforms)
    }

def make_table(entity, cols, x=10, y=10, w=1240, h=300, z=0):
    vc_name = uuid.uuid4().hex[:20]
    from_name = entity[:1].lower()
    
    projections_values = []
    select_items = []
    meta_select = []
    selects_dt = []
    ordering = list(range(len(cols)))
    
    for i, col in enumerate(cols):
        q_name = f"{entity}.{col}"
        projections_values.append({"queryRef": q_name})
        select_items.append({
            "Column": {"Expression": {"SourceRef": {"Source": from_name}}, "Property": col},
            "Name": q_name,
            "NativeReferenceName": col
        })
        meta_select.append({"Restatement": col, "Name": q_name, "Type": 2048 if i<2 else 1})
        selects_dt.append({
            "displayName": col,
            "queryName": q_name,
            "roles": {"Values": True},
            "type": {"category": None, "underlyingType": 1},
            "expr": {"Column": {"Expression": {"SourceRef": {"Entity": entity}}, "Property": col}}
        })
        
    config = {
        "name": vc_name,
        "layouts": [{"id": 0, "position": {"x": x, "y": y, "z": z, "width": w, "height": h, "tabOrder": z}}],
        "singleVisual": {
            "visualType": "tableEx",
            "projections": {"Values": projections_values},
            "prototypeQuery": {
                "Version": 2,
                "From": [{"Name": from_name, "Entity": entity, "Type": 0}],
                "Select": select_items
            }
        }
    }
    
    query = {
        "Commands": [{
            "SemanticQueryDataShapeCommand": {
                "Query": {
                    "Version": 2,
                    "From": [{"Name": from_name, "Entity": entity, "Type": 0}],
                    "Select": select_items
                },
                "Binding": {"Primary": {"Groupings": [{"Projections": ordering}]}, "Version": 1},
                "ExecutionMetricsKind": 1
            }
        }]
    }
    
    data_transforms = {
        "projectionOrdering": {"Values": ordering},
        "queryMetadata": {"Select": meta_select},
        "visualElements": [{"DataRoles": [{"Name": "Values", "Projection": i, "isActive": False} for i in ordering]}],
        "selects": selects_dt
    }
    
    return {
        "x": x, "y": y, "width": w, "height": h, "z": z,
        "config": json.dumps(config),
        "query": json.dumps(query),
        "dataTransforms": json.dumps(data_transforms)
    }

def make_scatter(entity, detail_col, x_col, y_col, size_col=None, x=10, y=10, w=600, h=330, z=0):
    vc_name = uuid.uuid4().hex[:20]
    from_name = entity[:1].lower()
    
    q_detail = f"{entity}.{detail_col}"
    q_x = f"Avg({entity}.{x_col})"
    q_y = f"Avg({entity}.{y_col})"
    
    select_items = [
        {"Column": {"Expression": {"SourceRef": {"Source": from_name}}, "Property": detail_col}, "Name": q_detail, "NativeReferenceName": detail_col},
        {"Aggregation": {"Expression": {"Column": {"Expression": {"SourceRef": {"Source": from_name}}, "Property": x_col}}, "Function": 1}, "Name": q_x, "NativeReferenceName": f"Avg of {x_col}"},
        {"Aggregation": {"Expression": {"Column": {"Expression": {"SourceRef": {"Source": from_name}}, "Property": y_col}}, "Function": 1}, "Name": q_y, "NativeReferenceName": f"Avg of {y_col}"}
    ]
    
    projections = {
        "Details": [{"queryRef": q_detail, "active": True}],
        "X": [{"queryRef": q_x}],
        "Y": [{"queryRef": q_y}]
    }
    
    if size_col:
        q_size = f"Sum({entity}.{size_col})"
        select_items.append({"Aggregation": {"Expression": {"Column": {"Expression": {"SourceRef": {"Source": from_name}}, "Property": size_col}}, "Function": 0}, "Name": q_size, "NativeReferenceName": f"Sum of {size_col}"})
        projections["Size"] = [{"queryRef": q_size}]
        
    config = {
        "name": vc_name,
        "layouts": [{"id": 0, "position": {"x": x, "y": y, "z": z, "width": w, "height": h, "tabOrder": z}}],
        "singleVisual": {
            "visualType": "scatterChart",
            "projections": projections,
            "prototypeQuery": {
                "Version": 2,
                "From": [{"Name": from_name, "Entity": entity, "Type": 0}],
                "Select": select_items
            }
        }
    }
    
    query = {
        "Commands": [{
            "SemanticQueryDataShapeCommand": {
                "Query": {
                    "Version": 2,
                    "From": [{"Name": from_name, "Entity": entity, "Type": 0}],
                    "Select": select_items
                },
                "Binding": {"Primary": {"Groupings": [{"Projections": list(range(len(select_items)))}]}, "Version": 1},
                "ExecutionMetricsKind": 1
            }
        }]
    }
    
    data_transforms = {
        "projectionOrdering": {"Details": [0], "X": [1], "Y": [2]} | ({"Size": [3]} if size_col else {}),
        "queryMetadata": {"Select": [{"Restatement": item["NativeReferenceName"], "Name": item["Name"], "Type": 1} for item in select_items]},
        "visualElements": [{"DataRoles": [{"Name": k, "Projection": i, "isActive": (k == "Details")} for i, k in enumerate(projections.keys())]}],
        "selects": [
            {"displayName": detail_col, "queryName": q_detail, "roles": {"Details": True}, "type": {"category": None, "underlyingType": 1}, "expr": {"Column": {"Expression": {"SourceRef": {"Entity": entity}}, "Property": detail_col}}},
            {"displayName": f"Avg of {x_col}", "queryName": q_x, "roles": {"X": True}, "type": {"category": None, "underlyingType": 259}, "expr": {"Aggregation": {"Expression": {"Column": {"Expression": {"SourceRef": {"Entity": entity}}, "Property": x_col}}, "Function": 1}}},
            {"displayName": f"Avg of {y_col}", "queryName": q_y, "roles": {"Y": True}, "type": {"category": None, "underlyingType": 259}, "expr": {"Aggregation": {"Expression": {"Column": {"Expression": {"SourceRef": {"Entity": entity}}, "Property": y_col}}, "Function": 1}}}
        ] + ([{"displayName": f"Sum of {size_col}", "queryName": q_size, "roles": {"Size": True}, "type": {"category": None, "underlyingType": 259}, "expr": {"Aggregation": {"Expression": {"Column": {"Expression": {"SourceRef": {"Entity": entity}}, "Property": size_col}}, "Function": 0}}}] if size_col else [])
    }
    
    return {
        "x": x, "y": y, "width": w, "height": h, "z": z,
        "config": json.dumps(config),
        "query": json.dumps(query),
        "dataTransforms": json.dumps(data_transforms)
    }

print("Visual builders compiled. Assembling full 4-page report...")

# Build Page 1: Industry Overview
p1_vcs = [
    make_card("fact_aum", "aum_lakh_crore", func=0, display_name="Total AUM (₹ Lakh Cr)", x=20, y=15, w=290, h=110, z=0),
    make_card("monthly_sip_inflows", "sip_inflow_crore", func=4, display_name="Monthly SIP Inflow (₹ Cr)", x=330, y=15, w=290, h=110, z=1),
    make_card("industry_folio_count", "total_folios_crore", func=4, display_name="Mutual Fund Folios (Cr)", x=640, y=15, w=290, h=110, z=2),
    make_card("fact_aum", "num_schemes", func=4, display_name="Active Schemes", x=950, y=15, w=310, h=110, z=3),
    make_bar_chart("monthly_sip_inflows", "month", "sip_inflow_crore", func=0, visual_type="lineChart", x=20, y=140, w=600, h=550, z=4),
    make_bar_chart("fact_aum", "fund_house", "aum_lakh_crore", func=0, visual_type="clusteredBarChart", x=640, y=140, w=620, h=550, z=5)
]

# Build Page 2: Fund Performance
p2_vcs = [
    make_slicer("fact_performance", "category", x=20, y=15, w=380, h=80, z=0),
    make_slicer("fact_performance", "plan", x=420, y=15, w=380, h=80, z=1),
    make_slicer("fact_performance", "risk_grade", x=820, y=15, w=440, h=80, z=2),
    make_scatter("fact_performance", "scheme_name", "return_3yr_pct", "std_dev_ann_pct", "aum_crore", x=20, y=110, w=600, h=300, z=3),
    make_bar_chart("fact_performance", "category", "return_3yr_pct", func=1, visual_type="columnChart", x=640, y=110, w=620, h=300, z=4),
    make_table("fact_performance", ["scheme_name", "category", "return_3yr_pct", "sharpe_ratio", "expense_ratio_pct"], x=20, y=425, w=1240, h=280, z=5)
]

# Build Page 3: Investor Analytics
p3_vcs = [
    make_slicer("fact_transactions", "city_tier", x=20, y=15, w=380, h=80, z=0),
    make_slicer("fact_transactions", "age_group", x=420, y=15, w=380, h=80, z=1),
    make_slicer("fact_transactions", "gender", x=820, y=15, w=440, h=80, z=2),
    make_bar_chart("fact_transactions", "state", "amount_inr", func=0, visual_type="clusteredBarChart", x=20, y=110, w=480, h=590, z=3),
    make_donut("fact_transactions", "transaction_type", "amount_inr", func=0, x=520, y=110, w=360, h=280, z=4),
    make_bar_chart("fact_transactions", "age_group", "amount_inr", func=1, visual_type="columnChart", x=900, y=110, w=360, h=280, z=5),
    make_bar_chart("fact_transactions", "transaction_date", "amount_inr", func=0, visual_type="lineChart", x=520, y=410, w=740, h=290, z=6)
]

# Build Page 4: SIP & Market Trends
p4_vcs = [
    make_bar_chart("monthly_sip_inflows", "month", "sip_inflow_crore", func=0, visual_type="columnChart", x=20, y=15, w=1240, h=340, z=0),
    make_bar_chart("category_inflows", "category", "net_inflow_crore", func=0, visual_type="clusteredBarChart", x=20, y=375, w=650, h=330, z=1),
    make_bar_chart("monthly_sip_inflows", "month", "active_sip_accounts_crore", func=4, visual_type="lineChart", x=690, y=375, w=570, h=330, z=2)
]

full_report = {
    "config": json.dumps({
        "version": "5.50",
        "themeCollection": {"baseTheme": {"name": "CY25SU12", "version": "1.0", "type": 2}}
    }),
    "layoutOptimization": 0,
    "sections": [
        {"name": "Section_P1", "displayName": "1. Industry Overview", "ordinal": 0, "width": 1280, "height": 720, "visualContainers": p1_vcs},
        {"name": "Section_P2", "displayName": "2. Fund Performance", "ordinal": 1, "width": 1280, "height": 720, "visualContainers": p2_vcs},
        {"name": "Section_P3", "displayName": "3. Investor Analytics", "ordinal": 2, "width": 1280, "height": 720, "visualContainers": p3_vcs},
        {"name": "Section_P4", "displayName": "4. SIP & Market Trends", "ordinal": 3, "width": 1280, "height": 720, "visualContainers": p4_vcs}
    ]
}

report_json_path = os.path.join(REPORT_DIR, "report.json")
with open(report_json_path, "w", encoding="utf-8") as f:
    json.dump(full_report, f, indent=2)

print(f"Generated complete report.json with 22 fully bound live visuals across 4 pages!")
print(f"Saved: {report_json_path}")
