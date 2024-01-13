const map = L.map('map').setView([52.25, 21.0], 7); // Adjust as needed
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: '© OpenStreetMap contributors'
}).addTo(map);

let warsawGenres = [];

fetch('https://fzk6hts2n3.execute-api.eu-west-1.amazonaws.com/test/genres/warsaw')
  .then(response => response.json())
  .then(data => {
    warsawGenres = data; // Store the data for later use
  })
  .catch(error => console.error('Error fetching genre data:', error));

  L.geoJSON(geoData, {
    onEachFeature: function (feature, layer) {
      if (feature.properties.NAME_1 === "Mazowieckie") { // Assuming this is the correct property
        layer.on('click', function () {
          // Check if the data for Warsaw is available
          if (warsawGenres.length > 0) {
            const topGenresText = warsawGenres.map(genre => `${genre.genre}: ${genre.count}`).join(', ');
            layer.bindPopup(`Top Genres in Warsaw: ${topGenresText}`).openPopup();
          } else {
            layer.bindPopup('Loading genres data...').openPopup();
          }
        });
      }
    }
  }).addTo(map);
  
