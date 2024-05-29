let map;
let locations = []; // Array to hold data from CSV file
const myLocations = []; // Declare myLocations as a global variable
const markers = []; // Array to hold markers
let crimeFileName = "assets/csv/ELECTION_data_loc_m_y.csv";



// Define global variables for marker opacity and selected marker
let markerOpacity = 1;
let selectedMarker = null;
const originalOpacities = new Map();


// months = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]

document.getElementById('crime-select').addEventListener('change', function() {
  crimeFileName = this.value;
  console.log(crimeFileName);
  initMap(); 
});

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    zoom: 6,
    center: { lat: 15.3173, lng: 75.7139 }, // Centered around Karnataka, India
    mapTypeControl: false,
  });

  const infoWindow = new google.maps.InfoWindow({
    content: "",
    disableAutoPan: true,
  });

  // Fetch CSV data and then perform geocoding
  fetch(crimeFileName)
    .then((response) => response.text())
    .then((csvData) => {
      locations = parseCSV(csvData); // Parse CSV data to extract place, year, and month
      geocodeLocations(locations); // Geocode locations
    })
    .catch((error) => {
      console.error("Error reading CSV file:", error);
    });
}

function parseCSV(csvData) {
  const lines = csvData.split('\n');
  const result = [];

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();
    if (line !== '') {
      const items = line.split(',').map(item => item.trim()); // Split each line by comma and trim spaces
      const place = items.slice(0, -2).join(','); // Combine the first columns as place
      const month = parseInt(items[items.length - 2], 10); // Get the year from the second last column
      const year = parseInt(items[items.length - 1], 10); // Get the month from the last column

      // Check if year and month are valid numbers
      if (!isNaN(year) && !isNaN(month)) {
        result.push({ place, year, month }); // Push an object with place, year, and month into result array

        // Log place, year, and month
        console.log(`Place: ${place}, Year: ${year}, Month: ${month}`);
      } else {
        console.warn(`Invalid data format at line ${i + 1}: ${line}`);
      }
    }
  }

  return result;
}


async function geocodeLocations(locations) {
  for (const location of locations) {
    try {
      const position = await geocode({ address: location.place });
      myLocations.push({ position, year: location.year, month: location.month }); // Push the geocoded position object along with year and month into myLocations array
      createMarker(position, location.year, location.month); // Create marker for this location
    } catch (error) {
      console.error("Error geocoding location:", location.place, error);
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

function createMarker(position, year, month) {

    const marker = new google.maps.Marker({
      position,
      map,
      title: `Crime (${month} ${year})`,
      label: {
        text: month.toString(), // Number to be displayed as label
        color: 'white', // Label text color
        fontWeight: 'bold', // Font weight of label text
      },
    });
  
    marker.addListener("click", () => {
      selectedMarker = marker; // Store the clicked marker
      highlightSelectedMarker();
    });
  
    markers.push(marker); // Push the marker into the markers array
  }
  
  function highlightSelectedMarker() {
    const selectedLabel = parseInt(selectedMarker.getLabel().text);
    markers.forEach(marker => {
      const markerLabel = parseInt(marker.getLabel().text);
      if (markerLabel === selectedLabel) {
        marker.setOpacity(1); // Highlight markers with the same label
      } else {
        if (!originalOpacities.has(marker)) {
          originalOpacities.set(marker, marker.getOpacity()); // Store the original opacity
        }
        marker.setOpacity(0.1); // Fade markers with different labels
      }
    });
  }
  
  document.getElementById('reset-button').addEventListener('click', () => {
    resetMarkers();
  });
  
  function resetMarkers() {
    markers.forEach(marker => {
      marker.setOpacity(1); // Reset opacity for all markers
    });
  }

}

window.initMap = initMap;
