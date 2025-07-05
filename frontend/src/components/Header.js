import React, { useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom'; // Importamos useNavigate
import AuthContext from '../context/AuthContext';

const Header = () => {
  const { user, logoutUser } = useContext(AuthContext);
  const navigate = useNavigate(); // Lo usamos aquí

  const handleLogout = () => {
    logoutUser();
    navigate('/login'); // Redirigimos al hacer logout
  };

  return (
    <header>
      <nav>
        <Link to="/">Inicio</Link>
        &nbsp; | &nbsp;
        {user ? (
          <button onClick={handleLogout}>Cerrar Sesión</button>
        ) : (
          <>
            <Link to="/login">Iniciar Sesión</Link>
            &nbsp; | &nbsp;
            <Link to="/register">Registrarse</Link>
          </>
        )}
      </nav>
      {user && <p>Hola, {user.username}</p>}
      <hr />
    </header>
  );
};

export default Header;