import React, { useState } from 'react';
import api from '../services/api';

const RatingModal = ({ providerId, onClose, onSuccess }) => {
  const [ratings, setRatings] = useState({
    quality: 'Bueno', price: 'Bueno', communication: 'Bueno', deadline: 'Bueno'
  });

  const handleChange = (e) => {
    setRatings({ ...ratings, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post(`/providers/${providerId}/rate/`, ratings);
      alert('¡Gracias por tu calificación!');
      onSuccess(); // Función para refrescar los datos
      onClose(); // Cierra el modal
    } catch (error) {
      alert(error.response?.data?.error || 'Hubo un error al enviar la calificación.');
    }
  };

  const renderOptions = (name) => (
    <div>
      <label>{name.charAt(0).toUpperCase() + name.slice(1)}:</label>
      {['Muy bueno', 'Bueno', 'Regular', 'Malo'].map(value => (
        <label key={value}>
          <input type="radio" name={name} value={value} checked={ratings[name] === value} onChange={handleChange} />
          {value}
        </label>
      ))}
    </div>
  );

  return (
    <div className="modal-backdrop">
      <div className="modal-content">
        <h2>Calificar Proveedor</h2>
        <form onSubmit={handleSubmit}>
          {renderOptions('quality')}
          {renderOptions('price')}
          {renderOptions('communication')}
          {renderOptions('deadline')}
          <button type="submit">Enviar Calificación</button>
          <button type="button" onClick={onClose}>Cancelar</button>
        </form>
      </div>
    </div>
  );
};

export default RatingModal;