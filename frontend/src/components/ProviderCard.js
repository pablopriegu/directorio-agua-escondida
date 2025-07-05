import React, { useState, useContext } from 'react';
import { Link } from 'react-router-dom';
import AuthContext from '../context/AuthContext';
import RatingModal from './RatingModal';

const ProviderCard = ({ provider, refreshProviders }) => {
  const { user } = useContext(AuthContext);
  const [isModalOpen, setModalOpen] = useState(false);

  return (
    <>
      <div className="provider-card" style={{ border: '1px solid black', margin: '10px', padding: '10px' }}>
        <h3>{provider.name}</h3>
        <p><strong>Teléfono:</strong> {provider.phone}</p>
        <p><strong>Población:</strong> {provider.location}</p>
        <div className="rating-info">
          <span>Calificación Global: {provider.global_rating.toFixed(1)} / 20</span>
          <br />
          <span>({provider.rating_count} {provider.rating_count === 1 ? 'evaluación' : 'evaluaciones'})</span>
        </div>

        {/* ESTA ES LA SECCIÓN CORREGIDA */}
        <div className="card-actions">
          <Link to={`/provider/${provider.id}/comments`}>Ver Comentarios</Link>
          {user && <button onClick={() => setModalOpen(true)}>Calificar</button>}
        </div>
      </div>

      {isModalOpen && (
        <RatingModal
          providerId={provider.id}
          onClose={() => setModalOpen(false)}
          onSuccess={refreshProviders}
        />
      )}
    </>
  );
};

export default ProviderCard;