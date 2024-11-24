document.addEventListener("DOMContentLoaded", function () {
    const actorsContainer = document.getElementById("actors-container");

    actorsContainer.innerHTML = `
        <div class="d-flex justify-content-center mt-3 mb-3">
            <div class="spinner-border custom-spinner" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
    `;

    fetch("/api/top-actors/")
        .then(response => response.json())
        .then(data => {
            actorsContainer.innerHTML = "";

            if (data.error) {
                actorsContainer.innerHTML = `<p class="text-danger">${data.error}</p>`;
            } else if (data.actors && data.actors.length > 0) {

                const ratedTitle = document.createElement("h2");
                ratedTitle.classList.add("rated-actors", "text-center", "mb-4");
                ratedTitle.textContent = "Top Cast";
                actorsContainer.before(ratedTitle);

                const carousel = document.createElement("div");
                carousel.id = "actorsCarousel";
                carousel.classList.add("carousel", "slide");
                carousel.setAttribute("data-bs-ride", "carousel");

                const carouselInner = document.createElement("div");
                carouselInner.classList.add("carousel-inner");

                for (let i = 0; i < data.actors.length; i += 8) {
                    const carouselItem = document.createElement("div");
                    carouselItem.classList.add("carousel-item");
                    if (i === 0) carouselItem.classList.add("active");

                    const row = document.createElement("div");
                    row.style.textAlign = "center";

                    data.actors.slice(i, i + 8).forEach(actor => {
                        const col = document.createElement("span");
                        col.classList.add("rounded-image-container");

                        col.innerHTML = `
                            <img src="${actor.ProfileImage || '/static/images/placeholder.png'}" 
                                 alt="${actor.Name}" 
                                 class="rounded-image">
                                 <p class="mt-2">
                                    <a href="${actor.IMDbLink}" class="name-actors-p" target="_blank">
                                    ${actor.Name} 
                                    </a>
                                 </p>
                        `;
                        row.appendChild(col);
                    });

                    carouselItem.appendChild(row);
                    carouselInner.appendChild(carouselItem);
                }

                carousel.appendChild(carouselInner);

                carousel.insertAdjacentHTML(
                    "beforeend",
                    `
                    <button class="carousel-control-prev" type="button" data-bs-target="#actorsCarousel" data-bs-slide="prev">
                        <span class="carousel-control-prev-icon" aria-hidden="true" style="transform: scale(0.86);"></span>
                        <span class="visually-hidden">Previous</span>
                    </button>
                    <button class="carousel-control-next" type="button" data-bs-target="#actorsCarousel" data-bs-slide="next">
                        <span class="carousel-control-next-icon" aria-hidden="true" style="transform: scale(0.86);"></span>
                        <span class="visually-hidden">Next</span>
                    </button>
                    `
                );

                actorsContainer.appendChild(carousel);
            } else {
                actorsContainer.innerHTML = `<p class="text-warning">Актеры не найдены.</p>`;
            }
        })
        .catch(error => {
            actorsContainer.innerHTML = `<p class="text-danger">Произошла ошибка: ${error}</p>`;
        });
});