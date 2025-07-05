import React, { useState, useEffect, useCallback, useContext } from 'react';
import api from '../services/api';
import ProviderList from '../components/ProviderList';
import AddProviderModal from '../components/AddProviderModal';
import AuthContext from '../context/AuthContext';

const HomePage = () => {
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [providers, setProviders] = useState([]);
  const [isAddModalOpen, setAddModalOpen] = useState(false);
  const { user } = useContext(AuthContext);

  const fetchProviders = useCallback(() => {
    if (selectedCategory) {
      api.get(`/providers/?category=${selectedCategory}`)
        .then(response => {
          setProviders(response.data);
        })
        .catch(error => {
          console.error('Hubo un error al obtener los proveedores:', error);
        });
    } else {
      setProviders([]);
    }
  }, [selectedCategory]);

  useEffect(() => {
    api.get('/categories/')
      .then(response => setCategories(response.data))
      .catch(error => console.error('Hubo un error al obtener las categorías:', error));
  }, []);

  useEffect(() => {
    fetchProviders();
  }, [fetchProviders]);

  return (
    <div>
      <h1>Directorio de Proveedores Agua Escondida</h1>

      <div className="controls">
        <select onChange={(e) => setSelectedCategory(e.target.value)} value={selectedCategory}>
          <option value="">-- Seleccione una categoría --</option>
          {categories.map(category => (
            <option key={category.id} value={category.id}>{category.name}</option>
          ))}
        </select>

        {user && <button onClick={() => setAddModalOpen(true)}>Dar de alta un Proveedor</button>}
      </div>
{isAddModalOpen && (
        <AddProviderModal
          categories={categories}
          onClose={() => setAddModalOpen(false)}
          onSuccess={() => {
            fetchProviders(); // Refresca la lista después de añadir
            setAddModalOpen(false);
          }}
        />
      )}
      <ProviderList providers={providers} refreshProviders={fetchProviders} />
          </div>
  );
};

export default HomePage;