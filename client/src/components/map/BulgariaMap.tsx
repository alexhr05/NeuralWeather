import { useMemo } from 'react';
import { MapContainer, TileLayer } from 'react-leaflet';
import 'leaflet/dist/leaflet.css'
import TemperatureOverlay from './TemperatureOverlay';
import TemperatureLegend from './TemperatureLegend';
import { bulgariaCoordinatePoints } from '../../utils/bulgariaCoordinates';

type Props = {
  tempValues: number[]
};

export default function BulgariaMap({ tempValues }: Props) {
  const temperatureGrid = useMemo(
    () => ({
      lats: bulgariaCoordinatePoints.lats,
      lons: bulgariaCoordinatePoints.lons,
      values: tempValues
    }),
    [tempValues]
  );

  const min = tempValues.length ? Math.min(...tempValues) : 0;
  const max = tempValues.length ? Math.max(...tempValues) : 0;

  return (
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

      <TemperatureOverlay temperatureGrid={temperatureGrid} />
      {tempValues.length > 0 && <TemperatureLegend min={min} max={max} />}
    </MapContainer>
  )
}