import type { Coordinate } from "../types/Coordinate";

export const bulgariaCoordinatePoints = {
  lats: [44.25, 44, 43.75, 43.5, 43.25, 43, 42.75, 42.5, 42.25, 42, 41.75, 41.5, 41.25],
  lons: [22, 22.25, 22.5, 22.75, 23, 23.25, 23.5, 23.75, 24, 24.25, 24.5, 24.75, 25, 25.25, 25.5, 25.75, 26, 26.25, 26.5, 26.75, 27, 27.25, 27.5, 27.75, 28, 28.25, 28.5],
};

export function getBulgariaCoordinates(): Coordinate[] {
  return bulgariaCoordinatePoints.lats.flatMap((lat) =>
    bulgariaCoordinatePoints.lons.map((long) => ({
      latitude: lat,
      longitude: long
    }))
  );
}