import { useState } from 'react';
import { MapContainer, TileLayer, useMapEvents } from 'react-leaflet';
import 'leaflet/dist/leaflet.css'
import TemperatureOverlay from './TemperatureOverlay';

function ClickHandler({ onCoords }: { onCoords: (lat: number, lng: number) => void }) {
  useMapEvents({
    click(e) {
      onCoords(e.latlng.lat, e.latlng.lng)
    },
  });
  return null
}

export default function BulgariaMap() {
  const [coords, setCoords] = useState<{ lat: number, lng: number } | null>(null);

  return (
    <div>
      <MapContainer
        center={[42.73, 25.48]}
        zoom={8}
        style={{ height: '800px', width: '100%' }}
        className='rounded-xl'
      >
        <TileLayer
          url='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
          attribution="© OpenStreetMap contributors"
        />

        <TemperatureOverlay />
        <ClickHandler onCoords={(lat, lng) => setCoords({ lat, lng })} />
      </MapContainer>

      {coords && (
        <div>
          <p>Latitude: {coords.lat}</p>
          <p>Longitude: {coords.lng}</p>
        </div>
      )}
    </div>
  )
}