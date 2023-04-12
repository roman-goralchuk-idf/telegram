async function startDelivery(url) {
  let div = document.getElementById('delivery_start_response');

  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json;charset=utf-8'
    }
  })
  .then((response) => response.json())
  .then((data) => {
        let response = document.createElement('p')
        let deliveryProcess = document.createElement('p')

        response.innerHTML = `${data.response}`
        deliveryProcess.innerHTML = `${data.delivery_process}`

        div.appendChild(response);
        div.appendChild(taskProcess)
  });
  document.getElementById("delivery_start_description").style.display = "none";
  div.style.display = "block";
}