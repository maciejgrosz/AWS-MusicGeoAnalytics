const myMap = L.map('map').setView([0, 0], 2);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(myMap);

const geoJsonData = {
  type: 'FeatureCollection',
  features: [
    {
      type: 'Feature',
      properties: { country: 'USA', genre: 'Pop', artist: 'Artist A' },
      geometry: { type: 'Point', coordinates: [-95.7129, 37.0902] },
    },
  ],
};

L.geoJSON(geoJsonData, {
  onEachFeature: function (feature, layer) {
    layer.bindPopup(`
      ${feature.properties.country}
      ${feature.properties.genre}
      ${feature.properties.artist}
    `);
  },
}).addTo(myMap);
