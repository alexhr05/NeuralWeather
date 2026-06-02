import { useMemo } from 'react';
import { MapContainer, TileLayer } from 'react-leaflet';
import 'leaflet/dist/leaflet.css'
import TemperatureOverlay from './TemperatureOverlay';
import TemperatureLegend from './TemperatureLegend';
import { bulgariaCoordinatePoints } from '../../utils/bulgariaCoordinates';

type Props = {
  tempValues: number[];
  currentModel: string;
};

export default function BulgariaMap({ tempValues, currentModel }: Props) {
  const temperatureGrid = useMemo(
    () => ({
      lats: bulgariaCoordinatePoints.lats,
      lons: bulgariaCoordinatePoints.lons,
      values: tempValues
    }),
    [tempValues]
  );

  const dataMin = tempValues.length ? Math.min(...tempValues) : undefined;
  const dataMax = tempValues.length ? Math.max(...tempValues) : undefined;

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
      {tempValues.length > 0 && <TemperatureLegend model={currentModel} dataMin={dataMin} dataMax={dataMax} />}
    </MapContainer>
  )
}