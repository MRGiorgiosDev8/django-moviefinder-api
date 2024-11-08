document.addEventListener("DOMContentLoaded", function() {
    fetch(`/api/random-high-rated/`)
        .then(response => response.json())
        .then(data => {
            const randomMovieInfo = document.getElementById("random-movie-info");
            randomMovieInfo.innerHTML = "<h2>High-Rated Random Movies</h2>";

            if (data.movies && data.movies.length > 0) {
                data.movies.forEach(movie => {
                    randomMovieInfo.innerHTML += `
                        <div class="movie-card">
                            <h3>${movie.Title} (${movie.Year})</h3>
                            <img src="${movie.Poster}" alt="${movie.Title} Poster" style="width:100px;height:auto;">
                            <p><strong>IMDb Rating:</strong> ${movie.imdbRating}</p>
                            <a href="https://www.imdb.com/title/${movie.imdbID}" target="_blank">View on IMDb</a>
                        </div>
                    `;
                });
            } else {
                randomMovieInfo.innerHTML += `<p>No high-rated movies found.</p>`;
            }
        })
        .catch(error => {
            document.getElementById("random-movie-info").innerHTML = `<p>An error occurred: ${error}</p>`;
        });
});

document.getElementById("movie-search-form").addEventListener("submit", function(event) {
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
                data.movies.forEach(movie => {
                    movieInfo.innerHTML += `
                        <div class="movie-card">
                            <h3>${movie.Title} (${movie.Year})</h3>
                            <img src="${movie.Poster}" alt="${movie.Title} Poster" style="width:100px;height:auto;">
                            <a href="https://www.imdb.com/title/${movie.imdbID}" target="_blank">View on IMDb</a>
                        </div>
                    `;
                });
            }
        })
        .catch(error => {
            document.getElementById("movie-info").innerHTML = `<p>An error occurred: ${error}</p>`;
        });
});