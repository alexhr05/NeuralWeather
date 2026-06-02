import { useEffect } from 'react';
import { useMap } from 'react-leaflet';
import * as L from 'leaflet';
import * as d3 from 'd3';

type Props = {
  model: string;
  dataMin?: number;
  dataMax?: number;
};

const legendConfig: Record<string, { title: string; unit: string; min: number; max: number }> = {
  'base_model.keras':  { title: 'Temperature (°C)',       unit: '°',     min: -30, max: 50        },
  'solar_model.keras': { title: 'Solar Radiation (J/m²)', unit: ' J/m²', min: 0,   max: 3_645_696 },
};

export default function TemperatureLegend({ model, dataMin, dataMax }: Props) {
  const map = useMap();

  useEffect(() => {
    const config = legendConfig[model] ?? { title: model, unit: '', min: 0, max: 1 };
    const { min, max } = config;

    const legend = new L.Control({ position: 'bottomright' });

    legend.onAdd = () => {
      const div = L.DomUtil.create('div');
      div.style.cssText = `
        background: rgba(255,255,255,0.85);
        padding: 8px 12px;
        border-radius: 8px;
        font-size: 16px;
        font-family: sans-serif;
        line-height: 1.4;
        box-shadow: 0 1px 5px rgba(0,0,0,0.3);
      `;

      const steps = 5;
      const labels = d3.range(steps + 1).map(i => {
        const t = i / steps;
        return {
          value: max - t * (max - min),
          color: d3.interpolateRdBu(t),
        };
      });

      const gradientStops = labels
        .map((l, i) => `${l.color} ${(i / steps) * 100}%`)
        .join(', ');

      const minMaxRow = (dataMin !== undefined && dataMax !== undefined)
        ? `<div style="margin-top:6px; font-size:13px; color:#555; border-top:1px solid #ddd; padding-top:4px;">
            <div>Min: <b>${dataMin.toFixed(1)}${config.unit}</b></div>
            <div>Max: <b>${dataMax.toFixed(1)}${config.unit}</b></div>
          </div>`
        : '';

      div.innerHTML = `
        <div style="font-weight:600; margin-bottom:6px; color:#333;">${config.title}</div>
        <div style="display:flex; align-items:stretch; gap:6px;">
          <div style="width:18px; background:linear-gradient(to bottom, ${gradientStops}); border-radius:3px; min-height:110px;"></div>
          <div style="display:flex; flex-direction:column; justify-content:space-between;">
            ${labels.map(l => `<span style="color:#333;">${l.value.toFixed(1)}${config.unit}</span>`).join('')}
          </div>
        </div>
        ${minMaxRow}
      `;

      return div;
    };

    legend.addTo(map);
    return () => { legend.remove(); };
  }, [map, model, dataMin, dataMax]);

  return null;
}
