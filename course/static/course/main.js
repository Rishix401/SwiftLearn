// Function to get the value of a cookie
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// function to edit note
function edit_note(element) {
  const title = prompt('Enter note title:');
  const desc = prompt('Enter note description:');
  const noteId = element.parentElement.parentElement.dataset.noteId;

  // Send a POST request to the server to edit the note
  fetch('create-note', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify({
      'title': title,
      'desc': desc,
      'noteId': noteId,
    })
  })
    .then(response => {
      // Update the note title and description with the new values
      element.parentElement.parentElement.previousElementSibling.textContent = title;
      element.parentElement.parentElement.parentElement.nextElementSibling.textContent = desc;
    })
    .catch(error => {
      console.log(error);
    });
}

// function to delete note
function delete_note(element) {
  const noteId = element.parentElement.parentElement.dataset.noteId;

  // Send a POST request to the server to delete the note
  fetch(`/delete-note`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify({
      'noteId': noteId,
    })
  })
    .then(response => {
      element.parentElement.parentElement.parentElement.parentElement.remove();
    })
    .catch(error => {
      console.log(error);
    });
}

// function for working of star and to limit textarea content
function starsTxtArea() {
  // get all the stars
  const stars = document.querySelectorAll('.star');

  // add a click event listener to each star
  stars.forEach((star) => {
    star.addEventListener('click', (event) => {
      const clickedStar = event.target;
      const clickedStarIndex = Array.from(stars).indexOf(clickedStar);

      // set the color of clicked star and previous stars to #DDDDDD
      for (let i = 0; i <= clickedStarIndex; i++) {
        stars[i].style.fill = '#FBBA02';
      }

      // set the color of unclicked stars to original color
      for (let i = clickedStarIndex + 1; i < stars.length; i++) {
        stars[i].style.fill = '#DDDDDD';
      }

      document.querySelector('#rating').value = clickedStarIndex + 1;
    });
  });

  // limit textarea chars up to 350
  const commentTextArea = document.getElementById("comment");
  const charsLeftSpan = document.getElementById("chars-left");
  const maxChars = 350;

  commentTextArea.addEventListener("input", function () {
    const currentChars = commentTextArea.value.length;
    if (currentChars > maxChars) {
      commentTextArea.value = commentTextArea.value.substring(0, maxChars);
      charsLeftSpan.textContent = "0";
    } else {
      charsLeftSpan.textContent = maxChars - currentChars;
    }
  });
}

document.addEventListener('DOMContentLoaded', function () {

  // An array of objects that contain link IDs and their corresponding container IDs.
  const links = [
    { id: 'courses-link', container: 'courses-container' },
    { id: 'dates-link', container: 'dates-container' },
    { id: 'discussions-link', container: 'discussions-container' },
    { id: 'faqs-link', container: 'faqs-container' },
  ];

  try {
    // Add 'border-bottom' class to 'courses-link'
    document.querySelector('#courses-link').classList.add('border-bottom');
  } catch (error) { console.log(error) }

  // Loop through the 'links' array and add a click event listener to each link.
  try {
    links.forEach(link => {
      const linkEl = document.querySelector(`#${link.id}`);
      const containerEl = document.querySelector(`#${link.container}`);

      linkEl.addEventListener('click', () => {
        links.forEach(otherLink => {
          const otherLinkEl = document.querySelector(`#${otherLink.id}`);
          const otherContainerEl = document.querySelector(`#${otherLink.container}`);

          // If the clicked link matches the current iteration's link, show the container and add the 'border-bottom' class to the link element. Otherwise, hide the container and remove the 'border-bottom' class.
          if (link.id === otherLink.id) {
            containerEl.style.display = 'block';
            otherLinkEl.classList.add('border-bottom');
          } else {
            otherContainerEl.style.display = 'none';
            otherLinkEl.classList.remove('border-bottom');
          }
        });
      });
    });
  } catch (error) { console.log(error) }

  try {
    // Remove bottom border from last child of 'lectures-link'
    document.querySelector('#lectures-link').lastElementChild.style.border = 'none';
  } catch (error) { console.log(error) }

  try {
    // Get references to the video player and relevant IDs.
    let myPlayer = videojs('my-video');
    let userID = "{{user.id}}";
    let lectureID = "{{lecture.id}}";
    let key = `progress-${userID}-${lectureID}`;
    let lastProgress = localStorage.getItem(key);
    let hasBeenPlayed = false;

    // When the video starts playing, set the time to the last saved progress if it hasn't been played before.
    myPlayer.on('play', function () {
      if (!hasBeenPlayed) {
        myPlayer.currentTime(lastProgress);
        hasBeenPlayed = true;
      }
    });

    // Whenever the video time updates, save the current time to local storage.
    myPlayer.on('timeupdate', function () {
      if (!myPlayer.ended()) {
        localStorage.setItem(key, myPlayer.currentTime());
      }
    });

    // When the video ends, set the progress to 0 and submit a form containing the watched video data.
    myPlayer.on('ended', function () {
      localStorage.setItem(key, 0);

      let form = document.getElementById('watched-form');
      let formData = new FormData(form);

      fetch(form.action, {
        method: form.method,
        body: formData
      }).then(response => {
        console.log(response);
      }).catch(error => {
        console.log(error);
      });
    });

  } catch (error) { console.log(error) }


  try {
    // add, edit and delete note logic. 
    let addNote = document.querySelector('#add-note');
    addNote.addEventListener('click', function () {
      const title = prompt('Enter note title:');
      const desc = prompt('Enter note description:');

      // Send a POST request to the server to create a new note
      fetch('create-note', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
          'title': title,
          'desc': desc,
        })
      })
        .then(response => {
          location.reload();
        })
        .catch(error => {
          console.log(error);
        });
    });

    // Add event listener to the document to handle note edit and delete actions
    document.addEventListener('click', function (event) {
      const element = event.target;

      if (element.classList.contains('edit-note')) {
        edit_note(element);
      } else if (element.classList.contains('delete-note')) {
        delete_note(element);
      }
    });
  } catch (error) { console.log(error) }


  // run starsTxtArea function
  try { starsTxtArea() } catch (error) { console.log(error) }

  try {
    // get the edit button element
    const editButton = document.querySelector('.edit-comment-btn');

    // add an event listener to the edit button
    editButton.addEventListener('click', () => {

      rating = document.querySelector('#my-rating').dataset.rating;
      comment = document.querySelector('#my-comment').textContent;

      // hide the review text
      const userCmnt = document.querySelector('#review').firstElementChild;
      userCmnt.style.display = 'none';
      // userCmnt.remove()

      // show the edit form
      const editForm = document.createElement('form');
      editFormInnerHtml = `
      <input type="hidden" name="csrfmiddlewaretoken" value="${getCookie('csrftoken')}">
          <div id="rate-us">
            <div class="flex space-x-2 items-center mt-7 mb-2">
              <p class="text-xl mr-4 font-medium">RATE US: </p>
              <input type="hidden" name="rating" id="rating" value="${rating}">`
      for (let i = 0; i < 5; i++) {
        let rt = i + 1;
        let starClass = 'star fill-[#FBBA02]';
        if (rt > rating) {
          starClass = 'star fill-[#DDDDDD]';
        }
        editFormInnerHtml += `
        <svg class="w-7 h-7 cursor-pointer" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512">
        <path class="star ${starClass}" data-rating="${rating}" d="M316.9 18C311.6 7 300.4 0 288.1 0s-23.4 7-28.8 18L195 150.3 51.4 171.5c-12 1.8-22 10.2-25.7 21.7s-.7 24.2 7.9 32.7L137.8 329 113.2 474.7c-2 12 3 24.2 12.9 31.3s23 8 33.8 2.3l128.3-68.5 128.3 68.5c10.8 5.7 23.9 4.9 33.8-2.3s14.9-19.3 12.9-31.3L438.5 329 542.7 225.9c8.6-8.5 11.7-21.2 7.9-32.7s-13.7-19.9-25.7-21.7L381.2 150.3 316.9 18z"/>
      </svg>
                `;
      }
      editFormInnerHtml += `
            </div>
            <textarea name="comment" id="comment" rows="4" placeholder="Tell us about your experience (Maximum 350 characters)" class="font-mono p-4 w-full overflow-auto border-[1px] border-[#cad8dd] rounded-sm outline-none"></textarea>
            <div class="flex justify-between">
              <p>Number of characters left - <span id="chars-left">350</span></p>
              <div class="flex space-x-3">
                <button id="update-btn" class="bg-[#30bbe2] text-white py-1.5 px-3 rounded-md" type="submit">UPDATE</button>
                <button id="cancel-btn" class="bg-[#30bbe2] text-white py-1.5 px-3 rounded-md" type="button">CANCEL</button>
              </div>
            </div>
          </div>`;

      editForm.innerHTML = editFormInnerHtml;

      editForm.action = 'review'
      editForm.method = 'POST'

      const review = document.querySelector('#review').firstElementChild;
      review.before(editForm);

      document.querySelector('#comment').value = comment

      starsTxtArea()

      document.querySelector('#cancel-btn').addEventListener('click', function () {
        editForm.remove();
      })
    });
  } catch (error) { console.log(error) }

});
