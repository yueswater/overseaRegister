PAYMENT_METADATA = {
    "學費": {"amount": 6240, "required": False, "reducible": True, "ask": False},
    "雜費": {"amount": 1820, "required": False, "reducible": True, "ask": False},
    "實習實驗費": {"amount": 0, "required": True, "reducible": False, "ask": False},
    "電腦及網路通訊使用費": {
        "amount": 400,
        "required": True,
        "reducible": False,
        "ask": False,
    },
    "平時課輔費": {"amount": 0, "required": False, "reducible": False, "ask": True},
    "住宿費": {"amount": 4800, "required": False, "reducible": False, "ask": True},
    "班級費": {"amount": 50, "required": True, "reducible": False, "ask": False},
    "家長會費": {"amount": 100, "required": True, "reducible": False, "ask": False},
    "學生團體保險費": {
        "amount": 200,
        "required": True,
        "reducible": False,
        "ask": False,
    },
    "班級冷氣維護費": {
        "amount": 200,
        "required": True,
        "reducible": False,
        "ask": False,
    },
    "僑生健康保險費": {"amount": 0, "required": False, "reducible": True, "ask": False},
    "僑生保險費": {"amount": 600, "required": False, "reducible": False, "ask": True},
    "宿舍冷氣維護費": {
        "amount": 500,
        "required": False,
        "reducible": False,
        "ask": True,
    },
    "伙食費": {"amount": 11050, "required": False, "reducible": False, "ask": True},
    "新生健檢費": {"amount": 450, "required": True, "reducible": False, "ask": False},
    "書籍費": {"amount": 2962, "required": True, "reducible": False, "ask": False},
    "模擬考費": {"amount": 20, "required": True, "reducible": False, "ask": False},
    "跑班冷氣費": {"amount": 20, "required": False, "reducible": False, "ask": True},
}

REQUIRED_ITEMS = [k for k, v in PAYMENT_METADATA.items() if v["required"]]
REDUCIBLE_ITEMS = [k for k, v in PAYMENT_METADATA.items() if v["reducible"]]
OPTIONAL_ITEMS = [k for k, v in PAYMENT_METADATA.items() if v["ask"]]
ALL_ITEMS = list(PAYMENT_METADATA.keys())
