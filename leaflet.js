// Define a highlight style
const highlightStyle = {
  color: '#ff7800', // Example highlight color
  weight: 5,        // Border weight
  fillOpacity: 0.7  // Fill opacity
};
const defaultStyle = {
  color: '#3388ff', // Example default color
  weight: 2,        // Border weight
  fillOpacity: 0.2  // Fill opacity
};
// Keep a reference to all region layers
regionLayers = {};


const map = L.map('map').setView([52.25, 21.0], 7); // Adjust as needed
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: '© OpenStreetMap contributors'
}).addTo(map);

const regionToCityMapping = {
  "Mazowieckie": ["warsaw"],
  "Łódzkie": ["lodz"],
  "Śląskie": ["katowice", "gliwice"],
  "Zachodniopomorskie": ["szczecin"],
  "Wielkopolskie": ["poznan"],
  "Pomorskie": ["gdansk", "gdynia"],
  "Małopolskie": ["krakow"],
  "Podkarpackie": ["rzeszow"]
};


function fetchGenreData(cityName) {
  return fetch(`https://fzk6hts2n3.execute-api.eu-west-1.amazonaws.com/test/genres/${cityName}`)
    .then(response => response.json())
    .catch(error => {
      console.error(`Error fetching genre data for ${cityName}:`, error);
      return []; // Return an empty array in case of error
  
    });
}

L.geoJSON(geoData, {
  onEachFeature: function (feature, layer) {
    const regionName = feature.properties.NAME_1;
    regionLayers[regionName] = layer;
    layer.on('click', function () {
      const cities = regionToCityMapping[regionName];
      if (cities && cities.length > 0) {
        Promise.all(cities.map(city => fetchGenreData(city)))
          .then(results => {
            const genreTexts = results.map((genres, index) => {
              const city = cities[index];
              const genresList = genres.map(genre => `${genre.genre}: ${genre.count}`).join(', ');
              return `${city.charAt(0).toUpperCase() + city.slice(1)} - ${genresList}`;
            }).join('<br>');

            layer.bindPopup(`Top Genres in ${regionName}:<br>${genreTexts}`).openPopup();
          })
          .catch(error => {
            console.error(`Error fetching data for ${regionName}:`, error);
            layer.bindPopup(`Error loading genre data for ${regionName}`).openPopup();
          });
      } else {
        layer.bindPopup(`No data available for ${regionName}`).openPopup();
      }
    });
  },
  style: function (feature) {
    // You can also set a default style for regions here
    return defaultStyle;
  }
}).addTo(map);
  
