import React, { useState } from 'react';
import api from '../services/api'; // Importamos api
import { useNavigate } from 'react-router-dom'; // Importamos para redirigir

const RegisterPage = () => {
  const [formData, setFormData] = useState({
    username: '',
    first_name: '',
    last_name: '',
    email: '',
    phone_number: '',
    password: '',
    password2: ''
  });
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Enviamos los datos del formulario a la API
      await api.post('/register/', formData);
      alert('¡Registro exitoso! Tu cuenta está pendiente de aprobación por un administrador.');
      navigate('/'); // Redirigimos al inicio
    } catch (error) {
      console.error('Error en el registro:', error.response.data);
      alert('Hubo un error en el registro. Revisa la consola para más detalles.');
    }
  };

  return (
    <div>
      <h2>Formulario de Registro</h2>
      <form onSubmit={handleSubmit}>
        {/* Actualiza los inputs para que coincidan con el estado */}
        <input type="text" name="username" placeholder="Nombre de Usuario" onChange={handleChange} required />
        <input type="text" name="first_name" placeholder="Nombre(s)" onChange={handleChange} required />
        <input type="text" name="last_name" placeholder="Apellidos" onChange={handleChange} required />
        <input type="email" name="email" placeholder="Correo Electrónico" onChange={handleChange} required />
        <input type="text" name="phone_number" placeholder="Celular" onChange={handleChange} />
        <input type="password" name="password" placeholder="Contraseña" onChange={handleChange} required />
        <input type="password" name="password2" placeholder="Confirmar Contraseña" onChange={handleChange} required />
        <button type="submit">Registrarse</button>
      </form>
    </div>
  );
};

export default RegisterPage;