import { updateDeliveryButton } from "./deliveryIdButtonUpdate.js";
let deliveryStatuses;

function findDeliveryById(baseUrl, statuses) {
  window.onload = (event) => {
    let currentUrl = window.location.pathname;
    let id = currentUrl.substring(currentUrl.lastIndexOf('/') + 1);
    let url = baseUrl + id;
    deliveryStatuses = statuses;
    getDeliveryById(url)
  }
}

async function getDeliveryById(url) {
  await fetch(url, {
    method: "GET",
    headers: {
      "Content-Type": "application/json;charset=utf-8"
    },
  })
    .then((response) => response.json())
    .then((delivery) => {
      buildTable(delivery);
      buildUpdateForm(delivery);
      updateDeliveryButton();
    })
}

function buildTable(delivery) {
  let tableBody = document.getElementById("deliveryIdBody");
  for (const key in delivery) {
    let newRow = tableBody.insertRow();
    let field = newRow.insertCell(0);
    field.innerHTML = key.replace("_", " ");
    let value = newRow.insertCell(1);
    if (key.includes("date")) {
      let date = new Date(delivery[key]);
      value.innerHTML = date.toString();
    } else {
      value.innerHTML = delivery[key];
    }
  }
}

function buildUpdateForm(delivery) {
  let form = document.getElementById("deliveryIdForm");
  let fBody = document.createDocumentFragment();

  let fStatus = getSelection(
    id = "fStatus",
    list = taskStatuses,
    labelText = "Select delivery status",
  );
  fBody.appendChild(fStatus.get("data"));
  fBody.appendChild(fStatus.get("label"));

  let fDescription = getInputText(
    type = "input",
    id = "fDescription",
    placeholder = "Note...",
    labelText = "Any useful information about this",
    defaultText = delivery.description
  );
  fBody.appendChild(fDescription.get("data"));
  fBody.appendChild(fDescription.get("label"));

  let fListIds = getInputText(
    type = "textarea",
    id = "fListIds",
    placeholder = "1, 2, 3...",
    labelText = "Telegram ids",
    defaultText = delivery.telegram_ids
  );
  fBody.appendChild(fListIds.get("data"));
  fBody.appendChild(fListIds.get("label"));

  let fMessage = getInputText(
    type = "textarea",
    id = "fMessage",
    placeholder = "Text message",
    labelText = "Write message here",
    defaultText = delivery.message
  );
  fBody.appendChild(fMessage.get("data"));
  fBody.appendChild(fMessage.get("label"));

  let fButton = document.createElement("input");
  fButton.className = "btn btn-primary float-end";
  fButton.type = "button";
  fButton.value = "UPDATE";
  fBody.appendChild(fButton);

  form.appendChild(fBody)
}

function getSelection(id, list, labelText) {
  let map = new Map();
  let select = document.createElement("select");
  select.className = "form-select";
  select.id = id
  for (const n in list) {
    let selectOption = document.createElement("option");
    selectOption.innerText = list[n];
    select.appendChild(selectOption);
  }
  map.set("data", select)
  let label = getLabel(id, labelText)
  map.set("label", label)
  return map;
}


function getInputText(type, id, placeholder, labelText, defaultText) {
  let map = new Map();
  let text = document.createElement(type);
  text.className = "form-control";
  text.id = id;
  text.type = "text";
  text.placeholder = placeholder;
  if (defaultText != null) {
    text.value = defaultText
  }
  map.set("data", text)
  let label = getLabel(id, labelText)
  map.set("label", label)
  return map;
}

function getLabel(id, labelText) {
  let textLabel = document.createElement("label");
  textLabel.htmlFor = id;
  textLabel.innerText = labelText;
  textLabel.className = "fst-italic fw-light form-label";
  return textLabel;
}