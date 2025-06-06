document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('loginForm');
  const registerForm = document.getElementById('registerForm');

  if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const data = new URLSearchParams(new FormData(loginForm));
      const res = await fetch('/login', { method: 'POST', body: data });
      if (res.ok) {
        const role = await res.text();
        sessionStorage.setItem("role", role);
        window.location.href = "books.html";
      } else {
        alert('Ошибка входа');
      }
    });
  }

  if (registerForm) {
    registerForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const data = new URLSearchParams(new FormData(registerForm));
      const res = await fetch('/register', { method: 'POST', body: data });
      if (res.ok) {
        alert("Регистрация прошла успешно");
        window.location.href = "index.html";
      } else {
        alert('Ошибка регистрации');
      }
    });
  }

  if (window.location.pathname.endsWith("books.html")) {
    loadBooks();
  }
});

async function loadBooks() {
  const res = await fetch('/books');
  const books = await res.json();
  const tbody = document.querySelector('#bookTable tbody');
  const form = document.getElementById('bookForm');
  const role = sessionStorage.getItem("role");
  if (role === "admin") form.classList.remove("hidden");

  books.forEach(book => {
    const tr = document.createElement('tr');
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
  let buttons = '';
  if (role === "admin") {
    buttons += `<button onclick="deleteBook(${book.id}, ${book.isRented})">Удалить</button>`;
  } else {
    buttons += book.isRented
      ? `<button onclick="returnBook(${book.id})">Вернуть</button>`
      : `<button onclick="rentBook(${book.id})">Взять</button>`;
  }
  return buttons;
}

async function rentBook(id) {
  await fetch('/books/rent', {
    method: 'POST',
    body: `id=${id}`
  });
  location.reload();
}

async function returnBook(id) {
  await fetch('/books/return', {
    method: 'POST',
    body: `id=${id}`
  });
  location.reload();
}

async function deleteBook(id, rented) {
  if (rented) {
    alert("Нельзя удалить книгу, она в аренде");
    return;
  }
  await fetch('/books/delete', {
    method: 'POST',
    body: `id=${id}`
  });
  location.reload();
}

async function addBook() {
  const title = document.getElementById("bookTitle").value;
  const author = document.getElementById("bookAuthor").value;
  const data = `title=${title}&author=${author}`;
  await fetch('/books/add', { method: 'POST', body: data });
  location.reload();
}

async function logout() {
  await fetch('/logout');
  sessionStorage.clear();
  window.location.href = "index.html";
}
