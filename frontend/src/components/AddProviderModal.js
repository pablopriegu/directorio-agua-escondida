import React, { useState } from 'react';
import api from '../services/api';

const AddProviderModal = ({ categories, onClose, onSuccess }) => {
  const [formData, setFormData] = useState({
    name: '',
    phone: '',
    location: '',
    category: categories.length > 0 ? categories[0].id : ''
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post('/providers/', formData);
      alert('Proveedor añadido con éxito.');
      onSuccess();
      onClose();
    } catch (error) {
      console.error("Error adding provider:", error.response.data);
      alert('Hubo un error al añadir el proveedor.');
    }
  };

  return (
    <div className="modal-backdrop">
      <div className="modal-content">
        <h2>Dar de alta un Proveedor</h2>
        <form onSubmit={handleSubmit}>
          <input type="text" name="name" placeholder="Nombre o Razón Social" onChange={handleChange} required />
          <input type="text" name="phone" placeholder="Teléfono" onChange={handleChange} required />
          <input type="text" name="location" placeholder="Población" onChange={handleChange} required />
          <select name="category" value={formData.category} onChange={handleChange}>
            {categories.map(cat => (
              <option key={cat.id} value={cat.id}>{cat.name}</option>
            ))}
          </select>
          <button type="submit">Añadir Proveedor</button>
          <button type="button" onClick={onClose}>Cancelar</button>
        </form>
      </div>
    </div>
  );
};

export default AddProviderModal;