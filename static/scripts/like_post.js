document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".fa-heart").forEach((heart) => {
    heart.addEventListener("click", () => {
      const postId = heart.dataset.postId;
      const likes = document.getElementById(`like-${postId}`);
      const likesText = likes.textContent;
      let likesCount;
      if (likesText.length == 0) {
        likesCount = 0;
      } else {
        likesCount = parseInt(likesText);
      }
      console.log(likesCount)
      const csrfToken = document.getElementById("csrf-token").value;
      if (heart.classList.contains("liked")) {
        heart.classList.remove("liked");
        likesCount -= 1;
        if (likesCount == 0) {
          likes.innerHTML = '';
        } else {
          likes.innerHTML = `${likesCount}`;
        }
        fetch(`/unlike/${postId}/`, {
          method: "POST",
          headers: {
            "X-CSRFToken": csrfToken,
          },
        })
          .then((response) => {
            if (response.redirected && response.url.includes("login")) {
              // If the response indicates a redirection to the login page
              // You can handle the redirection here, for example, by displaying a message or prompting the user to log in
              window.location.href = response.url;
            }
            if (!response.ok) {
              throw new Error("Failed to unlike post");
            }
            return response.json();
          })
          .then((data) => {
            console.log(data);
          })
          .catch((error) => {
            console.error(
              "There was a problem with the fetch operation:",
              error
            );
          });
      } else {
        heart.classList.add("liked");
        likesCount += 1;
        likes.innerHTML = `${likesCount}`;
        fetch(`/like/${postId}/`, {
          method: "POST",
          headers: {
            "X-CSRFToken": csrfToken,
          },
        })
          .then((response) => {
            if (response.redirected && response.url.includes("login")) {
              window.location.href = response.url;
            }
            if (!response.ok) {
              throw new Error("Failed to unlike post");
            }
            return response.json();
          })
          .then((data) => {
            console.log(data);
          })
          .catch((error) => {
            console.error(
              "There was a problem with the fetch operation:",
              error
            );
          });
      }
    });
  });
});
