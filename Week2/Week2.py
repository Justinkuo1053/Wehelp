# Q1
print("----------Q1----------")
green_station = [
  'Songshan', 'Nanjing Sanmin', 'Taipei Arena', 'Nanjing Fuxing',
  'Songjiang Nanjing', 'Zhongshan', 'Beimen', 'Ximen', 'Xiaonanmen',
  'Chiang Kai-Shek Memorial Hall', 'Guting', 'Taipower Building',
  'Gongguan', 'Wanlong', 'Jingmei', 'Dapinglin', 'Qizhang', 'Xiaobitan',
  'Xindian City Hall', 'Xindian'
]

messages = {
  "Bob": "I'm at Ximen MRT station.",
  "Mary": "I have a drink near Jingmei MRT station.",
  "Copper": "I just saw a concert at Taipei Arena.",
  "Leslie": "I'm at home near Xiaobitan station.",
  "Vivian": "I'm at Xindian station waiting for you."
}

def clean_up(messages):
  clean_messages = messages.copy()
  for message, text in messages.items():
    for station in green_station:
      if "Xiaobitan" in text:
        clean_messages[message] = green_station.index("Qizhang") + 0.1
        break
      elif "Xindian City Hall" in text:
        clean_messages[message] = green_station.index("Xindian City Hall")
        break
      elif station in text:
        clean_messages[message] = green_station.index(station)
        break
  return clean_messages

def find_and_print(messages, current_station):
  current_station_index = green_station.index(current_station)
  cleaned_messages = clean_up(messages)

  for message, index in cleaned_messages.items():
    cleaned_messages[message] = abs(index - current_station_index)

  min_distance = min(cleaned_messages.values())
  closest_message_key = None

  for key, value in cleaned_messages.items():
    if value == min_distance:
      closest_message_key = key
      break

  print(closest_message_key)

find_and_print(messages, "Wanlong")  # Should print "Mary"
find_and_print(messages, "Songshan") # print Copper
find_and_print(messages, "Qizhang") # print Leslie
find_and_print(messages, "Ximen") # print Bob
find_and_print(messages, "Xindian City Hall") # print Vivian
print("----------Q2----------")
# Q2
# 增加一個結構來追蹤顧問的預約狀態
consultant_schedules = {
    "John": [],
    "Bob": [],
    "Jenny": [],
}

def book(consultants, hour, duration, criteria):
    # 過濾出在指定時間可預約的顧問
    available_consultants = [consultant for consultant in consultants if is_consultant_available(consultant, hour, duration)]

    if not available_consultants:
        print("No Service")
        return

    # 根據優先考慮進行排序
    if criteria == "price":
        available_consultants.sort(key=lambda c: c["price"])
    elif criteria == "rate":
        available_consultants.sort(key=lambda c: c["rate"], reverse=True)

    # 選擇最合適的顧問(排序後的第一位)
    consultant = available_consultants[0]
    print(consultant["name"])

    # 更新顧問的預約時間
    consultant_schedules[consultant["name"]].append({"start": hour, "end": hour + duration})

def is_consultant_available(consultant, hour, duration):
    # 檢查顧問是否在該時間段內已經有預約
    for booking in consultant_schedules[consultant["name"]]:
        if hour < booking["end"] and hour + duration > booking["start"]:
            return False
    return True

consultants = [
    {"name": "John", "rate": 4.5, "price": 1000},
    {"name": "Bob", "rate": 3.0, "price": 1200},
    {"name": "Jenny", "rate": 3.8, "price": 800},
]

book(consultants, 15, 1, "price") # Jenny
book(consultants, 11, 2, "price") # Jenny
book(consultants, 10, 2, "price") # John
book(consultants, 20, 2, "rate") # John
book(consultants, 11, 1, "rate") # Bob
book(consultants, 11, 2, "rate") # No Service
book(consultants, 14, 3, "price") # John

print("----------Q3----------")
# Q3
def func(*data):
    middle_names = {}
    original_names = {}

    for name in data:
        middle_name = ""
        if len(name) == 2 or len(name) == 3:
            middle_name = name[1]
        elif len(name) == 4 or len(name) == 5:
            middle_name = name[2]

        if middle_name in middle_names:
            middle_names[middle_name] += 1
        else:
            middle_names[middle_name] = 1
            original_names[middle_name] = name

    unique_middle_names = [key for key, value in middle_names.items() if value == 1]

    if len(unique_middle_names) == 1:
        print(original_names[unique_middle_names[0]])
    else:
        print("沒有")

func("彭大牆", "陳王明雅", "吳明")  # print 彭大牆
func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花")  # print 林花花
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花")  # print 沒有
func("郭宣雅", "夏曼藍波安", "郭宣恆")  # print

print("----------Q4----------")
# Q4
def get_number(index):
    # 確定在當前週期中的位置(每三個一組:+4、+4、-1)
    position_in_cycle = (index - 1) % 3
    # 完整週期的數量
    cycle = (index - 1) // 3

    # 在完成所有完整週期後的基礎數字
    base_number = cycle * 7

    # 根據當前週期中的位置調整數值
    if position_in_cycle == 0:
        # 週期的第一個數(加4)
        return base_number + 4
    elif position_in_cycle == 1:
        # 週期的第二個數(再加4)
        return base_number + 8
    else:
        # 週期的第三個數(減1)
        return base_number + 7
    

print(get_number(1))  # 應該打印出 4
print(get_number(5))  # 應該打印出 15
print(get_number(10)) # 應該打印出 25
print(get_number(30)) # 應該打印出 70
