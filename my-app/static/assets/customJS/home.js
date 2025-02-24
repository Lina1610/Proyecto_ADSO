// Verifica si loaderOut ya está declarado antes de asignarle el valor
if (typeof loaderOut === 'undefined') {
  const loaderOut = document.querySelector("#loader-out");

  function fadeOut(element) {
    let opacity = 1;
    const timer = setInterval(function () {
      if (opacity <= 0.1) {
        clearInterval(timer);
        element.style.display = "none";
      }
      element.style.opacity = opacity;
      opacity -= opacity * 0.1;
    }, 50);
  }
  fadeOut(loaderOut);
}

// Función para eliminar empleado
function eliminarEmpleado(id_empleado, foto_empleado) {
  if (confirm("¿Estas seguro que deseas Eliminar el empleado?")) {
    let url = `/borrar-empleado/${id_empleado}/${foto_empleado}`;
    if (url) {
      window.location.href = url;
    }
  }
}

// Validación de contraseñas al enviar el formulario
document.getElementById('register-form')?.addEventListener('submit', function (e) {
  const pass = document.getElementById('pass_user').value;
  const confirmPass = document.getElementById('confirm_pass_user').value;

  if (pass !== confirmPass) {
    e.preventDefault(); // Prevenir el envío del formulario
    alert('Las contraseñas no coinciden. Por favor, verifique.');
  }
});

// Indicador de fortaleza de la contraseña
document.getElementById('pass_user')?.addEventListener('input', function () {
  const password = this.value;
  const strengthBar = document.getElementById('password-strength');
  let strength = 0;

  if (password.length >= 8) strength++;
  if (password.match(/[a-z]/)) strength++;
  if (password.match(/[A-Z]/)) strength++;
  if (password.match(/[0-9]/)) strength++;
  if (password.match(/[^a-zA-Z0-9]/)) strength++;

  const strengthText = ['Débil', 'Moderada', 'Fuerte', 'Muy fuerte', 'Excelente'][strength - 1];
  strengthBar.textContent = `Fortaleza: ${strengthText}`;
  strengthBar.style.color = ['red', 'orange', '#FFA500', 'green', 'darkgreen'][strength - 1];
});

// Inicialización de intl-tel-input
document.addEventListener("DOMContentLoaded", function () {
  const input = document.querySelector("#telefono");
  const codigoPaisInput = document.querySelector("#codigo_pais");

  if (input && codigoPaisInput) {
    // Inicializamos intl-tel-input
    const iti = window.intlTelInput(input, {
      utilsScript: "https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/17.0.8/js/utils.js",
      preferredCountries: ["co", "us", "mx", "es"], // Países preferidos
      separateDialCode: true, // Mostrar el código de país por separado
      initialCountry: "auto",  // Detectar el país automáticamente
      geoIpLookup: function (callback) {
        fetch("https://ipapi.co/json/")
          .then(response => response.json())
          .then(data => callback(data.country_code))
          .catch(() => callback("us")); // Si falla, asigna por defecto "us"
      },
      autoPlaceholder: "aggressive",  // Formato automático del número
    });

    // Actualizar el campo oculto con el código de país
    input.addEventListener('input', function () {
      const countryData = iti.getSelectedCountryData();
      codigoPaisInput.value = countryData.dialCode;
    });

    // Limpiar el campo de teléfono al cambiar de país
    input.addEventListener('countrychange', function () {
      const countryData = iti.getSelectedCountryData();
      codigoPaisInput.value = countryData.dialCode;
      input.value = ""; // Limpiar el campo de teléfono
    });

    // Validación del formulario al enviar
    document.getElementById("register-form")?.addEventListener("submit", function (e) {
      if (!iti.isValidNumber()) {
        e.preventDefault(); // Evita el envío si el número es inválido
        alert("Número de teléfono inválido. Por favor, verifique.");
        return;
      }

      const fullNumber = iti.getNumber();
      console.log("Número completo:", fullNumber);

      const countryData = iti.getSelectedCountryData();
      console.log("Código de país:", countryData.dialCode);
      console.log("Nombre del país:", countryData.name);
    });
  } else {
    console.error("No se encontró el campo de teléfono o el campo de código de país.");
  }
});


function eliminarUsuario(id) {
  if (confirm("¿Estás seguro de eliminar este usuario?")) {
      fetch(`/eliminar-usuario/${id}`, {
          method: "GET",
      })
      .then((response) => response.json())
      .then((data) => {
          if (data.success) {
              // Eliminar la fila de la tabla sin recargar la página
              const fila = document.getElementById(`usuario_${id}`);
              if (fila) {
                  fila.remove();
              }
              alert("Usuario eliminado correctamente");
          } else {
              alert("Error al eliminar el usuario");
          }
      })
      .catch((error) => console.error("Error:", error));
  }
}