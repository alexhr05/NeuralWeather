import type { Coordinate } from '../types/Coordinate';
import type { CoordTemperature } from '../types/CoordTemperature';

type RequestBody = {
  year: number;
  month: number;
  day: number;
  hour: number;
  coordinate: Coordinate[];
  model: string;
};

const API_URL = 'http://127.0.0.1:8000';

export async function getTemperatures(data: RequestBody): Promise<CoordTemperature[]> {
  const res = await fetch(`${API_URL}/use`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  return res.json();
}