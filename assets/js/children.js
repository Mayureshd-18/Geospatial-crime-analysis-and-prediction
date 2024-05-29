let map;
let locations = []; // Array to hold data from CSV file
const markers = []; // Array to hold markers
let markerCluster; // Variable to hold the MarkerClusterer instance
let crimeFileName = "assets/csv/children.csv"; // Replace with your CSV file name

document.getElementById('crime-select').addEventListener('change', function() {
  const selectedCrime = this.value;
  console.log(selectedCrime);
  filterMarkers(selectedCrime); // Filter markers based on selected crime
});

async function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    zoom: 12,
    center: { lat: 15.3173, lng: 75.7139 }, // Centered around Karnataka, India
    mapTypeControl: false,
  });

  // Fetch CSV data and then perform geocoding
  fetch(crimeFileName)
    .then((response) => response.text())
    .then((csvData) => {
      locations = parseCSV(csvData); // Parse CSV data to extract Year, Age, Present Address, and Crime
      geocodeLocations(locations); // Geocode locations
    })
    .catch((error) => {
      console.error("Error reading CSV file:", error);
    });
}

function parseCSV(csvData) {
  const lines = csvData.split('\n');
  const result = [];

  for (let i = 1; i < lines.length; i++) { // Start from index 1 to skip header
    const line = lines[i].trim();
    if (line !== '') {
      const items = line.split(',');
      const year = parseInt(items[0], 10);
      const age = parseInt(items[1], 10);
      const address = items.slice(2, -1).join(',').replace(/"/g, ''); // Extract address without crime group and remove double quotes
      const crime = items[items.length - 1];

      if (!isNaN(year) && !isNaN(age) && age <18) { // Filter based on age
        result.push({ age, crime, address }); // Push object with age, crime, and address into result array

        // Log age, crime, and location
        console.log(`Age: ${age}, Crime: ${crime}, Address: ${address}`);
      }
    }
  }

  return result;
}

async function geocodeLocations(locations) {
  for (const location of locations) {
    try {
      const position = await geocode({ address: location.address });
      createMarker(position, location.crime); // Create marker for this location with crime as label
    } catch (error) {
      console.error("Error geocoding location:", location.address, error);
    }
  }
}

function geocode(request) {
  const geocoder = new google.maps.Geocoder();
  return new Promise((resolve, reject) => {
    geocoder.geocode(request, (results, status) => {
      if (status === google.maps.GeocoderStatus.OK) {
        const location = results[0].geometry.location;
        const position = {
          lat: location.lat(),
          lng: location.lng(),
        };
        resolve(position); // Resolve the promise with the geocoded position object
      } else {
        reject(status); // Reject the promise with the geocoding status
      }
    });
  });
}

function createMarker(position, crime) {
  const marker = new google.maps.Marker({
    position,
    map,
    title: crime, // Use crime as marker title
  });

  markers.push(marker); // Push the marker into the markers array
}

function filterMarkers(selectedCrime) {
  markers.forEach(marker => {
    if (marker.title === selectedCrime) {
      marker.setVisible(true); // Show markers of the selected crime
    } else {
      marker.setVisible(false); // Hide markers not related to the selected crime
    }
  });

  // Refresh the MarkerClusterer with the updated markers
  if (markerCluster) {
    markerCluster.clearMarkers();
    markerCluster.addMarkers(markers);
  }
}

window.initMap = initMap;
