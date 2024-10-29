document.getElementById("movie-search-form").addEventListener("submit", function(event) {
    event.preventDefault();
    const query = document.getElementById("query").value;

    fetch(`/api/search/?query=${query}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById("movie-info").innerHTML = `<p>${data.error}</p>`;
            } else {
                document.getElementById("movie-info").innerHTML = `
                    <h3>${data.Title} (${data.Year})</h3>
                    <img src="${data.Poster}" alt="${data.Title} Poster" style="width:100px;height:auto;">
                    <p><strong>Rated:</strong> ${data.Rated}</p>
                    <p><strong>Released:</strong> ${data.Released}</p>
                    <p><strong>Runtime:</strong> ${data.Runtime}</p>
                    <p><strong>Genre:</strong> ${data.Genre}</p>
                    <p><strong>Director:</strong> ${data.Director}</p>
                    <p><strong>Actors:</strong> ${data.Actors}</p>
                    <p><strong>Plot:</strong> ${data.Plot}</p>
                    <p><strong>IMDb Rating:</strong> ${data.imdbRating}</p>
                `;
            }
        })
        .catch(error => {
            document.getElementById("movie-info").innerHTML = `<p>An error occurred: ${error}</p>`;
        });
});