document.addEventListener("DOMContentLoaded", function () {
    const randomMovieInfo = document.getElementById("random-movie-info");

    const spinnerContainer = document.createElement("div");
    spinnerContainer.id = "spinner-container";
    randomMovieInfo.appendChild(spinnerContainer);

    gsap.set("#spinner-container", { opacity: 1 });

    gsap.to(".spinner", {
        rotation: 360,
        duration: 1,
        ease: "power1.inOut",
        repeat: -1
    });

    fetch(`/api/random-high-rated/`)
        .then(response => response.json())
        .then(data => {
            randomMovieInfo.innerHTML = "";
            const ratedTitle = document.createElement("h2");
            ratedTitle.classList.add("rated-h2");
            ratedTitle.textContent = "Top 20 Movies";
            randomMovieInfo.appendChild(ratedTitle);

              gsap.fromTo(".rated-h2",
                { scale: 0, opacity: 0 },
                { scale: 1, opacity: 1, duration: 0.6, ease: "power2.out", delay: 0.4 }
            );

            gsap.to("#spinner-container", { opacity: 0, duration: 0.5 });

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
                            <img src="${movie.Poster}" alt="${movie.Title} Poster" class="img-fluid w-100" style="height: 307px;">
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
                        cardGroup.appendChild(movieCard);

                        gsap.fromTo(movieCard, { x: -100 }, { x: 0,  duration: 0.3, ease: "power1.inOut"  });
                    });

                    carouselItem.appendChild(cardGroup);
                    carouselInner.appendChild(carouselItem);
                }

                randomMovieInfo.appendChild(carouselInner);
                randomMovieInfo.insertAdjacentHTML("beforeend", `
                    <button class="carousel-control-prev" type="button" data-bs-target="#movieCarousel" data-bs-slide="prev">
                        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                        <span class="visually-hidden">Previous</span>
                    </button>
                    <button class="carousel-control-next" type="button" data-bs-target="#movieCarousel" data-bs-slide="next">
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
            randomMovieInfo.innerHTML = `<p>An error occurred: ${error}</p>`;
        });
});

document.getElementById("movie-search-form").addEventListener("submit", function (event) {
    event.preventDefault();
    const query = document.getElementById("query").value;

    const spinnerContainer = document.getElementById("spinner-container");
    gsap.set(spinnerContainer, { opacity: 1 });

    fetch(`/api/search/?query=${query}`)
        .then(response => response.json())
        .then(data => {
            const movieInfo = document.getElementById("movie-info");
            movieInfo.innerHTML = "";

            gsap.to(spinnerContainer, { opacity: 0, duration: 0.4, ease: "power1.inOut" });

            if (data.error) {
                movieInfo.innerHTML = `<p>${data.error}</p>`;
            } else {
                const listContainer = document.createElement("ul");
                listContainer.classList.add("list-group", "w-100");

                data.movies.forEach((movie, index) => {
                    const listItem = document.createElement("li");
                    listItem.classList.add("list-group-item", "d-flex", "align-items-center", "mb-2");

                    listItem.innerHTML = `
                        <img src="${movie.Poster}" alt="${movie.Title} Poster" class="img-thumbnail me-3" style="width:100px; height:auto;">
                        <div>
                            <h5>${movie.Title} (${movie.Year})</h5>
                            <p class="mb-1"><strong>IMDb Rating:</strong> ${movie.imdbRating}</p>
                            <a href="https://www.imdb.com/title/${movie.imdbID}" target="_blank" class="btn btn-link p-0">View on IMDb</a>
                        </div>
                    `;
                    listContainer.appendChild(listItem);

                    if (index < data.movies.length - 1) {
                        const hr = document.createElement("hr");
                        hr.style.border = "1px solid #ccc"; 
                        listContainer.appendChild(hr);
                    }

                    gsap.fromTo(listItem, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.3, ease: "power1.inOut" });
                });

                movieInfo.appendChild(listContainer);
            }
        })
        .catch(error => {
            document.getElementById("movie-info").innerHTML = `<p>An error occurred: ${error}</p>`;
        });
});