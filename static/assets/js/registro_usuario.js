// REGISTRO DE USUARIOS

// Funcionalidad para mostrar/ocultar contraseña
document.getElementById("togglePassword").addEventListener("click", function () {
    const passwordInput = document.getElementById("password");
    const icon = this.querySelector("i");
  
    if (passwordInput.type === "password") {
      passwordInput.type = "text";
      icon.classList.remove("bi-eye");
      icon.classList.add("bi-eye-slash");
    } else {
      passwordInput.type = "password";
      icon.classList.remove("bi-eye-slash");
      icon.classList.add("bi-eye");
    }
  });
  
  // Limitar la entrada de dígitos en el campo teléfono
  document.getElementById("telefono").addEventListener("input", function () {
    if (this.value.length > 13) {
      this.value = this.value.slice(0, 13);
    }
  });
  
  // Limitar la entrada de dígitos en el campo documento
  document.getElementById("documento").addEventListener("input", function () {
    if (this.value.length > 15) {
      this.value = this.value.slice(0, 15);
    }
  });
  
  // Validaciones específicas para la contraseña
  document.getElementById("password").addEventListener("input", function () {
    this.setCustomValidity("");
  });
  
  // Validar selects cuando cambian
  const selects = document.querySelectorAll("select[required]");
  selects.forEach(select => {
    select.addEventListener("change", function() {
      if (this.value) {
        this.setCustomValidity("");
      }
    });
  });
  
  // Validación general del formulario
  document.getElementById("registroForm").addEventListener("submit", function (event) {
    let formIsValid = true;
    
    // Validar selects
    selects.forEach(select => {
      if (!select.value) {
        select.setCustomValidity("Por favor, selecciona una opción");
        formIsValid = false;
      } else {
        select.setCustomValidity("");
      }
    });
  
    // Validar contraseña
    const password = document.getElementById("password").value;
    if (password.length < 8 || password.length > 20) {
      document.getElementById("password").setCustomValidity("La contraseña debe tener entre 8 y 20 caracteres");
      formIsValid = false;
    } else if (/^[a-zA-Z]+$/.test(password)) {
      document.getElementById("password").setCustomValidity("La contraseña no puede contener solo letras");
      formIsValid = false;
    } else if (/^\d+$/.test(password)) {
      document.getElementById("password").setCustomValidity("La contraseña no puede contener solo números");
      formIsValid = false;
    }
  
    // Validar correo
    const correo = document.getElementById("correo").value;
    const emailPattern = /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/;
    if (!emailPattern.test(correo)) {
      document.getElementById("correo").setCustomValidity("Ingresa un correo válido (por ejemplo, usuario@dominio.com)");
      formIsValid = false;
    }
  
    if (!formIsValid) {
      event.preventDefault();
      // Forzar la visualización de los mensajes de validación
      this.reportValidity();
    }
  });
  
  // Limpiar mensajes de error al escribir
  const inputs = document.querySelectorAll("input");
  inputs.forEach(input => {
    input.addEventListener("input", function () {
      this.setCustomValidity("");
    });
  });

// EDITAR

// Función para mostrar/ocultar la contraseña
document.getElementById("togglePassword").addEventListener("click", function () {
  const passwordInput = document.getElementById("new_pass_user");
  const icon = this.querySelector("i");

  if (passwordInput.type === "password") {
    passwordInput.type = "text";
    icon.classList.remove("bi-eye");
    icon.classList.add("bi-eye-slash");
  } else {
    passwordInput.type = "password";
    icon.classList.remove("bi-eye-slash");
    icon.classList.add("bi-eye");
  }
});

document.getElementById("toggleRepeatPassword").addEventListener("click", function () {
  const repeatPasswordInput = document.getElementById("repetir_pass_user");
  const icon = this.querySelector("i");

  if (repeatPasswordInput.type === "password") {
    repeatPasswordInput.type = "text";
    icon.classList.remove("bi-eye");
    icon.classList.add("bi-eye-slash");
  } else {
    repeatPasswordInput.type = "password";
    icon.classList.remove("bi-eye-slash");
    icon.classList.add("bi-eye");
  }
});

// Validaciones específicas para la contraseña
function validatePassword(input) {
  const password = input.value;

  if (password.length < 8) {
    input.setCustomValidity("La contraseña debe tener al menos 8 caracteres (actualmente tiene " + password.length + ")");
    return false;
  }

  if (password.length > 20) {
    input.setCustomValidity("La contraseña no puede tener más de 20 caracteres");
    return false;
  }

  if (/^[a-zA-Z]+$/.test(password)) {
    input.setCustomValidity("La contraseña no puede contener solo letras");
    return false;
  }

  if (/^\d+$/.test(password)) {
    input.setCustomValidity("La contraseña no puede contener solo números");
    return false;
  }

  input.setCustomValidity("");
  return true;
}

document.getElementById("new_pass_user").addEventListener("invalid", function () {
  validatePassword(this);
});

document.getElementById("repetir_pass_user").addEventListener("invalid", function () {
  validatePassword(this);
});

// Limpiar el mensaje de error cuando el usuario corrija la contraseña
document.getElementById("new_pass_user").addEventListener("input", function () {
  this.setCustomValidity("");
});

document.getElementById("repetir_pass_user").addEventListener("input", function () {
  this.setCustomValidity("");
});

// Validar que las contraseñas coincidan antes de enviar
document.getElementById("passwordForm").addEventListener("submit", function (event) {
  const newPassword = document.getElementById("new_pass_user").value;
  const repeatPassword = document.getElementById("repetir_pass_user").value;

  if (newPassword !== repeatPassword) {
    document.getElementById("repetir_pass_user").setCustomValidity("Las contraseñas no coinciden");
    event.preventDefault();
  } else {
    document.getElementById("repetir_pass_user").setCustomValidity("");
  }
});

// Validaciones para el formulario de edición
document.getElementById("editarForm").addEventListener("submit", function (event) {
  const nombreInput = document.getElementById("nombre");
  const apellidoInput = document.getElementById("apellido");
  const correoInput = document.getElementById("correo");
  const documentoInput = document.getElementById("documento");
  const telefonoInput = document.getElementById("telefono");

  // Validar nombre
  const nombre = nombreInput.value;
  if (nombre.length < 2 || nombre.length > 100) {
    nombreInput.setCustomValidity("El nombre debe tener entre 2 y 100 caracteres");
    event.preventDefault();
    return;
  } else {
    nombreInput.setCustomValidity("");
  }

  // Validar apellido
  const apellido = apellidoInput.value;
  if (apellido.length < 2 || apellido.length > 100) {
    apellidoInput.setCustomValidity("El apellido debe tener entre 2 y 100 caracteres");
    event.preventDefault();
    return;
  } else {
    apellidoInput.setCustomValidity("");
  }

  // Validar correo
  const correo = correoInput.value;
  if (correo.length > 50) {
    correoInput.setCustomValidity("El correo no puede exceder los 50 caracteres");
    event.preventDefault();
    return;
  }
  if (!correo.includes("@")) {
    correoInput.setCustomValidity("El correo debe contener un @");
    event.preventDefault();
    return;
  }
  const emailPattern = /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/;
  if (!emailPattern.test(correo)) {
    correoInput.setCustomValidity("Ingresa un correo válido (por ejemplo, usuario@dominio.com)");
    event.preventDefault();
    return;
  } else {
    correoInput.setCustomValidity("");
  }

  // Validar documento
  const documento = documentoInput.value;
  if (documento <= 0) {
    documentoInput.setCustomValidity("El documento debe ser un número mayor a 0");
    event.preventDefault();
    return;
  }
  if (String(documento).length < 10 || String(documento).length > 15) {
    documentoInput.setCustomValidity("El documento debe tener entre 10 y 15 dígitos");
    event.preventDefault();
    return;
  } else {
    documentoInput.setCustomValidity("");
  }

  // Validar teléfono
  const telefono = telefonoInput.value;
  if (telefono <= 0) {
    telefonoInput.setCustomValidity("El teléfono debe ser un número mayor a 0");
    event.preventDefault();
    return;
  }
  if (String(telefono).length < 7 || String(telefono).length > 13) {
    telefonoInput.setCustomValidity("El teléfono debe tener entre 7 y 13 dígitos");
    event.preventDefault();
    return;
  } else {
    telefonoInput.setCustomValidity("");
  }
});

// Limpiar mensajes de error al corregir
document.getElementById("nombre").addEventListener("input", function () {
  this.setCustomValidity("");
});

document.getElementById("apellido").addEventListener("input", function () {
  this.setCustomValidity("");
});

document.getElementById("correo").addEventListener("input", function () {
  this.setCustomValidity("");
});

document.getElementById("documento").addEventListener("input", function () {
  this.setCustomValidity("");
  if (this.value.length > 15) {
    this.value = this.value.slice(0, 15);
  }
});

document.getElementById("telefono").addEventListener("input", function () {
  this.setCustomValidity("");
  if (this.value.length > 13) {
    this.value = this.value.slice(0, 13);
  }
});