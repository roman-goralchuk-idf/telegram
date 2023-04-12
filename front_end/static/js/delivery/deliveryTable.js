let globalPageNum = 1;

class FormDto {
  constructor() {
    this.deliveriesIds = document.forms["deliveriesFilter"]["deliveriesIds"].value;
    this.status = document.forms["deliveriesFilter"]["deliveryStatus"].value;
    this.objOnPage = document.forms["deliveriesFilter"]["objOnPage"].value;
  }
}

async function createTable(url, outUrl) {
  let formData = new FormDto();
  let idsForFind = null;
  if (formData.deliveriesIds != '') {
    idsForFind = formData.deliveriesIds.split(/\D+/).map(Number);
  }
  let statusForFind = null;
  if (formData.status != 'all') {
    statusForFind = formData.status
  }
  await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json;charset=utf-8'
    },
    body: JSON.stringify({ "deliveries_ids": idsForFind, "status": statusForFind })
  })
    .then((response) => response.json())
    .then((deliveries) => {
      buildTable(deliveries, outUrl, formData.objOnPage);
    })
}

function buildTable(deliveries, outUrl, objOnPage) {
  let pagesCount = getPagesCount(deliveries.length, objOnPage);
  buildPagination(pagesCount);
  buildTableForPage(deliveries, objOnPage, outUrl);

  const nums = document.querySelector("#deliveryPage")
  const children = nums.children;
  const elementsArrayLen = children.length;
  const elementNamePreviousId = 0;
  const elementNameNextId = elementsArrayLen - 1;
  for (let i = 1; i < elementsArrayLen - 1; i++) {
    children[i].addEventListener('click', (e) => {
      clearActiveStatus(children[globalPageNum])
      globalPageNum = children[i].innerText;
      setActiveStatus(children[i])
      buildTableForPage(deliveries, objOnPage, outUrl);
    })
  }
  children[elementNamePreviousId].addEventListener('click', (e) => {
    if (globalPageNum > 1) {
      clearActiveStatus(children[globalPageNum])
      globalPageNum--;
      setActiveStatus(children[globalPageNum]);
      buildTableForPage(deliveries, objOnPage, outUrl);
    }
  })
  children[elementNameNextId].addEventListener('click', (e) => {
    if (globalPageNum < (elementsArrayLen - 2)) {
      clearActiveStatus(children[globalPageNum])
      globalPageNum++;
      setActiveStatus(children[globalPageNum]);
      buildTableForPage(deliveries, objOnPage, outUrl);
    }
  })
}

function setActiveStatus(element) {
  element.classList.add("active");
}

function buildTableForPage(deliveries, objOnPage, outUrl) {
  let notes = getSliceData(deliveries, objOnPage, globalPageNum);
  buildPartTable(notes, outUrl, getCellStartNumber(objOnPage, globalPageNum));
}

function clearActiveStatus(element) {
  element.classList.remove("active");
}

function getPagesCount(deliveriesCount, objOnPage) {
  let pagesCount = Math.ceil(deliveriesCount / objOnPage);
  return pagesCount;
}

function buildPagination(pagesCount) {
  updatePagination()
  let pagesArray = [...Array(pagesCount).keys()]
  let pages = document.querySelector("#deliveriesPages")
  let numerous = document.createDocumentFragment();
  pagesArray.forEach((pageNumber) => {
    let buttonName = pageNumber + 1;
    let li = createPaginationButton(buttonName, true);
    if (buttonName == 1) {
      li.classList.add("active");
    }
    numerous.appendChild(li);
  });
  pages.insertBefore(numerous, pages.children[1]);
}

function updatePagination() {
  const ul = document.querySelector("#deliveriesPages");
  ul.innerHTML = "";
  let pagination = document.createDocumentFragment();
  let liPrevious = createPaginationButton('Previous', false);
  pagination.appendChild(liPrevious);
  let liNext = createPaginationButton('Next', true);
  pagination.appendChild(liNext);
  ul.appendChild(pagination)
}

function createPaginationButton(buttonName, visible) {
  let li = document.createElement('li');
  const liList = li.classList;
  liList.add("page-item");
  let a = document.createElement('a');
  const aList = a.classList;
  aList.add("page-link");
  if (visible == false) {
    liList.add("disabled");
    a.ariaDisabled = true;
  }
  a.innerText = buttonName;
  li.appendChild(a);
  return li;
}

function getSliceData(deliveries, objOnPage, pageNum) {
  let pageDeliveryFrom = objOnPage * (pageNum - 1);
  let pageDeliveryTo = objOnPage * pageNum;
  let notes = deliveries.slice(pageDeliveryFrom, pageDeliveryTo);
  return notes;
}

function getCellStartNumber(objOnPage, pageNum) {
  return (pageNum - 1) * objOnPage + 1;
}

function buildPartTable(notes, outUrl, cellStartNum) {
  clearTable()
  notes.forEach((delivery, i) => {
    addLineToHTMLTable(
      cellStartNum + i,
      delivery.delivery_id,
      delivery.status,
      delivery.created_date,
      delivery.performed_date,
      delivery.description,
      outUrl
    );
  });
}

function clearTable() {
  document.querySelector("#tableDeliveryBody").innerHTML = "";
}

// Table build
function addLineToHTMLTable(count, taskId, status, createdDate, performedDate, description, outUrl) {
  // Get the body of the table using the selector API
  let tableBody = document.getElementById('tableDeliveryBody')
  // Add a new row at the end of the table
  let newRow = tableBody.insertRow();
  // add  new cells to the row
  let cell_num = newRow.insertCell(0);
  cell_num.innerHTML = `<b>${count}</b>`;
  let cell_deliveryId = newRow.insertCell(1);
  cell_deliveryId.innerHTML = deliveryId;
  let cell_status = newRow.insertCell(2);
  cell_status.innerHTML = status;
  let cell_dateCreate = newRow.insertCell(3);
  let dateCreate = new Date(createdDate);
  cell_dateCreate.innerHTML = `${dateCreate.toString()}`;
  let cell_datePerform = newRow.insertCell(4);
  let datePerform = new Date(performedDate);
  cell_datePerform.innerHTML = `${datePerform.toString()}`;
  let cell_description = newRow.insertCell(5);
  cell_description.innerHTML = description;
  let cell_link = newRow.insertCell(6);
  cell_link.innerHTML = `<a class="btn btn-primary btn-sm" target="_blank" href="${outUrl}/${deliveryId}">See delivery</a>`;
}
