import { useEffect, useState } from "react";
import "./App.css";

// 🔥 URL BACKEND (CAMBIA ESTO)
const API_URL = "https://TU-BACKEND.onrender.com";

function App() {
  const [productos, setProductos] = useState([]);
  const [categorias, setCategorias] = useState([]);
  const [categoriaSeleccionada, setCategoriaSeleccionada] = useState(null);
  const [busqueda, setBusqueda] = useState("");
  const [carrito, setCarrito] = useState([]);
  const [cargado, setCargado] = useState(false);
  const [mensaje, setMensaje] = useState("");
  const [mostrarCarrito, setMostrarCarrito] = useState(false);

  useEffect(() => {
    const data = localStorage.getItem("carrito");
    if (data) setCarrito(JSON.parse(data));
    setCargado(true);
  }, []);

  useEffect(() => {
    if (cargado) {
      localStorage.setItem("carrito", JSON.stringify(carrito));
    }
  }, [carrito, cargado]);

  // 🔥 CATEGORÍAS
  useEffect(() => {
    fetch(`${API_URL}/categorias`)
      .then((res) => res.json())
      .then((data) => {
        if (Array.isArray(data)) setCategorias(data);
        else setCategorias(data.data || []);
      });
  }, []);

  // 🔥 PRODUCTOS
  useEffect(() => {
    const url = busqueda
      ? `${API_URL}/productos/?search=${busqueda}`
      : `${API_URL}/productos/`;

    fetch(url)
      .then((res) => res.json())
      .then((data) => setProductos(data));
  }, [busqueda]);

  const agregarAlCarrito = (producto) => {
    setCarrito((prev) => {
      const existe = prev.find((item) => item.id === producto.id);
      if (existe) {
        return prev.map((item) =>
          item.id === producto.id
            ? { ...item, cantidad: item.cantidad + 1 }
            : item,
        );
      }
      return [...prev, { ...producto, cantidad: 1 }];
    });

    setMensaje("Producto agregado 🛒");
    setTimeout(() => setMensaje(""), 2000);
  };

  const quitarDelCarrito = (id) => {
    setCarrito((prev) => prev.filter((item) => item.id !== id));
  };

  // 🔥 CHECKOUT
  const finalizarCompra = () => {
    fetch(`${API_URL}/pedidos`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        productos: carrito,
        total: total,
      }),
    })
      .then((res) => res.json())
      .then(() => {
        setMensaje("✅ Compra realizada con éxito");
        setCarrito([]);
        setMostrarCarrito(false);
      })
      .catch(() => {
        setMensaje("❌ Error al procesar la compra");
      });

    setTimeout(() => setMensaje(""), 3000);
  };

  const total = carrito.reduce(
    (acc, item) => acc + item.precio * item.cantidad,
    0,
  );

  const mapaCategorias = {};
  categorias.forEach((cat) => {
    mapaCategorias[cat.id] = cat.nombre;
  });

  const productosFiltrados = categoriaSeleccionada
    ? productos.filter((p) => {
        const categoriaId =
          p.id_categoria || p.categoria_id || (p.categoria && p.categoria.id);
        return categoriaId === Number(categoriaSeleccionada);
      })
    : productos;

  return (
    <div className="container">
      <div className="header">
        <h1>Mi Tienda 🛒</h1>

        <input
          type="text"
          placeholder="Buscar producto..."
          className="search"
          value={busqueda}
          onChange={(e) => setBusqueda(e.target.value)}
        />

        <div className="carrito-info" onClick={() => setMostrarCarrito(true)}>
          🛒 {carrito.length}
        </div>
      </div>

      {mensaje && <div className="mensaje">{mensaje}</div>}

      <div>
        <button onClick={() => setCategoriaSeleccionada(null)}>Todos</button>
        {categorias.map((cat) => (
          <button key={cat.id} onClick={() => setCategoriaSeleccionada(cat.id)}>
            {cat.nombre}
          </button>
        ))}
      </div>

      <div className="grid">
        {productosFiltrados.map((p) => {
          const url = p.imagen
            ? `${API_URL}/images/${p.imagen.trim()}`
            : "https://via.placeholder.com/200";

          const categoriaId =
            p.id_categoria || p.categoria_id || (p.categoria && p.categoria.id);

          return (
            <div className="card" key={p.id}>
              <img src={url} alt={p.nombre} className="img" />
              <h2>{p.nombre}</h2>
              <p>Categoría: {mapaCategorias[categoriaId]}</p>
              <p>{"$" + p.precio.toLocaleString("es-CO")}</p>
              <button onClick={() => agregarAlCarrito(p)}>Comprar</button>
            </div>
          );
        })}
      </div>

      {mostrarCarrito && (
        <div className="modal">
          <div className="modal-content">
            <h2>🛒 Tu carrito</h2>

            {carrito.length === 0 ? (
              <p>Vacío</p>
            ) : (
              carrito.map((item) => (
                <div key={item.id}>
                  {item.nombre} x {item.cantidad}
                  <button onClick={() => quitarDelCarrito(item.id)}>❌</button>
                </div>
              ))
            )}

            <h3>Total: {"$" + total.toLocaleString("es-CO")}</h3>

            {carrito.length > 0 && (
              <button onClick={finalizarCompra}>Finalizar compra 💳</button>
            )}

            <button onClick={() => setMostrarCarrito(false)}>Cerrar</button>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
