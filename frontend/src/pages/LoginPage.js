import React, { useContext } from 'react';
import AuthContext from '../context/AuthContext';
import { useNavigate } from 'react-router-dom'; // Importamos useNavigate aquí

const LoginPage = () => {
  const { loginUser } = useContext(AuthContext);
  const navigate = useNavigate(); // Lo usamos aquí

  const handleSubmit = async (e) => { // La función ahora es async
    e.preventDefault();
    const username = e.target.username.value;
    const password = e.target.password.value;

    const loggedIn = await loginUser(username, password); // Esperamos el resultado

    if (loggedIn) {
        navigate('/'); // Redirigimos si el login fue exitoso
    }
  };

  return (
    <div>
      <h2>Iniciar Sesión</h2>
      <form onSubmit={handleSubmit}>
        <input type="text" name="username" placeholder="Nombre de Usuario" required />
        <input type="password" name="password" placeholder="Contraseña" required />
        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default LoginPage;