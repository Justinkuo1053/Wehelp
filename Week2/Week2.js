// Q1
console.log("----------Q1----------");

const greenStations = [
  "Songshan",
  "Nanjing Sanmin",
  "Taipei Arena",
  "Nanjing Fuxing",
  "Songjiang Nanjing",
  "Zhongshan",
  "Beimen",
  "Ximen",
  "Xiaonanmen",
  "Chiang Kai-Shek Memorial Hall",
  "Guting",
  "Taipower Building",
  "Gongguan",
  "Wanlong",
  "Jingmei",
  "Dapinglin",
  "Qizhang",
  "Xiaobitan",
  "Xindian City Hall",
  "Xindian",
];

const messages = {
  Bob: "I'm at Ximen MRT station.",
  Mary: "I have a drink near Jingmei MRT station.",
  Copper: "I just saw a concert at Taipei Arena.",
  Leslie: "I'm at home near Xiaobitan station.",
  Vivian: "I'm at Xindian station waiting for you.",
};

function cleanUp(messages) {
  const cleanMessages = { ...messages };
  for (const [key, text] of Object.entries(messages)) {
    for (const station of greenStations) {
      if (text.includes("Xiaobitan")) {
        cleanMessages[key] = greenStations.indexOf("Qizhang") + 0.1;
        break;
      } else if (text.includes("Xindian City Hall")) {
        cleanMessages[key] = greenStations.indexOf("Xindian City Hall");
        break;
      } else if (text.includes(station)) {
        cleanMessages[key] = greenStations.indexOf(station);
        break;
      }
    }
  }
  return cleanMessages;
}

function findAndPrint(messages, currentStation) {
  const currentStationIndex = greenStations.indexOf(currentStation);
  const cleanedMessages = cleanUp(messages);

  for (const [key, index] of Object.entries(cleanedMessages)) {
    cleanedMessages[key] = Math.abs(index - currentStationIndex);
  }

  const minDistance = Math.min(...Object.values(cleanedMessages));
  let closestMessageKey = null;

  for (const [key, value] of Object.entries(cleanedMessages)) {
    if (value === minDistance) {
      closestMessageKey = key;
      break;
    }
  }

  console.log(closestMessageKey);
}

findAndPrint(messages, "Wanlong"); // Should print "Mary"
findAndPrint(messages, "Songshan"); // print Copper
findAndPrint(messages, "Qizhang"); // print Leslie
findAndPrint(messages, "Ximen"); // print Bob
findAndPrint(messages, "Xindian City Hall"); // print Vivian

// Q2
console.log("----------Q2----------");
// 增加一個結構來追踪顧問的預約狀態
let consultantSchedules = {
  John: [],
  Bob: [],
  Jenny: [],
};

function book(consultants, hour, duration, criteria) {
  // 過濾出在指定時間可預約的顧問
  let availableConsultants = consultants.filter((consultant) => {
    // 檢查顧問是否在該時間段內已經有預約
    for (let i = 0; i < consultantSchedules[consultant.name].length; i++) {
      let booking = consultantSchedules[consultant.name][i];
      if (hour < booking.end && hour + duration > booking.start) {
        return false;
      }
    }
    return true;
  });

  if (availableConsultants.length === 0) {
    console.log("No Service");
    return;
  }

  // 根據優先考量進行排序
  if (criteria === "price") {
    availableConsultants.sort((a, b) => a.price - b.price);
  } else if (criteria === "rate") {
    availableConsultants.sort((a, b) => b.rate - a.rate);
  }

  // 選擇最合適的顧問（排序後的第一位）
  console.log(availableConsultants[0].name);

  // 更新顧問的預約時間
  consultantSchedules[availableConsultants[0].name].push({
    start: hour,
    end: hour + duration,
  });
}

const consultants = [
  { name: "John", rate: 4.5, price: 1000 },
  { name: "Bob", rate: 3, price: 1200 },
  { name: "Jenny", rate: 3.8, price: 800 },
];

// 進行預約
book(consultants, 15, 1, "price");
book(consultants, 11, 2, "price");
book(consultants, 10, 2, "price");
book(consultants, 20, 2, "rate");
book(consultants, 11, 1, "rate");
book(consultants, 11, 2, "rate");
book(consultants, 14, 3, "price");

// Q3
console.log("----------Q3----------");
function func(...data) {
  const middleNames = {};
  const originalNames = {};

  data.forEach((name) => {
    let middleName = "";
    if (name.length === 2 || name.length === 3) {
      middleName = name[1];
    } else if (name.length === 4 || name.length === 5) {
      middleName = name[2];
    }

    if (middleNames[middleName]) {
      middleNames[middleName]++;
    } else {
      middleNames[middleName] = 1;
      originalNames[middleName] = name;
    }
  });

  const uniqueMiddleNames = Object.keys(middleNames).filter(
    (key) => middleNames[key] === 1
  );

  if (uniqueMiddleNames.length === 1) {
    console.log(originalNames[uniqueMiddleNames[0]]);
  } else {
    console.log("沒有");
  }
}
// Test cases
func("彭大牆", "陳王明雅", "吳明"); // print 彭大牆
func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花"); // print 林花花
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花"); // print 沒有
func("郭宣雅", "夏曼藍波安", "郭宣恆"); // print

// Q4
console.log("----------Q4----------");
function getNumber(index) {
  // 確定在當前週期中的位置(每三個一組:+4、+4、-1)
  let positionInCycle = (index - 1) % 3;
  // 完整週期的數量
  let cycle = Math.floor((index - 1) / 3);

  // 在完成所有完整週期後的基礎數字
  let baseNumber = cycle * 7;

  // 根據當前週期中的位置調整數值
  if (positionInCycle === 0) {
    // 週期的第一個數(加4)
    return baseNumber + 4;
  } else if (positionInCycle === 1) {
    // 週期的第二個數(再加4)
    return baseNumber + 8;
  } else {
    // 週期的第三個數(減1)
    return baseNumber + 7;
  }
}

console.log(getNumber(1)); // 應該打印出 4
console.log(getNumber(5)); // 應該打印出 15
console.log(getNumber(10)); // 應該打印出 25
console.log(getNumber(30)); // 應該打印出 70
