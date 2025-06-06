document.addEventListener('DOMContentLoaded', () => {
  const role = sessionStorage.getItem("role") || "user";
  document.getElementById("user-info").innerText = "Вы вошли как: " + role;

  if (role === "admin") {
    document.getElementById("admin-actions").style.display = "block";
    document.getElementById("add-book-form").addEventListener("submit", async (e) => {
      e.preventDefault();
      const data = new URLSearchParams(new FormData(e.target));
      const res = await fetch("/books/add", { method: "POST", body: data });
      if (res.ok) {
        location.reload();
      } else {
        alert("Ошибка при добавлении книги");
      }
    });
  }

  loadBooks(role);
});

async function loadBooks(role) {
  const res = await fetch("/books");
  const books = await res.json();
  const tbody = document.querySelector("#books-table tbody");
  tbody.innerHTML = "";

  books.forEach(book => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${book.title}</td>
      <td>${book.author}</td>
      <td>${book.isRented ? "В аренде" : "Свободна"}</td>
      <td>${getActions(book, role)}</td>
    `;
    tbody.appendChild(tr);
  });
}

function getActions(book, role) {
  if (role === "admin") {
    return `
      <button onclick="deleteBook(${book.id}, ${book.isRented})">Удалить</button>
    `;
  } else {
    return book.isRented
      ? `<button onclick="returnBook(${book.id})">Сдать</button>`
      : `<button onclick="rentBook(${book.id})">Взять</button>`;
  }
}

async function deleteBook(id, isRented) {
  if (isRented) return alert("Нельзя удалить книгу, она в аренде!");
  const res = await fetch("/books/delete", {
    method: "POST",
    body: new URLSearchParams({ id })
  });
  if (res.ok) location.reload();
  else alert("Ошибка удаления");
}

async function rentBook(id) {
  const res = await fetch("/books/rent", {
    method: "POST",
    body: new URLSearchParams({ id })
  });
  if (res.ok) location.reload();
  else alert("Ошибка аренды");
}

async function returnBook(id) {
  const res = await fetch("/books/return", {
    method: "POST",
    body: new URLSearchParams({ id })
  });
  if (res.ok) location.reload();
  else alert("Ошибка возврата");
}
