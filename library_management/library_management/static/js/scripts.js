// Fetch and display authors
document.addEventListener("DOMContentLoaded", () => {
    const authorsList = document.getElementById("authors-list");
    const addAuthorForm = document.getElementById("add-author-form");

    // Fetch authors
    fetch("/api/authors/")
        .then((response) => response.json())
        .then((data) => {
            authorsList.innerHTML = "<ul>" + data.map(author => `<li>${author.name}</li>`).join("") + "</ul>";
        });

    // Add new author
    addAuthorForm.addEventListener("submit", (event) => {
        event.preventDefault();

        const name = document.getElementById("author-name").value;
        const bio = document.getElementById("author-bio").value;

        fetch("/api/authors/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ name, bio }),
        })
        .then((response) => response.json())
        .then((newAuthor) => {
            authorsList.innerHTML += `<li>${newAuthor.name}</li>`;
            addAuthorForm.reset();
        });
    });
});
