
async function updateTable(url, outUrl) {

  let taskIds = document.forms["taskFilter"]["taskIds"].value;
  let status = document.forms["taskFilter"]["taskStatus"].value;
  let objOnPage = document.forms["taskFilter"]["objOnPage"].value;

  // const div = document.getElementById('test')
  // div.innerText = `IDS: ${taskIds}`;


  let idsFind = null;
  if (taskIds != '') {
    idsFind = taskIds.split(/\D+/).map(Number);
  }

  let statusFind;
  if (status == 'all') {
    statusFind = null
  } else {
    statusFind = status
  }

  await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json;charset=utf-8'
    },
    body: JSON.stringify({"task_ids": idsFind, "status": statusFind})
  })
  .then((response) => response.json())
  .then((tasks) => {
    buildTable(tasks, outUrl, objOnPage);
  })
}

function clearTable() {
  document.querySelector("#tableTaskBody").innerHTML = "";
}

function buildTable(tasks, outUrl, objOnPage) {
  clearTable()

  var tasksCount = tasks.length;
  var pagesCount = Math.ceil(tasksCount/objOnPage);

  buildPagination(pagesCount)

  let pageNum = 2
  var pageTaskFrom = objOnPage * (pageNum - 1);
  var pageTaskTo = objOnPage * pageNum;

  let notes = tasks.slice(pageTaskFrom, pageTaskTo);
  
  notes.forEach((task, i) => {
    addLineToHTMLTable(
      i,
      task.task_id, 
      task.status,
      task.created_date,
      task.performed_date,
      task.description,
      outUrl
      );
  });
}

function buildPagination(pagesCount) {
  updatePagination()

  let pagesArray = [...Array(pagesCount).keys()]
  let pages = document.querySelector("#tasksPages")
  let numerous = document.createDocumentFragment();

  pagesArray.forEach((i) => {
    let buttonName = i + 1;
    let li = createPaginationButton(buttonName, true);
    numerous.appendChild(li);
  });
  pages.insertBefore(numerous, pages.children[1]);
}

function updatePagination() {
  const ul = document.querySelector("#tasksPages");
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

  a.addEventListener('click', (e) => {
    alert(buttonName)
  });

  return li;
}

// Table build
function addLineToHTMLTable(count, taskId, status, createdDate, performedDate, description, outUrl) {
  // Get the body of the table using the selector API
  var tableBody = document.getElementById('tableTaskBody')

  // Add a new row at the end of the table
  var newRow = tableBody.insertRow();

  // add  new cells to the row
  var cell_num = newRow.insertCell(0);
  cell_num.innerHTML = `<b>${count + 1}</b>`;

  var cell_taskId = newRow.insertCell(1);
  cell_taskId.innerHTML = taskId;

  var cell_status = newRow.insertCell(2);
  cell_status.innerHTML = status;

  var cell_dateCreate = newRow.insertCell(3);
  var dateCreate = new Date(createdDate);
  cell_dateCreate.innerHTML = `${dateCreate.toString()}`;

  var cell_datePerform = newRow.insertCell(4);
  var datePerform = new Date(performedDate);
  cell_datePerform.innerHTML = `${datePerform.toString()}`;

  var cell_description = newRow.insertCell(5);
  cell_description.innerHTML = description;

  var cell_link = newRow.insertCell(6);
  cell_link.innerHTML = `<a class="btn btn-primary btn-sm" target="_blank" href="${outUrl}${taskId}">See task</a>`;

}

