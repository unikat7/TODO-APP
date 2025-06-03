const apiBase = 'http://localhost:8000/app/'; // Update this to your API base URL

// DOM elements
const authSection = document.getElementById('auth-section');
const registerSection = document.getElementById('register-section');
const todoSection = document.getElementById('todo-section');

const loginUsername = document.getElementById('login-username');
const loginPassword = document.getElementById('login-password');
const btnLogin = document.getElementById('btn-login');
const btnShowRegister = document.getElementById('btn-show-register');

const regUsername = document.getElementById('reg-username');
const regPassword = document.getElementById('reg-password');
const regConfirmPassword = document.getElementById('reg-confirm-password');
const btnRegister = document.getElementById('btn-register');
const btnShowLogin = document.getElementById('btn-show-login');

const todoForm = document.getElementById('todo-form');
const todoInput = document.getElementById('todo-input');
const todoList = document.getElementById('todo-list');
const btnLogout = document.getElementById('btn-logout');

function setToken(token) {
  localStorage.setItem('access_token', token);
}

function getToken() {
  return localStorage.getItem('access_token');
}

function clearToken() {
  localStorage.removeItem('access_token');
}

function showSection(section) {
  authSection.style.display = section === 'auth' ? 'block' : 'none';
  registerSection.style.display = section === 'register' ? 'block' : 'none';
  todoSection.style.display = section === 'todo' ? 'block' : 'none';
}

// Show login or todos based on token
if (getToken()) {
  showSection('todo');
  loadTodos();
} else {
  showSection('auth');
}

// Toggle register form
btnShowRegister.onclick = () => showSection('register');
btnShowLogin.onclick = () => showSection('auth');

// Login
btnLogin.onclick = async () => {
  const username = loginUsername.value.trim();
  const password = loginPassword.value.trim();

  if (!username || !password) {
    alert('Enter username and password');
    return;
  }

  try {
    const response = await fetch('http://localhost:8000/api/token/', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ username, password }),
    });

    if (!response.ok) {
      const err = await response.json();
      alert('Login failed: ' + JSON.stringify(err));
      return;
    }

    const data = await response.json();
    setToken(data.access);
    showSection('todo');
    loadTodos();
  } catch (error) {
    alert('Login error: ' + error.message);
  }
};

// Register (send confirm_password as is; backend handles validation)
btnRegister.onclick = async () => {
  const username = regUsername.value.trim();
  const password = regPassword.value.trim();
  const confirmPassword = regConfirmPassword.value.trim();

  if (!username || !password || !confirmPassword) {
    alert('Please fill all fields');
    return;
  }

  try {
    const response = await fetch(apiBase + 'register/', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        username,
        password,
        confirm_password: confirmPassword
      }),
    });

    if (!response.ok) {
      const err = await response.json();
      alert('Registration failed: ' + JSON.stringify(err));
      return;
    }

    alert('Registration successful! Please login.');
    showSection('auth');
  } catch (error) {
    alert('Registration error: ' + error.message);
  }
};

// Load todos list
async function loadTodos() {
  const token = getToken();
  if (!token) return;

  try {
    const response = await fetch(apiBase + 'todos/', {
      headers: { Authorization: `Bearer ${token}` },
    });

    if (!response.ok) {
      if (response.status === 401) {
        alert('Session expired, please login again.');
        logout();
      } else {
        alert('Failed to load todos');
      }
      return;
    }

    const todos = await response.json();
    todoList.innerHTML = '';

    todos.forEach(todo => {
      const li = document.createElement('li');
      li.textContent = todo.title;

      const delBtn = document.createElement('button');
      delBtn.textContent = 'Delete';
      delBtn.onclick = () => deleteTodo(todo.id);

      li.appendChild(delBtn);
      todoList.appendChild(li);
    });
  } catch (error) {
    alert('Error loading todos: ' + error.message);
  }
}

// Add new todo
todoForm.onsubmit = async e => {
  e.preventDefault();

  const title = todoInput.value.trim();
  if (!title) return;

  const token = getToken();
  if (!token) return;

  try {
    const response = await fetch(apiBase + 'todos/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({ title }),
    });

    if (!response.ok) {
      alert('Failed to add todo');
      return;
    }

    todoInput.value = '';
    loadTodos();
  } catch (error) {
    alert('Error adding todo: ' + error.message);
  }
};

// Delete todo
async function deleteTodo(id) {
  const token = getToken();
  if (!token) return;

  try {
    const response = await fetch(apiBase + `todos/${id}/`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${token}` },
    });

    if (!response.ok) {
      alert('Failed to delete todo');
      return;
    }

    loadTodos();
  } catch (error) {
    alert('Error deleting todo: ' + error.message);
  }
}

// Logout
btnLogout.onclick = () => logout();

function logout() {
  clearToken();
  showSection('auth');
}
