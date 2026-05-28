import { useEffect } from 'react';
import { useMap } from 'react-leaflet';
import * as d3 from 'd3';
import * as topojson from 'topojson-client';
import type { Topology } from 'topojson-specification';
import worldData from 'world-atlas/countries-10m.json';

const world = worldData as unknown as Topology;
const countries = topojson.feature(
  world,
  (world.objects as Record<string, never>).countries
) as unknown as GeoJSON.FeatureCollection;
const bulgariaFeature = countries.features.find(f => f.id === '100')!;

type Props = {
  temperatureGrid: {
    lats: number[];
    lons: number[];
    values: number[];
  }
};

export default function TemperatureOverlay({ temperatureGrid }: Props) {
  const map = useMap();

  useEffect(() => {
    const { lats, lons, values } = temperatureGrid;
    const rows = lats.length;
    const cols = lons.length;

    // Step size between grid points
    const lonStep = (lons[cols - 1] - lons[0]) / (cols - 1);
    const latStep = (lats[0] - lats[rows - 1]) / (rows - 1);

    const flat = values.flat();
    const min = Math.min(...flat);
    const max = Math.max(...flat);

    const step = (max - min) / 20;
    // Start slightly below min so the first band covers cells at exactly the minimum value
    const thresholds = d3.range(min - step * 0.01, max, step);
    const contours = d3.contours().size([cols, rows]).thresholds(thresholds)(flat);

    const svg = d3
      .select(map.getPanes().overlayPane)
      .append('svg')
      .style('position', 'absolute')
      .style('pointer-events', 'none');

    const clipPathEl = svg
      .append('defs')
      .append('clipPath')
      .attr('id', 'bulgaria-clip')
      .append('path');

    const g = svg.append('g')
      .attr('class', 'leaflet-zoom-hide')
      .attr('clip-path', 'url(#bulgaria-clip)');

    function reset() {
      const b = map.getBounds();
      const tl = map.latLngToLayerPoint(b.getNorthWest());
      const br = map.latLngToLayerPoint(b.getSouthEast());

      svg
        .attr('width', br.x - tl.x)
        .attr('height', br.y - tl.y)
        .style('left', `${tl.x}px`)
        .style('top', `${tl.y}px`);

      // All coordinates are in SVG-local space (map-pane coords minus top-left offset)
      const toSvg = ([px, py]: [number, number]) => [px - tl.x, py - tl.y] as [number, number];

      // Projection for Bulgaria border (standard geo → SVG-local)
      const geoProj = d3.geoTransform({
        point(lon, lat) {
          const p = map.latLngToLayerPoint([lat, lon]);
          this.stream.point(...toSvg([p.x, p.y]));
        },
      });

      // Projection for contours (grid index space → geo → SVG-local)
      const contourProj = d3.geoTransform({
        point(cx, cy) {
          const lon = lons[0] + cx * lonStep;
          const lat = lats[0] - cy * latStep;
          const p = map.latLngToLayerPoint([lat, lon]);
          this.stream.point(...toSvg([p.x, p.y]));
        },
      });

      clipPathEl.attr('d', d3.geoPath().projection(geoProj)(bulgariaFeature));

      // Full-viewport rect clipped to Bulgaria — covers any gaps the contour bands leave
      g.selectAll<SVGRectElement, [null]>('.bg')
        .data([null] as [null])
        .join('rect')
        .attr('class', 'bg')
        .attr('x', 0)
        .attr('y', 0)
        .attr('width', br.x - tl.x)
        .attr('height', br.y - tl.y)
        .attr('fill', d3.interpolateRdBu(1))
        .attr('opacity', 0.75);

      g.selectAll<SVGPathElement, (typeof contours)[number]>('.contour')
        .data(contours)
        .join('path')
        .attr('class', 'contour')
        .attr('d', d3.geoPath().projection(contourProj))
        .attr('fill', d => d3.interpolateRdBu(1 - (d.value - min) / (max - min)))
        .attr('stroke', 'none')
        .attr('opacity', 0.75);
    }

    map.on('viewreset zoomend moveend', reset);
    reset();

    return () => {
      map.off('viewreset zoomend moveend', reset);
      svg.remove();
    };
  }, [map, temperatureGrid]);

  return null;
}