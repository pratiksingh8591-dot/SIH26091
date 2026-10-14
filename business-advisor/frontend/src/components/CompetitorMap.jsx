import { useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Circle } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Fix for default marker icons in Leaflet with Webpack/Vite
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

// Custom icons
const userIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

const competitorIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

export default function CompetitorMap({ userLocation, competitors, radiusKm, marketData }) {
  return (
    <div style={{ marginTop: '20px' }}>
      <h3>Competitor Map</h3>
      <div style={{ height: '400px', width: '100%', marginBottom: '20px', border: '1px solid #ddd', borderRadius: '8px', overflow: 'hidden' }}>
        <MapContainer
          center={[userLocation.latitude, userLocation.longitude]}
          zoom={13}
          style={{ height: '100%', width: '100%' }}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />

          {/* User location */}
          <Marker position={[userLocation.latitude, userLocation.longitude]} icon={userIcon}>
            <Popup>
              <strong>{userLocation.name}</strong><br/>
              Your Location
            </Popup>
          </Marker>

          {/* Radius circle */}
          <Circle
            center={[userLocation.latitude, userLocation.longitude]}
            radius={radiusKm * 1000}
            pathOptions={{ color: 'blue', fillColor: 'blue', fillOpacity: 0.1 }}
          />

          {/* Competitors */}
          {competitors.map((competitor, idx) => (
            <Marker
              key={idx}
              position={[competitor.latitude, competitor.longitude]}
              icon={competitorIcon}
            >
              <Popup>
                <strong>{competitor.name || 'Unnamed'}</strong><br/>
                Category: {competitor.category}<br/>
                Distance: {competitor.distance_km} km
              </Popup>
            </Marker>
          ))}
        </MapContainer>
      </div>

      {/* Metrics */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '15px', marginTop: '15px' }}>
        <div style={{ padding: '15px', background: '#f8f9fa', borderRadius: '8px', border: '1px solid #e0e0e0' }}>
          <div style={{ fontSize: '12px', color: '#666', marginBottom: '5px' }}>Total Competitors</div>
          <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#1a1a1a' }}>{marketData.competitor_count}</div>
        </div>

        <div style={{ padding: '15px', background: '#f8f9fa', borderRadius: '8px', border: '1px solid #e0e0e0' }}>
          <div style={{ fontSize: '12px', color: '#666', marginBottom: '5px' }}>Average Distance</div>
          <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#1a1a1a' }}>
            {marketData.average_distance ? `${marketData.average_distance} km` : 'N/A'}
          </div>
        </div>

        <div style={{ padding: '15px', background: '#f8f9fa', borderRadius: '8px', border: '1px solid #e0e0e0' }}>
          <div style={{ fontSize: '12px', color: '#666', marginBottom: '5px' }}>Nearest Competitor</div>
          <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#1a1a1a' }}>
            {marketData.nearest_distance ? `${marketData.nearest_distance} km` : 'N/A'}
          </div>
        </div>

        <div style={{ padding: '15px', background: '#f8f9fa', borderRadius: '8px', border: '1px solid #e0e0e0' }}>
          <div style={{ fontSize: '12px', color: '#666', marginBottom: '5px' }}>Density</div>
          <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#1a1a1a' }}>
            {marketData.competitor_density.toFixed(2)} /km²
          </div>
        </div>
      </div>

      <div style={{ marginTop: '10px', fontSize: '12px', color: '#666' }}>
        Source: OpenStreetMap
      </div>
    </div>
  );
}
