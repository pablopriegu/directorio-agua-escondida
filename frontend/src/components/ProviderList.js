import React from 'react';
import ProviderCard from './ProviderCard';

// 1. RECIBIMOS 'refreshProviders' COMO PROP
const ProviderList = ({ providers, refreshProviders }) => {
  if (!providers || providers.length === 0) {
    return <p>Seleccione una categoría para ver los proveedores.</p>;
  }

  return (
    <div className="provider-list">
      {providers.map(provider => (
        // 2. PASAMOS LA PROP 'refreshProviders' A CADA TARJETA
        <ProviderCard key={provider.id} provider={provider} refreshProviders={refreshProviders} />
      ))}
    </div>
  );
};

export default ProviderList;