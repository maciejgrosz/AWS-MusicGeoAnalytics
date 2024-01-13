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
  "Lodzkie": ["lodz"],
  "Slaskie": ["katowice", "gliwice"],
  "Zachodniopomorskie": ["szczecin"],
  "Wielkopolskie": ["poznan"],
  "Pomorskie": ["gdansk", "gdynia"],
  "Malopolskie": ["krakow"],
  "Podkarpackie": ["rzeszow"],
  "England": ["london", "birmingham"],
  "Scotland": ["glasgow", "edinburgh"],
  "Wales": ["cardiff", "swansea"],
  "Northern_Ireland": ["belfast", "londonderry"]
};

function convertRegionName(regionName) {
  const conversionMap = {
    'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l',
    'ń': 'n', 'ó': 'o', 'ś': 's', 'ź': 'z',
    'ż': 'z', 'Ą': 'A', 'Ć': 'C', 'Ę': 'E',
    'Ł': 'L', 'Ń': 'N', 'Ó': 'O', 'Ś': 'S',
    'Ź': 'Z', 'Ż': 'Z'
  };

  return regionName.split('').map(char => conversionMap[char] || char).join('');
}

function fetchGenreData(regionName) {
  return fetch(`https://fzk6hts2n3.execute-api.eu-west-1.amazonaws.com/test/genres/${regionName}`)
    .then(response => response.json())
    .catch(error => {
      console.error(`Error fetching genre data for ${cityName}:`, error);
      return []; // Return an empty array in case of error

  });
}

L.geoJSON(geoData, {
  onEachFeature: function (feature, layer) {
    const regionName = convertRegionName(feature.properties.NAME_1);
    regionLayers[regionName] = layer;
    layer.on('click', function () {
      fetchGenreData(regionName)
        .then(genreData => {
          // Check if genreData is an array and has elements
          if (Array.isArray(genreData) && genreData.length > 0) {
            const genreText = genreData.map(genre => `${genre.genre}: ${genre.count}`).join(', ');
            layer.bindPopup(`Top Genres in ${regionName}:<br>${genreText}`).openPopup();
          } else {
            layer.bindPopup(`No genre data available for ${regionName}`).openPopup();
          }
        })
        .catch(error => {
          console.error(`Error fetching data for ${regionName}:`, error);
          layer.bindPopup(`Error loading genre data for ${regionName}`).openPopup();
        });
    });
  },
  style: function (feature) {
    // You can also set a default style for regions here
    return defaultStyle;
  }
}).addTo(map);


// Load and add the Great Britain GeoJSON to the map
L.geoJSON(geoDataGb, {
  onEachFeature: function (feature, layer) {
    const regionName = convertRegionName(feature.properties.NAME_1);
    regionLayers[regionName] = layer;
    layer.on('click', function () {
      fetchGenreData(regionName)
        .then(genreData => {
          // Check if genreData is an array and has elements
          if (Array.isArray(genreData) && genreData.length > 0) {
            const genreText = genreData.map(genre => `${genre.genre}: ${genre.count}`).join(', ');
            layer.bindPopup(`Top Genres in ${regionName}:<br>${genreText}`).openPopup();
          } else {
            layer.bindPopup(`No genre data available for ${regionName}`).openPopup();
          }
        })
        .catch(error => {
          console.error(`Error fetching data for ${regionName}:`, error);
          layer.bindPopup(`Error loading genre data for ${regionName}`).openPopup();
        });
    });
  },
  style: function (feature) {
    // You can also set a default style for regions here
    return defaultStyle;
  }
}).addTo(map);