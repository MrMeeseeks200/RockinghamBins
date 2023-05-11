function jsonOnLoad() {
  const raw = this.contentWindow.document.body.textContent.trim();
  try {
    const data = JSON.parse(raw);
    /** do something with data */
    displayData(data);
  } catch (e) {
    console.warn(e.message);
  }
  this.remove();
}

function displayData(data) {
  /** do something with data */
  console.log(data);
  var content = document.getElementById("content");
  content.style.display = "flex";
  content.style.flexDirection = "column";
  content.style.alignItems = "center";
  var title = document.createElement("h1");
  var header = document.createElement("h1");
  var subHeader = document.createElement("h1");

  title.innerHTML = data.info.address;

  if (data.isRecycleWeek) {
    document.body.style.background = "#efb710";
    header.innerHTML = "Recycle Week";
  } else if (data.isGreenWasteWeek) {
    document.body.style.background = "#2b8023";
    header.innerHTML = "Green Waste Week";
  }
  subHeader.innerHTML = "Collection on " + data.binday;

  content.appendChild(title);
  content.appendChild(header);
  content.appendChild(subHeader);

  var nextRecycle = document.createElement("h2");
  var nextRecycleDate = data.nextRecycleDate;
  nextRecycle.innerHTML = "Next Recycle Day: " + nextRecycleDate;
  content.appendChild(nextRecycle);

  var nextGreen = document.createElement("h2");
  var nextGreeneDate = data.nextGreenWasteDate;
  nextGreen.innerHTML = "Next Green Waste Day: " + nextGreeneDate;
  content.appendChild(nextGreen);

  var verge = document.createElement("h1");
  verge.innerHTML = "Verge Collections";
  content.appendChild(verge);

  var nextGeneralVerge = document.createElement("h2");
  nextGeneralVerge.innerHTML =
    "Next General Waste Collection " + data.nextVergeGeneralWasteDate;
  if (data.isVergeGeneralWasteWeek) {
    nextGeneralVerge.style.backgroundColor = "pink";
  }
  content.appendChild(nextGeneralVerge);

  var nextGreenVerge = document.createElement("h2");
  nextGreenVerge.innerHTML =
    "Next Green Waste Collection " + data.nextVergeGreenWasteDate;
  if (data.isVergeGreenWasteWeek) {
    nextGreenVerge.style.backgroundColor = "pink";
  }
  content.appendChild(nextGreenVerge);
}
