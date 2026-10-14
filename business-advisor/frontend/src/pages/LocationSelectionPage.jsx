import { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, useMapEvents } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Fix for default marker icons
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

function LocationMarker({ position, setPosition }) {
  useMapEvents({
    click(e) {
      setPosition(e.latlng);
    },
  });

  return position ? <Marker position={position}></Marker> : null;
}

export default function LocationSelectionPage({ onAnalyze, categories }) {
  const [locationName, setLocationName] = useState('');
  const [position, setPosition] = useState({ lat: 19.0760, lng: 72.8777 }); // Default: Mumbai
  const [businessCategory, setBusinessCategory] = useState('restaurant');
  const [businessName, setBusinessName] = useState('');
  const [marginCapital, setMarginCapital] = useState(200000);
  const [radius, setRadius] = useState(10);

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!locationName.trim()) {
      alert('Please enter a location name');
      return;
    }

    if (!businessName.trim()) {
      alert('Please enter a business name');
      return;
    }

    if (marginCapital <= 0) {
      alert('Margin capital must be greater than zero');
      return;
    }

    const analysisData = {
      location: {
        name: locationName,
        latitude: position.lat,
        longitude: position.lng,
      },
      business: {
        name: businessName,
        category: businessCategory,
      },
      available_margin_capital: marginCapital,
      radius_km: radius,
    };

    onAnalyze(analysisData);
  };

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '20px' }}>
      <h2>Business Analysis Setup</h2>
      <p style={{ color: '#666', marginBottom: '30px' }}>
        Select your location, business type, and financial details to analyze market feasibility
      </p>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '30px', marginBottom: '30px' }}>
        {/* Left: Form */}
        <div>
          <form onSubmit={handleSubmit}>
            <div style={{ marginBottom: '20px' }}>
              <label style={{ display: 'block', marginBottom: '8px', fontWeight: 500 }}>
                Location Name *
              </label>
              <input
                type="text"
                value={locationName}
                onChange={(e) => setLocationName(e.target.value)}
                placeholder="e.g., Pune, Maharashtra"
                style={{
                  width: '100%',
                  padding: '12px',
                  border: '1px solid #ddd',
                  borderRadius: '6px',
                  fontSize: '14px',
                }}
                required
              />
            </div>

            <div style={{ marginBottom: '20px', padding: '15px', background: '#f8f9fa', borderRadius: '6px' }}>
              <div style={{ fontSize: '12px', color: '#666', marginBottom: '5px' }}>Selected Coordinates</div>
              <div style={{ fontSize: '14px', fontFamily: 'monospace' }}>
                Lat: {position.lat.toFixed(4)}, Lon: {position.lng.toFixed(4)}
              </div>
              <div style={{ fontSize: '12px', color: '#666', marginTop: '5px' }}>
                Click on the map to change location
              </div>
            </div>

            <div style={{ marginBottom: '20px' }}>
              <label style={{ display: 'block', marginBottom: '8px', fontWeight: 500 }}>
                Business Category *
              </label>
              <select
                value={businessCategory}
                onChange={(e) => setBusinessCategory(e.target.value)}
                style={{
                  width: '100%',
                  padding: '12px',
                  border: '1px solid #ddd',
                  borderRadius: '6px',
                  fontSize: '14px',
                }}
                required
              >
                {categories.map((cat) => (
                  <option key={cat.key} value={cat.key}>
                    {cat.name}
                  </option>
                ))}
              </select>
            </div>

            <div style={{ marginBottom: '20px' }}>
              <label style={{ display: 'block', marginBottom: '8px', fontWeight: 500 }}>
                Business Name *
              </label>
              <input
                type="text"
                value={businessName}
                onChange={(e) => setBusinessName(e.target.value)}
                placeholder="e.g., My Restaurant"
                style={{
                  width: '100%',
                  padding: '12px',
                  border: '1px solid #ddd',
                  borderRadius: '6px',
                  fontSize: '14px',
                }}
                required
              />
            </div>

            <div style={{ marginBottom: '20px' }}>
              <label style={{ display: 'block', marginBottom: '8px', fontWeight: 500 }}>
                Available Margin Capital (₹) *
              </label>
              <input
                type="number"
                value={marginCapital}
                onChange={(e) => setMarginCapital(Number(e.target.value))}
                min="1"
                step="1000"
                style={{
                  width: '100%',
                  padding: '12px',
                  border: '1px solid #ddd',
                  borderRadius: '6px',
                  fontSize: '14px',
                }}
                required
              />
              <div style={{ fontSize: '12px', color: '#666', marginTop: '5px' }}>
                This represents 10% of your total project cost
              </div>
            </div>

            <div style={{ marginBottom: '20px' }}>
              <label style={{ display: 'block', marginBottom: '8px', fontWeight: 500 }}>
                Analysis Radius: {radius} km
              </label>
              <input
                type="range"
                value={radius}
                onChange={(e) => setRadius(Number(e.target.value))}
                min="1"
                max="50"
                style={{ width: '100%' }}
              />
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', color: '#666' }}>
                <span>1 km</span>
                <span>50 km</span>
              </div>
            </div>

            <button
              type="submit"
              style={{
                width: '100%',
                padding: '15px',
                background: '#2563eb',
                color: 'white',
                border: 'none',
                borderRadius: '8px',
                fontSize: '16px',
                fontWeight: 600,
                cursor: 'pointer',
              }}
            >
              Analyze Business Feasibility
            </button>
          </form>
        </div>

        {/* Right: Map */}
        <div>
          <div style={{ height: '600px', border: '1px solid #ddd', borderRadius: '8px', overflow: 'hidden' }}>
            <MapContainer
              center={[position.lat, position.lng]}
              zoom={12}
              style={{ height: '100%', width: '100%' }}
            >
              <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              />
              <LocationMarker position={position} setPosition={setPosition} />
            </MapContainer>
          </div>
        </div>
      </div>
    </div>
  );
}
