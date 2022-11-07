async function startDelivery(url) {
  const div = document.getElementById('task_response');

  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json;charset=utf-8'
    }
  })
  .then((response) => response.json())
  .then((data) => {
        let response = document.createElement('p')
        let taskProcess = document.createElement('p')
        
        response.innerHTML = `${data.response}`
        taskProcess.innerHTML = `${data.task_process}`

        div.appendChild(response);
        div.appendChild(taskProcess)
  });
  document.getElementById("task_button").style.display = "none";
  div.style.display = "block";
}

//async function startDelivery(url) {
//  const response = await fetch(url, {
//    method: 'POST',
//    headers: {
//      'Content-Type': 'application/json;charset=utf-8'
//    },
//    body: JSON.stringify({"ids_to_start": [10, 15]})
//  })
//  .then((response) => response.json())
//  .then((commits) => {
//    document.getElementById("response_tasks").innerHTML = [commits.response, commits.ids];
//  });
//}