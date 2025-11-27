// Globe.jsx
import React, { useEffect, useRef } from "react";
import * as d3 from "d3";
import { feature, mesh } from "topojson-client";

// === Classe Versor (inchangée) ===
class Versor {
  static fromAngles([l, p, g]) {
    l *= Math.PI / 360;
    p *= Math.PI / 360;
    g *= Math.PI / 360;
    const sl = Math.sin(l), cl = Math.cos(l);
    const sp = Math.sin(p), cp = Math.cos(p);
    const sg = Math.sin(g), cg = Math.cos(g);
    return [
      cl * cp * cg + sl * sp * sg,
      sl * cp * cg - cl * sp * sg,
      cl * sp * cg + sl * cp * sg,
      cl * cp * sg - sl * sp * cg
    ];
  }

  static toAngles([a, b, c, d]) {
    return [
      Math.atan2(2 * (a * b + c * d), 1 - 2 * (b * b + c * c)) * 180 / Math.PI,
      Math.asin(Math.max(-1, Math.min(1, 2 * (a * c - d * b)))) * 180 / Math.PI,
      Math.atan2(2 * (a * d + b * c), 1 - 2 * (c * c + d * d)) * 180 / Math.PI
    ];
  }

  static interpolateAngles(a, b) {
    const i = Versor.interpolate(Versor.fromAngles(a), Versor.fromAngles(b));
    return t => Versor.toAngles(i(t));
  }

  static interpolateLinear([a1, b1, c1, d1], [a2, b2, c2, d2]) {
    a2 -= a1; b2 -= b1; c2 -= c1; d2 -= d1;
    const x = new Array(4);
    return t => {
      const l = Math.hypot(
        x[0] = a1 + a2 * t,
        x[1] = b1 + b2 * t,
        x[2] = c1 + c2 * t,
        x[3] = d1 + d2 * t
      );
      x[0] /= l; x[1] /= l; x[2] /= l; x[3] /= l;
      return x;
    };
  }

  static interpolate([a1, b1, c1, d1], [a2, b2, c2, d2]) {
    let dot = a1 * a2 + b1 * b2 + c1 * c2 + d1 * d2;
    if (dot < 0) a2 = -a2, b2 = -b2, c2 = -c2, d2 = -d2, dot = -dot;
    if (dot > 0.9995) return Versor.interpolateLinear([a1, b1, c1, d1], [a2, b2, c2, d2]);

    const theta0 = Math.acos(Math.max(-1, Math.min(1, dot)));
    const x = new Array(4);
    let na2 = a2 - a1 * dot;
    let nb2 = b2 - b1 * dot;
    let nc2 = c2 - c1 * dot;
    let nd2 = d2 - d1 * dot;
    const l = Math.hypot(na2, nb2, nc2, nd2);
    na2 /= l; nb2 /= l; nc2 /= l; nd2 /= l;

    return t => {
      const theta = theta0 * t;
      const s = Math.sin(theta);
      const c = Math.cos(theta);
      x[0] = a1 * c + na2 * s;
      x[1] = b1 * c + nb2 * s;
      x[2] = c1 * c + nc2 * s;
      x[3] = d1 * c + nd2 * s;
      return x;
    };
  }
}

// === Composant React contrôlé ===
// selectedCountryName : string correspondant à properties.name (ou à l'id du topojson)
const Globe = ({ width = 600, selectedCountryName }) => {
  const canvasRef = useRef(null);

  // On garde tout l'état D3 côté ref (pas dans le state React)
  const d3StateRef = useRef({
    initialized: false,
    projection: null,
    path: null,
    context: null,
    land: null,
    borders: null,
    countries: [],
    width: null,
    height: null,
    tilt: 20,
    lastP: [0, 0],
    lastR: [0, 0, 0]
  });

  // Initialisation : canvas, projection, chargement du monde
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const height = Math.min(width, 720);
    const dpr = window.devicePixelRatio || 1;
    const context = canvas.getContext("2d");

    // Canvas & retina
    canvas.width = width * dpr;
    canvas.height = height * dpr;
    canvas.style.width = `${width}px`;
    canvas.style.height = `${height}px`;
    context.setTransform(1, 0, 0, 1, 0, 0);
    context.scale(dpr, dpr);

    // Projection & path
    const projection = d3.geoOrthographic().fitExtent(
      [[10, 10], [width - 10, height - 10]],
      { type: "Sphere" }
    );

    const path = d3.geoPath(projection, context);

    // On stocke tout dans la ref
    d3StateRef.current = {
      initialized: true,
      projection,
      path,
      context,
      land: null,
      borders: null,
      countries: [],
      width,
      height,
      tilt: 20,
      lastP: [0, 0],
      lastR: [0, 0, 0]
    };

    // Fonction de rendu qui lit les données dans la ref
    const render = (country = null, arc = null) => {
      const state = d3StateRef.current;
      const { context, path, land, borders, width, height } = state;
      if (!context || !path) return;
      if (!land || !borders) return;

      context.clearRect(0, 0, width, height);

      // Terre
      context.beginPath();
      path(land);
      context.fillStyle = "#cccccc";
      context.fill();

      // Pays sélectionné en rouge
      if (country) {
        context.beginPath();
        path(country);
        context.fillStyle = "#8200cdff";
        context.fill();
      }

      // Frontières
      context.beginPath();
      path(borders);
      context.strokeStyle = "#ffffff";
      context.lineWidth = 0.5;
      context.stroke();

      // Contour du globe
      context.beginPath();
      path({ type: "Sphere" });
      context.strokeStyle = "#000000";
      context.lineWidth = 1.5;
      context.stroke();

      // Arc
      if (arc) {
        context.beginPath();
        path(arc);
        context.strokeStyle = "#000000";
        context.lineWidth = 1;
        context.stroke();
      }
    };

    // On garde le render dans la ref
    d3StateRef.current.render = render;

    let isCancelled = false;

    // Chargement du topojson
    const loadWorld = async () => {
      const world = await d3.json(
        "https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json"
      );
      if (!world || isCancelled) return;

      const land = feature(world, world.objects.land);
      const countries = feature(world, world.objects.countries).features;
      const borders = mesh(world, world.objects.countries, (a, b) => a !== b);

      d3StateRef.current.land = land;
      d3StateRef.current.countries = countries;
      d3StateRef.current.borders = borders;

      // Premier rendu (globe neutre)
      d3StateRef.current.render();
    };

    loadWorld();

    return () => {
      isCancelled = true;
    };
  }, [width]);

  // Effet : à chaque changement de selectedCountryName, on anime vers ce pays
  useEffect(() => {
    const state = d3StateRef.current;
    if (!state.initialized) return;
    if (!state.countries || state.countries.length === 0) return;
    if (!selectedCountryName) return;

    const { projection, render, tilt, countries } = state;
    if (!projection || !render) return;

    // On cherche le pays soit par name soit par id
    const country = countries.find(
      (c) =>
        c.properties?.name === selectedCountryName ||
        String(c.id) === String(selectedCountryName)
    );

    if (!country) {
      console.warn("Pays non trouvé dans le topojson :", selectedCountryName);
      return;
    }

    const p1 = state.lastP || [0, 0];
    const r1 = state.lastR || [0, 0, 0];

    const p2 = d3.geoCentroid(country);
    const r2 = [-p2[0], tilt - p2[1], 0];

    const ip = d3.geoInterpolate(p1, p2);
    const iv = Versor.interpolateAngles(r1, r2);

    state.lastP = p2;
    state.lastR = r2;

    let isCancelled = false;

    d3
      .transition()
      .duration(1250)
      .tween("render", () => (t) => {
        if (isCancelled) return;
        projection.rotate(iv(t));
        render(country, {
          type: "LineString",
          coordinates: [p1, ip(t)]
        });
      })
      .transition()
      .tween("render", () => (t) => {
        if (isCancelled) return;
        render(country, {
          type: "LineString",
          coordinates: [ip(t), p2]
        });
      });

    return () => {
      isCancelled = true;
    };
  }, [selectedCountryName]);

  return (
    <canvas
      ref={canvasRef}
      style={{ display: "block", margin: "0 auto" }}
    />
  );
};

export default Globe;
