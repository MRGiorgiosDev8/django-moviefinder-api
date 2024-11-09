document.addEventListener("DOMContentLoaded", function () {
    fetch(`/api/random-high-rated/`)
        .then(response => response.json())
        .then(data => {
            const randomMovieInfo = document.getElementById("random-movie-info");
            randomMovieInfo.innerHTML = "";

            if (data.movies && data.movies.length > 0) {
                const carouselInner = document.createElement("div");
                carouselInner.classList.add("carousel-inner");

                for (let i = 0; i < data.movies.length; i += 5) {
                    const carouselItem = document.createElement("div");
                    carouselItem.classList.add("carousel-item");
                    if (i === 0) carouselItem.classList.add("active");

                    const cardGroup = document.createElement("div");
                    cardGroup.classList.add("d-flex", "justify-content-center");

                    data.movies.slice(i, i + 5).forEach(movie => {
                        const movieCard = document.createElement("div");
                        movieCard.classList.add("movie-card", "card", "text-center");

                        movieCard.innerHTML = `
                            <img src="${movie.Poster}" alt="${movie.Title} Poster" class="img-fluid w-100" style="height: 300px;">
                            <p><strong>${movie.Title}</strong> (${movie.Year})</p>
                            <p><strong>IMDb Rating:</strong> ${movie.imdbRating}</p>
                            <a href="https://www.imdb.com/title/${movie.imdbID}" target="_blank" class="btn btn-link">View on IMDb</a>
                        `;
                        cardGroup.appendChild(movieCard);
                    });

                    carouselItem.appendChild(cardGroup);
                    carouselInner.appendChild(carouselItem);
                }

                randomMovieInfo.appendChild(carouselInner);
                randomMovieInfo.insertAdjacentHTML("beforeend", `
                    <button class="carousel-control-prev" type="button" data-bs-target="#random-movie-info" data-bs-slide="prev">
                        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                        <span class="visually-hidden">Previous</span>
                    </button>
                    <button class="carousel-control-next" type="button" data-bs-target="#random-movie-info" data-bs-slide="next">
                        <span class="carousel-control-next-icon" aria-hidden="true"></span>
                        <span class="visually-hidden">Next</span>
                    </button>
                `);

                randomMovieInfo.id = "movieCarousel";
            } else {
                randomMovieInfo.innerHTML = `<p>No high-rated movies found.</p>`;
            }
        })
        .catch(error => {
            document.getElementById("random-movie-info").innerHTML = `<p>An error occurred: ${error}</p>`;
        });
});

document.getElementById("movie-search-form").addEventListener("submit", function (event) {
    event.preventDefault();
    const query = document.getElementById("query").value;

    fetch(`/api/search/?query=${query}`)
        .then(response => response.json())
        .then(data => {
            const movieInfo = document.getElementById("movie-info");
            movieInfo.innerHTML = "";

            if (data.error) {
                movieInfo.innerHTML = `<p>${data.error}</p>`;
            } else {
                const cardContainer = document.createElement("div");
                cardContainer.classList.add("d-flex", "flex-wrap", "justify-content-start");

                data.movies.forEach(movie => {
                    const movieCard = document.createElement("div");
                    movieCard.classList.add("movie-card", "d-flex", "flex-column", "align-items-center", "m-3", "card");

                    movieCard.innerHTML = `
                        <img src="${movie.Poster}" alt="${movie.Title} Poster" class="img-fluid mb-3" style="width:150px; height:auto;">
                        <h3>${movie.Title} (${movie.Year})</h3>
                        <p><strong>IMDb Rating:</strong> ${movie.imdbRating}</p>
                        <a href="https://www.imdb.com/title/${movie.imdbID}" target="_blank" class="btn btn-link">View on IMDb</a>
                    `;
                    cardContainer.appendChild(movieCard);
                });

                movieInfo.appendChild(cardContainer);
            }
        })
        .catch(error => {
            document.getElementById("movie-info").innerHTML = `<p>An error occurred: ${error}</p>`;
        });
});