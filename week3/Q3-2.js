const src1 =
  "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1";

// 修改字過長問題
function shortedText(text) {
  if (text.length > 7) {
    return text.substring(0, 7) + "...";
  } else {
    return text;
  }
}

fetch(src1)
  .then((response) => {
    if (response.ok) {
      return response.json();
    }
  })
  .then((data1) => {
    // console.log(data1.data.results[0].stitle);

    // 創建名字的 Arrays
    // 創建url的 Arrays
    let titleList = [];
    let urlList = [];
    for (let i = 0; i < 13; i += 1) {
      let filestr = data1.data.results[i].filelist;
      let jpgIndex;
      jpgIndex = filestr.slice(4).indexOf("https");
      let ImageURL = filestr.substring(0, jpgIndex + 4);
      urlList.push(ImageURL);
      titleList.push(data1.data.results[i].stitle);
    }

    // 修改title name
    let title = document.querySelectorAll('[id="p-change"]');
    let titleArray = Array.from(title);
    for (let i = 0; i < 13; i += 1) {
      const elementP = titleArray[i];
      elementP.textContent = shortedText(titleList[i]);
    }

    // 修改 jpg (上方3個小的)
    let imgSmall = document.querySelectorAll(".author-img");
    let imgSmallArray = Array.from(imgSmall);
    for (let i = 0; i < 3; i += 1) {
      const elementP = imgSmallArray[i];
      elementP.src = urlList[i];
    }
    // 修改 jpg (下方10個)
    let imgBig = document.querySelectorAll(".background-image-container");
    let imgBigArray = Array.from(imgBig);
    for (let i = 0; i < 10; i += 1) {
      const elementP = imgBigArray[i];
      elementP.style.backgroundImage = `url(${urlList[i + 3]})`;
    }
  });

//------------------------------------------------------------------------------------
// 解決url叫不出來問題
//      elementP.style.backgroundImage = `url(${urlList[i + 3]})`;
// slice
//      https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/slice
