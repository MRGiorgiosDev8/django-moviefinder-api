document.addEventListener("DOMContentLoaded", function () {
    const popularMovieInfo = document.getElementById("most-popular-movies");

    /**
     * Отображает список популярных фильмов на странице.
     *
     * @param {Object} data - Объект данных, содержащий информацию о фильмах.
     * @param {Array} data.movies - Массив объектов фильмов.
     * @param {string} data.movies[].Title - Название фильма.
     * @param {string} data.movies[].Poster - URL постера фильма.
     * @param {string} data.movies[].imdbID - ID фильма на IMDb.
     * @param {string} data.movies[].Year - Год выпуска фильма.
     * @param {string} data.movies[].Genre - Жанр фильма.
     * @param {string} data.movies[].Actors - Актеры фильма.
     * @param {string} data.movies[].imdbRating - Рейтинг фильма на IMDb.
     * @param {string} data.movies[].Plot - Краткое описание сюжета фильма.
     */
    const displayMovies = (data) => {
        popularMovieInfo.innerHTML = "";

        const popularTitle = document.createElement("h2");
        popularTitle.classList.add("popular-h2");
        popularTitle.textContent = "Popular Releases";
        popularMovieInfo.appendChild(popularTitle);

        gsap.fromTo(
            ".popular-h2",
            { scale: 0, opacity: 0 },
            { scale: 1, opacity: 1, duration: 0.6, ease: "power2.out", delay: 0.4 }
        );

        if (data.movies && data.movies.length > 0) {
            const carouselInner = document.createElement("div");
            carouselInner.classList.add("carousel-inner");

            const isMobile = window.matchMedia("(max-width: 768px)").matches;
            const moviesPerCarouselItem = isMobile ? 2 : 5;

            for (let i = 0; i < data.movies.length; i += moviesPerCarouselItem) {
                const carouselItem = document.createElement("div");
                carouselItem.classList.add("carousel-item");
                if (i === 0) carouselItem.classList.add("active");

                const cardGroup = document.createElement("div");
                cardGroup.classList.add("d-flex", "justify-content-center");

                data.movies.slice(i, i + moviesPerCarouselItem).forEach(movie => {
                    const movieCard = document.createElement("div");
                    movieCard.classList.add("movie-card", "card", "text-center", "col-sm-12");

                    movieCard.innerHTML = `
                        <img src="${movie.Poster}" alt="${movie.Title} Poster" class="img-fluid w-100" data-bs-toggle="modal" data-bs-target="#movieModal-${movie.imdbID}">
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

            popularMovieInfo.appendChild(carouselInner);
            popularMovieInfo.insertAdjacentHTML(
                "beforeend",
                `
                <button class="carousel-control-prev" type="button" data-bs-target="#moviePopularCarousel" data-bs-slide="prev">
                    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                    <span class="visually-hidden">Previous</span>
                </button>
                <button class="carousel-control-next" type="button" data-bs-target="#moviePopularCarousel" data-bs-slide="next">
                    <span class="carousel-control-next-icon" aria-hidden="true"></span>
                    <span class="visually-hidden">Next</span>
                </button>
                `
            );

            popularMovieInfo.id = "movieCarousel";
        } else {
            popularMovieInfo.innerHTML = `<p>Не найдено ни одного фильма.</p>`;
        }
    };

    const cachedMovies = localStorage.getItem("cachedPopularMovies");

    popularMovieInfo.innerHTML = `
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
            fetch(`/api/most-popular-movies/`)
                .then(response => response.json())
                .then(data => {
                    if (data.movies && data.movies.length > 0) {
                        localStorage.setItem("cachedPopularMovies", JSON.stringify(data));
                    }
                    displayMovies(data);
                })
                .catch(error => {
                    popularMovieInfo.innerHTML = `<p>Произошла ошибка: ${error}</p>`;
                });
        }
    }, 3000);

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