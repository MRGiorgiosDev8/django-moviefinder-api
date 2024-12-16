document.addEventListener("DOMContentLoaded", function () {
    const randomMovieInfo = document.getElementById("random-movie-info");

    const displayMovies = (data) => {
        randomMovieInfo.innerHTML = "";

        const ratedTitle = document.createElement("h2");
        ratedTitle.classList.add("rated-h2");
        ratedTitle.textContent = "Top 20 Movies";
        randomMovieInfo.appendChild(ratedTitle);

        gsap.fromTo(
            ".rated-h2",
            { scale: 0, opacity: 0 },
            { scale: 1, opacity: 1, duration: 0.6, ease: "power2.out", delay: 0.4 }
        );

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
                        <img src="${movie.Poster}" alt="${movie.Title} Poster" class="img-fluid w-100" style="height: 307px;" data-bs-toggle="modal" data-bs-target="#movieModal-${movie.imdbID}">
                        <p class="p-card"><strong>${movie.Title}</strong></p>
                        <p><i class="fa fa-star" style="color: #FFD700; text-shadow:
                        -0.7px -0.7px 0.7px #656565,
                        0.7px -0.7px 0.7px #656565,
                        -0.7px  0.7px 0.7px #656565,
                        0.7px  0.7px 0.7px #656565;"></i> ${movie.imdbRating}</p>
                         <a href="https://www.imdb.com/title/${movie.imdbID}" target="_blank" class="btn btn-link link-imbd">
                            <i class="fa fa-hand-point-right"></i> <span class="imbd-text">IMDb</span>
                         </a>
                    `;

                    const addFavoriteButton = document.createElement("i");
                    addFavoriteButton.classList.add("fa", "fa-heart", "add-to-favorites", "random-add-favorites", "fs-5");

                    addFavoriteButton.addEventListener("click", function () {
                        const movieData = {
                            title: movie.Title,
                            imdb_id: movie.imdbID,
                            poster: movie.Poster,
                            year: movie.Year,
                            genre: movie.Genre,
                            actors: movie.Actors,
                            imdb_rating: movie.imdbRating,
                            plot: movie.Plot,
                            movie_url: `https://www.imdb.com/title/${movie.imdbID}/`
                        };

                        fetch("http://127.0.0.1:8000/accounts/add-to-favorites/", {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json",
                                "X-CSRFToken": getCookie("csrftoken"),
                            },
                            body: JSON.stringify(movieData),
                        })
                            .then(response => {
                                if (!response.ok) {
                                    return response.text().then(text => {
                                        throw new Error(`Error: ${text}`);
                                    });
                                }
                                return response.json();
                            })
                            .then(data => {
                                if (data.message) {
                                    alert(data.message);
                                } else {
                                    alert("Unexpected response");
                                }
                            })
                            .catch(error => {
                                console.error("Fetch error:", error);
                                alert(`Error: ${error.message}`);
                            });
                    });

                    movieCard.appendChild(addFavoriteButton);
                    cardGroup.appendChild(movieCard);

                    gsap.fromTo(addFavoriteButton,
                        {
                            scale: 0,
                        },
                        {
                            scale: 1,
                            duration: 0.5,
                            ease: "back.out(1.7)",
                            delay: 0.6,
                        }
                    );

                    const isAuthenticated = document.body.getAttribute("data-authenticated") === "true";

                    const hideFavoritesForGuests = (parentNode) => {
                        if (!isAuthenticated) {
                            parentNode.querySelectorAll(".add-to-favorites").forEach(button => {
                                button.style.display = "none";
                            });
                        }
                    };

                    const observer = new MutationObserver(mutations => {
                        mutations.forEach(mutation => {
                            if (mutation.type === "childList" && mutation.addedNodes.length > 0) {
                                mutation.addedNodes.forEach(node => {
                                    if (node.nodeType === Node.ELEMENT_NODE) {
                                        hideFavoritesForGuests(node);
                                    }
                                });
                            }
                        });
                    });

                    observer.observe(document.body, { childList: true, subtree: true });

                    hideFavoritesForGuests(document.body);

                    gsap.fromTo(
                        movieCard,
                        { x: -100 },
                        { x: 0, duration: 0.3, ease: "power1.inOut" }
                    );

                    const modal = document.createElement("div");
                    modal.classList.add("modal", "fade");
                    modal.id = `movieModal-${movie.imdbID}`;
                    modal.setAttribute("tabindex", "-1");
                    modal.setAttribute("aria-labelledby", `movieModalLabel-${movie.imdbID}`);
                    modal.setAttribute("aria-hidden", "true");
                    modal.innerHTML = `
                        <div class="modal-dialog">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <h5 class="modal-title" id="movieModalLabel-${movie.imdbID}">${movie.Title}</h5>
                                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                </div>
                                <div class="modal-body">
                                    <img src="${movie.Poster}" alt="${movie.Title} Poster" class="img-fluid">
                                     <p class="rating-modal"><i class="fa fa-star" style="color: #FFD700; text-shadow:
                                     -0.7px -0.7px 0.7px #656565,
                                      0.7px -0.7px 0.7px #656565,
                                      -0.7px  0.7px 0.7px #656565,
                                       0.7px  0.7px 0.7px #656565;"></i> ${movie.imdbRating}</p>
                                       <p><strong>Year:</strong> ${movie.Year}</p>
                                       <hr>
                                       <p><strong>Genre:</strong> ${movie.Genre}</p>
                                       <hr>
                                       <p><strong>Cast:</strong> ${movie.Actors}</p>
                                       <hr>
                                       <p><strong>Plot:</strong> ${movie.Plot}</p>
                                   </div>
                              </div>
                          </div>
                        `;
                    document.body.appendChild(modal);

                    modal.addEventListener('show.bs.modal', function () {
                        document.querySelector(`#movieModal-${movie.imdbID}`).style.display = "block";
                        gsap.fromTo(
                            modal,
                            { opacity: 0, scale: 0.8, x: -30 },
                            { opacity: 1, scale: 1, x: 0, duration: 0.3, ease: "power2.out" }
                        );
                    });
                });

                carouselItem.appendChild(cardGroup);
                carouselInner.appendChild(carouselItem);
            }

            randomMovieInfo.appendChild(carouselInner);
            randomMovieInfo.insertAdjacentHTML(
                "beforeend",
                `
                <button class="carousel-control-prev" type="button" data-bs-target="#movieCarousel" data-bs-slide="prev">
                    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                    <span class="visually-hidden">Previous</span>
                </button>
                <button class="carousel-control-next" type="button" data-bs-target="#movieCarousel" data-bs-slide="next">
                    <span class="carousel-control-next-icon" aria-hidden="true"></span>
                    <span class="visually-hidden">Next</span>
                </button>
                `
            );

            randomMovieInfo.id = "movieCarousel";
        } else {
            randomMovieInfo.innerHTML = `<p>Не найдено ни одного фильма.</p>`;
        }
    };

    const cachedMovies = localStorage.getItem("cachedRandomMovies");

    randomMovieInfo.innerHTML = `
        <div id="spinner-container" class="d-flex justify-content-center my-5">
            <div class="spinner-border custom-spinner" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
    `;

    setTimeout(() => {
        if (cachedMovies) {
            displayMovies(JSON.parse(cachedMovies));
        } else {
            fetch(`/api/random-high-rated/`)
                .then(response => response.json())
                .then(data => {
                    if (data.movies && data.movies.length > 0) {
                        localStorage.setItem("cachedRandomMovies", JSON.stringify(data));
                    }
                    displayMovies(data);
                })
                .catch(error => {
                    randomMovieInfo.innerHTML = `<p>Произошла ошибка: ${error}</p>`;
                });
        }
    }, 2000);

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});

document.getElementById("movie-search-form").addEventListener("submit", function (event) {
    event.preventDefault();
    const query = document.getElementById("query").value;

    const movieInfo = document.getElementById("movie-info");
    movieInfo.innerHTML = `
        <div class="d-flex justify-content-center mt-3">
            <div class="spinner-border custom-spinner" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
    `;

    fetch(`/api/search/?query=${query}`)
        .then(response => response.json())
        .then(data => {
            movieInfo.innerHTML = "";

            if (data.error) {
                movieInfo.innerHTML = `<p>${data.error}</p>`;
                return;
            }

            const listContainer = document.createElement("ul");
            listContainer.classList.add("list-group", "w-100");

            data.movies.forEach((movie, index) => {
                const listItem = document.createElement("li");
                listItem.classList.add("list-group-item", "d-flex", "align-items-center", "mb-2");

                listItem.innerHTML = `
                    <img src="${movie.Poster}" alt="${movie.Title} Poster" class="img-thumbnail me-3" style="width:100px; height:auto;">
                    <div class="d-flex justify-content-between w-100">
                        <div>
                            <h5>${movie.Title}</h5>
                            <p style="margin-left:1px;" class="text-muted">${movie.Year}</p>
                            <p style="padding:0; margin-right:3vh;">
                                <i class="fa fa-star" style="color: #FFD700; text-shadow:
                                    -0.7px -0.7px 0.7px #656565,
                                    0.7px -0.7px 0.7px #656565,
                                    -0.7px 0.7px 0.7px #656565,
                                    0.7px 0.7px 0.7px #656565;"></i> ${movie.imdbRating}
                            </p>
                            <a href="https://www.imdb.com/title/${movie.imdbID}" target="_blank" style="padding:0; margin-right:3vh;" class="btn btn-link link-imbd">
                                <span class="imbd-text">IMDb</span>
                            </a>
                        </div>
                        <i class="fa fa-info-circle info-icon" data-movie-title="${movie.Title}" style="font-size: 1.5em; color: #8d8d8d; opacity: 0.8; cursor: pointer; margin-left: 10px; align-self: center;"></i>
                    </div>
                `;

                const addFavoriteButton = document.createElement("i");
                addFavoriteButton.classList.add("fa", "fa-heart", "add-to-favorites", "search-add-favorites", "fs-5");

                gsap.fromTo(addFavoriteButton,
                    {
                        scale: 0,
                    },
                    {
                        scale: 1,
                        duration: 0.5,
                        ease: "back.out(1.7)",
                        delay: 0.6,
                    }
                );

                addFavoriteButton.addEventListener("click", function () {
                    const movieData = {
                        title: movie.Title,
                        imdb_id: movie.imdbID,
                        poster: movie.Poster,
                        year: movie.Year,
                        genre: movie.Genre,
                        actors: movie.Actors,
                        imdb_rating: movie.imdbRating,
                        plot: movie.Plot,
                        movie_url: `https://www.imdb.com/title/${movie.imdbID}/`
                    };

                    fetch("http://127.0.0.1:8000/accounts/add-to-favorites/", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                            "X-CSRFToken": getCookie("csrftoken"),
                        },
                        body: JSON.stringify(movieData),
                    });

                    const favorites = JSON.parse(localStorage.getItem("favorites")) || [];
                    favorites.push(movieData);
                    localStorage.setItem("favorites", JSON.stringify(favorites));

                    alert(`${movie.Title} added to favorites.`);
                });

                listItem.appendChild(addFavoriteButton);
                listContainer.appendChild(listItem);

                if (index < data.movies.length - 1) {
                    const hr = document.createElement("hr");
                    hr.style.border = "1px solid #ccc";
                    listContainer.appendChild(hr);
                }

                gsap.fromTo(listItem, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.3, ease: "power1.inOut" });
            });

            movieInfo.appendChild(listContainer);

            let modalOpen = false;

            document.querySelectorAll(".info-icon").forEach(icon => {
                icon.addEventListener("click", function () {
                    if (modalOpen) return;

                    modalOpen = true;

                    const movieTitle = this.dataset.movieTitle;

                    fetch(`/api/search/?query=${movieTitle}`)
                        .then(response => response.json())
                        .then(data => {
                            if (data.movies && data.movies.length > 0) {
                                const movie = data.movies[0];

                                const modal = document.createElement("div");
                                modal.classList.add("modal", "fade");
                                modal.id = `movieModal-${movie.imdbID}`;
                                modal.setAttribute("tabindex", "-1");
                                modal.setAttribute("aria-labelledby", `movieModalLabel-${movie.imdbID}`);
                                modal.setAttribute("aria-hidden", "true");

                                modal.innerHTML = `
                                    <div class="modal-dialog">
                                        <div class="modal-content">
                                            <div class="modal-header">
                                                <h5 class="modal-title" id="movieModalLabel-${movie.imdbID}">${movie.Title}</h5>
                                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                            </div>
                                            <div class="modal-body">
                                                <img src="${movie.Poster}" alt="${movie.Title} Poster" class="img-fluid" style="width: 230px; border-radius: 11px;">
                                                <p class="rating-modal"><i class="fa fa-star" style="color: #FFD700; text-shadow:
                                                 -0.7px -0.7px 0.7px #656565,
                                                 0.7px -0.7px 0.7px #656565,
                                                -0.7px  0.7px 0.7px #656565,
                                                 0.7px  0.7px 0.7px #656565;"></i> ${movie.imdbRating}</p>
                                                <p><strong>Year:</strong> ${movie.Year}</p>
                                                <hr>
                                                <p><strong>Genre:</strong> ${movie.Genre}</p>
                                                <hr>
                                                <p><strong>Cast:</strong> ${movie.Actors}</p>
                                                <hr>
                                                <p><strong>Plot:</strong> ${movie.Plot}</p>
                                            </div>
                                        </div>
                                    </div>
                                `;

                                document.body.appendChild(modal);

                                const bootstrapModal = new bootstrap.Modal(modal);
                                bootstrapModal.show();

                                modal.addEventListener("hidden.bs.modal", function () {
                                    modal.remove();
                                    modalOpen = false;
                                });

                                gsap.fromTo(modal, { opacity: 0, scale: 0.8, x: -30 }, { opacity: 1, scale: 1, x: 0, duration: 0.3, ease: "power2.out" });
                            } else {
                                alert("No film data was found.");
                            }
                        })
                        .catch(error => {
                            alert(`Произошла ошибка: ${error}`);
                        });
                });
            });
        })
        .catch(error => {
            movieInfo.innerHTML = `<p>Произошла ошибка: ${error}</p>`;
        });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}