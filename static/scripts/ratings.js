// get all the stars from the food rating
const oneFood = document.getElementById("food-1");
const twoFood = document.getElementById("food-2");
const threeFood = document.getElementById("food-3");
const fourFood = document.getElementById("food-4");
const fiveFood = document.getElementById("food-5");

// get all the stars from the accommodation rating
const oneAcc = document.getElementById("accommodation-1");
const twoAcc = document.getElementById("accommodation-2");
const threeAcc = document.getElementById("accommodation-3");
const fourAcc = document.getElementById("accommodation-4");
const fiveAcc = document.getElementById("accommodation-5");

// form and ratings
const blogForm = document.getElementById('blog_form');
const foodRating = document.getElementById('food_rating');
const foodStars = document.querySelectorAll('.food-stars');
const accRating = document.getElementById('accommodation_rating');
const accStars = document.querySelectorAll('.accommodation-stars')

// Food Stars Checking
const foodStarsList = [oneFood, twoFood, threeFood, fourFood, fiveFood];
foodStarsList.forEach((item, index) => {
  item.addEventListener('click', () => {
    foodStarsList.forEach((item, i) => {
      if (i <= index) {
        item.classList.add('checked');
      } else {
        item.classList.remove('checked');
      }
    });
  });
});

// Accommodation Stars Checking
const accStarsList = [oneAcc, twoAcc, threeAcc, fourAcc, fiveAcc];
accStarsList.forEach((item, index) => {
  item.addEventListener('click', () => {
    accStarsList.forEach((item, i) => {
      if (i <= index) {
        item.classList.add('checked');
      } else {
        item.classList.remove('checked');
      }
    });
  });
});

blogForm.addEventListener('submit', (event) => {
  event.preventDefault(); // Prevents default form submission
  let foodReview = 0;
  let accReview = 0;
  foodStars.forEach((star) => {
    if (star.classList.contains('checked')) {
      foodReview += 1;
    }
  });
  accStars.forEach((star) => {
    if (star.classList.contains('checked')) {
      accReview += 1;
    }
  });

  foodRating.value = JSON.stringify(foodReview);
  accRating.value = JSON.stringify(accReview);
  // Submit the form
  blogForm.submit();
});

// sets the stars to the correct review in case of an update
document.addEventListener('DOMContentLoaded', () => {
  const foodReview = parseInt(foodRating.value);
  const accReview = parseInt(accRating.value);
  foodStarsList.forEach((item, index) => {
    if (index < foodReview) {
      item.classList.add('checked')
    }
  });
  accStarsList.forEach((item, index) => {
    if (index < accReview) {
      item.classList.add('checked');
    }
  });
});
