import './style.css';

const API_URL = 'http://127.0.0.1:8000/api/';
let carrito = [];
let carritoPago = []; 
let cerrarCarrito = () => {}; 

function flyToCart(buttonElement) {
  const productCard = buttonElement.closest('.producto-card');
  const imgElement = productCard.querySelector('img');
  const cartIcon = document.getElementById('btn-carrito');

  if (!imgElement || !cartIcon) return;

  const imgRect = imgElement.getBoundingClientRect();
  const cartRect = cartIcon.getBoundingClientRect();

  const flyImg = imgElement.cloneNode(true);
  flyImg.style.position = 'fixed';
  flyImg.style.zIndex = '9999'; 
  flyImg.style.pointerEvents = 'none'; 
  flyImg.style.borderRadius = '10px';
  flyImg.style.transition = 'none'; 
  
  flyImg.style.left = imgRect.left + 'px';
  flyImg.style.top = imgRect.top + 'px';
  flyImg.style.width = imgRect.width + 'px';
  flyImg.style.height = imgRect.height + 'px';
  
  document.body.appendChild(flyImg);

  const deltaX = (cartRect.left + cartRect.width / 2) - (imgRect.left + imgRect.width / 2);
  const deltaY = (cartRect.top + cartRect.height / 2) - (imgRect.top + imgRect.height / 2);

  const animation = flyImg.animate([
    { 
      transform: 'translate(0, 0) scale(1)', 
      opacity: 1 
    },
    { 
      transform: `translate(${deltaX / 2}px, ${deltaY - 50}px) scale(0.6)`, 
      opacity: 0.8 
    },
    { 
      transform: `translate(${deltaX}px, ${deltaY}px) scale(0.1)`, 
      opacity: 0.2 
    }
  ], {
    duration: 700, 
    easing: 'ease-in-out'
  });

  animation.onfinish = () => {
    flyImg.remove(); 
    
    cartIcon.animate([
      { transform: 'scale(1)' },
      { transform: 'scale(1.4)' },
      { transform: 'scale(1)' }
    ], { duration: 200 });
  };
}

async function cargarCategorias() {
  const respuesta = await fetch(`${API_URL}categorias/`);
  const categorias = await respuesta.json();
  const nav = document.getElementById('categorias-nav');
  
  categorias.forEach(cat => {
    const li = document.createElement('li');
    li.innerHTML = `<a href="#" data-id="${cat.id}">${cat.nombre}</a>`;
    nav.appendChild(li);
  });
}

async function cargarProductos(categoriaId = null) {
  let url = `${API_URL}productos/`;
  if (categoriaId) url += `?categoria=${categoriaId}`;
  
  const respuesta = await fetch(url);
  const productos = await respuesta.json();
  const container = document.getElementById('productos-container');
  container.innerHTML = ''; 

  productos.forEach(prod => {
    const card = document.createElement('div');
    card.className = 'producto-card';
    card.innerHTML = `
      <img src="${prod.imagen}" alt="${prod.nombre}">
      <div class="producto-info">
        <h3>${prod.nombre}</h3>
        <p>${prod.descripcion}</p>
        <div class="precio-stock">
          <span class="precio">S/ ${prod.precio}</span>
          <span class="stock">Stock: ${prod.stock}</span>
        </div>
        <button class="btn-comprar" data-id="${prod.id}" ${prod.stock === 0 ? 'disabled' : ''}>
          ${prod.stock === 0 ? 'Agotado' : 'Agregar al Carrito'}
        </button>
      </div>
    `;
    container.appendChild(card);
  });
}

function agregarAlCarrito(productoId) {
  const existente = carrito.find(item => item.id === productoId);
  if (existente) {
    existente.cantidad++;
  } else {
    carrito.push({ id: productoId, cantidad: 1 });
  }
  renderizarCarrito();
}

function eliminarDelCarrito(productoId) {
  carrito = carrito.filter(item => item.id !== productoId);
  renderizarCarrito();
}

async function renderizarCarrito() {
  const itemsContainer = document.getElementById('carrito-items');
  const totalSpan = document.getElementById('carrito-total');
  const contadorSpan = document.getElementById('contador-carrito');
  
  itemsContainer.innerHTML = '';
  let total = 0;
  let totalItems = 0;

  if (carrito.length === 0) {
    itemsContainer.innerHTML = '<p>Tu carrito está vacío</p>';
    totalSpan.innerText = '0.00';
    contadorSpan.innerText = '0';
    return;
  }

  const respuesta = await fetch(`${API_URL}productos/`);
  const productos = await respuesta.json();

  carrito.forEach(item => {
    const prod = productos.find(p => p.id === item.id);
    if (prod) {
      const subtotal = prod.precio * item.cantidad;
      total += subtotal;
      totalItems += item.cantidad;

      const div = document.createElement('div');
      div.className = 'item-carrito';
      div.innerHTML = `
        <div>
          <h4>${prod.nombre}</h4>
          <p>Cant: ${item.cantidad} x S/ ${prod.precio}</p>
        </div>
        <div>
          <span>S/ ${subtotal.toFixed(2)}</span>
          <button class="btn-eliminar" data-id="${prod.id}">🗑️</button>
        </div>
      `;
      itemsContainer.appendChild(div);
    }
  });

  totalSpan.innerText = total.toFixed(2);
  contadorSpan.innerText = totalItems;
}

async function procesarPagoBackend() {
  if (!carritoPago || carritoPago.length === 0) {
    console.log("Carrito vacío o ya procesado.");
    return;
  }

  try {
    console.log("Enviando carrito a Django:", carritoPago);

    const respuesta = await fetch(`${API_URL}pagar/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ items: carritoPago })
    });

    const data = await respuesta.json();
    console.log("Respuesta de Django:", data);

    if (respuesta.ok && data.status === 'success') {
      alert(`✅ ¡Pago exitoso por S/ ${data.total.toFixed(2)} con PayPal! Gracias por tu compra.`);
      
      carrito = []; 
      carritoPago = []; 
      
      renderizarCarrito(); 
      cerrarCarrito(); 
      cargarProductos(); 
      
      document.getElementById('modal-pago').classList.remove('active');
      document.getElementById('paypal-button-container').innerHTML = '';
    } else {
      alert(`Error al procesar el pedido en nuestro servidor: ${data.error || 'Error desconocido'}`);
    }
  } catch (error) {
    console.error(error);
    alert('Error después del pago PayPal: ' + error.message);
  }
}

function renderPaypalButtons(total) {
  const container = document.getElementById('paypal-button-container');
  container.innerHTML = ''; 

  if (typeof paypal === 'undefined') {
    container.innerHTML = '<p style="color:red; text-align:center; font-weight:bold;">Error: No se cargó el SDK de PayPal.</p>';
    return;
  }

  const montoSeguro = parseFloat(total).toFixed(2);

  paypal.Buttons({
    createOrder: function(data, actions) {
      return actions.order.create({
        purchase_units: [{
          amount: {
            currency_code: "USD",
            value: montoSeguro
          }
        }]
      });
    },
    onApprove: function(data, actions) {
      return actions.order.capture().then(function(details) {
        console.log("Pago aprobado por PayPal:", details);
        return procesarPagoBackend();
      });
    },
    onCancel: function(data) {
      alert('Pago cancelado por el usuario.');
    },
    onError: function(err) {
      console.error("Error en PayPal:", err);
      alert('Hubo un error en el proceso de PayPal.');
    }
  }).render('#paypal-button-container');
}

document.addEventListener('DOMContentLoaded', () => {
  cargarCategorias();
  cargarProductos();

  // --- EVENTOS DE NAVEGACIÓN ---

  // 1. Click en el Logo / Nombre -> Volver a ver todos los productos
  document.getElementById('inicio-logo').addEventListener('click', () => {
    cargarProductos(); 
    document.getElementById('titulo-categoria').innerText = "Todos los Juegos"; 
    
    document.querySelectorAll('#categorias-nav a').forEach(a => a.classList.remove('active'));
  });

  // 2. Click en las Categorías del menú (Delegación de eventos)
  document.getElementById('categorias-nav').addEventListener('click', (e) => {
    if (e.target.tagName === 'A') {
      e.preventDefault(); 
      
      const categoriaId = e.target.dataset.id; 
      const categoriaNombre = e.target.innerText; 
      
      document.getElementById('titulo-categoria').innerText = categoriaNombre;
      
      document.querySelectorAll('#categorias-nav a').forEach(a => a.classList.remove('active'));
      e.target.classList.add('active');
      
      cargarProductos(categoriaId);
    }
  });

  // --- FIN EVENTOS DE NAVEGACIÓN ---

  const sidebar = document.getElementById('carrito-sidebar');
  const overlay = document.getElementById('overlay');

  document.getElementById('btn-carrito').addEventListener('click', () => {
    sidebar.classList.add('active');
    overlay.classList.add('active');
  });

  cerrarCarrito = () => {
    sidebar.classList.remove('active');
    overlay.classList.remove('active');
  };

  document.getElementById('btn-cerrar-carrito').addEventListener('click', cerrarCarrito);
  overlay.addEventListener('click', cerrarCarrito);

  // Agregar al carrito (Delegación de eventos con animación integrada)
  document.getElementById('productos-container').addEventListener('click', (e) => {
    if (e.target.classList.contains('btn-comprar')) {
      const id = parseInt(e.target.dataset.id);
      
      flyToCart(e.target); // ¡Dispara el efecto visual del vuelo!
      
      agregarAlCarrito(id);
    }
  });

  document.getElementById('carrito-items').addEventListener('click', (e) => {
    if (e.target.classList.contains('btn-eliminar')) {
      const id = parseInt(e.target.dataset.id);
      eliminarDelCarrito(id);
    }
  });

  document.getElementById('btn-pagar').addEventListener('click', () => {
    if (carrito.length === 0) {
      alert('Tu carrito está vacío');
      return;
    }
    
    carritoPago = JSON.parse(JSON.stringify(carrito));
    console.log("Carrito congelado para pago:", carritoPago);
    
    const totalPagar = document.getElementById('carrito-total').innerText; 
    document.getElementById('monto-modal').innerText = totalPagar;
    document.getElementById('modal-pago').classList.add('active');

    renderPaypalButtons(totalPagar);
  });

  document.getElementById('btn-cerrar-modal').addEventListener('click', () => {
    document.getElementById('modal-pago').classList.remove('active');
    document.getElementById('paypal-button-container').innerHTML = '';
  });
});